"""
Módulo de gestão de ginásios.
Cada ginásio tem dados completamente isolados (clientes, planos, despesas,
pagamentos, transações e contadores próprios), sem interferência entre si.
"""

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_PASTA = os.path.dirname(os.path.abspath(__file__))
_FICHEIRO_GINASIOS = os.path.join(_PASTA, "ginasios.json")

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
_ginasios: dict = {}
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
    carregar_ginasios()
    if not nome or not isinstance(nome, str) or nome.strip() == "":
        return None, 400
    if not morada or not isinstance(morada, str) or morada.strip() == "":
        return None, 400
    if not telefone or not isinstance(telefone, str):
        return None, 400
    telefone = telefone.strip()
    if not telefone.isdigit() or len(telefone) != 9:
        return None, 400

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
    guardar_ginasios()
    return ginasio, 201


def obter_ginasio(id_ginasio: int):
    """Devolve (ginasio, 200) ou (None, 404)."""
    carregar_ginasios()
    g = _ginasios.get(id_ginasio)
    if g is None:
        return None, 404
    return g, 200


def modificar_ginasio(id_ginasio: int, nome: str, morada: str, telefone: str):
    """Atualiza os dados de identificação do ginásio. Campos vazios mantêm valor."""
    carregar_ginasios()
    if id_ginasio not in _ginasios:
        return None, 404
    g = _ginasios[id_ginasio]

    nome    = nome.strip()    if nome    else ""
    morada  = morada.strip()  if morada  else ""
    telefone = telefone.strip() if telefone else ""

    if nome == "":
        nome = g["nome"]
    else:
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
    guardar_ginasios()
    return g, 200


def remover_ginasio(id_ginasio: int):
    """Remove um ginásio. Retorna (id, 200) ou (None, 404)."""
    carregar_ginasios()
    if id_ginasio not in _ginasios:
        return None, 404
    del _ginasios[id_ginasio]
    guardar_ginasios()
    return id_ginasio, 200


# ---------------------------------------------------------------------------
# Listagem / visualização
# ---------------------------------------------------------------------------

def mostrar_ginasios():
    """Imprime todos os ginásios. Retorna (lista, codigo)."""
    carregar_ginasios()
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
    carregar_ginasios()
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


def _ids_ginasios() -> list:
    carregar_ginasios()
    return list(_ginasios.keys())


def _resumo_ginasios():
    """Imprime uma linha resumida por ginásio (para seleção rápida)."""
    carregar_ginasios()
    if not _ginasios:
        return [], 204
    print(_CINZA + "Ginasios disponiveis:" + _RESET)
    for gid, g in _ginasios.items():
        print(_AMARELO + "[" + str(gid) + "] " + _RESET +
              _BRANCO + g["nome"] + _RESET +
              _CINZA + " — " + g["morada"] + _RESET)
    return list(_ginasios.values()), 200


# ---------------------------------------------------------------------------
# Guardar / Carregar ginásios
# ---------------------------------------------------------------------------

def guardar_ginasios():
    """Guarda apenas os dados dos ginásios em ginasios.json."""
    def _d(d):
        return d.isoformat() if hasattr(d, "isoformat") else str(d)

    ginasios_serial = {}
    for gid, g in _ginasios.items():
        d = g["dados"]
        ginasios_serial[str(gid)] = {
            "id":       g["id"],
            "nome":     g["nome"],
            "morada":   g["morada"],
            "telefone": g["telefone"],
            "dados": {
                "clientes":             {str(k): v for k, v in d["clientes"].items()},
                "planos":               {str(k): list(v) for k, v in d["planos"].items()},
                "despesas":             [list(x) for x in d["despesas"]],
                "pagamentos":           {str(k): dict(v) for k, v in d["pagamentos"].items()},
                "transacoes":           list(d["transacoes"]),
                "proximo_id_cliente":   d["proximo_id_cliente"],
                "proximo_id_plano":     d["proximo_id_plano"],
                "proximo_id_despesa":   d["proximo_id_despesa"],
                "proximo_id_pagamento": d["proximo_id_pagamento"],
                "proximo_id_transacao": d["proximo_id_transacao"],
                "saldo_acumulado":      d["saldo_acumulado"],
                "data_simulada":        _d(d["data_simulada"]),
            }
        }

    payload = {
        "proximo_id_ginasio": _proximo_id_ginasio,
        "ginasios":           ginasios_serial,
    }
    with open(_FICHEIRO_GINASIOS, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print("\033[92mGinasios guardados em: " + _FICHEIRO_GINASIOS + "\033[0m")


def carregar_ginasios() -> bool:
    """Carrega os dados dos ginásios de ginasios.json. Devolve True se carregou."""
    global _proximo_id_ginasio
    if not os.path.exists(_FICHEIRO_GINASIOS):
        return False

    from datetime import date

    with open(_FICHEIRO_GINASIOS, "r", encoding="utf-8") as f:
        payload = json.load(f)

    _ginasios.clear()
    _proximo_id_ginasio = payload.get("proximo_id_ginasio", 1)

    for gid_str, g_serial in payload.get("ginasios", {}).items():
        gid   = int(gid_str)
        d_s   = g_serial["dados"]
        d     = _novo_estado_dados()

        d["clientes"].clear()
        for k, v in d_s["clientes"].items():
            d["clientes"][int(k)] = v

        d["planos"].clear()
        for k, v in d_s["planos"].items():
            d["planos"][int(k)] = tuple(v)

        d["despesas"].clear()
        for item in d_s["despesas"]:
            d["despesas"].append(tuple(item))

        d["pagamentos"].clear()
        for k, v in d_s["pagamentos"].items():
            d["pagamentos"][int(k)] = v

        d["transacoes"].clear()
        d["transacoes"].extend(d_s["transacoes"])

        d["proximo_id_cliente"]   = d_s["proximo_id_cliente"]
        d["proximo_id_plano"]     = d_s["proximo_id_plano"]
        d["proximo_id_despesa"]   = d_s["proximo_id_despesa"]
        d["proximo_id_pagamento"] = d_s["proximo_id_pagamento"]
        d["proximo_id_transacao"] = d_s["proximo_id_transacao"]
        d["saldo_acumulado"]      = d_s["saldo_acumulado"]
        d["data_simulada"]        = date.fromisoformat(d_s["data_simulada"])

        _ginasios[gid] = {
            "id":       g_serial["id"],
            "nome":     g_serial["nome"],
            "morada":   g_serial["morada"],
            "telefone": g_serial["telefone"],
            "dados":    d,
        }

    return True
