import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src import dados
    from src.dados import clientes
    from src.planos import obter_plano
except ImportError:
    import dados
    from dados import clientes
    from planos import obter_plano

_RESET      = "\033[0m"
_BOLD       = "\033[1m"
_BRANCO     = "\033[97m"
_CINZA      = "\033[90m"
_VERDE      = "\033[32m"
_VERDE_B    = "\033[92m"
_AMARELO    = "\033[33m"
_VERMELHO_B = "\033[91m"
_MAGENTA    = "\033[35m"

def _arredondar(valor):
    return round(valor, 2)

def _ids_clientes():
    return list(clientes.keys())

def adicionar_cliente(nome, data_nascimento, telefone, id_plano, data_inicio):
    if not nome:
        return None, 400
    for id_c in clientes:
        if clientes[id_c]["nome"] == nome:
            return None, 409
    plano, codigo = obter_plano(id_plano)
    if codigo == 404:
        return None, 404
    clientes[dados.proximo_id_cliente] = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "telefone": telefone,
        "id_plano": id_plano,
        "data_inicio": data_inicio
    }
    dados.proximo_id_cliente = dados.proximo_id_cliente + 1
    return clientes[dados.proximo_id_cliente - 1], 201

def obter_cliente(id_cliente):
    cliente = clientes.get(id_cliente)
    if cliente is None:
        return None, 404
    return cliente, 200

def modificar_cliente(id_cliente, nome, data_nascimento, telefone, id_plano_str, data_inicio):
    if id_cliente not in clientes:
        return None, 404
    dados_cliente = clientes[id_cliente]
    if nome != "":
        for id_c in clientes:
            if id_c != id_cliente and clientes[id_c]["nome"] == nome:
                return None, 409
        dados_cliente["nome"] = nome
    if data_nascimento != "":
        dados_cliente["data_nascimento"] = data_nascimento
    if telefone != "":
        dados_cliente["telefone"] = telefone
    if id_plano_str != "":
        try:
            novo_id = int(id_plano_str)
        except (ValueError, TypeError):
            return None, 400
        plano, codigo = obter_plano(novo_id)
        if codigo == 404:
            return None, 404
        dados_cliente["id_plano"] = novo_id
    if data_inicio != "":
        dados_cliente["data_inicio"] = data_inicio
    return dados_cliente, 200

def remover_cliente(id_cliente):
    if id_cliente not in clientes:
        return None, 404
    del clientes[id_cliente]
    return id_cliente, 200

def mostrar_clientes():
    if len(clientes) == 0:
        return [], 204
    print()
    print(_VERDE + _BOLD + "[ CLIENTES ]" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    for id_cliente, dados_cliente in clientes.items():
        plano, _ = obter_plano(dados_cliente["id_plano"])
        if plano:
            nome_plano, num_treinos, preco_treino = plano
            preco_mensal = _arredondar(num_treinos * preco_treino)
        else:
            nome_plano, preco_mensal = "Sem plano", 0.0
        print(_AMARELO + "ID: "           + _RESET + _BRANCO  + str(id_cliente)                  + _RESET)
        print(_CINZA   + "Nome: "         + _RESET + _BRANCO  + dados_cliente["nome"]            + _RESET)
        print(_CINZA   + "Nascimento: "   + _RESET           + dados_cliente["data_nascimento"])
        print(_CINZA   + "Telefone: "     + _RESET           + dados_cliente["telefone"])
        print(_CINZA   + "Plano: "        + _RESET + _MAGENTA + nome_plano                       + _RESET)
        print(_CINZA   + "Inicio plano: " + _RESET           + dados_cliente["data_inicio"])
        print(_CINZA   + "Mensalidade: "  + _RESET + _VERDE   + str(preco_mensal) + " EUR"       + _RESET)
        print(_CINZA + "-" * 40 + _RESET)
    return list(clientes.values()), 200

def mostrar_cliente(id_cliente):
    if id_cliente not in clientes:
        return None, 404
    dados_cliente = clientes[id_cliente]
    plano, _ = obter_plano(dados_cliente["id_plano"])
    if plano:
        nome_plano, num_treinos, preco_treino = plano
        preco_mensal = _arredondar(num_treinos * preco_treino)
    else:
        nome_plano, num_treinos, preco_treino, preco_mensal = "Sem plano", 0, 0.0, 0.0
    print()
    print(_VERDE + _BOLD + "[ CLIENTE ]" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    print(_AMARELO + "ID: "           + _RESET + _BRANCO  + str(id_cliente)                  + _RESET)
    print(_CINZA   + "Nome: "         + _RESET + _BRANCO  + dados_cliente["nome"]            + _RESET)
    print(_CINZA   + "Nascimento: "   + _RESET           + dados_cliente["data_nascimento"])
    print(_CINZA   + "Telefone: "     + _RESET           + dados_cliente["telefone"])
    print(_CINZA   + "Plano: "        + _RESET + _MAGENTA + nome_plano                       + _RESET)
    print(_CINZA   + "Treinos/mes: "  + _RESET           + str(num_treinos))
    print(_CINZA   + "Preco/treino: " + _RESET + _VERDE   + str(preco_treino) + " EUR"       + _RESET)
    print(_CINZA   + "Mensalidade: "  + _RESET + _VERDE   + str(preco_mensal) + " EUR"       + _RESET)
    print(_CINZA   + "Inicio plano: " + _RESET           + dados_cliente["data_inicio"])
    print(_CINZA + "-" * 40 + _RESET)
    return dados_cliente, 200

def pesquisar_cliente(pesquisa):
    if not pesquisa:
        return None, 400
    print()
    print(_VERDE + _BOLD + "[ RESULTADOS ]" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    encontrados = []
    for id_cliente, dados_cliente in clientes.items():
        if pesquisa.lower() in dados_cliente["nome"].lower():
            plano, _ = obter_plano(dados_cliente["id_plano"])
            nome_plano = plano[0] if plano else "Sem plano"
            print(_AMARELO + "ID: "    + _RESET + _BRANCO  + str(id_cliente)       + _RESET)
            print(_CINZA   + "Nome: "  + _RESET + _BRANCO  + dados_cliente["nome"] + _RESET)
            print(_CINZA   + "Plano: " + _RESET + _MAGENTA + nome_plano            + _RESET)
            print(_CINZA + "-" * 40 + _RESET)
            encontrados.append(dados_cliente)
    if not encontrados:
        return [], 404
    return encontrados, 200
