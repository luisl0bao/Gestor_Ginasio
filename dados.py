clientes = {}   # { id: { "nome": ..., "data_nascimento": ..., "telefone": ..., "id_plano": ..., "data_inicio": ... } }
planos = {}     # { id: (nome, num_treinos, preco_por_treino) }
despesas = []   # [ (id, descricao, valor) ]

proximo_id_plano = 1
proximo_id_cliente = 1
proximo_id_despesa = 1
proximo_mes = 1
saldo_acumulado = 0.0
