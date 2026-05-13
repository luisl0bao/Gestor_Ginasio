import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src import dados
    from src.dados import despesas
except ImportError:
    import dados
    from dados import despesas

_PASTA = os.path.dirname(os.path.abspath(__file__))
_FICHEIRO_DESPESAS = os.path.join(_PASTA, "despesas.json")


def guardar_despesas():
    """Guarda apenas os dados das despesas em despesas.json."""
    payload = {
        "despesas":           [list(d) for d in despesas],
        "proximo_id_despesa": dados.proximo_id_despesa,
    }
    with open(_FICHEIRO_DESPESAS, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print("\033[92mDespesas guardadas em: " + _FICHEIRO_DESPESAS + "\033[0m")


def carregar_despesas() -> bool:
    """Carrega os dados das despesas de despesas.json. Devolve True se carregou."""
    if not os.path.exists(_FICHEIRO_DESPESAS):
        return False
    with open(_FICHEIRO_DESPESAS, "r", encoding="utf-8") as f:
        payload = json.load(f)
    despesas.clear()
    for item in payload["despesas"]:
        despesas.append(tuple(item))
    dados.proximo_id_despesa = payload["proximo_id_despesa"]
    return True

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
    """Usa data simulada se disponível, senão data real."""
    return dados.data_simulada_str()

def registar_transacao_saida(descricao, valor, data=None):
    """Regista uma saída no log de transações. Chamável externamente (ex: simular_mes)."""
    if not hasattr(dados, "transacoes"):
        dados.transacoes = []
    if not hasattr(dados, "proximo_id_transacao"):
        dados.proximo_id_transacao = 1
    if data is None:
        data = _data_hoje()
    dados.transacoes.append({
        "id":        dados.proximo_id_transacao,
        "tipo":      "saida",
        "descricao": descricao,
        "valor":     _arredondar(valor),
        "data":      data
    })
    dados.proximo_id_transacao += 1

def adicionar_despesa(descricao, valor, data_despesa=None):
    if not descricao:
        return None, 400
    if not isinstance(valor, (int, float)) or valor <= 0:
        return None, 400
    if data_despesa is None:
        data_despesa = _data_hoje()
    nova = (dados.proximo_id_despesa, descricao, _arredondar(valor), data_despesa)
    despesas.append(nova)
    registar_transacao_saida(descricao, valor, data=data_despesa)
    dados.proximo_id_despesa += 1
    return nova, 201

def obter_despesa(id_despesa):
    for despesa in despesas:
        if despesa[0] == id_despesa:
            return despesa, 200
    return None, 404

def remover_despesa(id_despesa):
    for despesa in despesas:
        if despesa[0] == id_despesa:
            despesas.remove(despesa)
            return id_despesa, 200
    return None, 404

def mostrar_despesas():
    if len(despesas) == 0:
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
    return list(despesas), 200

def mostrar_despesa(id_despesa):
    despesa, codigo = obter_despesa(id_despesa)
    if codigo == 404:
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
