"""
Módulo de gestão de ginásios.
Cada ginásio tem dados completamente isolados (clientes, planos, despesas,
pagamentos, transações e contadores próprios), sem interferência entre si.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ---------------------------------------------------------------------------
# Cores ANSI
# ---------------------------------------------------------------------------
_RESET      = "\033[0m"
_BOLD       = "\033[1m"
_BRANCO     = "\033[97m"
_CINZA      = "\033[90m"
_VERDE      = "\033[32m"
_VERDE_B    = "\033[92m"
_AMARELO    = "\033[33m"
_VERMELHO   = "\033[31m"
_VERMELHO_B = "\033[91m"
_MAGENTA    = "\033[35m"

# ---------------------------------------------------------------------------
# Armazenamento global de ginásios
# ---------------------------------------------------------------------------
# Estrutura de cada ginásio:
# {
#   "id": int,
#   "nome": str,
#   "morada": str,
#   "telefone": str,
#   "dados": {          ← estado isolado equivalente a dados.py
#       "clientes": {},
#       "planos": {},
#       "despesas": [],
#       "pagamentos": {},
#       "transacoes": [],
#       "proximo_id_cliente": 1,
#       "proximo_id_plano": 1,
#       "proximo_id_despesa": 1,
#       "proximo_id_pagamento": 1,
#       "proximo_id_transacao": 1,
#       "saldo_acumulado": 0.0,
#   }
# }

_ginasios: dict = {}          # id_ginasio -> dict
_proximo_id_ginasio: int = 1


def _novo_estado_dados() -> dict:
    """Cria um estado de dados vazio e isolado para um ginásio."""
    from datetime import date
    return {
        "clientes":              {},
        "planos":                {},
        "despesas":              [],
        "pagamentos":            {},
        "transacoes":            [],
        "proximo_id_cliente":    1,
        "proximo_id_plano":      1,
        "proximo_id_despesa":    1,
        "proximo_id_pagamento":  1,
        "proximo_id_transacao":  1,
        "saldo_acumulado":       0.0,
        "data_simulada":         date(2025, 1, 1),
    }


# ---------------------------------------------------------------------------
# CRUD de ginásios
# ---------------------------------------------------------------------------

def adicionar_ginasio(nome: str, morada: str, telefone: str):
    """Cria um ginásio novo com dados isolados. Retorna (obj, codigo)."""
    global _proximo_id_ginasio
    if not nome or not isinstance(nome, str) or nome.strip() == "":
        return None, 400
    if not morada or not isinstance(morada, str) or morada.strip() == "":
        return None, 400
    if not telefone or not isinstance(telefone, str):
        return None, 400
    telefone = telefone.strip()
    if not telefone.isdigit() or len(telefone) != 9:
        return None, 400

    # Verificar nome duplicado
    nome = nome.strip()
    morada = morada.strip()
    for g in _ginasios.values():
        if g["nome"].lower() == nome.lower():
            return None, 409

    ginasio = {
        "id":      _proximo_id_ginasio,
        "nome":    nome,
        "morada":  morada,
        "telefone": telefone,
        "dados":   _novo_estado_dados(),
    }
    _ginasios[_proximo_id_ginasio] = ginasio
    _proximo_id_ginasio += 1
    return ginasio, 201


def obter_ginasio(id_ginasio: int):
    """Devolve (ginasio, 200) ou (None, 404)."""
    g = _ginasios.get(id_ginasio)
    if g is None:
        return None, 404
    return g, 200


def modificar_ginasio(id_ginasio: int, nome: str, morada: str, telefone: str):
    """Atualiza os dados de identificação do ginásio. Campos vazios mantêm valor."""
    if id_ginasio not in _ginasios:
        return None, 404
    g = _ginasios[id_ginasio]

    nome    = nome.strip()    if nome    else ""
    morada  = morada.strip()  if morada  else ""
    telefone = telefone.strip() if telefone else ""

    if nome == "":
        nome = g["nome"]
    else:
        # Verificar duplicado (ignorando o próprio)
        for gid, gv in _ginasios.items():
            if gid != id_ginasio and gv["nome"].lower() == nome.lower():
                return None, 409

    if morada == "":
        morada = g["morada"]

    if telefone == "":
        telefone = g["telefone"]
    else:
        if not telefone.isdigit() or len(telefone) != 9:
            return None, 400

    g["nome"]     = nome
    g["morada"]   = morada
    g["telefone"] = telefone
    return g, 200


def remover_ginasio(id_ginasio: int):
    """Remove um ginásio. Retorna (id, 200) ou (None, 404)."""
    if id_ginasio not in _ginasios:
        return None, 404
    del _ginasios[id_ginasio]
    return id_ginasio, 200


# ---------------------------------------------------------------------------
# Listagem / visualização
# ---------------------------------------------------------------------------

def mostrar_ginasios():
    """Imprime todos os ginásios. Retorna (lista, codigo)."""
    if not _ginasios:
        return [], 204
    print()
    print(_VERDE + _BOLD + "[ GINASIOS ]" + _RESET)
    print(_CINZA + "-" * 44 + _RESET)
    for gid, g in _ginasios.items():
        total_clientes = len(g["dados"]["clientes"])
        total_planos   = len(g["dados"]["planos"])
        print(_AMARELO + "ID: "       + _RESET + _BRANCO  + str(gid)            + _RESET)
        print(_CINZA   + "Nome: "     + _RESET + _BRANCO  + g["nome"]           + _RESET)
        print(_CINZA   + "Morada: "   + _RESET + _BRANCO  + g["morada"]         + _RESET)
        print(_CINZA   + "Telefone: " + _RESET + _BRANCO  + g["telefone"]       + _RESET)
        print(_CINZA   + "Clientes: " + _RESET + _AMARELO + str(total_clientes) + _RESET)
        print(_CINZA   + "Planos: "   + _RESET + _AMARELO + str(total_planos)   + _RESET)
        print(_CINZA + "-" * 44 + _RESET)
    return list(_ginasios.values()), 200


def mostrar_ginasio(id_ginasio: int):
    """Imprime detalhes de um ginásio. Retorna (obj, codigo)."""
    g = _ginasios.get(id_ginasio)
    if g is None:
        return None, 404
    total_clientes = len(g["dados"]["clientes"])
    total_planos   = len(g["dados"]["planos"])
    total_despesas = len(g["dados"]["despesas"])
    print()
    print(_VERDE + _BOLD + "[ GINASIO ]" + _RESET)
    print(_CINZA + "-" * 44 + _RESET)
    print(_AMARELO + "ID: "        + _RESET + _BRANCO  + str(g["id"])        + _RESET)
    print(_CINZA   + "Nome: "      + _RESET + _BRANCO  + g["nome"]           + _RESET)
    print(_CINZA   + "Morada: "    + _RESET + _BRANCO  + g["morada"]         + _RESET)
    print(_CINZA   + "Telefone: "  + _RESET + _BRANCO  + g["telefone"]       + _RESET)
    print(_CINZA   + "Clientes: "  + _RESET + _AMARELO + str(total_clientes) + _RESET)
    print(_CINZA   + "Planos: "    + _RESET + _AMARELO + str(total_planos)   + _RESET)
    print(_CINZA   + "Despesas: "  + _RESET + _AMARELO + str(total_despesas) + _RESET)
    print(_CINZA + "-" * 44 + _RESET)
    return g, 200


# ---------------------------------------------------------------------------
# Helpers para o menu
# ---------------------------------------------------------------------------

def _ids_ginasios() -> list:
    return list(_ginasios.keys())


def _resumo_ginasios():
    """Imprime uma linha resumida por ginásio (para seleção rápida)."""
    if not _ginasios:
        return [], 204
    print(_CINZA + "Ginasios disponiveis:" + _RESET)
    for gid, g in _ginasios.items():
        print(_AMARELO + "[" + str(gid) + "] " + _RESET +
              _BRANCO + g["nome"] + _RESET +
              _CINZA + " — " + g["morada"] + _RESET)
    return list(_ginasios.values()), 200
