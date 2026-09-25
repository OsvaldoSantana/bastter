# -*- coding: utf-8 -*-
"""
analisar_sessoes.py -- para onde vai o tempo das sessoes do Claude Code (24/09/2026).

Le as transcricoes que o Claude Code grava em ~/.claude/projects/<projeto>/*.jsonl e
decompoe o tempo de cada PEDIDO seu (do seu prompt ate a ultima acao antes do proximo):

  modelo      tempo em que o modelo estava gerando (entre um evento e a resposta dele)
  ferramentas tempo entre o pedido de uma ferramenta e o resultado dela (pytest, ruff,
              leitura de arquivo, rede...) -- inclui espera de permissao, se houver
  compactacao resumo automatico de contexto, quando o contexto encheu

E conta o que pesa no custo de cada chamada ao modelo: o tamanho do contexto.

So le. Nao grava nada fora de --saida. Nao copia o texto dos seus prompts nem das
respostas: do prompt ficam so os 60 primeiros caracteres, para voce reconhecer o pedido.
Comandos de terminal ficam truncados em 90 caracteres.

USO (PowerShell, na pasta do projeto):
    py -3.11 tools\\analisar_sessoes.py
    py -3.11 tools\\analisar_sessoes.py --desde 2026-09-20
Saida: data\\analise-sessoes\\relatorio.md (+ turnos.csv, ferramentas.csv, sessoes.csv)
"""
import argparse
import collections
import csv
import datetime as dt
import glob
import json
import os
import re
import sys

BIG_DOCS = ("CLAUDE.md", "PENDENCIAS.md", "ACHADOS.md", "PLANO.md")


def ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def pasta_do_projeto(padrao):
    base = os.path.join(os.path.expanduser("~"), ".claude", "projects")
    cands = [p for p in glob.glob(os.path.join(base, "*")) if os.path.isdir(p)
             and re.search(padrao, os.path.basename(p), re.I)]
    return base, cands


def ler(caminho):
    out = []
    with open(caminho, encoding="utf-8", errors="replace") as f:
        for linha in f:
            try:
                out.append(json.loads(linha))
            except ValueError:
                pass
    return out


def texto_humano(d):
    """O conteudo de um prompt SEU (nao resultado de ferramenta), ou None."""
    if d.get("type") != "user" or d.get("isSidechain") or d.get("isMeta"):
        return None
    c = (d.get("message") or {}).get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list) and c and all(isinstance(b, dict) for b in c):
        if any(b.get("type") == "tool_result" for b in c):
            return None
        t = " ".join(b.get("text", "") for b in c if b.get("type") == "text")
        return t or None
    return None


def categoria(nome, entrada):
    if nome != "Bash" and nome != "PowerShell":
        if nome in ("Read", "Edit", "Write") and isinstance(entrada, dict):
            base = os.path.basename(str(entrada.get("file_path", "")))
            return f"{nome}:{base}" if base in BIG_DOCS else nome
        return nome
    cmd = str((entrada or {}).get("command", ""))
    for chave, rot in (("pytest", "pytest"), ("ruff", "ruff"), ("mypy", "mypy"),
                       ("git ", "git"), ("pip ", "pip"), ("gh ", "gh")):
        if chave in cmd:
            return f"Bash:{rot}"
    if re.search(r"\bpython|\bpy\b|py -3", cmd):
        return "Bash:python"
    return "Bash:outro"


def uniao_s(intervalos):
    """Segundos cobertos pela UNIAO dos intervalos (inicio, fim).

    Ferramentas rodam em PARALELO (varias buscas de uma vez): a soma passa do tempo de
    parede. Conta-se a uniao, nao a soma (24/09)."""
    uni, fim_ = 0.0, None
    for a, b in sorted(intervalos):
        if fim_ is None or a > fim_:
            uni += (b - a).total_seconds(); fim_ = b
        elif b > fim_:
            uni += (b - fim_).total_seconds(); fim_ = b
    return uni


def analisar_sessao(caminho, desde):
    evs = [d for d in ler(caminho) if d.get("timestamp")]
    evs.sort(key=lambda d: d["timestamp"])
    if not evs:
        return None, [], []
    if desde and ts(evs[-1]["timestamp"]).date() < desde:
        return None, [], []
    sid = os.path.basename(caminho)[:8]
    turnos, ferr = [], []
    atual = None
    pend = {}                       # tool_use_id -> (nome, cat, t0, resumo)
    vistos = set()                  # message.id ja contados (streaming grava por bloco)
    anterior = None
    compact = []

    def fecha():
        if atual:
            atual["dur_s"] = (atual["fim"] - atual["ini"]).total_seconds()
            atual["ferr_soma_s"] = atual["ferr_s"]
            atual["ferr_s"] = uniao_s(atual.pop("iv"))
            turnos.append(atual)

    for d in evs:
        t = ts(d["timestamp"])
        if d.get("type") == "system" and d.get("subtype") == "compact_boundary":
            ms = (d.get("compactMetadata") or {}).get("durationMs") or 0
            compact.append(ms / 1000)
            if atual:
                atual["compact_s"] += ms / 1000
                atual["compactacoes"] += 1
        h = texto_humano(d)
        if h is not None:
            fecha()
            atual = dict(sessao=sid, ini=t, fim=t, prompt=h.strip().replace("\n", " ")[:60],
                         chamadas=0, modelo_s=0.0, ferr_s=0.0, compact_s=0.0,
                         compactacoes=0, n_ferr=0, ctx_max=0, ctx_1a=0, saida_tok=0,
                         cache_lido=0, cache_criado=0, iv=[])
            anterior = t
            continue
        if atual is None or d.get("isSidechain"):
            continue
        msg = d.get("message") or {}
        if d.get("type") in ("assistant", "user"):
            # so resposta do modelo e resultado de ferramenta fecham o pedido: anexos,
            # lembretes e registros de custo chegam depois e nao sao trabalho
            atual["fim"] = max(atual["fim"], t)
        if d.get("type") == "assistant":
            mid = msg.get("id")
            if mid not in vistos:
                vistos.add(mid)
                atual["chamadas"] += 1
                if anterior:
                    atual["modelo_s"] += max(0.0, (t - anterior).total_seconds())
                u = msg.get("usage") or {}
                ctx = (u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0)
                       + u.get("cache_creation_input_tokens", 0))
                atual["ctx_max"] = max(atual["ctx_max"], ctx)
                atual["ctx_1a"] = atual["ctx_1a"] or ctx
                atual["saida_tok"] += u.get("output_tokens", 0)
                atual["cache_lido"] += u.get("cache_read_input_tokens", 0)
                atual["cache_criado"] += u.get("cache_creation_input_tokens", 0)
            for b in msg.get("content") or []:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    ent = b.get("input") or {}
                    resumo = str(ent.get("command") or ent.get("file_path")
                                 or ent.get("pattern") or ent.get("description") or "")
                    pend[b.get("id")] = (b.get("name"), categoria(b.get("name"), ent), t,
                                         resumo.replace("\n", " ")[:90])
            anterior = t
        elif d.get("type") == "user":
            conteudo = msg.get("content")
            for b in (conteudo if isinstance(conteudo, list) else []):
                if isinstance(b, dict) and b.get("type") == "tool_result":
                    p = pend.pop(b.get("tool_use_id"), None)
                    if p:
                        s = max(0.0, (t - p[2]).total_seconds())
                        atual["ferr_s"] += s
                        atual["iv"].append((p[2], t))
                        atual["n_ferr"] += 1
                        ferr.append(dict(sessao=sid, turno_ini=atual["ini"].isoformat(),
                                         ferramenta=p[0], categoria=p[1], s=round(s, 1),
                                         resumo=p[3]))
            anterior = t
    fecha()

    custo = [d for d in evs if d.get("type") == "cost-state"]
    c = custo[-1] if custo else {}
    ses = dict(sessao=sid, arquivo=os.path.basename(caminho),
               inicio=evs[0]["timestamp"], fim=evs[-1]["timestamp"],
               turnos=len(turnos), compactacoes=len(compact),
               api_s=round((c.get("totalAPIDuration") or 0) / 1000),
               ferr_s=round((c.get("totalToolDuration") or 0) / 1000),
               total_s=round((c.get("totalDuration") or 0) / 1000),
               custo_usd=round(c.get("totalCostUSD") or 0, 2))
    return ses, turnos, ferr


def hms(s):
    s = int(s)
    return f"{s // 3600}h{s % 3600 // 60:02d}m" if s >= 3600 else f"{s // 60}m{s % 60:02d}s"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--projeto", default="Bastter", help="regex no nome da pasta do projeto")
    ap.add_argument("--desde", help="AAAA-MM-DD: so sessoes que terminaram a partir daqui")
    ap.add_argument("--pasta", help="pasta com os .jsonl (padrao: ~/.claude/projects/*<projeto>*)")
    ap.add_argument("--saida", default=os.path.join("data", "analise-sessoes"))
    a = ap.parse_args(argv)
    desde = dt.date.fromisoformat(a.desde) if a.desde else None
    if a.pasta:
        pastas = [a.pasta]
    else:
        base, pastas = pasta_do_projeto(a.projeto)
        if not pastas:
            print(f"nenhuma pasta com '{a.projeto}' em {base}", file=sys.stderr)
            return 2
    arquivos = sorted(f for p in pastas for f in glob.glob(os.path.join(p, "*.jsonl")))
    sessoes, turnos, ferr = [], [], []
    for f in arquivos:
        s, t, fe = analisar_sessao(f, desde)
        if s and t:
            sessoes.append(s); turnos += t; ferr += fe
    if not turnos:
        print("nenhum turno encontrado", file=sys.stderr)
        return 1
    os.makedirs(a.saida, exist_ok=True)
    for nome, linhas in (("sessoes.csv", sessoes), ("turnos.csv", turnos),
                         ("ferramentas.csv", ferr)):
        with open(os.path.join(a.saida, nome), "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(linhas[0]) if linhas else ["vazio"],
                               delimiter=";")
            w.writeheader()
            for ln in linhas:
                w.writerow({k: (v.isoformat() if isinstance(v, dt.datetime) else v)
                            for k, v in ln.items()})

    R = []
    tot = sum(t["dur_s"] for t in turnos)
    mod = sum(t["modelo_s"] for t in turnos)
    fs = sum(t["ferr_s"] for t in turnos)
    cp = sum(t["compact_s"] for t in turnos)
    R.append(f"# Para onde vai o tempo -- {len(sessoes)} sessoes, {len(turnos)} pedidos\n")
    R.append(f"Gerado em {dt.datetime.now():%d/%m/%Y %H:%M}. Pasta(s): {len(pastas)}. "
             f"Arquivos: {len(arquivos)}.\n")
    R.append("## Total\n")
    R.append("| | tempo | % |\n|---|---|---|")
    for rot, v in (("modelo gerando", mod), ("ferramentas", fs), ("compactacao", cp),
                   ("resto (nao atribuido)", max(0.0, tot - mod - fs - cp))):
        R.append(f"| {rot} | {hms(v)} | {100 * v / tot:.0f}% |")
    R.append(f"| **total dos pedidos** | **{hms(tot)}** | |\n")
    ch = sum(t["chamadas"] for t in turnos)
    R.append(f"Chamadas ao modelo: {ch} ({mod / max(ch, 1):.1f} s cada, em media). "
             f"Tokens de saida: {sum(t['saida_tok'] for t in turnos):,}. "
             f"Contexto lido do cache: {sum(t['cache_lido'] for t in turnos):,} tokens.\n")

    R.append("## Os 15 pedidos mais longos\n")
    R.append("| inicio | dur | modelo | ferr | chamadas | ferr n | ctx 1a -> max (k tok) "
             "| compact | pedido |")
    R.append("|---|---|---|---|---|---|---|---|---|")
    for t in sorted(turnos, key=lambda x: -x["dur_s"])[:15]:
        R.append(f"| {t['ini']:%d/%m %H:%M} | {hms(t['dur_s'])} | {hms(t['modelo_s'])} | "
                 f"{hms(t['ferr_s'])} | {t['chamadas']} | {t['n_ferr']} | "
                 f"{t['ctx_1a'] // 1000} -> {t['ctx_max'] // 1000} | {t['compactacoes']} | "
                 f"{t['prompt'].replace('|', '/')} |")

    R.append("\n## Ferramentas por categoria\n")
    agg = collections.defaultdict(lambda: [0, 0.0, 0.0])
    for f in ferr:
        g = agg[f["categoria"]]; g[0] += 1; g[1] += f["s"]; g[2] = max(g[2], f["s"])
    R.append("| categoria | n | tempo total | media | maior |\n|---|---|---|---|---|")
    for k, (n, s, mx) in sorted(agg.items(), key=lambda kv: -kv[1][1])[:20]:
        R.append(f"| {k} | {n} | {hms(s)} | {s / n:.1f} s | {mx:.0f} s |")

    R.append("\n## As 15 chamadas de ferramenta mais lentas\n")
    R.append("| s | categoria | resumo |\n|---|---|---|")
    for f in sorted(ferr, key=lambda x: -x["s"])[:15]:
        R.append(f"| {f['s']:.0f} | {f['categoria']} | `{f['resumo'].replace('|', '/')}` |")

    R.append("\n## Leituras dos documentos grandes\n")
    cont = collections.Counter(f["categoria"] for f in ferr if ":" in f["categoria"]
                               and f["categoria"].split(":", 1)[1] in BIG_DOCS)
    R.append("| leitura/edicao | vezes |\n|---|---|")
    for k, v in cont.most_common():
        R.append(f"| {k} | {v} |")
    tam = {d: os.path.getsize(d) for d in BIG_DOCS if os.path.exists(d)}
    if tam:
        R.append("\nTamanho hoje: " + ", ".join(f"{k} {v / 1024:.0f} KB (~{v // 4 // 1000}k tok)"
                                                for k, v in tam.items()))

    R.append("\n## Sessoes\n")
    R.append("| sessao | inicio | pedidos | compact | API (s) | ferr (s) | total (s) | custo US$ |")
    R.append("|---|---|---|---|---|---|---|---|")
    for s in sessoes:
        R.append(f"| {s['sessao']} | {s['inicio'][:16]} | {s['turnos']} | {s['compactacoes']} | "
                 f"{s['api_s']} | {s['ferr_s']} | {s['total_s']} | {s['custo_usd']} |")
    rel = os.path.join(a.saida, "relatorio.md")
    with open(rel, "w", encoding="utf-8") as fh:
        fh.write("\n".join(R) + "\n")
    print("\n".join(R[:12]))
    print(f"\nrelatorio completo: {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
