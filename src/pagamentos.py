try:
    from src import dados
    from src.clientes import clientes
    from src.planos import obter_plano
except ImportError:
    import dados
    from clientes import clientes
    from planos import obter_plano

# garantir estrutura
if not hasattr(dados, "pagamentos"):
    dados.pagamentos = {}
if not hasattr(dados, "proximo_id_pagamento"):
    dados.proximo_id_pagamento = 1
if not hasattr(dados, "transacoes"):
    dados.transacoes = []
if not hasattr(dados, "proximo_id_transacao"):
    dados.proximo_id_transacao = 1

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

def _data_atual():
    return dados.data_simulada_str()

def _registar_transacao(descricao, valor, tipo="entrada", data=None):
    if data is None:
        data = _data_atual()
    dados.transacoes.append({
        "id":        dados.proximo_id_transacao,
        "tipo":      tipo,
        "descricao": descricao,
        "valor":     _arredondar(valor),
        "data":      data
    })
    dados.proximo_id_transacao += 1

def _nome_cliente(id_cliente):
    c = clientes.get(id_cliente)
    return c["nome"] if c else f"Cliente #{id_cliente}"


def criar_pagamento(id_cliente, valor, plano, dia_pagamento=None):
    if id_cliente not in clientes:
        return None
    if dia_pagamento is None:
        dia_pagamento = _data_atual()
    novo_id = dados.proximo_id_pagamento
    nome    = _nome_cliente(id_cliente)
    dados.pagamentos[novo_id] = {
        "id":            novo_id,
        "id_cliente":    id_cliente,
        "nome_cliente":  nome,
        "valor":         _arredondar(float(valor)),
        "dia_pagamento": dia_pagamento,
        "plano":         plano
    }
    _registar_transacao(
        descricao=f"Pagamento {nome} - {plano}",
        valor=valor,
        tipo="entrada",
        data=dia_pagamento
    )
    dados.proximo_id_pagamento += 1
    return dados.pagamentos[novo_id]


def listar_pagamentos():
    return list(dados.pagamentos.values())

def buscar_pagamento(id_pagamento):
    return dados.pagamentos.get(id_pagamento)

def atualizar_pagamento(id_pagamento, valor=None, plano=None, dia_pagamento=None):
    pagamento = dados.pagamentos.get(id_pagamento)
    if not pagamento:
        return None
    if valor is not None:
        pagamento["valor"] = _arredondar(float(valor))
    if plano is not None:
        pagamento["plano"] = plano
    if dia_pagamento is not None:
        pagamento["dia_pagamento"] = dia_pagamento
    return pagamento

def apagar_pagamento(id_pagamento):
    if id_pagamento in dados.pagamentos:
        del dados.pagamentos[id_pagamento]
        return True
    return False


def gerar_pagamentos_fim_do_mes():
    """Gera automaticamente um pagamento para cada cliente com a data simulada."""
    for id_cliente, cliente in clientes.items():
        id_plano           = cliente.get("id_plano")
        plano_info, codigo = obter_plano(id_plano)
        if codigo != 200 or not plano_info:
            print(f"Erro no plano do cliente {id_cliente}")
            continue
        nome_plano   = plano_info[0]
        num_treinos  = plano_info[1]
        preco_treino = plano_info[2]
        total_mensal = round(num_treinos * preco_treino, 2)
        criar_pagamento(
            id_cliente=id_cliente,
            valor=total_mensal,
            plano=nome_plano
        )


# ──────────────────────────────────────────────────────────────────
#  MENU PAGAMENTOS
# ──────────────────────────────────────────────────────────────────

def _mostrar_pagamentos():
    pagamentos = listar_pagamentos()
    if not pagamentos:
        print(_AMARELO + "Nenhum pagamento registado." + _RESET)
        return
    total = 0.0
    print()
    print(_VERDE + _BOLD + "[ PAGAMENTOS DE CLIENTES ]" + _RESET)
    print(_CINZA + "-" * 55 + _RESET)
    for p in pagamentos:
        total += p["valor"]
        print(_AMARELO + f"ID: {p['id']:<4}" + _RESET +
              _CINZA   + "  Data: "  + _RESET + _BRANCO  + p["dia_pagamento"] + _RESET +
              _CINZA   + "  Nome: "  + _RESET + _BRANCO  + p["nome_cliente"]  + _RESET)
        print(_CINZA   + "     Plano: " + _RESET + _MAGENTA + p["plano"] + _RESET +
              _CINZA   + "  Valor: " + _RESET + _VERDE   + f"{p['valor']:.2f} EUR" + _RESET)
        print(_CINZA + "-" * 55 + _RESET)
    print(_VERDE_B + _BOLD + f"Total recebido: {_arredondar(total):.2f} EUR" + _RESET)


def _mostrar_transacoes():
    transacoes = getattr(dados, "transacoes", [])
    if not transacoes:
        print(_AMARELO + "Nenhuma transacao registada." + _RESET)
        return
    total_entrada = 0.0
    total_saida   = 0.0
    print()
    print(_VERDE + _BOLD + "[ HISTORICO DE TRANSACOES ]" + _RESET)
    print(_CINZA + "-" * 60 + _RESET)
    for t in transacoes:
        if t["tipo"] == "entrada":
            sinal = _VERDE_B + "+" + _RESET
            cor   = _VERDE
            total_entrada += t["valor"]
        else:
            sinal = _VERMELHO_B + "-" + _RESET
            cor   = _VERMELHO
            total_saida += t["valor"]
        print(_AMARELO + f"ID: {t['id']:<4}" + _RESET +
              _CINZA   + "  Data: "  + _RESET + _BRANCO + t["data"] + _RESET +
              "  " + sinal + "  " + cor + f"{t['valor']:.2f} EUR" + _RESET)
        print(_CINZA + "     " + t["descricao"] + _RESET)
        print(_CINZA + "-" * 60 + _RESET)
    print(_VERDE_B   + f"Entradas: +{_arredondar(total_entrada):.2f} EUR" + _RESET)
    print(_VERMELHO_B + f"Saidas:   -{_arredondar(total_saida):.2f} EUR"  + _RESET)
    saldo = _arredondar(total_entrada - total_saida)
    cor_s = _VERDE_B if saldo >= 0 else _VERMELHO_B
    print(cor_s + _BOLD + f"Saldo:    {saldo:+.2f} EUR" + _RESET)


def menu_pagamentos():
    while True:
        print()
        print(_VERDE + _BOLD + "[ PAGAMENTOS ]" + _RESET)
        print(_CINZA + "-" * 40 + _RESET)
        print(_MAGENTA + _BOLD + "[1]" + _RESET + " " + _BRANCO + "Ver pagamentos de clientes"    + _RESET)
        print(_MAGENTA + _BOLD + "[2]" + _RESET + " " + _BRANCO + "Historico de todas transacoes" + _RESET)
        print(_MAGENTA + _BOLD + "[3]" + _RESET + " " + _BRANCO + "Atualizar pagamento"           + _RESET)
        print(_MAGENTA + _BOLD + "[4]" + _RESET + " " + _BRANCO + "Apagar pagamento"              + _RESET)
        print(_MAGENTA + _BOLD + "[5]" + _RESET + " " + _BRANCO + "Resumo financeiro"             + _RESET)
        print(_MAGENTA + _BOLD + "[0]" + _RESET + " " + _BRANCO + "Voltar"                        + _RESET)
        print(_CINZA + "-" * 40 + _RESET)

        op = input(_MAGENTA + _BOLD + "> " + _RESET).strip()

        if op == "1":
            _mostrar_pagamentos()

        elif op == "2":
            _mostrar_transacoes()

        elif op == "3":
            if not listar_pagamentos():
                print(_AMARELO + "Nenhum pagamento para atualizar." + _RESET)
                continue
            _mostrar_pagamentos()
            try:
                id_pag    = int(input(_AMARELO + "ID pagamento: " + _RESET))
                novo_val  = input(_AMARELO + "Novo valor (Enter para manter): " + _RESET).strip()
                nova_data = input(_AMARELO + "Nova data DD/MM/AAAA (Enter para manter): " + _RESET).strip()
                kwargs = {}
                if novo_val:
                    kwargs["valor"] = float(novo_val)
                if nova_data:
                    kwargs["dia_pagamento"] = nova_data
                resultado = atualizar_pagamento(id_pag, **kwargs)
                if resultado:
                    print(_VERDE_B + "Pagamento atualizado." + _RESET)
                else:
                    print(_VERMELHO_B + "Pagamento nao encontrado." + _RESET)
            except ValueError:
                print(_VERMELHO_B + "Valor invalido." + _RESET)

        elif op == "4":
            if not listar_pagamentos():
                print(_AMARELO + "Nenhum pagamento para apagar." + _RESET)
                continue
            _mostrar_pagamentos()
            try:
                id_pag = int(input(_AMARELO + "ID pagamento a remover: " + _RESET))
                if apagar_pagamento(id_pag):
                    print(_VERDE_B + "Pagamento removido." + _RESET)
                else:
                    print(_VERMELHO_B + "Pagamento nao encontrado." + _RESET)
            except ValueError:
                print(_VERMELHO_B + "ID invalido." + _RESET)

        elif op == "5":
            total_pag  = sum(p["valor"] for p in listar_pagamentos())
            transacoes = getattr(dados, "transacoes", [])
            total_ent  = sum(t["valor"] for t in transacoes if t["tipo"] == "entrada")
            total_sai  = sum(t["valor"] for t in transacoes if t["tipo"] == "saida")
            saldo_liq  = _arredondar(total_ent - total_sai)
            print()
            print(_VERDE + _BOLD + "[ RESUMO FINANCEIRO ]" + _RESET)
            print(_CINZA + "-" * 40 + _RESET)
            print(_CINZA + "Total pagamentos recebidos: " + _RESET + _VERDE_B    + f"{_arredondar(total_pag):.2f} EUR" + _RESET)
            print(_CINZA + "Total entradas (log):       " + _RESET + _VERDE_B    + f"{_arredondar(total_ent):.2f} EUR" + _RESET)
            print(_CINZA + "Total saidas (despesas):    " + _RESET + _VERMELHO_B + f"{_arredondar(total_sai):.2f} EUR" + _RESET)
            cor = _VERDE_B if saldo_liq >= 0 else _VERMELHO_B
            print(_CINZA + "Saldo liquido:              " + _RESET + cor + _BOLD + f"{saldo_liq:+.2f} EUR" + _RESET)
            print(_CINZA + "-" * 40 + _RESET)

        elif op == "0":
            break

        else:
            print(_VERMELHO_B + "400 Opcao invalida." + _RESET)
