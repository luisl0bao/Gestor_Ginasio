import os
from src.CoresANSII import VERDE, VERDE_B, VERMELHO, VERMELHO_B, AMARELO, BRANCO, CINZA, BOLD, RESET, MAGENTA
from src import dados
from dados import clientes, planos, despesas
from src.planos import (adicionar_plano, mostrar_planos, mostrar_plano, modificar_plano,
                    remover_plano, _ids_planos)
from src.clientes import (adicionar_cliente, mostrar_clientes, mostrar_cliente, modificar_cliente,
                      remover_cliente, pesquisar_cliente, _ids_clientes)
from src.despesas import (adicionar_despesa, mostrar_despesas, mostrar_despesa, remover_despesa)
from src.relatorios import mostrar_relatorio_financeiro, mostrar_estatisticas, simular_mes
from src.utils import (_pedir_texto, _pedir_inteiro_positivo, _pedir_decimal_positivo,
                   _pedir_data, _pedir_telefone, _pedir_id_valido, _pedir_confirmacao)
from datetime import date

def _limpar_ecra():
    os.system("cls" if os.name == "nt" else "clear")

def _aguardar_enter():
    input(CINZA + "Enter para continuar..." + RESET)
    _limpar_ecra()

def _mostrar_cabecalho(titulo):
    _limpar_ecra()
    from relatorios import _calcular_receita_mensal, _calcular_total_despesas, _calcular_saldo
    receita = _calcular_receita_mensal()
    total_desp = _calcular_total_despesas()
    saldo = _calcular_saldo()
    print()
    print(VERDE + BOLD + "[ " + titulo + " ]" + RESET)
    print(CINZA + "-" * 40 + RESET)
    print(CINZA + "Receita: "    + RESET + VERDE + str(receita) + " EUR" + RESET +
          CINZA + "  Despesas: " + RESET + VERMELHO + str(total_desp) + " EUR" + RESET +
          CINZA + "  Lucro por mes: " + RESET + (VERDE_B if saldo >= 0 else VERMELHO_B) + BOLD + str(saldo) + " EUR" + RESET)
    print(CINZA + "Lucro total: " + RESET +
          (VERDE_B if dados.saldo_acumulado >= 0 else VERMELHO_B) +
          BOLD + str(dados.saldo_acumulado) + " EUR" + RESET)
    print(CINZA + "-" * 40 + RESET)
    print()

# ---------- CRUD PLANOS ----------
def _criar_plano():
    _limpar_ecra()
    print(VERDE + BOLD + "[ NOVO PLANO ]" + RESET)
    print()
    nome = _pedir_texto("Nome do plano: ")
    num_treinos = _pedir_inteiro_positivo("Numero de treinos por mes: ")
    preco_treino = _pedir_decimal_positivo("Preco por treino (EUR): ")
    adicionar_plano(nome, num_treinos, preco_treino)
    _aguardar_enter()

def _ler_planos():
    _limpar_ecra()
    mostrar_planos()
    _aguardar_enter()

def _ler_plano():
    if len(planos) == 0:
        print(VERMELHO_B + "Nao existe nenhum plano." + RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_planos()
    id_plano = _pedir_id_valido("ID do plano: ", _ids_planos())
    _limpar_ecra()
    mostrar_plano(id_plano)
    _aguardar_enter()

def _atualizar_plano():
    if len(planos) == 0:
        print(VERMELHO_B + "Nao existe nenhum plano." + RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_planos()
    id_plano = _pedir_id_valido("ID do plano: ", _ids_planos())
    print(CINZA + "(Enter para manter o valor actual)" + RESET)
    nome = input(AMARELO + "Novo nome: " + RESET).strip()
    num_treinos = input(AMARELO + "Novo num. treinos: " + RESET).strip()
    preco_treino = input(AMARELO + "Novo preco/treino: " + RESET).strip()
    modificar_plano(id_plano, nome, num_treinos, preco_treino)
    _aguardar_enter()

def _deletar_plano():
    if len(planos) == 0:
        print(VERMELHO_B + "Nao existe nenhum plano." + RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_planos()
    id_plano = _pedir_id_valido("ID do plano: ", _ids_planos())
    confirmar = _pedir_confirmacao("Confirmar remocao")
    if confirmar:
        remover_plano(id_plano)
    else:
        print(CINZA + "Cancelado." + RESET)
    _aguardar_enter()

def menu_planos():
    while True:
        _mostrar_cabecalho("PLANOS DE TREINO")
        print(MAGENTA + BOLD + "[1]" + RESET + " " + BRANCO + "Criar plano"     + RESET)
        print(MAGENTA + BOLD + "[2]" + RESET + " " + BRANCO + "Ler planos"      + RESET)
        print(MAGENTA + BOLD + "[3]" + RESET + " " + BRANCO + "Ler plano"       + RESET)
        print(MAGENTA + BOLD + "[4]" + RESET + " " + BRANCO + "Atualizar plano" + RESET)
        print(MAGENTA + BOLD + "[5]" + RESET + " " + BRANCO + "Deletar plano"   + RESET)
        print(MAGENTA + BOLD + "[0]" + RESET + " " + BRANCO + "Voltar"          + RESET)
        print(CINZA + "-" * 40 + RESET)
        opcao = input(MAGENTA + BOLD + "> " + RESET).strip()

        if opcao == "1": _criar_plano()
        elif opcao == "2": _ler_planos()
        elif opcao == "3": _ler_plano()
        elif opcao == "4": _atualizar_plano()
        elif opcao == "5": _deletar_plano()
        elif opcao == "0": break
        else:
            print(VERMELHO_B + "Opcao invalida." + RESET)
            _aguardar_enter()

# ---------- CRUD CLIENTES ----------
def _criar_cliente():
    if len(planos) == 0:
        print(VERMELHO_B + "Nao existe nenhum plano. Cria um plano primeiro." + RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    print(VERDE + BOLD + "[ NOVO CLIENTE ]" + RESET)
    print()
    nome = _pedir_texto("Nome: ")
    data_nascimento = _pedir_data("Data de nascimento")
    telefone = _pedir_telefone("Telefone: ")
    from planos import _resumo_planos
    _resumo_planos()
    id_plano = _pedir_id_valido("ID do plano: ", _ids_planos())
    data_inicio = str(date.today()).replace("-", "/")
    print(VERDE + "DATA DE INICIO DO PLANO: " + MAGENTA + data_inicio + RESET)
    adicionar_cliente(nome, data_nascimento, telefone, id_plano, data_inicio)
    _aguardar_enter()

def _ler_clientes():
    _limpar_ecra()
    mostrar_clientes()
    _aguardar_enter()

def _ler_cliente():
    if len(clientes) == 0:
        print(VERMELHO_B + "Nao existe nenhum cliente." + RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_clientes()
    id_cliente = _pedir_id_valido("ID do cliente: ", _ids_clientes())
    _limpar_ecra()
    mostrar_cliente(id_cliente)
    _aguardar_enter()

def _atualizar_cliente():
    if len(clientes) == 0:
        print(VERMELHO_B + "Nao existe nenhum cliente." + RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_clientes()
    id_cliente = _pedir_id_valido("ID do cliente: ", _ids_clientes())
    print(CINZA + "(Enter para manter o valor actual)" + RESET)
    nome = input(AMARELO + "Novo nome: " + RESET).strip()
    data_nascimento = input(AMARELO + "Nova data nascimento (DD/MM/AAAA): " + RESET).strip()
    telefone = input(AMARELO + "Novo telefone: " + RESET).strip()
    id_plano_str = ""
    if len(planos) > 0:
        from planos import _resumo_planos
        _resumo_planos()
        id_plano_str = input(AMARELO + "Novo ID do plano: " + RESET).strip()
        while id_plano_str != "" and not (id_plano_str.isdigit() and int(id_plano_str) in _ids_planos()):
            print(VERMELHO_B + "ID invalido." + RESET)
            _resumo_planos()
            id_plano_str = input(AMARELO + "Novo ID do plano: " + RESET).strip()
    data_inicio = input(AMARELO + "Nova data inicio (DD/MM/AAAA): " + RESET).strip()
    modificar_cliente(id_cliente, nome, data_nascimento, telefone, id_plano_str, data_inicio)
    _aguardar_enter()

def _deletar_cliente():
    if len(clientes) == 0:
        print(VERMELHO_B + "Nao existe nenhum cliente." + RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_clientes()
    id_cliente = _pedir_id_valido("ID do cliente: ", _ids_clientes())
    confirmar = _pedir_confirmacao("Confirmar remocao")
    if confirmar:
        remover_cliente(id_cliente)
    else:
        print(CINZA + "Cancelado." + RESET)
    _aguardar_enter()

def menu_clientes():
    while True:
        _mostrar_cabecalho("CLIENTES")
        print(MAGENTA + BOLD + "[1]" + RESET + " " + BRANCO + "Criar cliente"     + RESET)
        print(MAGENTA + BOLD + "[2]" + RESET + " " + BRANCO + "Ler clientes"      + RESET)
        print(MAGENTA + BOLD + "[3]" + RESET + " " + BRANCO + "Ler cliente"       + RESET)
        print(MAGENTA + BOLD + "[4]" + RESET + " " + BRANCO + "Atualizar cliente" + RESET)
        print(MAGENTA + BOLD + "[5]" + RESET + " " + BRANCO + "Deletar cliente"   + RESET)
        print(MAGENTA + BOLD + "[6]" + RESET + " " + BRANCO + "Pesquisar cliente" + RESET)
        print(MAGENTA + BOLD + "[0]" + RESET + " " + BRANCO + "Voltar"            + RESET)
        print(CINZA + "-" * 40 + RESET)
        opcao = input(MAGENTA + BOLD + "> " + RESET).strip()

        if opcao == "1": _criar_cliente()
        elif opcao == "2": _ler_clientes()
        elif opcao == "3": _ler_cliente()
        elif opcao == "4": _atualizar_cliente()
        elif opcao == "5": _deletar_cliente()
        elif opcao == "6":
            _limpar_ecra()
            pesquisa = _pedir_texto("Nome a pesquisar: ")
            pesquisar_cliente(pesquisa)
            _aguardar_enter()
        elif opcao == "0": break
        else:
            print(VERMELHO_B + "Opcao invalida." + RESET)
            _aguardar_enter()

# ---------- CRUD DESPESAS ----------
def _criar_despesa():
    _limpar_ecra()
    print(VERDE + BOLD + "[ NOVA DESPESA ]" + RESET)
    print()
    descricao = _pedir_texto("Descricao: ")
    valor = _pedir_decimal_positivo("Valor (EUR): ")
    adicionar_despesa(descricao, valor)
    _aguardar_enter()

def _ler_despesas():
    _limpar_ecra()
    mostrar_despesas()
    _aguardar_enter()

def _ler_despesa():
    if len(despesas) == 0:
        print(VERMELHO_B + "Nao existe nenhuma despesa." + RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_despesas()
    ids_validos = [d[0] for d in despesas]
    id_despesa = _pedir_id_valido("ID da despesa: ", ids_validos)
    _limpar_ecra()
    mostrar_despesa(id_despesa)
    _aguardar_enter()

def _deletar_despesa():
    if len(despesas) == 0:
        print(VERMELHO_B + "Nao existe nenhuma despesa." + RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_despesas()
    ids_validos = [d[0] for d in despesas]
    id_despesa = _pedir_id_valido("ID da despesa: ", ids_validos)
    confirmar = _pedir_confirmacao("Confirmar remocao")
    if confirmar:
        remover_despesa(id_despesa)
    else:
        print(CINZA + "Cancelado." + RESET)
    _aguardar_enter()

def menu_despesas():
    while True:
        _mostrar_cabecalho("DESPESAS")
        print(MAGENTA + BOLD + "[1]" + RESET + " " + BRANCO + "Criar despesa"   + RESET)
        print(MAGENTA + BOLD + "[2]" + RESET + " " + BRANCO + "Ler despesas"    + RESET)
        print(MAGENTA + BOLD + "[3]" + RESET + " " + BRANCO + "Ler despesa"     + RESET)
        print(MAGENTA + BOLD + "[4]" + RESET + " " + BRANCO + "Deletar despesa" + RESET)
        print(MAGENTA + BOLD + "[0]" + RESET + " " + BRANCO + "Voltar"          + RESET)
        print(CINZA + "-" * 40 + RESET)
        opcao = input(MAGENTA + BOLD + "> " + RESET).strip()

        if opcao == "1": _criar_despesa()
        elif opcao == "2": _ler_despesas()
        elif opcao == "3": _ler_despesa()
        elif opcao == "4": _deletar_despesa()
        elif opcao == "0": break
        else:
            print(VERMELHO_B + "Opcao invalida." + RESET)
            _aguardar_enter()

def menu_principal():
    while True:
        _mostrar_cabecalho("GESTOR DE GINASIO")
        print(MAGENTA + BOLD + "[1]" + RESET + " " + BRANCO + "Clientes"             + RESET)
        print(MAGENTA + BOLD + "[2]" + RESET + " " + BRANCO + "Planos de treino"     + RESET)
        print(MAGENTA + BOLD + "[3]" + RESET + " " + BRANCO + "Despesas"             + RESET)
        print(MAGENTA + BOLD + "[4]" + RESET + " " + BRANCO + "Relatorio financeiro" + RESET)
        print(MAGENTA + BOLD + "[5]" + RESET + " " + BRANCO + "Estatisticas"         + RESET)
        print(MAGENTA + BOLD + "[6]" + RESET + " " + BRANCO + "Simular mes"          + RESET)
        print(MAGENTA + BOLD + "[0]" + RESET + " " + BRANCO + "Sair"                 + RESET)
        print(CINZA + "-" * 40 + RESET)
        opcao = input(MAGENTA + BOLD + "> " + RESET).strip()

        if opcao == "1": menu_clientes()
        elif opcao == "2": menu_planos()
        elif opcao == "3": menu_despesas()
        elif opcao == "4":
            _limpar_ecra()
            mostrar_relatorio_financeiro()
            _aguardar_enter()
        elif opcao == "5":
            _limpar_ecra()
            mostrar_estatisticas()
            _aguardar_enter()
        elif opcao == "6":
            _limpar_ecra()
            simular_mes()
            _aguardar_enter()
        elif opcao == "0":
            _limpar_ecra()
            print(VERDE + "Ate logo." + RESET)
            break
        else:
            print(VERMELHO_B + "Opcao invalida." + RESET)
            _aguardar_enter()
