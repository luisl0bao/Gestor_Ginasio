import os
import funcoes
from datetime import date
from funcoes  import *
from utils    import *
from CoresANSII import *


def limpar_ecra():
    os.system("cls" if os.name == "nt" else "clear")


def aguardar_enter():
    input(CINZA + "Enter para continuar..." + RESET)
    limpar_ecra()


def mostrar_cabecalho(titulo):
    limpar_ecra()
    receita    = calcular_receita_mensal()
    total_desp = calcular_total_despesas()
    saldo      = calcular_saldo()
    print()
    print(VERDE + BOLD + "[ " + titulo + " ]" + RESET)
    print(CINZA + "-" * 40 + RESET)
    print(CINZA + "Receita: "    + RESET + VERDE + str(receita) + " EUR" + RESET +
          CINZA + "  Despesas: " + RESET + VERMELHO + str(total_desp) + " EUR" + RESET +
          CINZA + "  Lucro por mes: " + RESET + (VERDE_B if saldo >= 0 else VERMELHO_B) + BOLD + str(saldo) + " EUR" + RESET)
    print(CINZA + "Lucro total: " + RESET +
          (VERDE_B if funcoes.saldo_acumulado >= 0 else VERMELHO_B) +
          BOLD + str(funcoes.saldo_acumulado) + " EUR" + RESET)
    print(CINZA + "-" * 40 + RESET)
    print()


# ══════════════════════════════════════════
# CRUD PLANOS
# ══════════════════════════════════════════

def criar_plano():
    limpar_ecra()
    print(VERDE + BOLD + "[ NOVO PLANO ]" + RESET)
    print()
    nome         = pedir_texto("Nome do plano: ")
    num_treinos  = pedir_inteiro_positivo("Numero de treinos por mes: ")
    preco_treino = pedir_decimal_positivo("Preco por treino (EUR): ")
    adicionar_plano(nome, num_treinos, preco_treino)
    aguardar_enter()


def ler_planos():
    limpar_ecra()
    mostrar_planos()
    aguardar_enter()


def ler_plano():
    if len(planos) == 0:
        print(VERMELHO_B + "Nao existe nenhum plano." + RESET)
        aguardar_enter()
        return
    limpar_ecra()
    mostrar_planos()
    id_plano = pedir_id_valido("ID do plano: ", ids_planos())
    limpar_ecra()
    mostrar_plano(id_plano)
    aguardar_enter()


def atualizar_plano():
    if len(planos) == 0:
        print(VERMELHO_B + "Nao existe nenhum plano." + RESET)
        aguardar_enter()
        return
    limpar_ecra()
    mostrar_planos()
    id_plano = pedir_id_valido("ID do plano: ", ids_planos())
    print(CINZA + "(Enter para manter o valor actual)" + RESET)
    nome         = input(AMARELO + "Novo nome: "          + RESET).strip()
    num_treinos  = input(AMARELO + "Novo num. treinos: "  + RESET).strip()
    preco_treino = input(AMARELO + "Novo preco/treino: "  + RESET).strip()
    modificar_plano(id_plano, nome, num_treinos, preco_treino)
    aguardar_enter()


def deletar_plano():
    if len(planos) == 0:
        print(VERMELHO_B + "Nao existe nenhum plano." + RESET)
        aguardar_enter()
        return
    limpar_ecra()
    mostrar_planos()
    id_plano  = pedir_id_valido("ID do plano: ", ids_planos())
    confirmar = pedir_confirmacao("Confirmar remocao")
    if confirmar:
        remover_plano(id_plano)
    else:
        print(CINZA + "Cancelado." + RESET)
    aguardar_enter()


def menu_planos():
    while True:
        mostrar_cabecalho("PLANOS DE TREINO")
        print(MAGENTA + BOLD + "[1]" + RESET + " " + BRANCO + "Criar plano"     + RESET)
        print(MAGENTA + BOLD + "[2]" + RESET + " " + BRANCO + "Ler planos"      + RESET)
        print(MAGENTA + BOLD + "[3]" + RESET + " " + BRANCO + "Ler plano"       + RESET)
        print(MAGENTA + BOLD + "[4]" + RESET + " " + BRANCO + "Atualizar plano" + RESET)
        print(MAGENTA + BOLD + "[5]" + RESET + " " + BRANCO + "Deletar plano"   + RESET)
        print(MAGENTA + BOLD + "[0]" + RESET + " " + BRANCO + "Voltar"          + RESET)
        print(CINZA + "-" * 40 + RESET)
        opcao = input(MAGENTA + BOLD + "> " + RESET).strip()

        if   opcao == "1": criar_plano()
        elif opcao == "2": ler_planos()
        elif opcao == "3": ler_plano()
        elif opcao == "4": atualizar_plano()
        elif opcao == "5": deletar_plano()
        elif opcao == "0": break
        else:
            print(VERMELHO_B + "Opcao invalida." + RESET)
            aguardar_enter()


# ══════════════════════════════════════════
# CRUD CLIENTES
# ══════════════════════════════════════════

def criar_cliente():
    if len(planos) == 0:
        print(VERMELHO_B + "Nao existe nenhum plano. Cria um plano primeiro." + RESET)
        aguardar_enter()
        return
    limpar_ecra()
    print(VERDE + BOLD + "[ NOVO CLIENTE ]" + RESET)
    print()
    nome            = pedir_texto("Nome: ")
    data_nascimento = pedir_data("Data de nascimento")
    telefone        = pedir_telefone("Telefone: ")
    resumo_planos()
    id_plano        = pedir_id_valido("ID do plano: ", ids_planos())
    data_inicio     = str(date.today()).replace("-", "/")
    print(VERDE + "DATA DE INICIO DO PLANO: " + MAGENTA + data_inicio + RESET)
    adicionar_cliente(nome, data_nascimento, telefone, id_plano, data_inicio)
    aguardar_enter()


def ler_clientes():
    limpar_ecra()
    mostrar_clientes()
    aguardar_enter()


def ler_cliente():
    if len(clientes) == 0:
        print(VERMELHO_B + "Nao existe nenhum cliente." + RESET)
        aguardar_enter()
        return
    limpar_ecra()
    mostrar_clientes()
    id_cliente = pedir_id_valido("ID do cliente: ", ids_clientes())
    limpar_ecra()
    mostrar_cliente(id_cliente)
    aguardar_enter()


def atualizar_cliente():
    if len(clientes) == 0:
        print(VERMELHO_B + "Nao existe nenhum cliente." + RESET)
        aguardar_enter()
        return
    limpar_ecra()
    mostrar_clientes()
    id_cliente = pedir_id_valido("ID do cliente: ", ids_clientes())
    print(CINZA + "(Enter para manter o valor actual)" + RESET)
    nome            = input(AMARELO + "Novo nome: "                          + RESET).strip()
    data_nascimento = input(AMARELO + "Nova data nascimento (DD/MM/AAAA): "  + RESET).strip()
    telefone        = input(AMARELO + "Novo telefone: "                      + RESET).strip()
    id_plano_str    = ""
    if len(planos) > 0:
        resumo_planos()
        id_plano_str = input(AMARELO + "Novo ID do plano: " + RESET).strip()
        while id_plano_str != "" and not (id_plano_str.isdigit() and int(id_plano_str) in ids_planos()):
            print(VERMELHO_B + "ID invalido." + RESET)
            resumo_planos()
            id_plano_str = input(AMARELO + "Novo ID do plano: " + RESET).strip()
    data_inicio = input(AMARELO + "Nova data inicio (DD/MM/AAAA): " + RESET).strip()
    modificar_cliente(id_cliente, nome, data_nascimento, telefone, id_plano_str, data_inicio)
    aguardar_enter()


def deletar_cliente():
    if len(clientes) == 0:
        print(VERMELHO_B + "Nao existe nenhum cliente." + RESET)
        aguardar_enter()
        return
    limpar_ecra()
    mostrar_clientes()
    id_cliente = pedir_id_valido("ID do cliente: ", ids_clientes())
    confirmar  = pedir_confirmacao("Confirmar remocao")
    if confirmar:
        remover_cliente(id_cliente)
    else:
        print(CINZA + "Cancelado." + RESET)
    aguardar_enter()


def menu_clientes():
    while True:
        mostrar_cabecalho("CLIENTES")
        print(MAGENTA + BOLD + "[1]" + RESET + " " + BRANCO + "Criar cliente"     + RESET)
        print(MAGENTA + BOLD + "[2]" + RESET + " " + BRANCO + "Ler clientes"      + RESET)
        print(MAGENTA + BOLD + "[3]" + RESET + " " + BRANCO + "Ler cliente"       + RESET)
        print(MAGENTA + BOLD + "[4]" + RESET + " " + BRANCO + "Atualizar cliente" + RESET)
        print(MAGENTA + BOLD + "[5]" + RESET + " " + BRANCO + "Deletar cliente"   + RESET)
        print(MAGENTA + BOLD + "[6]" + RESET + " " + BRANCO + "Pesquisar cliente" + RESET)
        print(MAGENTA + BOLD + "[0]" + RESET + " " + BRANCO + "Voltar"            + RESET)
        print(CINZA + "-" * 40 + RESET)
        opcao = input(MAGENTA + BOLD + "> " + RESET).strip()

        if   opcao == "1": criar_cliente()
        elif opcao == "2": ler_clientes()
        elif opcao == "3": ler_cliente()
        elif opcao == "4": atualizar_cliente()
        elif opcao == "5": deletar_cliente()
        elif opcao == "6":
            limpar_ecra()
            pesquisa = pedir_texto("Nome a pesquisar: ")
            pesquisar_cliente(pesquisa)
            aguardar_enter()
        elif opcao == "0": break
        else:
            print(VERMELHO_B + "Opcao invalida." + RESET)
            aguardar_enter()


# ══════════════════════════════════════════
# CRUD DESPESAS
# ══════════════════════════════════════════

def criar_despesa():
    limpar_ecra()
    print(VERDE + BOLD + "[ NOVA DESPESA ]" + RESET)
    print()
    descricao = pedir_texto("Descricao: ")
    valor     = pedir_decimal_positivo("Valor (EUR): ")
    adicionar_despesa(descricao, valor)
    aguardar_enter()


def ler_despesas():
    limpar_ecra()
    mostrar_despesas()
    aguardar_enter()


def ler_despesa():
    if len(despesas) == 0:
        print(VERMELHO_B + "Nao existe nenhuma despesa." + RESET)
        aguardar_enter()
        return
    limpar_ecra()
    mostrar_despesas()
    ids_validos = [d[0] for d in despesas]
    id_despesa  = pedir_id_valido("ID da despesa: ", ids_validos)
    limpar_ecra()
    mostrar_despesa(id_despesa)
    aguardar_enter()


def deletar_despesa():
    if len(despesas) == 0:
        print(VERMELHO_B + "Nao existe nenhuma despesa." + RESET)
        aguardar_enter()
        return
    limpar_ecra()
    mostrar_despesas()
    ids_validos = [d[0] for d in despesas]
    id_despesa  = pedir_id_valido("ID da despesa: ", ids_validos)
    confirmar   = pedir_confirmacao("Confirmar remocao")
    if confirmar:
        remover_despesa(id_despesa)
    else:
        print(CINZA + "Cancelado." + RESET)
    aguardar_enter()


def menu_despesas():
    while True:
        mostrar_cabecalho("DESPESAS")
        print(MAGENTA + BOLD + "[1]" + RESET + " " + BRANCO + "Criar despesa"   + RESET)
        print(MAGENTA + BOLD + "[2]" + RESET + " " + BRANCO + "Ler despesas"    + RESET)
        print(MAGENTA + BOLD + "[3]" + RESET + " " + BRANCO + "Ler despesa"     + RESET)
        print(MAGENTA + BOLD + "[4]" + RESET + " " + BRANCO + "Deletar despesa" + RESET)
        print(MAGENTA + BOLD + "[0]" + RESET + " " + BRANCO + "Voltar"          + RESET)
        print(CINZA + "-" * 40 + RESET)
        opcao = input(MAGENTA + BOLD + "> " + RESET).strip()

        if   opcao == "1": criar_despesa()
        elif opcao == "2": ler_despesas()
        elif opcao == "3": ler_despesa()
        elif opcao == "4": deletar_despesa()
        elif opcao == "0": break
        else:
            print(VERMELHO_B + "Opcao invalida." + RESET)
            aguardar_enter()


# ══════════════════════════════════════════
# MENU PRINCIPAL
# ══════════════════════════════════════════

def menu_principal():
    while True:
        mostrar_cabecalho("GESTOR DE GINASIO")
        print(MAGENTA + BOLD + "[1]" + RESET + " " + BRANCO + "Clientes"             + RESET)
        print(MAGENTA + BOLD + "[2]" + RESET + " " + BRANCO + "Planos de treino"     + RESET)
        print(MAGENTA + BOLD + "[3]" + RESET + " " + BRANCO + "Despesas"             + RESET)
        print(MAGENTA + BOLD + "[4]" + RESET + " " + BRANCO + "Relatorio financeiro" + RESET)
        print(MAGENTA + BOLD + "[5]" + RESET + " " + BRANCO + "Estatisticas"         + RESET)
        print(MAGENTA + BOLD + "[6]" + RESET + " " + BRANCO + "Simular mes"          + RESET)
        print(MAGENTA + BOLD + "[0]" + RESET + " " + BRANCO + "Sair"                 + RESET)
        print(CINZA + "-" * 40 + RESET)
        opcao = input(MAGENTA + BOLD + "> " + RESET).strip()

        if   opcao == "1": menu_clientes()
        elif opcao == "2": menu_planos()
        elif opcao == "3": menu_despesas()
        elif opcao == "4":
            limpar_ecra()
            mostrar_relatorio_financeiro()
            aguardar_enter()
        elif opcao == "5":
            limpar_ecra()
            mostrar_estatisticas()
            aguardar_enter()
        elif opcao == "6":
            limpar_ecra()
            simular_mes()
            aguardar_enter()
        elif opcao == "0":
            limpar_ecra()
            print(VERDE + "Ate logo." + RESET)
            break
        else:
            print(VERMELHO_B + "Opcao invalida." + RESET)
            aguardar_enter()


# ══════════════════════════════════════════
# DADOS POR DEFEITO
# ══════════════════════════════════════════

def carregar_dados():
    adicionar_plano("Basico",   8,  3.50)
    adicionar_plano("Standard", 12, 3.00)
    adicionar_plano("Premium",  20, 2.50)

    adicionar_despesa("Agua e Luz",    90.00)
    adicionar_despesa("Equipamentos", 160.00)

    adicionar_cliente("Joao Silva",      "15/03/2002", "912345678", 1, "01/01/2025")
    adicionar_cliente("Ana Ferreira",    "22/07/1996", "923456789", 2, "01/01/2025")
    adicionar_cliente("Carlos Sousa",    "05/11/1989", "934567890", 1, "01/02/2025")
    adicionar_cliente("Marta Oliveira",  "30/09/2005", "945678901", 2, "01/02/2025")
    adicionar_cliente("Rui Costa",       "14/04/1982", "956789012", 1, "01/03/2025")
    adicionar_cliente("Sofia Martins",   "08/12/1998", "967890123", 3, "01/03/2025")
    adicionar_cliente("Pedro Rodrigues", "19/06/1993", "978901234", 1, "01/01/2025")
    adicionar_cliente("Ines Almeida",    "27/01/2000", "989012345", 2, "01/04/2025")
    adicionar_cliente("Tiago Lopes",     "03/08/1986", "910123456", 1, "01/04/2025")
    adicionar_cliente("Beatriz Nunes",   "11/05/2003", "921234567", 3, "01/05/2025")


# ══════════════════════════════════════════
if __name__ == "__main__":
    carregar_dados()
    menu_principal()
