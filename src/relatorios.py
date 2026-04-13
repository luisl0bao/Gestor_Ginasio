from src import dados
from dados import clientes, planos, despesas
from src.planos import obter_plano
from src.CoresANSII import VERDE, VERDE_B, VERMELHO, VERMELHO_B, AMARELO, BRANCO, CINZA, BOLD, RESET, MAGENTA

def _arredondar(valor):
    return round(valor, 2)

def _calcular_receita_mensal():
    total = 0.0
    for cliente in clientes.values():
        plano = obter_plano(cliente["id_plano"])
        if plano:
            num_treinos, preco_treino = plano[1], plano[2]
            total = total + (num_treinos * preco_treino)
    return _arredondar(total)

def _calcular_total_despesas():
    total = 0.0
    for despesa in despesas:
        total = total + despesa[2]
    return _arredondar(total)

def _calcular_saldo():
    return _arredondar(_calcular_receita_mensal() - _calcular_total_despesas())

def mostrar_relatorio_financeiro():
    receita = _calcular_receita_mensal()
    total_desp = _calcular_total_despesas()
    saldo = _calcular_saldo()
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
        print(CINZA + "Saldo final: " + RESET + VERDE_B + str(saldo) + " EUR" + RESET)
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
    if planos and clientes:
        nome_plano_popular = ""
        max_clientes = 0
        for id_plano, dados_plano in planos.items():
            total = sum(1 for c in clientes.values() if c["id_plano"] == id_plano)
            if total > max_clientes:
                max_clientes = total
                nome_plano_popular = dados_plano[0]
        print(CINZA + "Plano mais popular: " + RESET + MAGENTA + nome_plano_popular + RESET)
    receita = _calcular_receita_mensal()
    total_desp = _calcular_total_despesas()
    saldo = _calcular_saldo()
    print(CINZA + "Receita mensal: " + RESET + VERDE + str(receita) + " EUR" + RESET)
    print(CINZA + "Total despesas: " + RESET + VERMELHO + str(total_desp) + " EUR" + RESET)
    if saldo >= 0:
        print(CINZA + "Saldo final: " + RESET + VERDE_B + str(saldo) + " EUR" + RESET)
    else:
        print(CINZA + "Saldo final: " + RESET + VERMELHO_B + str(saldo) + " EUR" + RESET)
    print(CINZA + "-" * 40 + RESET)

def simular_mes():
    receita_simulada = 0.0
    print()
    print(VERDE + BOLD + "[ SIMULACAO MENSAL - MES " + str(dados.proximo_mes) + " ]" + RESET)
    print(CINZA + "-" * 40 + RESET)
    print(BRANCO + BOLD + "Entradas" + RESET)
    for cliente in clientes.values():
        plano = obter_plano(cliente["id_plano"])
        if plano:
            num_treinos, preco_treino = plano[1], plano[2]
            valor = _arredondar(num_treinos * preco_treino)
            receita_simulada = receita_simulada + valor
            print(CINZA + cliente["nome"] + " (" + plano[0] + "): " +
                  RESET + VERDE + "+" + str(valor) + " EUR" + RESET)
    receita_simulada = _arredondar(receita_simulada)
    print()
    print(BRANCO + BOLD + "Saidas" + RESET)
    total_gasto = 0.0
    for despesa in despesas:
        total_gasto = total_gasto + despesa[2]
        print(CINZA + despesa[1] + ": " + RESET + VERMELHO + "-" + str(despesa[2]) + " EUR" + RESET)
    total_gasto = _arredondar(total_gasto)
    resultado = _arredondar(receita_simulada - total_gasto)
    dados.saldo_acumulado = _arredondar(dados.saldo_acumulado + resultado)
    print()
    print(BRANCO + BOLD + "Resultado" + RESET)
    print(CINZA + "Receita: "  + RESET + VERDE + str(receita_simulada) + " EUR" + RESET)
    print(CINZA + "Despesas: " + RESET + VERMELHO + str(total_gasto) + " EUR" + RESET)
    if resultado >= 0:
        print(CINZA + "Resultado: "   + RESET + VERDE_B + str(resultado) + " EUR" + RESET)
    else:
        print(CINZA + "Resultado: "   + RESET + VERMELHO_B + str(resultado) + " EUR" + RESET)
    if dados.saldo_acumulado >= 0:
        print(CINZA + "Lucro total: " + RESET + VERDE_B + str(dados.saldo_acumulado) + " EUR" + RESET)
    else:
        print(CINZA + "Lucro total: " + RESET + VERMELHO_B + str(dados.saldo_acumulado) + " EUR" + RESET)
    print(CINZA + "-" * 40 + RESET)
    dados.proximo_mes = dados.proximo_mes + 1
