import os
import sys
from src.pagamentos import menu_pagamentos
from datetime import date

try:
    from src.ginasios import (
        adicionar_ginasio, obter_ginasio, modificar_ginasio,
        remover_ginasio, mostrar_ginasios, mostrar_ginasio,
        _ids_ginasios, _resumo_ginasios, _ginasios,
    )
except ImportError:
    from ginasios import (
        adicionar_ginasio, obter_ginasio, modificar_ginasio,
        remover_ginasio, mostrar_ginasios, mostrar_ginasio,
        _ids_ginasios, _resumo_ginasios, _ginasios,
    )

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src import dados
    from src.dados import clientes, planos, despesas
    from src.planos import adicionar_plano, mostrar_planos, mostrar_plano, modificar_plano, remover_plano, _ids_planos, _resumo_planos
    from src.clientes import adicionar_cliente, mostrar_clientes, mostrar_cliente, modificar_cliente, remover_cliente, pesquisar_cliente, _ids_clientes
    from src.despesas import adicionar_despesa, mostrar_despesas, mostrar_despesa, remover_despesa
    from src.pagamentos import menu_pagamentos
    from src.ginasios import (
        adicionar_ginasio, obter_ginasio, modificar_ginasio,
        remover_ginasio, mostrar_ginasios, mostrar_ginasio,
        _ids_ginasios, _resumo_ginasios, _ginasios,
    )
    from src.relatorios import mostrar_relatorio_financeiro, mostrar_estatisticas, simular_mes, _calcular_receita_mensal, _calcular_total_despesas, _calcular_saldo
    from src.utils import _pedir_texto, _pedir_inteiro_positivo, _pedir_decimal_positivo, _pedir_data, _pedir_telefone, _pedir_id_valido, _pedir_confirmacao
except ImportError:
    import dados
    from dados import clientes, planos, despesas
    from planos import adicionar_plano, mostrar_planos, mostrar_plano, modificar_plano, remover_plano, _ids_planos, _resumo_planos
    from clientes import adicionar_cliente, mostrar_clientes, mostrar_cliente, modificar_cliente, remover_cliente, pesquisar_cliente, _ids_clientes
    from despesas import adicionar_despesa, mostrar_despesas, mostrar_despesa, remover_despesa
    from pagamentos import menu_pagamentos
    from ginasios import (
        adicionar_ginasio, obter_ginasio, modificar_ginasio,
        remover_ginasio, mostrar_ginasios, mostrar_ginasio,
        _ids_ginasios, _resumo_ginasios, _ginasios,
    )
    from relatorios import mostrar_relatorio_financeiro, mostrar_estatisticas, simular_mes, _calcular_receita_mensal, _calcular_total_despesas, _calcular_saldo
    from utils import _pedir_texto, _pedir_inteiro_positivo, _pedir_decimal_positivo, _pedir_data, _pedir_telefone, _pedir_id_valido, _pedir_confirmacao

_RESET      = "\033[0m"
_BOLD       = "\033[1m"
_BRANCO     = "\033[97m"
_CINZA      = "\033[90m"
_VERDE      = "\033[32m"
_VERDE_B    = "\033[92m"
_AMARELO    = "\033[33m"
_VERMELHO   = "\033[31m"
_VERMELHO_B = "\033[91m"
_MAGENTA    = "\033[35m"

def _limpar_ecra():
    os.system("cls" if os.name == "nt" else "clear")

def _aguardar_enter():
    input(_CINZA + "Enter para continuar..." + _RESET)
    _limpar_ecra()

def _mostrar_cabecalho(titulo):
    _limpar_ecra()
    receita    = _calcular_receita_mensal()
    total_desp = _calcular_total_despesas()
    saldo      = _calcular_saldo()
    print()
    print(_VERDE + _BOLD + "[ " + titulo + " ]" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    print(_CINZA + "Receita: "    + _RESET + _VERDE + str(receita) + " EUR" + _RESET +
          _CINZA + "  Despesas: " + _RESET + _VERMELHO + str(total_desp) + " EUR" + _RESET +
          _CINZA + "  Lucro por mes: " + _RESET +
          (_VERDE_B if saldo >= 0 else _VERMELHO_B) + _BOLD + str(saldo) + " EUR" + _RESET)
    print(_CINZA + "Lucro total: " + _RESET +
          (_VERDE_B if dados.saldo_acumulado >= 0 else _VERMELHO_B) +
          _BOLD + str(dados.saldo_acumulado) + " EUR" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    print()

def _criar_plano():
    _limpar_ecra()
    print(_VERDE + _BOLD + "[ NOVO PLANO ]" + _RESET)
    print()
    nome         = _pedir_texto("Nome do plano: ")
    num_treinos  = _pedir_inteiro_positivo("Numero de treinos por mes: ")
    preco_treino = _pedir_decimal_positivo("Preco por treino (EUR): ")
    obj, codigo  = adicionar_plano(nome, num_treinos, preco_treino)
    if codigo == 201:
        print(_VERDE_B + str(codigo) + " Sucesso, plano " + str(obj[0]) + " adicionado." + _RESET)
    elif codigo == 400:
        print(_VERMELHO_B + str(codigo) + " Dados invalidos." + _RESET)
    _aguardar_enter()

def _ler_planos():
    _limpar_ecra()
    obj, codigo = mostrar_planos()
    if codigo == 204:
        print(_AMARELO + str(codigo) + " Nenhum plano registado." + _RESET)
    _aguardar_enter()

def _ler_plano():
    if len(planos) == 0:
        print(_VERMELHO_B + "404 Nao existe nenhum plano." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_planos()
    id_plano    = _pedir_id_valido("ID do plano: ", _ids_planos())
    _limpar_ecra()
    obj, codigo = mostrar_plano(id_plano)
    if codigo == 404:
        print(_VERMELHO_B + str(codigo) + " Plano nao encontrado." + _RESET)
    _aguardar_enter()

def _atualizar_plano():
    if len(planos) == 0:
        print(_VERMELHO_B + "404 Nao existe nenhum plano." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_planos()
    id_plano     = _pedir_id_valido("ID do plano: ", _ids_planos())
    print(_CINZA + "(Enter para manter o valor actual)" + _RESET)
    nome         = input(_AMARELO + "Novo nome: "         + _RESET).strip()
    num_treinos  = input(_AMARELO + "Novo num. treinos: " + _RESET).strip()
    preco_treino = input(_AMARELO + "Novo preco/treino: " + _RESET).strip()
    obj, codigo  = modificar_plano(id_plano, nome, num_treinos, preco_treino)
    if codigo == 200:
        print(_VERDE_B + str(codigo) + " Sucesso, plano " + str(obj[0]) + " atualizado." + _RESET)
    elif codigo == 404:
        print(_VERMELHO_B + str(codigo) + " Plano nao encontrado." + _RESET)
    elif codigo == 400:
        print(_VERMELHO_B + str(codigo) + " Dados invalidos." + _RESET)
    _aguardar_enter()

def _deletar_plano():
    if len(planos) == 0:
        print(_VERMELHO_B + "404 Nao existe nenhum plano." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_planos()
    id_plano  = _pedir_id_valido("ID do plano: ", _ids_planos())
    confirmar = _pedir_confirmacao("Confirmar remocao")
    if confirmar:
        obj, codigo = remover_plano(id_plano)
        if codigo == 200:
            print(_VERDE_B + str(codigo) + " Sucesso, plano " + str(obj) + " removido." + _RESET)
        elif codigo == 404:
            print(_VERMELHO_B + str(codigo) + " Plano nao encontrado." + _RESET)
        elif codigo == 409:
            print(_VERMELHO_B + str(codigo) + " Conflito: existem clientes com este plano. Remove-os primeiro." + _RESET)
    else:
        print(_CINZA + "Cancelado." + _RESET)
    _aguardar_enter()

def menu_planos():
    while True:
        _mostrar_cabecalho("PLANOS DE TREINO")
        print(_MAGENTA + _BOLD + "[1]" + _RESET + " " + _BRANCO + "Criar plano"     + _RESET)
        print(_MAGENTA + _BOLD + "[2]" + _RESET + " " + _BRANCO + "Ler planos"      + _RESET)
        print(_MAGENTA + _BOLD + "[3]" + _RESET + " " + _BRANCO + "Ler plano"       + _RESET)
        print(_MAGENTA + _BOLD + "[4]" + _RESET + " " + _BRANCO + "Atualizar plano" + _RESET)
        print(_MAGENTA + _BOLD + "[5]" + _RESET + " " + _BRANCO + "Deletar plano"   + _RESET)
        print(_MAGENTA + _BOLD + "[6]" + _RESET + " " + _BRANCO + "Guardar planos"  + _RESET)
        print(_MAGENTA + _BOLD + "[0]" + _RESET + " " + _BRANCO + "Voltar"          + _RESET)
        print(_CINZA + "-" * 40 + _RESET)
        opcao = input(_MAGENTA + _BOLD + "> " + _RESET).strip()
        if   opcao == "1": _criar_plano()
        elif opcao == "2": _ler_planos()
        elif opcao == "3": _ler_plano()
        elif opcao == "4": _atualizar_plano()
        elif opcao == "5": _deletar_plano()
        elif opcao == "6":
            guardar_planos()
            _aguardar_enter()
        elif opcao == "0": break
        else:
            print(_VERMELHO_B + "400 Opcao invalida." + _RESET)
            _aguardar_enter()

def _criar_cliente():
    if len(planos) == 0:
        print(_VERMELHO_B + "404 Nao existe nenhum plano. Cria um plano primeiro." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    print(_VERDE + _BOLD + "[ NOVO CLIENTE ]" + _RESET)
    print()
    nome            = _pedir_texto("Nome: ")
    data_nascimento = _pedir_data("Data de nascimento")
    telefone        = _pedir_telefone("Telefone: ")
    _resumo_planos()
    id_plano        = _pedir_id_valido("ID do plano: ", _ids_planos())
    data_inicio     = str(date.today()).replace("-", "/")
    print(_VERDE + "DATA DE INICIO DO PLANO: " + _MAGENTA + data_inicio + _RESET)
    obj, codigo     = adicionar_cliente(nome, data_nascimento, telefone, id_plano, data_inicio)
    if codigo == 201:
        print(_VERDE_B + str(codigo) + " Sucesso, cliente " + str(obj["nome"]) + " adicionado." + _RESET)
    elif codigo == 409:
        print(_VERMELHO_B + str(codigo) + " Conflito: ja existe um cliente com esse nome." + _RESET)
    elif codigo == 404:
        print(_VERMELHO_B + str(codigo) + " Plano nao encontrado." + _RESET)
    elif codigo == 400:
        print(_VERMELHO_B + str(codigo) + " Dados invalidos." + _RESET)
    _aguardar_enter()

def _ler_clientes():
    _limpar_ecra()
    obj, codigo = mostrar_clientes()
    if codigo == 204:
        print(_AMARELO + str(codigo) + " Nenhum cliente registado." + _RESET)
    _aguardar_enter()

def _ler_cliente():
    if len(clientes) == 0:
        print(_VERMELHO_B + "404 Nao existe nenhum cliente." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_clientes()
    id_cliente  = _pedir_id_valido("ID do cliente: ", _ids_clientes())
    _limpar_ecra()
    obj, codigo = mostrar_cliente(id_cliente)
    if codigo == 404:
        print(_VERMELHO_B + str(codigo) + " Cliente nao encontrado." + _RESET)
    _aguardar_enter()

def _atualizar_cliente():
    if len(clientes) == 0:
        print(_VERMELHO_B + "404 Nao existe nenhum cliente." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_clientes()
    id_cliente      = _pedir_id_valido("ID do cliente: ", _ids_clientes())
    print(_CINZA + "(Enter para manter o valor actual)" + _RESET)
    nome            = input(_AMARELO + "Novo nome: "                         + _RESET).strip()
    data_nascimento = input(_AMARELO + "Nova data nascimento (DD/MM/AAAA): " + _RESET).strip()
    telefone        = input(_AMARELO + "Novo telefone: "                     + _RESET).strip()
    id_plano_str    = ""
    if len(planos) > 0:
        _resumo_planos()
        id_plano_str = input(_AMARELO + "Novo ID do plano: " + _RESET).strip()
        while id_plano_str != "" and not (id_plano_str.isdigit() and int(id_plano_str) in _ids_planos()):
            print(_VERMELHO_B + "400 ID invalido." + _RESET)
            _resumo_planos()
            id_plano_str = input(_AMARELO + "Novo ID do plano: " + _RESET).strip()
    data_inicio = input(_AMARELO + "Nova data inicio (DD/MM/AAAA): " + _RESET).strip()
    obj, codigo = modificar_cliente(id_cliente, nome, data_nascimento, telefone, id_plano_str, data_inicio)
    if codigo == 200:
        print(_VERDE_B + str(codigo) + " Sucesso, cliente " + str(obj["nome"]) + " atualizado." + _RESET)
    elif codigo == 404:
        print(_VERMELHO_B + str(codigo) + " Cliente ou plano nao encontrado." + _RESET)
    elif codigo == 409:
        print(_VERMELHO_B + str(codigo) + " Conflito: ja existe um cliente com esse nome." + _RESET)
    elif codigo == 400:
        print(_VERMELHO_B + str(codigo) + " Dados invalidos." + _RESET)
    _aguardar_enter()

def _deletar_cliente():
    if len(clientes) == 0:
        print(_VERMELHO_B + "404 Nao existe nenhum cliente." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_clientes()
    id_cliente = _pedir_id_valido("ID do cliente: ", _ids_clientes())
    confirmar  = _pedir_confirmacao("Confirmar remocao")
    if confirmar:
        obj, codigo = remover_cliente(id_cliente)
        if codigo == 200:
            print(_VERDE_B + str(codigo) + " Sucesso, cliente " + str(obj) + " removido." + _RESET)
        elif codigo == 404:
            print(_VERMELHO_B + str(codigo) + " Cliente nao encontrado." + _RESET)
    else:
        print(_CINZA + "Cancelado." + _RESET)
    _aguardar_enter()

def menu_clientes():
    while True:
        _mostrar_cabecalho("CLIENTES")
        print(_MAGENTA + _BOLD + "[1]" + _RESET + " " + _BRANCO + "Criar cliente"     + _RESET)
        print(_MAGENTA + _BOLD + "[2]" + _RESET + " " + _BRANCO + "Ler clientes"      + _RESET)
        print(_MAGENTA + _BOLD + "[3]" + _RESET + " " + _BRANCO + "Ler cliente"       + _RESET)
        print(_MAGENTA + _BOLD + "[4]" + _RESET + " " + _BRANCO + "Atualizar cliente" + _RESET)
        print(_MAGENTA + _BOLD + "[5]" + _RESET + " " + _BRANCO + "Deletar cliente"   + _RESET)
        print(_MAGENTA + _BOLD + "[6]" + _RESET + " " + _BRANCO + "Pesquisar cliente" + _RESET)
        print(_MAGENTA + _BOLD + "[7]" + _RESET + " " + _BRANCO + "Guardar clientes"  + _RESET)
        print(_MAGENTA + _BOLD + "[0]" + _RESET + " " + _BRANCO + "Voltar"            + _RESET)
        print(_CINZA + "-" * 40 + _RESET)
        opcao = input(_MAGENTA + _BOLD + "> " + _RESET).strip()
        if   opcao == "1": _criar_cliente()
        elif opcao == "2": _ler_clientes()
        elif opcao == "3": _ler_cliente()
        elif opcao == "4": _atualizar_cliente()
        elif opcao == "5": _deletar_cliente()
        elif opcao == "6":
            _limpar_ecra()
            pesquisa    = _pedir_texto("Nome a pesquisar: ")
            obj, codigo = pesquisar_cliente(pesquisa)
            if codigo == 404:
                print(_AMARELO + str(codigo) + " Nenhum cliente encontrado." + _RESET)
            elif codigo == 400:
                print(_VERMELHO_B + str(codigo) + " Termo de pesquisa invalido." + _RESET)
            _aguardar_enter()
        elif opcao == "7":
            guardar_clientes()
            _aguardar_enter()
        elif opcao == "0": break
        else:
            print(_VERMELHO_B + "400 Opcao invalida." + _RESET)
            _aguardar_enter()

def _criar_despesa():
    _limpar_ecra()
    print(_VERDE + _BOLD + "[ NOVA DESPESA ]" + _RESET)
    print()
    descricao        = _pedir_texto("Descricao: ")
    valor            = _pedir_decimal_positivo("Valor (EUR): ")
    data_str         = input(_AMARELO + "Data (DD/MM/AAAA, Enter = hoje): " + _RESET).strip()
    data_despesa     = data_str if data_str else None
    obj, codigo      = adicionar_despesa(descricao, valor, data_despesa)
    if codigo == 201:
        print(_VERDE_B + str(codigo) + " Sucesso, despesa " + str(obj[1]) + " adicionada." + _RESET)
    elif codigo == 400:
        print(_VERMELHO_B + str(codigo) + " Dados invalidos." + _RESET)
    _aguardar_enter()

def _ler_despesas():
    _limpar_ecra()
    obj, codigo = mostrar_despesas()
    if codigo == 204:
        print(_AMARELO + str(codigo) + " Nenhuma despesa registada." + _RESET)
    _aguardar_enter()

def _ler_despesa():
    if len(despesas) == 0:
        print(_VERMELHO_B + "404 Nao existe nenhuma despesa." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_despesas()
    ids_validos = [d[0] for d in despesas]
    id_despesa  = _pedir_id_valido("ID da despesa: ", ids_validos)
    _limpar_ecra()
    obj, codigo = mostrar_despesa(id_despesa)
    if codigo == 404:
        print(_VERMELHO_B + str(codigo) + " Despesa nao encontrada." + _RESET)
    _aguardar_enter()

def _deletar_despesa():
    if len(despesas) == 0:
        print(_VERMELHO_B + "404 Nao existe nenhuma despesa." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_despesas()
    ids_validos = [d[0] for d in despesas]
    id_despesa  = _pedir_id_valido("ID da despesa: ", ids_validos)
    confirmar   = _pedir_confirmacao("Confirmar remocao")
    if confirmar:
        obj, codigo = remover_despesa(id_despesa)
        if codigo == 200:
            print(_VERDE_B + str(codigo) + " Sucesso, despesa " + str(obj) + " removida." + _RESET)
        elif codigo == 404:
            print(_VERMELHO_B + str(codigo) + " Despesa nao encontrada." + _RESET)
    else:
        print(_CINZA + "Cancelado." + _RESET)
    _aguardar_enter()

def menu_despesas():
    while True:
        _mostrar_cabecalho("DESPESAS")
        print(_MAGENTA + _BOLD + "[1]" + _RESET + " " + _BRANCO + "Criar despesa"    + _RESET)
        print(_MAGENTA + _BOLD + "[2]" + _RESET + " " + _BRANCO + "Ler despesas"     + _RESET)
        print(_MAGENTA + _BOLD + "[3]" + _RESET + " " + _BRANCO + "Ler despesa"      + _RESET)
        print(_MAGENTA + _BOLD + "[4]" + _RESET + " " + _BRANCO + "Deletar despesa"  + _RESET)
        print(_MAGENTA + _BOLD + "[5]" + _RESET + " " + _BRANCO + "Guardar despesas" + _RESET)
        print(_MAGENTA + _BOLD + "[0]" + _RESET + " " + _BRANCO + "Voltar"           + _RESET)
        print(_CINZA + "-" * 40 + _RESET)
        opcao = input(_MAGENTA + _BOLD + "> " + _RESET).strip()
        if   opcao == "1": _criar_despesa()
        elif opcao == "2": _ler_despesas()
        elif opcao == "3": _ler_despesa()
        elif opcao == "4": _deletar_despesa()
        elif opcao == "5":
            guardar_despesas()
            _aguardar_enter()
        elif opcao == "0": break
        else:
            print(_VERMELHO_B + "400 Opcao invalida." + _RESET)
            _aguardar_enter()

# ===========================================================================
# MENU GINÁSIOS
# ===========================================================================

def _criar_ginasio():
    """Cria um novo ginásio com nome, morada e telefone."""
    _limpar_ecra()
    print(_VERDE + _BOLD + "[ NOVO GINASIO ]" + _RESET)
    print()
    nome     = _pedir_texto("Nome do ginasio: ")
    morada   = _pedir_texto("Morada: ")
    telefone = _pedir_telefone("Telefone: ")
    obj, codigo = adicionar_ginasio(nome, morada, telefone)
    if codigo == 201:
        print(_VERDE_B + str(codigo) + " Sucesso, ginasio '" + obj["nome"] + "' criado (ID " + str(obj["id"]) + ")." + _RESET)
    elif codigo == 409:
        print(_VERMELHO_B + str(codigo) + " Conflito: ja existe um ginasio com esse nome." + _RESET)
    elif codigo == 400:
        print(_VERMELHO_B + str(codigo) + " Dados invalidos." + _RESET)
    _aguardar_enter()


def _ler_ginasios():
    """Lista todos os ginásios."""
    _limpar_ecra()
    obj, codigo = mostrar_ginasios()
    if codigo == 204:
        print(_AMARELO + str(codigo) + " Nenhum ginasio registado." + _RESET)
    _aguardar_enter()


def _ler_ginasio():
    """Mostra detalhes de um ginásio específico."""
    if not _ginasios:
        print(_VERMELHO_B + "404 Nao existe nenhum ginasio." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    _resumo_ginasios()
    print()
    id_ginasio = _pedir_id_valido("ID do ginasio: ", _ids_ginasios())
    _limpar_ecra()
    obj, codigo = mostrar_ginasio(id_ginasio)
    if codigo == 404:
        print(_VERMELHO_B + str(codigo) + " Ginasio nao encontrado." + _RESET)
    _aguardar_enter()


def _atualizar_ginasio():
    """Atualiza nome, morada e/ou telefone de um ginásio."""
    if not _ginasios:
        print(_VERMELHO_B + "404 Nao existe nenhum ginasio." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    _resumo_ginasios()
    print()
    id_ginasio = _pedir_id_valido("ID do ginasio: ", _ids_ginasios())
    print(_CINZA + "(Enter para manter o valor actual)" + _RESET)
    nome     = input(_AMARELO + "Novo nome: "     + _RESET).strip()
    morada   = input(_AMARELO + "Nova morada: "   + _RESET).strip()
    telefone = input(_AMARELO + "Novo telefone: " + _RESET).strip()

    # Validar telefone só se foi fornecido
    if telefone != "" and (not telefone.isdigit() or len(telefone) != 9):
        print(_VERMELHO_B + "400 Telefone invalido (deve ter 9 digitos)." + _RESET)
        _aguardar_enter()
        return

    obj, codigo = modificar_ginasio(id_ginasio, nome, morada, telefone)
    if codigo == 200:
        print(_VERDE_B + str(codigo) + " Sucesso, ginasio '" + obj["nome"] + "' atualizado." + _RESET)
    elif codigo == 404:
        print(_VERMELHO_B + str(codigo) + " Ginasio nao encontrado." + _RESET)
    elif codigo == 409:
        print(_VERMELHO_B + str(codigo) + " Conflito: ja existe um ginasio com esse nome." + _RESET)
    elif codigo == 400:
        print(_VERMELHO_B + str(codigo) + " Dados invalidos." + _RESET)
    _aguardar_enter()


def _deletar_ginasio():
    """Remove um ginásio (e todos os seus dados)."""
    if not _ginasios:
        print(_VERMELHO_B + "404 Nao existe nenhum ginasio." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    _resumo_ginasios()
    print()
    id_ginasio = _pedir_id_valido("ID do ginasio: ", _ids_ginasios())
    g, _ = obter_ginasio(id_ginasio)
    print()
    print(_VERMELHO_B + "ATENCAO: Esta operacao eliminara o ginasio '" + g["nome"] + "' e TODOS os seus dados." + _RESET)
    confirmar = _pedir_confirmacao("Confirmar remocao")
    if confirmar:
        obj, codigo = remover_ginasio(id_ginasio)
        if codigo == 200:
            print(_VERDE_B + str(codigo) + " Sucesso, ginasio ID " + str(obj) + " removido." + _RESET)
        elif codigo == 404:
            print(_VERMELHO_B + str(codigo) + " Ginasio nao encontrado." + _RESET)
    else:
        print(_CINZA + "Cancelado." + _RESET)
    _aguardar_enter()


# ---------------------------------------------------------------------------
# Submenu de gestão interna de um ginásio (planos e clientes isolados)
# ---------------------------------------------------------------------------

def _menu_ginasio_interno(id_ginasio: int):
    """
    Abre um submenu para gerir os dados internos (planos e clientes)
    do ginásio selecionado, usando os dados isolados desse ginásio.
    """
    from src import ginasios as _mod_ginasios

    g = _mod_ginasios._ginasios.get(id_ginasio)
    if g is None:
        print(_VERMELHO_B + "404 Ginasio nao encontrado." + _RESET)
        _aguardar_enter()
        return

    d = g["dados"]   # estado isolado deste ginásio

    # ------------------------------------------------------------------
    # Helpers para planos locais
    # ------------------------------------------------------------------
    def _arredondar(v):
        return round(v, 2)

    def _ids_planos_loc():
        return list(d["planos"].keys())

    def _resumo_planos_loc():
        if not d["planos"]:
            print(_AMARELO + "Nenhum plano neste ginasio." + _RESET)
            return
        print(_CINZA + "Planos:" + _RESET)
        for pid, p in d["planos"].items():
            pm = _arredondar(p[1] * p[2])
            print(_AMARELO + "[" + str(pid) + "] " + _RESET +
                  _BRANCO + p[0] + _RESET +
                  _CINZA + " - " + str(p[1]) + " treinos - " + str(pm) + " EUR/mes" + _RESET)

    def _mostrar_planos_loc():
        if not d["planos"]:
            print(_AMARELO + "204 Nenhum plano registado." + _RESET)
            return
        print(_VERDE + _BOLD + "[ PLANOS — " + g["nome"] + " ]" + _RESET)
        print(_CINZA + "-" * 44 + _RESET)
        for pid, p in d["planos"].items():
            pm = _arredondar(p[1] * p[2])
            tc = sum(1 for c in d["clientes"].values() if c["id_plano"] == pid)
            print(_AMARELO + "ID: "           + _RESET + _BRANCO  + str(pid) + _RESET)
            print(_CINZA   + "Nome: "         + _RESET + _BRANCO  + p[0]    + _RESET)
            print(_CINZA   + "Treinos/mes: "  + _RESET + str(p[1]))
            print(_CINZA   + "Preco/treino: " + _RESET + _VERDE   + str(p[2]) + " EUR" + _RESET)
            print(_CINZA   + "Total mensal: " + _RESET + _VERDE   + str(pm)   + " EUR" + _RESET)
            print(_CINZA   + "Clientes: "     + _RESET + _AMARELO + str(tc)   + _RESET)
            print(_CINZA + "-" * 44 + _RESET)

    def _criar_plano_loc():
        _limpar_ecra()
        print(_VERDE + _BOLD + "[ NOVO PLANO — " + g["nome"] + " ]" + _RESET)
        print()
        nome         = _pedir_texto("Nome do plano: ")
        num_treinos  = _pedir_inteiro_positivo("Numero de treinos por mes: ")
        preco_treino = _pedir_decimal_positivo("Preco por treino (EUR): ")
        pid = d["proximo_id_plano"]
        d["planos"][pid] = (nome, num_treinos, _arredondar(preco_treino))
        d["proximo_id_plano"] += 1
        print(_VERDE_B + "201 Sucesso, plano '" + nome + "' adicionado (ID " + str(pid) + ")." + _RESET)
        _aguardar_enter()

    def _ler_planos_loc():
        _limpar_ecra()
        _mostrar_planos_loc()
        _aguardar_enter()

    def _ler_plano_loc():
        if not d["planos"]:
            print(_VERMELHO_B + "404 Nao existe nenhum plano." + _RESET)
            _aguardar_enter()
            return
        _limpar_ecra()
        _mostrar_planos_loc()
        pid = _pedir_id_valido("ID do plano: ", _ids_planos_loc())
        _limpar_ecra()
        p = d["planos"][pid]
        pm = _arredondar(p[1] * p[2])
        print(_VERDE + _BOLD + "[ PLANO ]" + _RESET)
        print(_CINZA + "-" * 44 + _RESET)
        print(_AMARELO + "ID: "           + _RESET + _BRANCO + str(pid) + _RESET)
        print(_CINZA   + "Nome: "         + _RESET + _BRANCO + p[0]    + _RESET)
        print(_CINZA   + "Treinos/mes: "  + _RESET + str(p[1]))
        print(_CINZA   + "Preco/treino: " + _RESET + _VERDE  + str(p[2]) + " EUR" + _RESET)
        print(_CINZA   + "Total mensal: " + _RESET + _VERDE  + str(pm)   + " EUR" + _RESET)
        print(_CINZA + "-" * 44 + _RESET)
        _aguardar_enter()

    def _atualizar_plano_loc():
        if not d["planos"]:
            print(_VERMELHO_B + "404 Nao existe nenhum plano." + _RESET)
            _aguardar_enter()
            return
        _limpar_ecra()
        _mostrar_planos_loc()
        pid = _pedir_id_valido("ID do plano: ", _ids_planos_loc())
        plano_atual = d["planos"][pid]
        print(_CINZA + "(Enter para manter o valor actual)" + _RESET)
        nome         = input(_AMARELO + "Novo nome: "         + _RESET).strip()
        num_treinos  = input(_AMARELO + "Novo num. treinos: " + _RESET).strip()
        preco_treino = input(_AMARELO + "Novo preco/treino: " + _RESET).strip()

        nome         = nome         if nome         else plano_atual[0]
        if num_treinos:
            try:
                num_treinos = int(num_treinos)
                if num_treinos <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                print(_VERMELHO_B + "400 Dados invalidos." + _RESET)
                _aguardar_enter()
                return
        else:
            num_treinos = plano_atual[1]

        if preco_treino:
            try:
                preco_treino = _arredondar(float(preco_treino))
                if preco_treino <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                print(_VERMELHO_B + "400 Dados invalidos." + _RESET)
                _aguardar_enter()
                return
        else:
            preco_treino = plano_atual[2]

        d["planos"][pid] = (nome, num_treinos, preco_treino)
        print(_VERDE_B + "200 Sucesso, plano '" + nome + "' atualizado." + _RESET)
        _aguardar_enter()

    def _deletar_plano_loc():
        if not d["planos"]:
            print(_VERMELHO_B + "404 Nao existe nenhum plano." + _RESET)
            _aguardar_enter()
            return
        _limpar_ecra()
        _mostrar_planos_loc()
        pid = _pedir_id_valido("ID do plano: ", _ids_planos_loc())
        # Verificar se há clientes com este plano
        em_uso = any(c["id_plano"] == pid for c in d["clientes"].values())
        if em_uso:
            print(_VERMELHO_B + "409 Conflito: existem clientes com este plano. Remove-os primeiro." + _RESET)
            _aguardar_enter()
            return
        confirmar = _pedir_confirmacao("Confirmar remocao")
        if confirmar:
            del d["planos"][pid]
            print(_VERDE_B + "200 Sucesso, plano ID " + str(pid) + " removido." + _RESET)
        else:
            print(_CINZA + "Cancelado." + _RESET)
        _aguardar_enter()

    # ------------------------------------------------------------------
    # Helpers para clientes locais
    # ------------------------------------------------------------------
    def _ids_clientes_loc():
        return list(d["clientes"].keys())

    def _mostrar_clientes_loc():
        if not d["clientes"]:
            print(_AMARELO + "204 Nenhum cliente registado." + _RESET)
            return
        print(_VERDE + _BOLD + "[ CLIENTES — " + g["nome"] + " ]" + _RESET)
        print(_CINZA + "-" * 44 + _RESET)
        for cid, c in d["clientes"].items():
            nome_plano = d["planos"].get(c["id_plano"], ("Desconhecido",))[0]
            print(_AMARELO + "ID: "          + _RESET + _BRANCO  + str(cid)          + _RESET)
            print(_CINZA   + "Nome: "        + _RESET + _BRANCO  + c["nome"]         + _RESET)
            print(_CINZA   + "Nascimento: "  + _RESET + c["data_nascimento"])
            print(_CINZA   + "Telefone: "    + _RESET + c["telefone"])
            print(_CINZA   + "Plano: "       + _RESET + _VERDE   + nome_plano        + _RESET)
            print(_CINZA   + "Inicio: "      + _RESET + c["data_inicio"])
            print(_CINZA + "-" * 44 + _RESET)

    def _criar_cliente_loc():
        if not d["planos"]:
            print(_VERMELHO_B + "404 Nao existe nenhum plano. Cria um plano primeiro." + _RESET)
            _aguardar_enter()
            return
        _limpar_ecra()
        print(_VERDE + _BOLD + "[ NOVO CLIENTE — " + g["nome"] + " ]" + _RESET)
        print()
        nome            = _pedir_texto("Nome: ")
        # Verificar duplicado de nome
        for c in d["clientes"].values():
            if c["nome"].lower() == nome.lower():
                print(_VERMELHO_B + "409 Conflito: ja existe um cliente com esse nome." + _RESET)
                _aguardar_enter()
                return
        data_nascimento = _pedir_data("Data de nascimento")
        telefone        = _pedir_telefone("Telefone: ")
        _resumo_planos_loc()
        id_plano        = _pedir_id_valido("ID do plano: ", _ids_planos_loc())
        data_inicio     = str(date.today()).replace("-", "/")
        print(_VERDE + "DATA DE INICIO DO PLANO: " + _MAGENTA + data_inicio + _RESET)
        cid = d["proximo_id_cliente"]
        d["clientes"][cid] = {
            "nome":            nome,
            "data_nascimento": data_nascimento,
            "telefone":        telefone,
            "id_plano":        id_plano,
            "data_inicio":     data_inicio,
        }
        d["proximo_id_cliente"] += 1
        print(_VERDE_B + "201 Sucesso, cliente '" + nome + "' adicionado (ID " + str(cid) + ")." + _RESET)
        _aguardar_enter()

    def _ler_clientes_loc():
        _limpar_ecra()
        _mostrar_clientes_loc()
        _aguardar_enter()

    def _ler_cliente_loc():
        if not d["clientes"]:
            print(_VERMELHO_B + "404 Nao existe nenhum cliente." + _RESET)
            _aguardar_enter()
            return
        _limpar_ecra()
        _mostrar_clientes_loc()
        cid = _pedir_id_valido("ID do cliente: ", _ids_clientes_loc())
        _limpar_ecra()
        c = d["clientes"][cid]
        nome_plano = d["planos"].get(c["id_plano"], ("Desconhecido",))[0]
        print(_VERDE + _BOLD + "[ CLIENTE ]" + _RESET)
        print(_CINZA + "-" * 44 + _RESET)
        print(_AMARELO + "ID: "         + _RESET + _BRANCO + str(cid)          + _RESET)
        print(_CINZA   + "Nome: "       + _RESET + _BRANCO + c["nome"]         + _RESET)
        print(_CINZA   + "Nascimento: " + _RESET + c["data_nascimento"])
        print(_CINZA   + "Telefone: "   + _RESET + c["telefone"])
        print(_CINZA   + "Plano: "      + _RESET + _VERDE  + nome_plano        + _RESET)
        print(_CINZA   + "Inicio: "     + _RESET + c["data_inicio"])
        print(_CINZA + "-" * 44 + _RESET)
        _aguardar_enter()

    def _atualizar_cliente_loc():
        if not d["clientes"]:
            print(_VERMELHO_B + "404 Nao existe nenhum cliente." + _RESET)
            _aguardar_enter()
            return
        _limpar_ecra()
        _mostrar_clientes_loc()
        cid = _pedir_id_valido("ID do cliente: ", _ids_clientes_loc())
        c_atual = d["clientes"][cid]
        print(_CINZA + "(Enter para manter o valor actual)" + _RESET)
        nome            = input(_AMARELO + "Novo nome: "                         + _RESET).strip()
        data_nascimento = input(_AMARELO + "Nova data nascimento (DD/MM/AAAA): " + _RESET).strip()
        telefone        = input(_AMARELO + "Novo telefone: "                     + _RESET).strip()
        id_plano_str    = ""
        if d["planos"]:
            _resumo_planos_loc()
            id_plano_str = input(_AMARELO + "Novo ID do plano: " + _RESET).strip()
            while id_plano_str != "" and not (id_plano_str.isdigit() and int(id_plano_str) in _ids_planos_loc()):
                print(_VERMELHO_B + "400 ID invalido." + _RESET)
                _resumo_planos_loc()
                id_plano_str = input(_AMARELO + "Novo ID do plano: " + _RESET).strip()
        data_inicio = input(_AMARELO + "Nova data inicio (DD/MM/AAAA): " + _RESET).strip()

        # Verificar duplicado de nome (excluindo o próprio)
        if nome:
            for other_id, other_c in d["clientes"].items():
                if other_id != cid and other_c["nome"].lower() == nome.lower():
                    print(_VERMELHO_B + "409 Conflito: ja existe um cliente com esse nome." + _RESET)
                    _aguardar_enter()
                    return

        d["clientes"][cid] = {
            "nome":            nome            if nome            else c_atual["nome"],
            "data_nascimento": data_nascimento if data_nascimento else c_atual["data_nascimento"],
            "telefone":        telefone        if telefone        else c_atual["telefone"],
            "id_plano":        int(id_plano_str) if id_plano_str else c_atual["id_plano"],
            "data_inicio":     data_inicio     if data_inicio     else c_atual["data_inicio"],
        }
        print(_VERDE_B + "200 Sucesso, cliente '" + d["clientes"][cid]["nome"] + "' atualizado." + _RESET)
        _aguardar_enter()

    def _deletar_cliente_loc():
        if not d["clientes"]:
            print(_VERMELHO_B + "404 Nao existe nenhum cliente." + _RESET)
            _aguardar_enter()
            return
        _limpar_ecra()
        _mostrar_clientes_loc()
        cid = _pedir_id_valido("ID do cliente: ", _ids_clientes_loc())
        confirmar = _pedir_confirmacao("Confirmar remocao")
        if confirmar:
            del d["clientes"][cid]
            print(_VERDE_B + "200 Sucesso, cliente ID " + str(cid) + " removido." + _RESET)
        else:
            print(_CINZA + "Cancelado." + _RESET)
        _aguardar_enter()

    # ------------------------------------------------------------------
    # Sub-submenus
    # ------------------------------------------------------------------
    def _submenu_planos_ginasio():
        while True:
            _limpar_ecra()
            print(_VERDE + _BOLD + "[ PLANOS — " + g["nome"] + " ]" + _RESET)
            print(_CINZA + "-" * 44 + _RESET)
            print(_MAGENTA + _BOLD + "[1]" + _RESET + " " + _BRANCO + "Criar plano"     + _RESET)
            print(_MAGENTA + _BOLD + "[2]" + _RESET + " " + _BRANCO + "Ler planos"      + _RESET)
            print(_MAGENTA + _BOLD + "[3]" + _RESET + " " + _BRANCO + "Ler plano"       + _RESET)
            print(_MAGENTA + _BOLD + "[4]" + _RESET + " " + _BRANCO + "Atualizar plano" + _RESET)
            print(_MAGENTA + _BOLD + "[5]" + _RESET + " " + _BRANCO + "Deletar plano"   + _RESET)
            print(_MAGENTA + _BOLD + "[0]" + _RESET + " " + _BRANCO + "Voltar"          + _RESET)
            print(_CINZA + "-" * 44 + _RESET)
            opcao = input(_MAGENTA + _BOLD + "> " + _RESET).strip()
            if   opcao == "1": _criar_plano_loc()
            elif opcao == "2": _ler_planos_loc()
            elif opcao == "3": _ler_plano_loc()
            elif opcao == "4": _atualizar_plano_loc()
            elif opcao == "5": _deletar_plano_loc()
            elif opcao == "0": break
            else:
                print(_VERMELHO_B + "400 Opcao invalida." + _RESET)
                _aguardar_enter()

    def _submenu_clientes_ginasio():
        while True:
            _limpar_ecra()
            print(_VERDE + _BOLD + "[ CLIENTES — " + g["nome"] + " ]" + _RESET)
            print(_CINZA + "-" * 44 + _RESET)
            print(_MAGENTA + _BOLD + "[1]" + _RESET + " " + _BRANCO + "Criar cliente"     + _RESET)
            print(_MAGENTA + _BOLD + "[2]" + _RESET + " " + _BRANCO + "Ler clientes"      + _RESET)
            print(_MAGENTA + _BOLD + "[3]" + _RESET + " " + _BRANCO + "Ler cliente"       + _RESET)
            print(_MAGENTA + _BOLD + "[4]" + _RESET + " " + _BRANCO + "Atualizar cliente" + _RESET)
            print(_MAGENTA + _BOLD + "[5]" + _RESET + " " + _BRANCO + "Deletar cliente"   + _RESET)
            print(_MAGENTA + _BOLD + "[0]" + _RESET + " " + _BRANCO + "Voltar"            + _RESET)
            print(_CINZA + "-" * 44 + _RESET)
            opcao = input(_MAGENTA + _BOLD + "> " + _RESET).strip()
            if   opcao == "1": _criar_cliente_loc()
            elif opcao == "2": _ler_clientes_loc()
            elif opcao == "3": _ler_cliente_loc()
            elif opcao == "4": _atualizar_cliente_loc()
            elif opcao == "5": _deletar_cliente_loc()
            elif opcao == "0": break
            else:
                print(_VERMELHO_B + "400 Opcao invalida." + _RESET)
                _aguardar_enter()

    # ------------------------------------------------------------------
    # Menu interno do ginásio selecionado
    # ------------------------------------------------------------------
    while True:
        _limpar_ecra()
        print(_VERDE + _BOLD + "[ " + g["nome"].upper() + " ]" + _RESET)
        print(_CINZA + "Morada: " + g["morada"] + "  |  Tel: " + g["telefone"] + _RESET)
        print(_CINZA + "-" * 44 + _RESET)
        print(_MAGENTA + _BOLD + "[1]" + _RESET + " " + _BRANCO + "Gerir planos"   + _RESET)
        print(_MAGENTA + _BOLD + "[2]" + _RESET + " " + _BRANCO + "Gerir clientes" + _RESET)
        print(_MAGENTA + _BOLD + "[0]" + _RESET + " " + _BRANCO + "Voltar"         + _RESET)
        print(_CINZA + "-" * 44 + _RESET)
        opcao = input(_MAGENTA + _BOLD + "> " + _RESET).strip()
        if   opcao == "1": _submenu_planos_ginasio()
        elif opcao == "2": _submenu_clientes_ginasio()
        elif opcao == "0": break
        else:
            print(_VERMELHO_B + "400 Opcao invalida." + _RESET)
            _aguardar_enter()


def menu_ginasios():
    """Menu principal de gestão de ginásios."""
    while True:
        _limpar_ecra()
        print(_VERDE + _BOLD + "[ GINASIOS ]" + _RESET)
        print(_CINZA + "-" * 44 + _RESET)
        print(_MAGENTA + _BOLD + "[1]" + _RESET + " " + _BRANCO + "Criar ginasio"     + _RESET)
        print(_MAGENTA + _BOLD + "[2]" + _RESET + " " + _BRANCO + "Listar ginasios"   + _RESET)
        print(_MAGENTA + _BOLD + "[3]" + _RESET + " " + _BRANCO + "Ver ginasio"       + _RESET)
        print(_MAGENTA + _BOLD + "[4]" + _RESET + " " + _BRANCO + "Atualizar ginasio" + _RESET)
        print(_MAGENTA + _BOLD + "[5]" + _RESET + " " + _BRANCO + "Remover ginasio"   + _RESET)
        print(_MAGENTA + _BOLD + "[6]" + _RESET + " " + _BRANCO + "Entrar num ginasio (gerir planos/clientes)" + _RESET)
        print(_MAGENTA + _BOLD + "[7]" + _RESET + " " + _BRANCO + "Guardar ginasios"  + _RESET)
        print(_MAGENTA + _BOLD + "[0]" + _RESET + " " + _BRANCO + "Voltar"            + _RESET)
        print(_CINZA + "-" * 44 + _RESET)
        opcao = input(_MAGENTA + _BOLD + "> " + _RESET).strip()
        if   opcao == "1": _criar_ginasio()
        elif opcao == "2": _ler_ginasios()
        elif opcao == "3": _ler_ginasio()
        elif opcao == "4": _atualizar_ginasio()
        elif opcao == "5": _deletar_ginasio()
        elif opcao == "6":
            if not _ginasios:
                print(_VERMELHO_B + "404 Nao existe nenhum ginasio. Cria um primeiro." + _RESET)
                _aguardar_enter()
            else:
                _limpar_ecra()
                _resumo_ginasios()
                print()
                id_ginasio = _pedir_id_valido("ID do ginasio: ", _ids_ginasios())
                _menu_ginasio_interno(id_ginasio)
        elif opcao == "7":
            guardar_ginasios()
            _aguardar_enter()
        elif opcao == "0": break
        else:
            print(_VERMELHO_B + "400 Opcao invalida." + _RESET)
            _aguardar_enter()


# ===========================================================================
# FIM DO BLOCO GINÁSIOS
# ===========================================================================

def menu_principal():
    while True:
        _mostrar_cabecalho("GESTOR DE GINASIO  |  Ginasio Default")
        print(_MAGENTA + _BOLD + "[1]" + _RESET + " " + _BRANCO + "Clientes"             + _RESET)
        print(_MAGENTA + _BOLD + "[2]" + _RESET + " " + _BRANCO + "Planos de treino"     + _RESET)
        print(_MAGENTA + _BOLD + "[3]" + _RESET + " " + _BRANCO + "Despesas"             + _RESET)
        print(_MAGENTA + _BOLD + "[4]" + _RESET + " " + _BRANCO + "Relatorio financeiro" + _RESET)
        print(_MAGENTA + _BOLD + "[5]" + _RESET + " " + _BRANCO + "Estatisticas"         + _RESET)
        print(_MAGENTA + _BOLD + "[6]" + _RESET + " " + _BRANCO + "Simular mes"          + _RESET)
        print(_MAGENTA + _BOLD + "[7]" + _RESET + " " + _BRANCO + "Pagamentos"           + _RESET)
        print(_MAGENTA + _BOLD + "[8]" + _RESET + " " + _BRANCO + "Ginasios"             + _RESET)
        print(_MAGENTA + _BOLD + "[0]" + _RESET + " " + _BRANCO + "Sair"                 + _RESET)
        print(_CINZA + "-" * 40 + _RESET)
        opcao = input(_MAGENTA + _BOLD + "> " + _RESET).strip()
        if   opcao == "1": menu_clientes()
        elif opcao == "2": menu_planos()
        elif opcao == "3": menu_despesas()
        elif opcao == "4":
            _limpar_ecra()
            obj, codigo = mostrar_relatorio_financeiro()
            if codigo == 500:
                print(_VERMELHO_B + str(codigo) + " Erro interno ao gerar relatorio." + _RESET)
            _aguardar_enter()
        elif opcao == "5":
            _limpar_ecra()
            obj, codigo = mostrar_estatisticas()
            if codigo == 500:
                print(_VERMELHO_B + str(codigo) + " Erro interno ao gerar estatisticas." + _RESET)
            _aguardar_enter()

        elif opcao == "7":
            menu_pagamentos()

        elif opcao == "8":
            menu_ginasios()

        elif opcao == "6":
            _limpar_ecra()
            obj, codigo = simular_mes()
            if codigo == 500:
                print(_VERMELHO_B + str(codigo) + " Erro interno ao simular mes." + _RESET)
            _aguardar_enter()
        elif opcao == "0":
            _limpar_ecra()
            print(_VERDE + "Ate logo." + _RESET)
            break
        else:
            print(_VERMELHO_B + "400 Opcao invalida." + _RESET)
            _aguardar_enter()
