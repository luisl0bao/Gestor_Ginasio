from Gestor_Ginasio.src import dados
from dados import planos
from CoresANSII import VERDE_B, VERMELHO_B, AMARELO, BRANCO, VERDE, CINZA, BOLD, RESET

# __Crud_____

def _arredondar(valor):
    return round(valor, 2)

def _ids_planos():
    return list(planos.keys())

def adicionar_plano(nome, num_treinos, preco_por_treino):
    planos[dados.proximo_id_plano] = (nome, num_treinos, _arredondar(preco_por_treino))
    dados.proximo_id_plano = dados.proximo_id_plano + 1
    print(VERDE_B + "Plano adicionado." + RESET)

def obter_plano(id_plano):
    return planos.get(id_plano)

def modificar_plano(id_plano, nome, num_treinos, preco_por_treino):
    if id_plano not in planos:
        print(VERMELHO_B + "Plano nao encontrado." + RESET)
        return
    plano_atual = planos[id_plano]
    if nome == "":
        nome = plano_atual[0]
    if num_treinos == "":
        num_treinos = plano_atual[1]
    else:
        num_treinos = int(num_treinos)
    if preco_por_treino == "":
        preco_por_treino = plano_atual[2]
    else:
        preco_por_treino = _arredondar(float(preco_por_treino))
    planos[id_plano] = (nome, num_treinos, preco_por_treino)
    print(VERDE_B + "Plano atualizado." + RESET)

def remover_plano(id_plano):
    if id_plano not in planos:
        print(VERMELHO_B + "Plano nao encontrado." + RESET)
        return
    from dados import clientes
    for id_cliente in clientes:
        if clientes[id_cliente]["id_plano"] == id_plano:
            print(VERMELHO_B + "Existem clientes com este plano. Remove-os primeiro." + RESET)
            return
    del planos[id_plano]
    print(VERDE_B + "Plano removido." + RESET)

def mostrar_planos():
    if len(planos) == 0:
        print(AMARELO + "Nenhum plano registado." + RESET)
        return
    print()
    print(VERDE + BOLD + "[ PLANOS ]" + RESET)
    print(CINZA + "-" * 40 + RESET)
    for id_plano, dados in planos.items():
        from dados import clientes
        total_clientes = sum(1 for c in clientes.values() if c["id_plano"] == id_plano)
        preco_mensal = _arredondar(dados[1] * dados[2])
        print(AMARELO + "ID: "            + RESET + BRANCO + str(id_plano)     + RESET)
        print(CINZA   + "Nome: "          + RESET + BRANCO + dados[0]          + RESET)
        print(CINZA   + "Treinos/mes: "   + RESET + str(dados[1]))
        print(CINZA   + "Preco/treino: "  + RESET + VERDE  + str(dados[2])     + " EUR" + RESET)
        print(CINZA   + "Total mensal: "  + RESET + VERDE  + str(preco_mensal) + " EUR" + RESET)
        print(CINZA   + "Clientes: "      + RESET + AMARELO + str(total_clientes) + RESET)
        print(CINZA + "-" * 40 + RESET)

def mostrar_plano(id_plano):
    if id_plano not in planos:
        print(VERMELHO_B + "Plano nao encontrado." + RESET)
        return
    dados = planos[id_plano]
    preco_mensal = _arredondar(dados[1] * dados[2])
    print()
    print(VERDE + BOLD + "[ PLANO ]" + RESET)
    print(CINZA + "-" * 40 + RESET)
    print(AMARELO + "ID: "           + RESET + BRANCO + str(id_plano)     + RESET)
    print(CINZA   + "Nome: "         + RESET + BRANCO + dados[0]          + RESET)
    print(CINZA   + "Treinos/mes: "  + RESET + str(dados[1]))
    print(CINZA   + "Preco/treino: " + RESET + VERDE  + str(dados[2])     + " EUR" + RESET)
    print(CINZA   + "Total mensal: " + RESET + VERDE  + str(preco_mensal) + " EUR" + RESET)
    print(CINZA + "-" * 40 + RESET)

def _resumo_planos():
    if len(planos) == 0:
        return
    print(CINZA + "Planos disponiveis:" + RESET)
    for id_plano, dados in planos.items():
        preco_mensal = _arredondar(dados[1] * dados[2])
        print(AMARELO + "[" + str(id_plano) + "] " + RESET +
              BRANCO + dados[0] + RESET +
              CINZA + " - " + str(dados[1]) + " treinos - " + str(preco_mensal) + " EUR/mes" + RESET)
