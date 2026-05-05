from datetime import date, timedelta
import calendar

clientes = {}
planos = {}
despesas = []
pagamentos = {}
transacoes = []   # log unificado: {"id", "tipo", "descricao", "valor", "data"}

proximo_id_pagamento = 1
proximo_id_plano = 1
proximo_id_cliente = 1
proximo_id_despesa = 1
proximo_id_transacao = 1
proximo_mes = 1
saldo_acumulado = 0.0

# Data simulada — começa em 01/01/2025 e avança a cada simulação de mês
data_simulada = date(2025, 1, 1)

def avancar_mes():
    """Avança data_simulada para o primeiro dia do mês seguinte."""
    global data_simulada
    # Usa o número real de dias do mês actual
    dias_no_mes = calendar.monthrange(data_simulada.year, data_simulada.month)[1]
    data_simulada = data_simulada + timedelta(days=dias_no_mes)

def data_simulada_str():
    return data_simulada.strftime("%d/%m/%Y")
