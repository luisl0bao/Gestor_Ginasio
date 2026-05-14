import os
import json

try:
    from src import dados
    from src.clientes import clientes
    from src.planos import obter_plano
    from src.utils import _pedir_decimal_positivo, _pedir_id_valido, _pedir_confirmacao, _pedir_data
except ImportError:
    import dados
    from clientes import clientes
    from planos import obter_plano
    from utils import _pedir_decimal_positivo, _pedir_id_valido, _pedir_confirmacao, _pedir_data

_PASTA = os.path.dirname(os.path.abspath(__file__))
_FICHEIRO_PAGAMENTOS = os.path.join(_PASTA, "pagamentos.json")


def guardar_pagamentos():
    """Guarda apenas os dados dos pagamentos e transações em pagamentos.json."""
    payload = {
        "pagamentos":           {str(k): dict(v) for k, v in dados.pagamentos.items()},
        "transacoes":           list(dados.transacoes),
        "proximo_id_pagamento": dados.proximo_id_pagamento,
        "proximo_id_transacao": dados.proximo_id_transacao,
    }
    with open(_FICHEIRO_PAGAMENTOS, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print("\033[92mPagamentos guardados em: " + _FICHEIRO_PAGAMENTOS + "\033[0m")


def carregar_pagamentos() -> bool:
    """Carrega os dados dos pagamentos de pagamentos.json. Devolve True se carregou."""
    if not os.path.exists(_FICHEIRO_PAGAMENTOS):
        return False
    with open(_FICHEIRO_PAGAMENTOS, "r", encoding="utf-8") as f:
        payload = json.load(f)
    dados.pagamentos.clear()
    for k, v in payload["pagamentos"].items():
        dados.pagamentos[int(k)] = v
    dados.transacoes.clear()
    dados.transacoes.extend(payload["transacoes"])
    dados.proximo_id_pagamento = payload["proximo_id_pagamento"]
    dados.proximo_id_transacao = payload["proximo_id_transacao"]
    return True

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
_CIANO      = "\033[36m"
_CIANO_B    = "\033[96m"


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
    carregar_pagamentos()
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
    guardar_pagamentos()
    return dados.pagamentos[novo_id]


def listar_pagamentos():
    carregar_pagamentos()
    return list(dados.pagamentos.values())

def buscar_pagamento(id_pagamento):
    carregar_pagamentos()
    return dados.pagamentos.get(id_pagamento)

def atualizar_pagamento(id_pagamento, valor=None, plano=None, dia_pagamento=None):
    carregar_pagamentos()
    pagamento = dados.pagamentos.get(id_pagamento)
    if not pagamento:
        return None
    if valor is not None:
        pagamento["valor"] = _arredondar(float(valor))
    if plano is not None:
        pagamento["plano"] = plano
    if dia_pagamento is not None:
        pagamento["dia_pagamento"] = dia_pagamento
    guardar_pagamentos()
    return pagamento

def apagar_pagamento(id_pagamento):
    carregar_pagamentos()
    if id_pagamento in dados.pagamentos:
        del dados.pagamentos[id_pagamento]
        guardar_pagamentos()
        return True
    return False


def gerar_pagamentos_fim_do_mes():
    """Gera automaticamente um pagamento para cada cliente com a data simulada."""
    carregar_pagamentos()
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

def _limpar_ecra():
    os.system("cls" if os.name == "nt" else "clear")

def _aguardar_enter():
    input(_CINZA + "Enter para continuar..." + _RESET)
    _limpar_ecra()


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
    carregar_pagamentos()
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
        elif t["tipo"] == "saida":
            sinal = _VERMELHO_B + "-" + _RESET
            cor   = _VERMELHO
            total_saida += t["valor"]
        elif t["tipo"] == "transferencia_entrada":
            sinal = _CIANO_B + "+" + _RESET
            cor   = _CIANO
            total_entrada += t["valor"]
        elif t["tipo"] == "transferencia_saida":
            sinal = _CIANO_B + "-" + _RESET
            cor   = _CIANO
            total_saida += t["valor"]
        else:
            sinal = " "
            cor   = _BRANCO
        print(_AMARELO + f"ID: {t['id']:<4}" + _RESET +
              _CINZA   + "  Data: "  + _RESET + _BRANCO + t["data"] + _RESET +
              "  " + sinal + "  " + cor + f"{t['valor']:.2f} EUR" + _RESET)
        print(_CINZA + "     " + t["descricao"] + _RESET)
        print(_CINZA + "-" * 60 + _RESET)
    print(_VERDE_B    + f"Entradas: +{_arredondar(total_entrada):.2f} EUR" + _RESET)
    print(_VERMELHO_B + f"Saidas:   -{_arredondar(total_saida):.2f} EUR"   + _RESET)
    saldo = _arredondar(total_entrada - total_saida)
    cor_s = _VERDE_B if saldo >= 0 else _VERMELHO_B
    print(cor_s + _BOLD + f"Saldo:    {saldo:+.2f} EUR" + _RESET)


def _adicionar_pagamento():
    """Adiciona um pagamento manualmente, tal como as despesas."""
    carregar_pagamentos()
    if not clientes:
        print(_VERMELHO_B + "404 Nao existe nenhum cliente registado." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    print(_VERDE + _BOLD + "[ NOVO PAGAMENTO ]" + _RESET)
    print()
    print(_CINZA + "Clientes disponiveis:" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    for id_c, c in clientes.items():
        print(_AMARELO + f"  [{id_c}]" + _RESET + " " + _BRANCO + c["nome"] + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    print()
    id_cliente = _pedir_id_valido("ID do cliente: ", list(clientes.keys()))
    nome_cliente = _nome_cliente(id_cliente)
    id_plano_cliente = clientes[id_cliente].get("id_plano")
    plano_info, codigo = obter_plano(id_plano_cliente)
    if codigo == 200 and plano_info:
        nome_plano_sugerido = plano_info[0]
        valor_sugerido      = round(plano_info[1] * plano_info[2], 2)
        print(_CINZA + f"Plano atual: " + _RESET + _MAGENTA + nome_plano_sugerido + _RESET +
              _CINZA + f"  Valor mensal: " + _RESET + _VERDE + f"{valor_sugerido:.2f} EUR" + _RESET)
        print(_CINZA + "(Enter para usar o plano e valor atuais)" + _RESET)
        plano_input = input(_AMARELO + "Nome do plano: " + _RESET).strip()
        plano       = plano_input if plano_input else nome_plano_sugerido
        valor_input = input(_AMARELO + "Valor (EUR): "   + _RESET).strip()
        valor       = float(valor_input) if valor_input else valor_sugerido
    else:
        plano = input(_AMARELO + "Nome do plano: " + _RESET).strip() or "Sem plano"
        valor = _pedir_decimal_positivo("Valor (EUR): ")
    data_input    = input(_AMARELO + "Data (DD/MM/AAAA, Enter = hoje): " + _RESET).strip()
    dia_pagamento = data_input if data_input else None
    resultado = criar_pagamento(id_cliente, valor, plano, dia_pagamento)
    if resultado:
        print(_VERDE_B + f"201 Sucesso, pagamento de {nome_cliente} adicionado." + _RESET)
    else:
        print(_VERMELHO_B + "400 Erro ao adicionar pagamento." + _RESET)
    _aguardar_enter()


def _remover_pagamento():
    """Remove um pagamento com confirmacao, tal como as despesas."""
    if not listar_pagamentos():
        print(_AMARELO + "Nenhum pagamento para remover." + _RESET)
        _aguardar_enter()
        return
    _limpar_ecra()
    _mostrar_pagamentos()
    print()
    ids_validos = list(dados.pagamentos.keys())
    id_pag      = _pedir_id_valido("ID do pagamento a remover: ", ids_validos)
    confirmar   = _pedir_confirmacao("Confirmar remocao")
    if confirmar:
        if apagar_pagamento(id_pag):
            print(_VERDE_B + f"200 Sucesso, pagamento {id_pag} removido." + _RESET)
        else:
            print(_VERMELHO_B + "404 Pagamento nao encontrado." + _RESET)
    else:
        print(_CINZA + "Cancelado." + _RESET)
    _aguardar_enter()


def _adicionar_transferencia():
    """Regista uma transferencia (entrada ou saida) no historico de transacoes."""
    _limpar_ecra()
    print(_VERDE + _BOLD + "[ NOVA TRANSFERENCIA ]" + _RESET)
    print()
    descricao = input(_AMARELO + "Descricao: " + _RESET).strip()
    if not descricao:
        print(_VERMELHO_B + "400 Descricao obrigatoria." + _RESET)
        _aguardar_enter()
        return
    valor = _pedir_decimal_positivo("Valor (EUR): ")
    print(_CIANO + "[1]" + _RESET + " Entrada  " + _CIANO + "[2]" + _RESET + " Saida")
    tipo_input = input(_AMARELO + "Tipo: " + _RESET).strip()
    if tipo_input == "1":
        tipo = "transferencia_entrada"
        label = "entrada"
    elif tipo_input == "2":
        tipo = "transferencia_saida"
        label = "saida"
    else:
        print(_VERMELHO_B + "400 Opcao invalida. Usa 1 ou 2." + _RESET)
        _aguardar_enter()
        return
    data_input = input(_AMARELO + "Data (DD/MM/AAAA, Enter = hoje): " + _RESET).strip()
    data       = data_input if data_input else None
    _registar_transacao(
        descricao=f"Transferencia: {descricao}",
        valor=valor,
        tipo=tipo,
        data=data
    )
    guardar_pagamentos()
    print(_CIANO_B + f"201 Sucesso, transferencia de {valor:.2f} EUR ({label}) registada." + _RESET)
    _aguardar_enter()


def menu_pagamentos():
    while True:
        _limpar_ecra()
        print(_VERDE + _BOLD + "[ PAGAMENTOS ]" + _RESET)
        print(_CINZA + "-" * 40 + _RESET)
        print(_MAGENTA + _BOLD + "[1]" + _RESET + " " + _BRANCO + "Ver pagamentos de clientes"    + _RESET)
        print(_MAGENTA + _BOLD + "[2]" + _RESET + " " + _BRANCO + "Historico de transacoes"       + _RESET)
        print(_MAGENTA + _BOLD + "[3]" + _RESET + " " + _BRANCO + "Adicionar pagamento"           + _RESET)
        print(_MAGENTA + _BOLD + "[4]" + _RESET + " " + _BRANCO + "Remover pagamento"             + _RESET)
        print(_MAGENTA + _BOLD + "[5]" + _RESET + " " + _BRANCO + "Adicionar transferencia"       + _RESET)
        print(_MAGENTA + _BOLD + "[6]" + _RESET + " " + _BRANCO + "Atualizar pagamento"           + _RESET)
        print(_MAGENTA + _BOLD + "[7]" + _RESET + " " + _BRANCO + "Resumo financeiro"             + _RESET)
        print(_MAGENTA + _BOLD + "[8]" + _RESET + " " + _BRANCO + "Guardar pagamentos"            + _RESET)
        print(_MAGENTA + _BOLD + "[0]" + _RESET + " " + _BRANCO + "Voltar"                        + _RESET)
        print(_CINZA + "-" * 40 + _RESET)

        op = input(_MAGENTA + _BOLD + "> " + _RESET).strip()

        if op == "1":
            _limpar_ecra()
            _mostrar_pagamentos()
            _aguardar_enter()

        elif op == "2":
            _limpar_ecra()
            _mostrar_transacoes()
            _aguardar_enter()

        elif op == "3":
            _adicionar_pagamento()

        elif op == "4":
            _remover_pagamento()

        elif op == "5":
            _adicionar_transferencia()

        elif op == "6":
            _limpar_ecra()
            if not listar_pagamentos():
                print(_AMARELO + "Nenhum pagamento para atualizar." + _RESET)
                _aguardar_enter()
                continue
            _mostrar_pagamentos()
            print()
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
                    print(_VERDE_B + "200 Pagamento atualizado." + _RESET)
                else:
                    print(_VERMELHO_B + "404 Pagamento nao encontrado." + _RESET)
            except ValueError:
                print(_VERMELHO_B + "400 Valor invalido." + _RESET)
            _aguardar_enter()

        elif op == "7":
            _limpar_ecra()
            carregar_pagamentos()
            total_pag  = sum(p["valor"] for p in listar_pagamentos())
            transacoes = getattr(dados, "transacoes", [])
            total_ent  = sum(t["valor"] for t in transacoes if t["tipo"] in ("entrada", "transferencia_entrada"))
            total_sai  = sum(t["valor"] for t in transacoes if t["tipo"] in ("saida",   "transferencia_saida"))
            saldo_liq  = _arredondar(total_ent - total_sai)
            print()
            print(_VERDE + _BOLD + "[ RESUMO FINANCEIRO ]" + _RESET)
            print(_CINZA + "-" * 44 + _RESET)
            print(_CINZA + "Total pagamentos registados: " + _RESET + _VERDE_B    + f"{_arredondar(total_pag):.2f} EUR" + _RESET)
            print(_CINZA + "Total entradas:              " + _RESET + _VERDE_B    + f"{_arredondar(total_ent):.2f} EUR" + _RESET)
            print(_CINZA + "Total saidas:                " + _RESET + _VERMELHO_B + f"{_arredondar(total_sai):.2f} EUR" + _RESET)
            cor = _VERDE_B if saldo_liq >= 0 else _VERMELHO_B
            print(_CINZA + "Saldo liquido:               " + _RESET + cor + _BOLD + f"{saldo_liq:+.2f} EUR" + _RESET)
            print(_CINZA + "-" * 44 + _RESET)
            _aguardar_enter()

        elif op == "0":
            break

        elif op == "8":
            guardar_pagamentos()
            _aguardar_enter()

        else:
            print(_VERMELHO_B + "400 Opcao invalida." + _RESET)
            _aguardar_enter()
