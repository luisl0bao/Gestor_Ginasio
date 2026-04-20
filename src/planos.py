import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src import dados
    from src.dados import planos
except ImportError:
    import dados
    from dados import planos

_RESET      = "\033[0m"
_BOLD       = "\033[1m"
_BRANCO     = "\033[97m"
_CINZA      = "\033[90m"
_VERDE      = "\033[32m"
_VERDE_B    = "\033[92m"
_AMARELO    = "\033[33m"
_VERMELHO_B = "\033[91m"

def _arredondar(valor):
    return round(valor, 2)

def _ids_planos():
    return list(planos.keys())

def adicionar_plano(nome, num_treinos, preco_por_treino):
    if not nome or not isinstance(nome, str):
        return None, 400
    if not isinstance(num_treinos, int) or num_treinos <= 0:
        return None, 400
    if not isinstance(preco_por_treino, (int, float)) or preco_por_treino <= 0:
        return None, 400
    planos[dados.proximo_id_plano] = (nome, num_treinos, _arredondar(preco_por_treino))
    dados.proximo_id_plano = dados.proximo_id_plano + 1
    return planos[dados.proximo_id_plano - 1], 201

def obter_plano(id_plano):
    plano = planos.get(id_plano)
    if plano is None:
        return None, 404
    return plano, 200

def modificar_plano(id_plano, nome, num_treinos, preco_por_treino):
    if id_plano not in planos:
        return None, 404
    plano_atual = planos[id_plano]
    if nome == "":
        nome = plano_atual[0]
    if num_treinos == "":
        num_treinos = plano_atual[1]
    else:
        try:
            num_treinos = int(num_treinos)
            if num_treinos <= 0:
                return None, 400
        except (TypeError, ValueError):
            return None, 400
    if preco_por_treino == "":
        preco_por_treino = plano_atual[2]
    else:
        try:
            preco_por_treino = _arredondar(float(preco_por_treino))
            if preco_por_treino <= 0:
                return None, 400
        except (TypeError, ValueError):
            return None, 400
    planos[id_plano] = (nome, num_treinos, preco_por_treino)
    return planos[id_plano], 200

def remover_plano(id_plano):
    if id_plano not in planos:
        return None, 404
    try:
        from src.dados import clientes as _clientes
    except ImportError:
        from dados import clientes as _clientes
    for id_cliente in _clientes:
        if _clientes[id_cliente]["id_plano"] == id_plano:
            return None, 409
    del planos[id_plano]
    return id_plano, 200

def mostrar_planos():
    if len(planos) == 0:
        return [], 204
    try:
        from src.dados import clientes as _clientes
    except ImportError:
        from dados import clientes as _clientes
    print()
    print(_VERDE + _BOLD + "[ PLANOS ]" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    for id_plano, dados_plano in planos.items():
        total_clientes = sum(1 for c in _clientes.values() if c["id_plano"] == id_plano)
        preco_mensal = _arredondar(dados_plano[1] * dados_plano[2])
        print(_AMARELO + "ID: "           + _RESET + _BRANCO  + str(id_plano)       + _RESET)
        print(_CINZA   + "Nome: "         + _RESET + _BRANCO  + dados_plano[0]      + _RESET)
        print(_CINZA   + "Treinos/mes: "  + _RESET + str(dados_plano[1]))
        print(_CINZA   + "Preco/treino: " + _RESET + _VERDE   + str(dados_plano[2]) + " EUR" + _RESET)
        print(_CINZA   + "Total mensal: " + _RESET + _VERDE   + str(preco_mensal)   + " EUR" + _RESET)
        print(_CINZA   + "Clientes: "     + _RESET + _AMARELO + str(total_clientes) + _RESET)
        print(_CINZA + "-" * 40 + _RESET)
    return list(planos.values()), 200

def mostrar_plano(id_plano):
    if id_plano not in planos:
        return None, 404
    dados_plano = planos[id_plano]
    preco_mensal = _arredondar(dados_plano[1] * dados_plano[2])
    print()
    print(_VERDE + _BOLD + "[ PLANO ]" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    print(_AMARELO + "ID: "           + _RESET + _BRANCO + str(id_plano)       + _RESET)
    print(_CINZA   + "Nome: "         + _RESET + _BRANCO + dados_plano[0]      + _RESET)
    print(_CINZA   + "Treinos/mes: "  + _RESET + str(dados_plano[1]))
    print(_CINZA   + "Preco/treino: " + _RESET + _VERDE  + str(dados_plano[2]) + " EUR" + _RESET)
    print(_CINZA   + "Total mensal: " + _RESET + _VERDE  + str(preco_mensal)   + " EUR" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    return dados_plano, 200

def _resumo_planos():
    if len(planos) == 0:
        return [], 204
    print(_CINZA + "Planos disponiveis:" + _RESET)
    for id_plano, dados_plano in planos.items():
        preco_mensal = _arredondar(dados_plano[1] * dados_plano[2])
        print(_AMARELO + "[" + str(id_plano) + "] " + _RESET +
              _BRANCO + dados_plano[0] + _RESET +
              _CINZA + " - " + str(dados_plano[1]) + " treinos - " + str(preco_mensal) + " EUR/mes" + _RESET)
    return list(planos.values()), 200
