from src import dados
from src.dados import clientes
from src.planos import obter_plano
from src.CoresANSII import VERDE_B, VERMELHO_B, AMARELO, BRANCO, VERDE, CINZA, BOLD, RESET, MAGENTA
# __Crud_____

def _arredondar(valor):
    return round(valor, 2)

def _ids_clientes():
    return list(clientes.keys())

def adicionar_cliente(nome, data_nascimento, telefone, id_plano, data_inicio):
    for id_c in clientes:
        if clientes[id_c]["nome"] == nome:
            print(VERMELHO_B + "Ja existe um cliente com esse nome." + RESET)
            return
    if obter_plano(id_plano) is None:
        print(VERMELHO_B + "Plano nao existe." + RESET)
        return
    clientes[dados.proximo_id_cliente] = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "telefone": telefone,
        "id_plano": id_plano,
        "data_inicio": data_inicio
    }
    dados.proximo_id_cliente = dados.proximo_id_cliente + 1
    print(VERDE_B + "Cliente adicionado." + RESET)

def obter_cliente(id_cliente):
    return clientes.get(id_cliente)

def modificar_cliente(id_cliente, nome, data_nascimento, telefone, id_plano_str, data_inicio):
    if id_cliente not in clientes:
        print(VERMELHO_B + "Cliente nao encontrado." + RESET)
        return
    dados = clientes[id_cliente]
    if nome != "":
        for id_c in clientes:
            if id_c != id_cliente and clientes[id_c]["nome"] == nome:
                print(VERMELHO_B + "Ja existe um cliente com esse nome." + RESET)
                return
        dados["nome"] = nome
    if data_nascimento != "":
        dados["data_nascimento"] = data_nascimento
    if telefone != "":
        dados["telefone"] = telefone
    if id_plano_str != "":
        novo_id = int(id_plano_str)
        if obter_plano(novo_id) is None:
            print(VERMELHO_B + "Plano nao existe." + RESET)
            return
        dados["id_plano"] = novo_id
    if data_inicio != "":
        dados["data_inicio"] = data_inicio
    print(VERDE_B + "Cliente atualizado." + RESET)

def remover_cliente(id_cliente):
    if id_cliente not in clientes:
        print(VERMELHO_B + "Cliente nao encontrado." + RESET)
        return
    del clientes[id_cliente]
    print(VERDE_B + "Cliente removido." + RESET)

def mostrar_clientes():
    if len(clientes) == 0:
        print(AMARELO + "Nenhum cliente registado." + RESET)
        return
    print()
    print(VERDE + BOLD + "[ CLIENTES ]" + RESET)
    print(CINZA + "-" * 40 + RESET)
    for id_cliente, dados in clientes.items():
        plano = obter_plano(dados["id_plano"])
        if plano:
            nome_plano, num_treinos, preco_treino = plano
            preco_mensal = _arredondar(num_treinos * preco_treino)
        else:
            nome_plano, preco_mensal = "Sem plano", 0.0
        print(AMARELO + "ID: "           + RESET + BRANCO  + str(id_cliente)          + RESET)
        print(CINZA   + "Nome: "         + RESET + BRANCO  + dados["nome"]            + RESET)
        print(CINZA   + "Nascimento: "   + RESET           + dados["data_nascimento"])
        print(CINZA   + "Telefone: "     + RESET           + dados["telefone"])
        print(CINZA   + "Plano: "        + RESET + MAGENTA + nome_plano               + RESET)
        print(CINZA   + "Inicio plano: " + RESET           + dados["data_inicio"])
        print(CINZA   + "Mensalidade: "  + RESET + VERDE   + str(preco_mensal) + " EUR" + RESET)
        print(CINZA + "-" * 40 + RESET)

def mostrar_cliente(id_cliente):
    if id_cliente not in clientes:
        print(VERMELHO_B + "Cliente nao encontrado." + RESET)
        return
    dados = clientes[id_cliente]
    plano = obter_plano(dados["id_plano"])
    if plano:
        nome_plano, num_treinos, preco_treino = plano
        preco_mensal = _arredondar(num_treinos * preco_treino)
    else:
        nome_plano, num_treinos, preco_treino, preco_mensal = "Sem plano", 0, 0.0, 0.0
    print()
    print(VERDE + BOLD + "[ CLIENTE ]" + RESET)
    print(CINZA + "-" * 40 + RESET)
    print(AMARELO + "ID: "           + RESET + BRANCO  + str(id_cliente)          + RESET)
    print(CINZA   + "Nome: "         + RESET + BRANCO  + dados["nome"]            + RESET)
    print(CINZA   + "Nascimento: "   + RESET           + dados["data_nascimento"])
    print(CINZA   + "Telefone: "     + RESET           + dados["telefone"])
    print(CINZA   + "Plano: "        + RESET + MAGENTA + nome_plano               + RESET)
    print(CINZA   + "Treinos/mes: "  + RESET           + str(num_treinos))
    print(CINZA   + "Preco/treino: " + RESET + VERDE   + str(preco_treino) + " EUR" + RESET)
    print(CINZA   + "Mensalidade: "  + RESET + VERDE   + str(preco_mensal) + " EUR" + RESET)
    print(CINZA   + "Inicio plano: " + RESET           + dados["data_inicio"])
    print(CINZA + "-" * 40 + RESET)

def pesquisar_cliente(pesquisa):
    print()
    print(VERDE + BOLD + "[ RESULTADOS ]" + RESET)
    print(CINZA + "-" * 40 + RESET)
    encontrou = False
    for id_cliente, dados in clientes.items():
        if pesquisa.lower() in dados["nome"].lower():
            plano = obter_plano(dados["id_plano"])
            nome_plano = plano[0] if plano else "Sem plano"
            print(AMARELO + "ID: "   + RESET + BRANCO  + str(id_cliente) + RESET)
            print(CINZA   + "Nome: " + RESET + BRANCO  + dados["nome"]   + RESET)
            print(CINZA   + "Plano: "+ RESET + MAGENTA + nome_plano      + RESET)
            print(CINZA + "-" * 40 + RESET)
            encontrou = True
    if not encontrou:
        print(AMARELO + "Nenhum cliente encontrado." + RESET)
