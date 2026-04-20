import os
from datetime import date

try:
    from src import dados
    from src.dados import clientes, planos, despesas
    from src.planos import (adicionar_plano, mostrar_planos, mostrar_plano, modificar_plano,
                            remover_plano, _ids_planos, _resumo_planos)
    from src.clientes import (adicionar_cliente, mostrar_clientes, mostrar_cliente, modificar_cliente,
                              remover_cliente, pesquisar_cliente, _ids_clientes)
    from src.despesas import (adicionar_despesa, mostrar_despesas, mostrar_despesa, remover_despesa)
    from src.relatorios import mostrar_relatorio_financeiro, mostrar_estatisticas, simular_mes
    from src.relatorios import _calcular_receita_mensal, _calcular_total_despesas, _calcular_saldo
    from src.utils import (_pedir_texto, _pedir_inteiro_positivo, _pedir_decimal_positivo,
                           _pedir_data, _pedir_telefone, _pedir_id_valido, _pedir_confirmacao)
except ImportError:
    import dados
    from dados import clientes, planos, despesas
    from planos import (adicionar_plano, mostrar_planos, mostrar_plano, modificar_plano,
                        remover_plano, _ids_planos, _resumo_planos)
    from clientes import (adicionar_cliente, mostrar_clientes, mostrar_cliente, modificar_cliente,
                          remover_cliente, pesquisar_cliente, _ids_clientes)
    from despesas import (adicionar_despesa, mostrar_despesas, mostrar_despesa, remover_despesa)
    from relatorios import mostrar_relatorio_financeiro, mostrar_estatisticas, simular_mes
    from relatorios import _calcular_receita_mensal, _calcular_total_despesas, _calcular_saldo
    from utils import (_pedir_texto, _pedir_inteiro_positivo, _pedir_decimal_positivo,
                       _pedir_data, _pedir_telefone, _pedir_id_valido, _pedir_confirmacao)
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
    receita   = _calcular_receita_mensal()
    total_desp = _calcular_total_despesas()
    saldo     = _calcular_saldo()
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
    try:
        nome        = _pedir_texto("Nome do plano: ")
        num_treinos = _pedir_inteiro_positivo("Numero de treinos por mes: ")
        preco_treino = _pedir_decimal_positivo("Preco por treino (EUR): ")
        adicionar_plano(nome, num_treinos, preco_treino)
    except Exception as erro:
        print(_VERMELHO_B + "[HTTP 500] Erro inesperado: " + str(erro) + _RESET)
    _aguardar_enter()

def _ler_planos():
    _limpar_ecra()
    mostrar_planos()
    _aguardar_enter()

def _ler_plano():
    if len(planos) == 0:
        print(_VERMELHO_B + "[HTTP 404] Nao existe nenhum plano." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_planos()
    try:
        id_plano = _pedir_id_valido("ID do plano: ", _ids_planos())
        _limpar_ecra()
        mostrar_plano(id_plano)
    except Exception as erro:
        print(_VERMELHO_B + "[HTTP 500] Erro inesperado: " + str(erro) + _RESET)
    _aguardar_enter()

def _atualizar_plano():
    if len(planos) == 0:
        print(_VERMELHO_B + "[HTTP 404] Nao existe nenhum plano." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_planos()
    try:
        id_plano = _pedir_id_valido("ID do plano: ", _ids_planos())
        print(_CINZA + "(Enter para manter o valor actual)" + _RESET)
        nome        = input(_AMARELO + "Novo nome: "         + _RESET).strip()
        num_treinos = input(_AMARELO + "Novo num. treinos: " + _RESET).strip()
        preco_treino = input(_AMARELO + "Novo preco/treino: " + _RESET).strip()
        modificar_plano(id_plano, nome, num_treinos, preco_treino)
    except Exception as erro:
        print(_VERMELHO_B + "[HTTP 500] Erro inesperado: " + str(erro) + _RESET)
    _aguardar_enter()

def _deletar_plano():
    if len(planos) == 0:
        print(_VERMELHO_B + "[HTTP 404] Nao existe nenhum plano." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_planos()
    try:
        id_plano = _pedir_id_valido("ID do plano: ", _ids_planos())
        confirmar = _pedir_confirmacao("Confirmar remocao")
        if confirmar:
            remover_plano(id_plano)
        else:
            print(_CINZA + "Cancelado." + _RESET)
    except Exception as erro:
        print(_VERMELHO_B + "[HTTP 500] Erro inesperado: " + str(erro) + _RESET)
    _aguardar_enter()

def menu_planos():
    while True:
        _mostrar_cabecalho("PLANOS DE TREINO")
        print(_MAGENTA + _BOLD + "[1]" + _RESET + " " + _BRANCO + "Criar plano"     + _RESET)
        print(_MAGENTA + _BOLD + "[2]" + _RESET + " " + _BRANCO + "Ler planos"      + _RESET)
        print(_MAGENTA + _BOLD + "[3]" + _RESET + " " + _BRANCO + "Ler plano"       + _RESET)
        print(_MAGENTA + _BOLD + "[4]" + _RESET + " " + _BRANCO + "Atualizar plano" + _RESET)
        print(_MAGENTA + _BOLD + "[5]" + _RESET + " " + _BRANCO + "Deletar plano"   + _RESET)
        print(_MAGENTA + _BOLD + "[0]" + _RESET + " " + _BRANCO + "Voltar"          + _RESET)
        print(_CINZA + "-" * 40 + _RESET)
        opcao = input(_MAGENTA + _BOLD + "> " + _RESET).strip()

        if   opcao == "1": _criar_plano()
        elif opcao == "2": _ler_planos()
        elif opcao == "3": _ler_plano()
        elif opcao == "4": _atualizar_plano()
        elif opcao == "5": _deletar_plano()
        elif opcao == "0": break
        else:
            print(_VERMELHO_B + "[HTTP 400] Opcao invalida." + _RESET)
            _aguardar_enter()

def _criar_cliente():
    if len(planos) == 0:
        print(_VERMELHO_B + "[HTTP 404] Nao existe nenhum plano. Cria um plano primeiro." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    print(_VERDE + _BOLD + "[ NOVO CLIENTE ]" + _RESET)
    print()
    try:
        nome             = _pedir_texto("Nome: ")
        data_nascimento  = _pedir_data("Data de nascimento")
        telefone         = _pedir_telefone("Telefone: ")
        _resumo_planos()
        id_plano         = _pedir_id_valido("ID do plano: ", _ids_planos())
        data_inicio      = str(date.today()).replace("-", "/")
        print(_VERDE + "DATA DE INICIO DO PLANO: " + _MAGENTA + data_inicio + _RESET)
        adicionar_cliente(nome, data_nascimento, telefone, id_plano, data_inicio)
    except Exception as erro:
        print(_VERMELHO_B + "[HTTP 500] Erro inesperado: " + str(erro) + _RESET)
    _aguardar_enter()

def _ler_clientes():
    _limpar_ecra()
    mostrar_clientes()
    _aguardar_enter()

def _ler_cliente():
    if len(clientes) == 0:
        print(_VERMELHO_B + "[HTTP 404] Nao existe nenhum cliente." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_clientes()
    try:
        id_cliente = _pedir_id_valido("ID do cliente: ", _ids_clientes())
        _limpar_ecra()
        mostrar_cliente(id_cliente)
    except Exception as erro:
        print(_VERMELHO_B + "[HTTP 500] Erro inesperado: " + str(erro) + _RESET)
    _aguardar_enter()

def _atualizar_cliente():
    if len(clientes) == 0:
        print(_VERMELHO_B + "[HTTP 404] Nao existe nenhum cliente." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_clientes()
    try:
        id_cliente      = _pedir_id_valido("ID do cliente: ", _ids_clientes())
        print(_CINZA + "(Enter para manter o valor actual)" + _RESET)
        nome            = input(_AMARELO + "Novo nome: "                              + _RESET).strip()
        data_nascimento = input(_AMARELO + "Nova data nascimento (DD/MM/AAAA): "      + _RESET).strip()
        telefone        = input(_AMARELO + "Novo telefone: "                          + _RESET).strip()
        id_plano_str    = ""
        if len(planos) > 0:
            _resumo_planos()
            id_plano_str = input(_AMARELO + "Novo ID do plano: " + _RESET).strip()
            while id_plano_str != "" and not (id_plano_str.isdigit() and int(id_plano_str) in _ids_planos()):
                print(_VERMELHO_B + "[HTTP 400] ID invalido." + _RESET)
                _resumo_planos()
                id_plano_str = input(_AMARELO + "Novo ID do plano: " + _RESET).strip()
        data_inicio = input(_AMARELO + "Nova data inicio (DD/MM/AAAA): " + _RESET).strip()
        modificar_cliente(id_cliente, nome, data_nascimento, telefone, id_plano_str, data_inicio)
    except Exception as erro:
        print(_VERMELHO_B + "[HTTP 500] Erro inesperado: " + str(erro) + _RESET)
    _aguardar_enter()

def _deletar_cliente():
    if len(clientes) == 0:
        print(_VERMELHO_B + "[HTTP 404] Nao existe nenhum cliente." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_clientes()
    try:
        id_cliente = _pedir_id_valido("ID do cliente: ", _ids_clientes())
        confirmar  = _pedir_confirmacao("Confirmar remocao")
        if confirmar:
            remover_cliente(id_cliente)
        else:
            print(_CINZA + "Cancelado." + _RESET)
    except Exception as erro:
        print(_VERMELHO_B + "[HTTP 500] Erro inesperado: " + str(erro) + _RESET)
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
            try:
                pesquisa = _pedir_texto("Nome a pesquisar: ")
                pesquisar_cliente(pesquisa)
            except Exception as erro:
                print(_VERMELHO_B + "[HTTP 500] Erro inesperado: " + str(erro) + _RESET)
            _aguardar_enter()
        elif opcao == "0": break
        else:
            print(_VERMELHO_B + "[HTTP 400] Opcao invalida." + _RESET)
            _aguardar_enter()

def _criar_despesa():
    _limpar_ecra()
    print(_VERDE + _BOLD + "[ NOVA DESPESA ]" + _RESET)
    print()
    try:
        descricao = _pedir_texto("Descricao: ")
        valor     = _pedir_decimal_positivo("Valor (EUR): ")
        adicionar_despesa(descricao, valor)
    except Exception as erro:
        print(_VERMELHO_B + "[HTTP 500] Erro inesperado: " + str(erro) + _RESET)
    _aguardar_enter()

def _ler_despesas():
    _limpar_ecra()
    mostrar_despesas()
    _aguardar_enter()

def _ler_despesa():
    if len(despesas) == 0:
        print(_VERMELHO_B + "[HTTP 404] Nao existe nenhuma despesa." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_despesas()
    try:
        ids_validos = [d[0] for d in despesas]
        id_despesa  = _pedir_id_valido("ID da despesa: ", ids_validos)
        _limpar_ecra()
        mostrar_despesa(id_despesa)
    except Exception as erro:
        print(_VERMELHO_B + "[HTTP 500] Erro inesperado: " + str(erro) + _RESET)
    _aguardar_enter()

def _deletar_despesa():
    if len(despesas) == 0:
        print(_VERMELHO_B + "[HTTP 404] Nao existe nenhuma despesa." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    mostrar_despesas()
    try:
        ids_validos = [d[0] for d in despesas]
        id_despesa  = _pedir_id_valido("ID da despesa: ", ids_validos)
        confirmar   = _pedir_confirmacao("Confirmar remocao")
        if confirmar:
            remover_despesa(id_despesa)
        else:
            print(_CINZA + "Cancelado." + _RESET)
    except Exception as erro:
        print(_VERMELHO_B + "[HTTP 500] Erro inesperado: " + str(erro) + _RESET)
    _aguardar_enter()

def menu_despesas():
    while True:
        _mostrar_cabecalho("DESPESAS")
        print(_MAGENTA + _BOLD + "[1]" + _RESET + " " + _BRANCO + "Criar despesa"   + _RESET)
        print(_MAGENTA + _BOLD + "[2]" + _RESET + " " + _BRANCO + "Ler despesas"    + _RESET)
        print(_MAGENTA + _BOLD + "[3]" + _RESET + " " + _BRANCO + "Ler despesa"     + _RESET)
        print(_MAGENTA + _BOLD + "[4]" + _RESET + " " + _BRANCO + "Deletar despesa" + _RESET)
        print(_MAGENTA + _BOLD + "[0]" + _RESET + " " + _BRANCO + "Voltar"          + _RESET)
        print(_CINZA + "-" * 40 + _RESET)
        opcao = input(_MAGENTA + _BOLD + "> " + _RESET).strip()

        if   opcao == "1": _criar_despesa()
        elif opcao == "2": _ler_despesas()
        elif opcao == "3": _ler_despesa()
        elif opcao == "4": _deletar_despesa()
        elif opcao == "0": break
        else:
            print(_VERMELHO_B + "[HTTP 400] Opcao invalida." + _RESET)
            _aguardar_enter()

def menu_principal():
    while True:
        _mostrar_cabecalho("GESTOR DE GINASIO")
        print(_MAGENTA + _BOLD + "[1]" + _RESET + " " + _BRANCO + "Clientes"             + _RESET)
        print(_MAGENTA + _BOLD + "[2]" + _RESET + " " + _BRANCO + "Planos de treino"     + _RESET)
        print(_MAGENTA + _BOLD + "[3]" + _RESET + " " + _BRANCO + "Despesas"             + _RESET)
        print(_MAGENTA + _BOLD + "[4]" + _RESET + " " + _BRANCO + "Relatorio financeiro" + _RESET)
        print(_MAGENTA + _BOLD + "[5]" + _RESET + " " + _BRANCO + "Estatisticas"         + _RESET)
        print(_MAGENTA + _BOLD + "[6]" + _RESET + " " + _BRANCO + "Simular mes"          + _RESET)
        print(_MAGENTA + _BOLD + "[0]" + _RESET + " " + _BRANCO + "Sair"                 + _RESET)
        print(_CINZA + "-" * 40 + _RESET)
        opcao = input(_MAGENTA + _BOLD + "> " + _RESET).strip()

        if   opcao == "1": menu_clientes()
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
            print(_VERDE + "Ate logo." + _RESET)
            break
        else:
            print(_VERMELHO_B + "[HTTP 400] Opcao invalida." + _RESET)
            _aguardar_enter()
