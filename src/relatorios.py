try:
    from src import dados
    from src.dados import clientes, planos, despesas
    from src.planos import obter_plano
except ImportError:
    import dados
    from dados import clientes, planos, despesas
    from planos import obter_plano

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

def _arredondar(valor):
    return round(valor, 2)

def _calcular_receita_mensal():
    total = 0.0
    for cliente in clientes.values():
        plano, codigo = obter_plano(cliente["id_plano"])
        if codigo == 200:
            total = total + (plano[1] * plano[2])
    return _arredondar(total)

def _calcular_total_despesas():
    total = 0.0
    for despesa in despesas:
        total = total + despesa[2]
    return _arredondar(total)

def _calcular_saldo():
    return _arredondar(_calcular_receita_mensal() - _calcular_total_despesas())

def mostrar_relatorio_financeiro():
    try:
        receita    = _calcular_receita_mensal()
        total_desp = _calcular_total_despesas()
        saldo      = _calcular_saldo()
        print()
        print(_VERDE + _BOLD + "[ RELATORIO FINANCEIRO ]" + _RESET)
        print(_CINZA + "-" * 40 + _RESET)
        print(_BRANCO + _BOLD + "Receitas" + _RESET)
        print(_CINZA + "Receita mensal: " + _RESET + _VERDE + str(receita) + " EUR" + _RESET)
        print()
        print(_BRANCO + _BOLD + "Despesas" + _RESET)
        for despesa in despesas:
            print(_CINZA + despesa[1] + ": " + _RESET + _VERMELHO + str(despesa[2]) + " EUR" + _RESET)
        print(_CINZA + "Total: " + _RESET + _VERMELHO_B + str(total_desp) + " EUR" + _RESET)
        print()
        print(_BRANCO + _BOLD + "Saldo" + _RESET)
        if saldo >= 0:
            print(_CINZA + "Saldo final: " + _RESET + _VERDE_B + str(saldo) + " EUR" + _RESET)
        else:
            print(_CINZA + "Saldo final: " + _RESET + _VERMELHO_B + str(saldo) + " EUR" + _RESET)
        print(_CINZA + "-" * 40 + _RESET)
        return {"receita": receita, "despesas": total_desp, "saldo": saldo}, 200
    except Exception as erro:
        print(_VERMELHO_B + "[HTTP 500] Erro interno ao gerar relatorio: " + str(erro) + _RESET)
        return None, 500

def mostrar_estatisticas():
    try:
        print()
        print(_VERDE + _BOLD + "[ ESTATISTICAS ]" + _RESET)
        print(_CINZA + "-" * 40 + _RESET)
        print(_CINZA + "Total clientes: " + _RESET + _AMARELO + str(len(clientes)) + _RESET)
        print(_CINZA + "Total planos: "   + _RESET + _AMARELO + str(len(planos))   + _RESET)
        print(_CINZA + "Total despesas: " + _RESET + _AMARELO + str(len(despesas)) + _RESET)
        nome_plano_popular = ""
        if planos and clientes:
            max_clientes = 0
            for id_plano, dados_plano in planos.items():
                total = sum(1 for c in clientes.values() if c["id_plano"] == id_plano)
                if total > max_clientes:
                    max_clientes = total
                    nome_plano_popular = dados_plano[0]
            if nome_plano_popular:
                print(_CINZA + "Plano mais popular: " + _RESET + _MAGENTA + nome_plano_popular + _RESET)
        receita    = _calcular_receita_mensal()
        total_desp = _calcular_total_despesas()
        saldo      = _calcular_saldo()
        print(_CINZA + "Receita mensal: " + _RESET + _VERDE    + str(receita)    + " EUR" + _RESET)
        print(_CINZA + "Total despesas: " + _RESET + _VERMELHO + str(total_desp) + " EUR" + _RESET)
        if saldo >= 0:
            print(_CINZA + "Saldo final: " + _RESET + _VERDE_B    + str(saldo) + " EUR" + _RESET)
        else:
            print(_CINZA + "Saldo final: " + _RESET + _VERMELHO_B + str(saldo) + " EUR" + _RESET)
        print(_CINZA + "-" * 40 + _RESET)
        return {"clientes": len(clientes), "planos": len(planos), "despesas": len(despesas),
                "receita": receita, "saldo": saldo, "plano_popular": nome_plano_popular}, 200
    except Exception as erro:
        print(_VERMELHO_B + "[HTTP 500] Erro interno ao gerar estatisticas: " + str(erro) + _RESET)
        return None, 500

def simular_mes():
    try:
        receita_simulada = 0.0
        print()
        print(_VERDE + _BOLD + "[ SIMULACAO MENSAL - MES " + str(dados.proximo_mes) + " ]" + _RESET)
        print(_CINZA + "-" * 40 + _RESET)
        print(_BRANCO + _BOLD + "Entradas" + _RESET)
        for cliente in clientes.values():
            plano, codigo = obter_plano(cliente["id_plano"])
            if codigo == 200:
                valor = _arredondar(plano[1] * plano[2])
                receita_simulada = receita_simulada + valor
                print(_CINZA + cliente["nome"] + " (" + plano[0] + "): " +
                      _RESET + _VERDE + "+" + str(valor) + " EUR" + _RESET)
        receita_simulada = _arredondar(receita_simulada)
        print()
        print(_BRANCO + _BOLD + "Saidas" + _RESET)
        total_gasto = 0.0
        for despesa in despesas:
            total_gasto = total_gasto + despesa[2]
            print(_CINZA + despesa[1] + ": " + _RESET + _VERMELHO + "-" + str(despesa[2]) + " EUR" + _RESET)
        total_gasto = _arredondar(total_gasto)
        resultado = _arredondar(receita_simulada - total_gasto)
        dados.saldo_acumulado = _arredondar(dados.saldo_acumulado + resultado)
        print()
        print(_BRANCO + _BOLD + "Resultado" + _RESET)
        print(_CINZA + "Receita: "  + _RESET + _VERDE    + str(receita_simulada) + " EUR" + _RESET)
        print(_CINZA + "Despesas: " + _RESET + _VERMELHO + str(total_gasto)      + " EUR" + _RESET)
        if resultado >= 0:
            print(_CINZA + "Resultado: "   + _RESET + _VERDE_B    + str(resultado)             + " EUR" + _RESET)
        else:
            print(_CINZA + "Resultado: "   + _RESET + _VERMELHO_B + str(resultado)             + " EUR" + _RESET)
        if dados.saldo_acumulado >= 0:
            print(_CINZA + "Lucro total: " + _RESET + _VERDE_B    + str(dados.saldo_acumulado) + " EUR" + _RESET)
        else:
            print(_CINZA + "Lucro total: " + _RESET + _VERMELHO_B + str(dados.saldo_acumulado) + " EUR" + _RESET)
        print(_CINZA + "-" * 40 + _RESET)
        dados.proximo_mes = dados.proximo_mes + 1
        return {"mes": dados.proximo_mes - 1, "receita": receita_simulada,
                "despesas": total_gasto, "resultado": resultado,
                "saldo_acumulado": dados.saldo_acumulado}, 200
    except Exception as erro:
        print(_VERMELHO_B + "[HTTP 500] Erro interno ao simular mes: " + str(erro) + _RESET)
        return None, 500
