<#
.SINOPSE
    Fase 0 — reconhecimento e captura da base CVM (DFP/ITR), com snapshot datado.

.POR QUE ESTE SCRIPT EXISTE ASSIM
    Ele NAO e o parser. E o capturador, e a diferenca importa: o parser pode ser
    reescrito a qualquer momento; o dado nao capturado hoje nao volta.

    A regra central: SNAPSHOT IMUTAVEL. Cada download vai para uma pasta com a data,
    e nunca sobrescreve. O arquivo da CVM e mutavel — enquanto o ano corre, empresas
    entregam e reentregam com VERSAO incrementada. Guardar so a ultima versao apaga
    a resposta a pergunta que o backtest faz: "o que era possivel saber no dia X?".

.MODOS
    -SoConferir    nao baixa os ZIP grandes. Le a listagem do servidor, mede tamanhos
                   e responde as perguntas em aberto. Rode ISTO primeiro.
    -Anos          baixa as safras pedidas. Ex.: -Anos 2010..2026  ou  -Anos 2026

.EXEMPLO
    .\fase0.ps1 -SoConferir
    .\fase0.ps1 -Anos 2010..2026
#>
[CmdletBinding()]
param(
    [int[]]$Anos,
    [switch]$SoConferir,
    [string]$Destino = "data\bronze\cvm",
    [switch]$Forcar
)

$ErrorActionPreference = "Stop"
$ProgressPreference    = "SilentlyContinue"   # sem isso, o Invoke-WebRequest fica ~10x mais lento

$BASE  = "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC"
$FORMS = @("DFP", "ITR")
$HOJE  = Get-Date -Format "yyyy-MM-dd"

function Secao($t) {
    Write-Host ""
    Write-Host ("=" * 78) -ForegroundColor DarkGray
    Write-Host $t -ForegroundColor Cyan
    Write-Host ("=" * 78) -ForegroundColor DarkGray
}

# ── Cabecalho HTTP, nas duas formas que o PowerShell usa ─────────────────────
# ARMADILHA REAL, encontrada antes de rodar: `$h.Headers['Content-Length'][0]`
# funciona no PowerShell 7 e QUEBRA EM SILENCIO no 5.1, que ainda e o padrao do
# Windows.
#   PS 7    Headers e Dictionary<string, IEnumerable<string>>  -> [0] = a string
#   PS 5.1  Headers e Dictionary<string, string>               -> [0] = o primeiro
#                                                                 CARACTERE
# No 5.1, "12345678"[0] devolve '1', e o script reportaria 1 byte sem erro nenhum.
# E o mesmo genero do F-02: ausencia virando numero plausivel.
function Cabecalho($resposta, $nome) {
    if (-not $resposta.Headers.ContainsKey($nome)) { return $null }
    $v = $resposta.Headers[$nome]
    if ($v -is [string]) { return $v }          # PS 5.1
    return @($v)[0]                             # PS 7
}

# ── Listagem do servidor ─────────────────────────────────────────────────────
# O portal serve um indice HTML simples. Extraimos os .zip e, quando presentes,
# a data e o tamanho da propria listagem — sao eles que dizem se a safra mudou.
function Get-ListagemCVM($form) {
    $url = "$BASE/$form/DADOS/"
    try {
        $r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 60
    } catch {
        Write-Host "  FALHA ao ler $url" -ForegroundColor Red
        Write-Host "  $($_.Exception.Message)" -ForegroundColor Red
        return @()
    }
    $itens = @()
    # linhas tipicas: <a href="dfp_cia_aberta_2024.zip">...</a>  2025-01-15 03:12  12M
    foreach ($m in [regex]::Matches($r.Content, '(?i)href="(?<f>[^"]*?\.zip)"')) {
        $nome = [System.IO.Path]::GetFileName($m.Groups['f'].Value)
        if ($itens.nome -contains $nome) { continue }
        $itens += [pscustomobject]@{ nome = $nome; url = "$url$nome" }
    }
    # data e tamanho vem do HEAD, que e barato e nao baixa o corpo
    foreach ($i in $itens) {
        try {
            $h = Invoke-WebRequest -Uri $i.url -Method Head -UseBasicParsing -TimeoutSec 30
            $i | Add-Member -NotePropertyName bytes      -NotePropertyValue ([int64](Cabecalho $h 'Content-Length'))
            $i | Add-Member -NotePropertyName modificado -NotePropertyValue (Cabecalho $h 'Last-Modified')
        } catch {
            $i | Add-Member -NotePropertyName bytes      -NotePropertyValue $null
            $i | Add-Member -NotePropertyName modificado -NotePropertyValue "(HEAD falhou)"
        }
    }
    return $itens
}

function MB($b) { if ($null -eq $b) { "     ?" } else { "{0,6:N1}" -f ($b / 1MB) } }

# ══ MODO RECONHECIMENTO ══════════════════════════════════════════════════════
if ($SoConferir) {
    Secao "FASE 0 — RECONHECIMENTO  ($HOJE)"
    Write-Host "Nao baixa os ZIP grandes. Responde o que nao deu para conferir da nuvem."

    $tudo = @{}
    foreach ($f in $FORMS) {
        Secao "$f — o que esta publicado"
        $itens = Get-ListagemCVM $f
        $tudo[$f] = $itens
        if (-not $itens) { Write-Host "  nada encontrado" -ForegroundColor Red; continue }
        Write-Host ("  {0,-34} {1,8}  {2}" -f "arquivo", "MB", "modificado")
        foreach ($i in ($itens | Sort-Object nome)) {
            Write-Host ("  {0,-34} {1,8}  {2}" -f $i.nome, (MB $i.bytes), $i.modificado)
        }
        $tot = ($itens | Measure-Object -Property bytes -Sum).Sum
        Write-Host ("`n  {0} arquivos, {1:N1} MB no total" -f $itens.Count, ($tot / 1MB)) -ForegroundColor Yellow
    }

    $geral = 0
    foreach ($f in $FORMS) { $geral += ($tudo[$f] | Measure-Object -Property bytes -Sum).Sum }
    Secao "DOWNLOAD COMPLETO CUSTARIA"
    Write-Host ("  {0:N0} MB  ({1:N2} GB)" -f ($geral / 1MB), ($geral / 1GB)) -ForegroundColor Yellow

    # ── A pergunta que decide a urgencia ─────────────────────────────────────
    Secao "A SAFRA CORRENTE E MUTAVEL? (a pergunta que decide o prazo)"
    $anoAtual = (Get-Date).Year
    foreach ($f in $FORMS) {
        $corrente = $tudo[$f] | Where-Object { $_.nome -match "_$anoAtual\.zip$" }
        $anterior = $tudo[$f] | Where-Object { $_.nome -match "_$($anoAtual-1)\.zip$" }
        if ($corrente) {
            Write-Host ("  $f $anoAtual  modificado em {0}" -f $corrente.modificado)
        } else {
            Write-Host "  $f $anoAtual  NAO EXISTE ainda no portal" -ForegroundColor DarkYellow
        }
        if ($anterior) {
            Write-Host ("  $f $($anoAtual-1)  modificado em {0}" -f $anterior.modificado)
        }
    }
    Write-Host ""
    Write-Host "  COMO LER: se a safra do ano CORRENTE tem data de modificacao recente" -ForegroundColor Gray
    Write-Host "  (dias, nao meses), ela esta sendo reescrita agora — e cada dia sem" -ForegroundColor Gray
    Write-Host "  snapshot e um dia de historia ponto-no-tempo perdido." -ForegroundColor Gray
    Write-Host ""
    Write-Host "  Se a safra do ano ANTERIOR tambem tem data recente, entao safra fechada" -ForegroundColor Gray
    Write-Host "  TAMBEM muda — e ai o snapshot vale para todas, nao so para a corrente." -ForegroundColor Gray

    Secao "PROXIMO PASSO"
    Write-Host "  .\fase0.ps1 -Anos 2010..$anoAtual" -ForegroundColor Green
    Write-Host "  (comece pelo ano corrente se quiser conferir o fluxo antes: -Anos $anoAtual)"
    return
}

# ══ MODO DOWNLOAD ════════════════════════════════════════════════════════════
if (-not $Anos) {
    Write-Host "Informe -Anos (ex.: -Anos 2010..2026) ou use -SoConferir" -ForegroundColor Red
    return
}

$raiz = Join-Path (Get-Location) $Destino
$snap = Join-Path $raiz $HOJE          # <- a data no CAMINHO. E o que torna imutavel.
Secao "FASE 0 — CAPTURA  (snapshot $HOJE)"
Write-Host "  destino: $snap"
Write-Host "  regra:   nunca sobrescreve. Rodar duas vezes no mesmo dia pula o que ja existe."

$manifesto = @()
foreach ($f in $FORMS) {
    $pasta = Join-Path $snap $f.ToLower()
    New-Item -ItemType Directory -Force -Path $pasta | Out-Null
    foreach ($ano in $Anos) {
        $nome = "$($f.ToLower())_cia_aberta_$ano.zip"
        $url  = "$BASE/$f/DADOS/$nome"
        $alvo = Join-Path $pasta $nome

        if ((Test-Path $alvo) -and -not $Forcar) {
            Write-Host ("  [ja existe] {0}" -f $nome) -ForegroundColor DarkGray
            continue
        }
        try {
            $t0 = Get-Date
            Invoke-WebRequest -Uri $url -OutFile $alvo -UseBasicParsing -TimeoutSec 600
            $seg = ((Get-Date) - $t0).TotalSeconds
            $b   = (Get-Item $alvo).Length
            $sha = (Get-FileHash $alvo -Algorithm SHA256).Hash.Substring(0, 16)
            Write-Host ("  [ok] {0,-32} {1,7:N1} MB  {2,5:N0}s  {3}" -f $nome, ($b/1MB), $seg, $sha) -ForegroundColor Green
            $manifesto += [pscustomobject]@{
                formulario = $f; ano = $ano; arquivo = $nome; bytes = $b
                sha256_16 = $sha; baixado_em = (Get-Date -Format "s"); url = $url
            }
        } catch {
            Write-Host ("  [FALHOU] {0}  {1}" -f $nome, $_.Exception.Message) -ForegroundColor Red
        }
    }
}

# ── O manifesto e o que torna o snapshot auditavel ───────────────────────────
# Sem ele, dois snapshots sao duas pastas de ZIP. Com ele, da para responder
# "este arquivo mudou entre 06/09 e 13/09?" comparando hash, sem reabrir nada.
if ($manifesto) {
    $mf = Join-Path $snap "manifesto.csv"
    $manifesto | Export-Csv -Path $mf -NoTypeInformation -Encoding UTF8
    Secao "MANIFESTO"
    Write-Host "  $mf"
    Write-Host ("  {0} arquivos, {1:N1} MB" -f $manifesto.Count, (($manifesto | Measure-Object bytes -Sum).Sum / 1MB))

    # comparacao com o snapshot anterior, se houver — e aqui que a mutabilidade aparece
    $anteriores = Get-ChildItem $raiz -Directory |
                  Where-Object { $_.Name -match '^\d{4}-\d{2}-\d{2}$' -and $_.Name -lt $HOJE } |
                  Sort-Object Name -Descending
    if ($anteriores) {
        $ant = $anteriores[0]
        $mfAnt = Join-Path $ant.FullName "manifesto.csv"
        if (Test-Path $mfAnt) {
            Secao ("MUDOU DESDE {0}?" -f $ant.Name)
            $velho = Import-Csv $mfAnt
            $mudou = 0
            foreach ($n in $manifesto) {
                $v = $velho | Where-Object { $_.arquivo -eq $n.arquivo }
                if (-not $v) { Write-Host ("  NOVO      {0}" -f $n.arquivo) -ForegroundColor Yellow; $mudou++ }
                elseif ($v.sha256_16 -ne $n.sha256_16) {
                    Write-Host ("  MUDOU     {0}   {1} -> {2}" -f $n.arquivo, $v.sha256_16, $n.sha256_16) -ForegroundColor Yellow
                    $mudou++
                }
            }
            if ($mudou -eq 0) {
                Write-Host "  nada mudou. A base esta estavel neste intervalo." -ForegroundColor Gray
            } else {
                Write-Host ""
                Write-Host ("  {0} arquivo(s) mudaram. Cada snapshot guardado e uma resposta" -f $mudou) -ForegroundColor Yellow
                Write-Host "  a 'o que era possivel saber naquele dia' que nao existiria sem ele." -ForegroundColor Yellow
            }
        }
    }
}

Secao "DEPOIS DISTO"
Write-Host "  1. Confira o conjunto de arquivos dentro de cada ZIP — ele MUDA entre safras."
Write-Host "     (composicao_capital so aparece em 2024; ver docs/fontes/cvm-enumeracoes-observadas.md)"
Write-Host "  2. NAO escreva o parser com lista fixa de arquivos. Varra o ZIP."
Write-Host "  3. Reagende: o ano corrente muda o tempo todo. Rodar semanalmente custa minutos."
