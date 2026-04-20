import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src import dados
    from src.dados import despesas
except ImportError:
    import dados
    from dados import despesas

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

def adicionar_despesa(descricao, valor):
    if not descricao:
        return None, 400
    if not isinstance(valor, (int, float)) or valor <= 0:
        return None, 400
    nova = (dados.proximo_id_despesa, descricao, _arredondar(valor))
    despesas.append(nova)
    dados.proximo_id_despesa = dados.proximo_id_despesa + 1
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
        print(_AMARELO + "ID: "        + _RESET + _BRANCO   + str(despesa[0]) + _RESET)
        print(_CINZA   + "Descricao: " + _RESET + _BRANCO   + despesa[1]      + _RESET)
        print(_CINZA   + "Valor: "     + _RESET + _VERMELHO + str(despesa[2]) + " EUR" + _RESET)
        print(_CINZA + "-" * 40 + _RESET)
    return list(despesas), 200

def mostrar_despesa(id_despesa):
    despesa, codigo = obter_despesa(id_despesa)
    if codigo == 404:
        return None, 404
    print()
    print(_VERDE + _BOLD + "[ DESPESA ]" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    print(_AMARELO + "ID: "        + _RESET + _BRANCO   + str(despesa[0]) + _RESET)
    print(_CINZA   + "Descricao: " + _RESET + _BRANCO   + despesa[1]      + _RESET)
    print(_CINZA   + "Valor: "     + _RESET + _VERMELHO + str(despesa[2]) + " EUR" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    return despesa, 200
