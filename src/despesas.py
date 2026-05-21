import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src import dados
    from src.dados import despesas
    from src.logger import obter_logger
except ImportError:
    import dados
    from dados import despesas
    from logger import obter_logger

log = obter_logger("despesas")

_PASTA             = os.path.dirname(os.path.abspath(__file__))
_FICHEIRO_DESPESAS = os.path.join(_PASTA, "despesas.json")

_RESET      = "\033[0m"
_BOLD       = "\033[1m"
_BRANCO     = "\033[97m"
_CINZA      = "\033[90m"
_VERDE      = "\033[32m"
_VERDE_B    = "\033[92m"
_AMARELO    = "\033[33m"
_VERMELHO   = "\033[31m"
_VERMELHO_B = "\033[91m"


def _arredondar(valor):
    return round(valor, 2)

def _data_hoje():
    return dados.data_simulada_str()


# ---------------------------------------------------------------------------
# Persistência
# ---------------------------------------------------------------------------

def guardar_despesas():
    log.info("A guardar despesas em %s", _FICHEIRO_DESPESAS)
    payload = {
        "despesas":           [list(d) for d in despesas],
        "proximo_id_despesa": dados.proximo_id_despesa,
    }
    try:
        with open(_FICHEIRO_DESPESAS, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        log.info("Despesas guardadas com sucesso (%d registos)", len(despesas))
    except OSError as e:
        log.critical("Erro ao guardar despesas: %s", e)


def carregar_despesas():
    if not os.path.exists(_FICHEIRO_DESPESAS):
        log.warning("Ficheiro %s nao encontrado — a iniciar sem dados", _FICHEIRO_DESPESAS)
        return False
    log.info("A carregar despesas de %s", _FICHEIRO_DESPESAS)
    try:
        with open(_FICHEIRO_DESPESAS, "r", encoding="utf-8") as f:
            payload = json.load(f)
        despesas.clear()
        for item in payload["despesas"]:
            despesas.append(tuple(item))
        dados.proximo_id_despesa = payload["proximo_id_despesa"]
        log.info("Despesas carregadas com sucesso (%d registos)", len(despesas))
        return True
    except (OSError, json.JSONDecodeError, KeyError) as e:
        log.error("Erro ao carregar despesas: %s", e)
        return False


# ---------------------------------------------------------------------------
# Auxiliares
# ---------------------------------------------------------------------------

def registar_transacao_saida(descricao, valor, data=None):
    if data is None:
        data = _data_hoje()
    log.info("A registar transacao saida: descricao='%s' valor=%.2f data=%s", descricao, valor, data)
    dados.transacoes.append({
        "id":        dados.proximo_id_transacao,
        "tipo":      "saida",
        "descricao": descricao,
        "valor":     _arredondar(valor),
        "data":      data,
    })
    dados.proximo_id_transacao += 1


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------

def adicionar_despesa(descricao, valor, data_despesa=None):
    log.info("Tentativa de adicionar despesa: descricao='%s' valor=%s", descricao, valor)
    carregar_despesas()
    if not descricao:
        log.warning("Descricao vazia — despesa nao criada")
        return None, 400
    if not isinstance(valor, (int, float)) or valor <= 0:
        log.warning("Valor invalido ao adicionar despesa: %s", valor)
        return None, 400
    if data_despesa is None:
        data_despesa = _data_hoje()
    nova = (dados.proximo_id_despesa, descricao, _arredondar(valor), data_despesa)
    despesas.append(nova)
    registar_transacao_saida(descricao, valor, data=data_despesa)
    dados.proximo_id_despesa += 1
    guardar_despesas()
    log.info("Despesa criada com sucesso: id=%d descricao='%s' valor=%.2f", nova[0], descricao, valor)
    return nova, 201


def obter_despesa(id_despesa):
    log.info("A obter despesa id=%d", id_despesa)
    carregar_despesas()
    for despesa in despesas:
        if despesa[0] == id_despesa:
            return despesa, 200
    log.warning("Despesa id=%d nao encontrada", id_despesa)
    return None, 404


def remover_despesa(id_despesa):
    log.info("Tentativa de remover despesa id=%d", id_despesa)
    carregar_despesas()
    for despesa in despesas:
        if despesa[0] == id_despesa:
            despesas.remove(despesa)
            guardar_despesas()
            log.info("Despesa id=%d removida com sucesso", id_despesa)
            return id_despesa, 200
    log.warning("Despesa id=%d nao encontrada para remocao", id_despesa)
    return None, 404


def mostrar_despesas():
    log.info("A listar todas as despesas")
    carregar_despesas()
    if len(despesas) == 0:
        log.info("Nenhuma despesa encontrada")
        return [], 204
    print()
    print(_VERDE + _BOLD + "[ DESPESAS ]" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    for despesa in despesas:
        data = despesa[3] if len(despesa) > 3 else "N/A"
        print(_AMARELO + "ID: "        + _RESET + _BRANCO   + str(despesa[0]) + _RESET)
        print(_CINZA   + "Descricao: " + _RESET + _BRANCO   + despesa[1]      + _RESET)
        print(_CINZA   + "Valor: "     + _RESET + _VERMELHO + str(despesa[2]) + " EUR" + _RESET)
        print(_CINZA   + "Data: "      + _RESET + _BRANCO   + data            + _RESET)
        print(_CINZA + "-" * 40 + _RESET)
    log.info("Listagem concluida: %d despesas apresentadas", len(despesas))
    return list(despesas), 200


def mostrar_despesa(id_despesa):
    log.info("A mostrar despesa id=%d", id_despesa)
    carregar_despesas()
    despesa, codigo = obter_despesa(id_despesa)
    if codigo == 404:
        log.warning("Despesa id=%d nao encontrada para mostrar", id_despesa)
        return None, 404
    data = despesa[3] if len(despesa) > 3 else "N/A"
    print()
    print(_VERDE + _BOLD + "[ DESPESA ]" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    print(_AMARELO + "ID: "        + _RESET + _BRANCO   + str(despesa[0]) + _RESET)
    print(_CINZA   + "Descricao: " + _RESET + _BRANCO   + despesa[1]      + _RESET)
    print(_CINZA   + "Valor: "     + _RESET + _VERMELHO + str(despesa[2]) + " EUR" + _RESET)
    print(_CINZA   + "Data: "      + _RESET + _BRANCO   + data            + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    return despesa, 200
