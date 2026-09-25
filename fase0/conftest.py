# -*- coding: utf-8 -*-
"""A fixture de sessao da P-141. O desenho, e por que a chave e o sha256, estao em
`memo_acervo.py`."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import memo_acervo  # noqa: E402


@pytest.fixture(scope="session")
def memo_do_acervo():
    return memo_acervo.novo_memo()
