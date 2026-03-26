from CoresANSII import *

# ─── DADOS ────────────────────────────────────────────────

clientes          = {}   # { id: { "nome": ..., "data_nascimento": ..., "telefone": ..., "id_plano": ..., "data_inicio": ... } }
planos            = {}   # { id: (nome, num_treinos, preco_por_treino) }
despesas          = []   # [ (id, descricao, valor) ]

proximo_id_plano   = 1
proximo_id_cliente = 1
proximo_id_despesa = 1
proximo_mes        = 1
saldo_acumulado    = 0.0


# ─── AUXILIARES ───────────────────────────────────────────

def arredondar(valor):
    return round(valor, 2)


def ids_planos():
    return list(planos.keys())


def ids_clientes():
    return list(clientes.keys())


def calcular_receita_mensal():
    total = 0.0
    for id_cliente in clientes:
        id_plano = clientes[id_cliente]["id_plano"]
        if id_plano in planos:
            num_treinos      = planos[id_plano][1]
            preco_por_treino = planos[id_plano][2]
            total = total + (num_treinos * preco_por_treino)
    return arredondar(total)


def calcular_total_despesas():
    total = 0.0
    for despesa in despesas:
        total = total + despesa[2]
    return arredondar(total)


def calcular_saldo():
    return arredondar(calcular_receita_mensal() - calcular_total_despesas())


# ─── FUNÇÕES PLANOS ───────────────────────────────────────

def adicionar_plano(nome, num_treinos, preco_por_treino):
    global proximo_id_plano
    planos[proximo_id_plano] = (nome, num_treinos, arredondar(preco_por_treino))
    proximo_id_plano = proximo_id_plano + 1
    print(VERDE_B + "Plano adicionado." + RESET)


def obter_plano(id_plano):
    if id_plano in planos:
        return planos[id_plano]
    return None


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
        preco_por_treino = arredondar(float(preco_por_treino))
    planos[id_plano] = (nome, num_treinos, preco_por_treino)
    print(VERDE_B + "Plano atualizado." + RESET)


def remover_plano(id_plano):
    if id_plano not in planos:
        print(VERMELHO_B + "Plano nao encontrado." + RESET)
        return
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
    for id_plano in planos:
        dados = planos[id_plano]
        total_clientes = 0
        for id_cliente in clientes:
            if clientes[id_cliente]["id_plano"] == id_plano:
                total_clientes = total_clientes + 1
        preco_mensal = arredondar(dados[1] * dados[2])
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
    preco_mensal = arredondar(dados[1] * dados[2])
    print()
    print(VERDE + BOLD + "[ PLANO ]" + RESET)
    print(CINZA + "-" * 40 + RESET)
    print(AMARELO + "ID: "           + RESET + BRANCO + str(id_plano)     + RESET)
    print(CINZA   + "Nome: "         + RESET + BRANCO + dados[0]          + RESET)
    print(CINZA   + "Treinos/mes: "  + RESET + str(dados[1]))
    print(CINZA   + "Preco/treino: " + RESET + VERDE  + str(dados[2])     + " EUR" + RESET)
    print(CINZA   + "Total mensal: " + RESET + VERDE  + str(preco_mensal) + " EUR" + RESET)
    print(CINZA + "-" * 40 + RESET)


def resumo_planos():
    if len(planos) == 0:
        return
    print(CINZA + "Planos disponiveis:" + RESET)
    for id_plano in planos:
        dados = planos[id_plano]
        preco_mensal = arredondar(dados[1] * dados[2])
        print(AMARELO + "[" + str(id_plano) + "] " + RESET +
              BRANCO + dados[0] + RESET +
              CINZA + " - " + str(dados[1]) + " treinos - " + str(preco_mensal) + " EUR/mes" + RESET)


# ─── FUNÇÕES CLIENTES ─────────────────────────────────────

def adicionar_cliente(nome, data_nascimento, telefone, id_plano, data_inicio):
    global proximo_id_cliente
    for id_c in clientes:
        if clientes[id_c]["nome"] == nome:
            print(VERMELHO_B + "Ja existe um cliente com esse nome." + RESET)
            return
    if id_plano not in planos:
        print(VERMELHO_B + "Plano nao existe." + RESET)
        return
    clientes[proximo_id_cliente] = {
        "nome":            nome,
        "data_nascimento": data_nascimento,
        "telefone":        telefone,
        "id_plano":        id_plano,
        "data_inicio":     data_inicio
    }
    proximo_id_cliente = proximo_id_cliente + 1
    print(VERDE_B + "Cliente adicionado." + RESET)


def obter_cliente(id_cliente):
    if id_cliente in clientes:
        return clientes[id_cliente]
    return None


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
        if novo_id not in planos:
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
    for id_cliente in clientes:
        dados    = clientes[id_cliente]
        id_plano = dados["id_plano"]
        if id_plano in planos:
            nome_plano   = planos[id_plano][0]
            num_treinos  = planos[id_plano][1]
            preco_treino = planos[id_plano][2]
            preco_mensal = arredondar(num_treinos * preco_treino)
        else:
            nome_plano   = "Sem plano"
            preco_mensal = 0.0
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
    dados    = clientes[id_cliente]
    id_plano = dados["id_plano"]
    if id_plano in planos:
        nome_plano   = planos[id_plano][0]
        num_treinos  = planos[id_plano][1]
        preco_treino = planos[id_plano][2]
        preco_mensal = arredondar(num_treinos * preco_treino)
    else:
        nome_plano   = "Sem plano"
        num_treinos  = 0
        preco_treino = 0.0
        preco_mensal = 0.0
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
    for id_cliente in clientes:
        dados = clientes[id_cliente]
        if pesquisa.lower() in dados["nome"].lower():
            id_plano = dados["id_plano"]
            if id_plano in planos:
                nome_plano = planos[id_plano][0]
            else:
                nome_plano = "Sem plano"
            print(AMARELO + "ID: "   + RESET + BRANCO  + str(id_cliente) + RESET)
            print(CINZA   + "Nome: " + RESET + BRANCO  + dados["nome"]   + RESET)
            print(CINZA   + "Plano: "+ RESET + MAGENTA + nome_plano      + RESET)
            print(CINZA + "-" * 40 + RESET)
            encontrou = True
    if not encontrou:
        print(AMARELO + "Nenhum cliente encontrado." + RESET)


# ─── FUNÇÕES DESPESAS ─────────────────────────────────────

def adicionar_despesa(descricao, valor):
    global proximo_id_despesa
    despesas.append((proximo_id_despesa, descricao, arredondar(valor)))
    proximo_id_despesa = proximo_id_despesa + 1
    print(VERDE_B + "Despesa registada." + RESET)


def obter_despesa(id_despesa):
    for despesa in despesas:
        if despesa[0] == id_despesa:
            return despesa
    return None


def remover_despesa(id_despesa):
    for despesa in despesas:
        if despesa[0] == id_despesa:
            despesas.remove(despesa)
            print(VERDE_B + "Despesa removida." + RESET)
            return
    print(VERMELHO_B + "Despesa nao encontrada." + RESET)


def mostrar_despesas():
    if len(despesas) == 0:
        print(AMARELO + "Nenhuma despesa registada." + RESET)
        return
    print()
    print(VERDE + BOLD + "[ DESPESAS ]" + RESET)
    print(CINZA + "-" * 40 + RESET)
    for despesa in despesas:
        print(AMARELO + "ID: "        + RESET + BRANCO   + str(despesa[0]) + RESET)
        print(CINZA   + "Descricao: " + RESET + BRANCO   + despesa[1]      + RESET)
        print(CINZA   + "Valor: "     + RESET + VERMELHO + str(despesa[2]) + " EUR" + RESET)
        print(CINZA + "-" * 40 + RESET)


def mostrar_despesa(id_despesa):
    despesa = obter_despesa(id_despesa)
    if despesa is None:
        print(VERMELHO_B + "Despesa nao encontrada." + RESET)
        return
    print()
    print(VERDE + BOLD + "[ DESPESA ]" + RESET)
    print(CINZA + "-" * 40 + RESET)
    print(AMARELO + "ID: "        + RESET + BRANCO   + str(despesa[0]) + RESET)
    print(CINZA   + "Descricao: " + RESET + BRANCO   + despesa[1]      + RESET)
    print(CINZA   + "Valor: "     + RESET + VERMELHO + str(despesa[2]) + " EUR" + RESET)
    print(CINZA + "-" * 40 + RESET)


# ─── RELATORIOS ───────────────────────────────────────────

def mostrar_relatorio_financeiro():
    receita    = calcular_receita_mensal()
    total_desp = calcular_total_despesas()
    saldo      = calcular_saldo()
    print()
    print(VERDE + BOLD + "[ RELATORIO FINANCEIRO ]" + RESET)
    print(CINZA + "-" * 40 + RESET)
    print(BRANCO + BOLD + "Receitas" + RESET)
    print(CINZA + "Receita mensal: " + RESET + VERDE + str(receita) + " EUR" + RESET)
    print()
    print(BRANCO + BOLD + "Despesas" + RESET)
    for despesa in despesas:
        print(CINZA + despesa[1] + ": " + RESET + VERMELHO + str(despesa[2]) + " EUR" + RESET)
    print(CINZA + "Total: " + RESET + VERMELHO_B + str(total_desp) + " EUR" + RESET)
    print()
    print(BRANCO + BOLD + "Saldo" + RESET)
    if saldo >= 0:
        print(CINZA + "Saldo final: " + RESET + VERDE_B    + str(saldo) + " EUR" + RESET)
    else:
        print(CINZA + "Saldo final: " + RESET + VERMELHO_B + str(saldo) + " EUR" + RESET)
    print(CINZA + "-" * 40 + RESET)


def mostrar_estatisticas():
    print()
    print(VERDE + BOLD + "[ ESTATISTICAS ]" + RESET)
    print(CINZA + "-" * 40 + RESET)
    print(CINZA + "Total clientes: " + RESET + AMARELO + str(len(clientes)) + RESET)
    print(CINZA + "Total planos: "   + RESET + AMARELO + str(len(planos))   + RESET)
    print(CINZA + "Total despesas: " + RESET + AMARELO + str(len(despesas)) + RESET)
    if len(planos) > 0 and len(clientes) > 0:
        nome_plano_popular = ""
        max_clientes = 0
        for id_plano in planos:
            total = 0
            for id_cliente in clientes:
                if clientes[id_cliente]["id_plano"] == id_plano:
                    total = total + 1
            if total > max_clientes:
                max_clientes = total
                nome_plano_popular = planos[id_plano][0]
        print(CINZA + "Plano mais popular: " + RESET + MAGENTA + nome_plano_popular + RESET)
    receita    = calcular_receita_mensal()
    total_desp = calcular_total_despesas()
    saldo      = calcular_saldo()
    print(CINZA + "Receita mensal: " + RESET + VERDE    + str(receita)    + " EUR" + RESET)
    print(CINZA + "Total despesas: " + RESET + VERMELHO + str(total_desp) + " EUR" + RESET)
    if saldo >= 0:
        print(CINZA + "Saldo final: " + RESET + VERDE_B    + str(saldo) + " EUR" + RESET)
    else:
        print(CINZA + "Saldo final: " + RESET + VERMELHO_B + str(saldo) + " EUR" + RESET)
    print(CINZA + "-" * 40 + RESET)


def simular_mes():
    global proximo_mes, saldo_acumulado
    receita_simulada = 0.0
    print()
    print(VERDE + BOLD + "[ SIMULACAO MENSAL - MES " + str(proximo_mes) + " ]" + RESET)
    print(CINZA + "-" * 40 + RESET)
    print(BRANCO + BOLD + "Entradas" + RESET)
    for id_cliente in clientes:
        dados    = clientes[id_cliente]
        id_plano = dados["id_plano"]
        if id_plano in planos:
            num_treinos  = planos[id_plano][1]
            preco_treino = planos[id_plano][2]
            valor        = arredondar(num_treinos * preco_treino)
            receita_simulada = receita_simulada + valor
            print(CINZA + dados["nome"] + " (" + planos[id_plano][0] + "): " +
                  RESET + VERDE + "+" + str(valor) + " EUR" + RESET)
    receita_simulada = arredondar(receita_simulada)
    print()
    print(BRANCO + BOLD + "Saidas" + RESET)
    total_gasto = 0.0
    for despesa in despesas:
        total_gasto = total_gasto + despesa[2]
        print(CINZA + despesa[1] + ": " + RESET + VERMELHO + "-" + str(despesa[2]) + " EUR" + RESET)
    total_gasto     = arredondar(total_gasto)
    resultado       = arredondar(receita_simulada - total_gasto)
    saldo_acumulado = arredondar(saldo_acumulado + resultado)
    print()
    print(BRANCO + BOLD + "Resultado" + RESET)
    print(CINZA + "Receita: "  + RESET + VERDE    + str(receita_simulada) + " EUR" + RESET)
    print(CINZA + "Despesas: " + RESET + VERMELHO + str(total_gasto)      + " EUR" + RESET)
    if resultado >= 0:
        print(CINZA + "Resultado: "   + RESET + VERDE_B    + str(resultado)       + " EUR" + RESET)
    else:
        print(CINZA + "Resultado: "   + RESET + VERMELHO_B + str(resultado)       + " EUR" + RESET)
    if saldo_acumulado >= 0:
        print(CINZA + "Lucro total: " + RESET + VERDE_B    + str(saldo_acumulado) + " EUR" + RESET)
    else:
        print(CINZA + "Lucro total: " + RESET + VERMELHO_B + str(saldo_acumulado) + " EUR" + RESET)
    print(CINZA + "-" * 40 + RESET)
    proximo_mes = proximo_mes + 1
