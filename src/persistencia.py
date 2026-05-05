"""
Módulo de persistência JSON.
Guarda e carrega TODOS os dados do programa:
  - Ginásio Default (dados em src.dados)
  - Todos os ginásios extras (src.ginasios)
  - Contadores globais
"""

import json
import os
from datetime import date

# Ficheiro de dados dentro da pasta src/
_PASTA_BASE = os.path.dirname(os.path.abspath(__file__))
FICHEIRO_JSON = os.path.join(_PASTA_BASE, "dados_ginasio.json")


# ---------------------------------------------------------------------------
# Serialização helpers
# ---------------------------------------------------------------------------

def _data_para_str(d) -> str:
    """Converte date para string ISO."""
    if isinstance(d, date):
        return d.isoformat()
    return str(d)


def _str_para_date(s: str) -> date:
    """Converte string ISO para date."""
    return date.fromisoformat(s)


# ---------------------------------------------------------------------------
# GUARDAR
# ---------------------------------------------------------------------------

def guardar():
    """
    Serializa o estado completo (ginásio default + ginásios extra)
    para dados_ginasio.json usando UTF-8.
    """
    try:
        from src import dados
        from src import ginasios as mod_gin
    except ImportError:
        import dados
        import ginasios as mod_gin

    # ── Ginásio Default ────────────────────────────────────────────
    # As despesas são listas de tuplos — converter para listas
    despesas_serial = []
    for d in dados.despesas:
        despesas_serial.append(list(d))

    # planos: chave int → (nome, num, preco) — converter chave para str (JSON só aceita str)
    planos_serial = {}
    for pid, p in dados.planos.items():
        planos_serial[str(pid)] = list(p)

    # pagamentos e transações já são dicts com tipos básicos
    pagamentos_serial = {}
    for pgid, pg in dados.pagamentos.items():
        pagamentos_serial[str(pgid)] = dict(pg)

    default_state = {
        "clientes":             {str(k): v for k, v in dados.clientes.items()},
        "planos":               planos_serial,
        "despesas":             despesas_serial,
        "pagamentos":           pagamentos_serial,
        "transacoes":           list(dados.transacoes),
        "proximo_id_cliente":   dados.proximo_id_cliente,
        "proximo_id_plano":     dados.proximo_id_plano,
        "proximo_id_despesa":   dados.proximo_id_despesa,
        "proximo_id_pagamento": dados.proximo_id_pagamento,
        "proximo_id_transacao": dados.proximo_id_transacao,
        "proximo_mes":          dados.proximo_mes,
        "saldo_acumulado":      dados.saldo_acumulado,
        "data_simulada":        _data_para_str(dados.data_simulada),
    }

    # ── Ginásios Extra ─────────────────────────────────────────────
    ginasios_serial = {}
    for gid, g in mod_gin._ginasios.items():
        d = g["dados"]
        # despesas locais
        desp_loc = [list(x) for x in d["despesas"]]
        # planos locais
        plan_loc = {str(pid): list(p) for pid, p in d["planos"].items()}
        # pagamentos locais
        pag_loc = {str(pgid): dict(pg) for pgid, pg in d["pagamentos"].items()}

        ginasios_serial[str(gid)] = {
            "id":       g["id"],
            "nome":     g["nome"],
            "morada":   g["morada"],
            "telefone": g["telefone"],
            "dados": {
                "clientes":             {str(k): v for k, v in d["clientes"].items()},
                "planos":               plan_loc,
                "despesas":             desp_loc,
                "pagamentos":           pag_loc,
                "transacoes":           list(d["transacoes"]),
                "proximo_id_cliente":   d["proximo_id_cliente"],
                "proximo_id_plano":     d["proximo_id_plano"],
                "proximo_id_despesa":   d["proximo_id_despesa"],
                "proximo_id_pagamento": d["proximo_id_pagamento"],
                "proximo_id_transacao": d["proximo_id_transacao"],
                "saldo_acumulado":      d["saldo_acumulado"],
                "data_simulada":        _data_para_str(d["data_simulada"]),
            }
        }

    payload = {
        "versao":                  1,
        "proximo_id_ginasio":      mod_gin._proximo_id_ginasio,
        "ginasio_default":         default_state,
        "ginasios":                ginasios_serial,
    }

    with open(FICHEIRO_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# CARREGAR
# ---------------------------------------------------------------------------

def carregar() -> bool:
    """
    Lê dados_ginasio.json e restaura todo o estado.
    Devolve True se carregou com sucesso, False se o ficheiro não existe.
    """
    if not os.path.exists(FICHEIRO_JSON):
        return False

    with open(FICHEIRO_JSON, "r", encoding="utf-8") as f:
        payload = json.load(f)

    try:
        from src import dados
        from src import ginasios as mod_gin
    except ImportError:
        import dados
        import ginasios as mod_gin

    # ── Ginásio Default ────────────────────────────────────────────
    ds = payload["ginasio_default"]

    # clientes: chave str → int
    dados.clientes.clear()
    for k, v in ds["clientes"].items():
        dados.clientes[int(k)] = v

    # planos: chave str → tuplo
    dados.planos.clear()
    for k, v in ds["planos"].items():
        dados.planos[int(k)] = tuple(v)

    # despesas: lista de listas → lista de tuplos
    dados.despesas.clear()
    for item in ds["despesas"]:
        dados.despesas.append(tuple(item))

    # pagamentos
    dados.pagamentos.clear()
    for k, v in ds["pagamentos"].items():
        dados.pagamentos[int(k)] = v

    # transações
    dados.transacoes.clear()
    dados.transacoes.extend(ds["transacoes"])

    # contadores e scalares
    dados.proximo_id_cliente   = ds["proximo_id_cliente"]
    dados.proximo_id_plano     = ds["proximo_id_plano"]
    dados.proximo_id_despesa   = ds["proximo_id_despesa"]
    dados.proximo_id_pagamento = ds["proximo_id_pagamento"]
    dados.proximo_id_transacao = ds["proximo_id_transacao"]
    dados.proximo_mes          = ds["proximo_mes"]
    dados.saldo_acumulado      = ds["saldo_acumulado"]
    dados.data_simulada        = _str_para_date(ds["data_simulada"])

    # ── Ginásios Extra ─────────────────────────────────────────────
    mod_gin._ginasios.clear()
    mod_gin._proximo_id_ginasio = payload.get("proximo_id_ginasio", 1)

    for gid_str, g_serial in payload.get("ginasios", {}).items():
        gid = int(gid_str)
        d_serial = g_serial["dados"]

        d = mod_gin._novo_estado_dados()

        # clientes
        d["clientes"].clear()
        for k, v in d_serial["clientes"].items():
            d["clientes"][int(k)] = v

        # planos
        d["planos"].clear()
        for k, v in d_serial["planos"].items():
            d["planos"][int(k)] = tuple(v)

        # despesas
        d["despesas"].clear()
        for item in d_serial["despesas"]:
            d["despesas"].append(tuple(item))

        # pagamentos
        d["pagamentos"].clear()
        for k, v in d_serial["pagamentos"].items():
            d["pagamentos"][int(k)] = v

        # transações
        d["transacoes"].clear()
        d["transacoes"].extend(d_serial["transacoes"])

        # contadores
        d["proximo_id_cliente"]   = d_serial["proximo_id_cliente"]
        d["proximo_id_plano"]     = d_serial["proximo_id_plano"]
        d["proximo_id_despesa"]   = d_serial["proximo_id_despesa"]
        d["proximo_id_pagamento"] = d_serial["proximo_id_pagamento"]
        d["proximo_id_transacao"] = d_serial["proximo_id_transacao"]
        d["saldo_acumulado"]      = d_serial["saldo_acumulado"]
        d["data_simulada"]        = _str_para_date(d_serial["data_simulada"])

        mod_gin._ginasios[gid] = {
            "id":       g_serial["id"],
            "nome":     g_serial["nome"],
            "morada":   g_serial["morada"],
            "telefone": g_serial["telefone"],
            "dados":    d,
        }

    return True
