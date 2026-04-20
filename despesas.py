try:
    from src import dados
    from src.dados import despesas
except ImportError:
    import dados
    from dados import despesas

# Cores ANSI inline
_RESET      = "\033[0m"
_BOLD       = "\033[1m"
_BRANCO     = "\033[97m"
_CINZA      = "\033[90m"
_VERDE      = "\033[32m"
_VERDE_B    = "\033[92m"
_AMARELO    = "\033[33m"
_VERMELHO   = "\033[31m"
_VERMELHO_B = "\033[91m"

# ---------- Helpers ----------

def _arredondar(valor):
    return round(valor, 2)

# ---------- CRUD ----------

def adicionar_despesa(descricao, valor):
    """[HTTP 201/400] Regista uma nova despesa."""
    try:
        if not descricao:
            raise ValueError("[HTTP 400] Descricao invalida.")
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("[HTTP 400] Valor invalido.")
        despesas.append((dados.proximo_id_despesa, descricao, _arredondar(valor)))
        dados.proximo_id_despesa = dados.proximo_id_despesa + 1
        print(_VERDE_B + "[HTTP 201] Despesa registada." + _RESET)
    except ValueError as erro:
        print(_VERMELHO_B + "Erro: " + str(erro) + _RESET)

def obter_despesa(id_despesa):
    """[HTTP 200/404] Devolve a despesa ou None se nao existir."""
    for despesa in despesas:
        if despesa[0] == id_despesa:
            return despesa
    return None

def remover_despesa(id_despesa):
    """[HTTP 200/404] Remove uma despesa."""
    for despesa in despesas:
        if despesa[0] == id_despesa:
            despesas.remove(despesa)
            print(_VERDE_B + "[HTTP 200] Despesa removida." + _RESET)
            return
    print(_VERMELHO_B + "[HTTP 404] Despesa nao encontrada." + _RESET)

# ---------- Listagem ----------

def mostrar_despesas():
    """[HTTP 200/204] Lista todas as despesas."""
    if len(despesas) == 0:
        print(_AMARELO + "[HTTP 204] Nenhuma despesa registada." + _RESET)
        return
    print()
    print(_VERDE + _BOLD + "[ DESPESAS ]" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    for despesa in despesas:
        print(_AMARELO + "ID: "        + _RESET + _BRANCO   + str(despesa[0]) + _RESET)
        print(_CINZA   + "Descricao: " + _RESET + _BRANCO   + despesa[1]      + _RESET)
        print(_CINZA   + "Valor: "     + _RESET + _VERMELHO + str(despesa[2]) + " EUR" + _RESET)
        print(_CINZA + "-" * 40 + _RESET)

def mostrar_despesa(id_despesa):
    """[HTTP 200/404] Mostra detalhes de uma despesa."""
    despesa = obter_despesa(id_despesa)
    if despesa is None:
        print(_VERMELHO_B + "[HTTP 404] Despesa nao encontrada." + _RESET)
        return
    print()
    print(_VERDE + _BOLD + "[ DESPESA ]" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    print(_AMARELO + "ID: "        + _RESET + _BRANCO   + str(despesa[0]) + _RESET)
    print(_CINZA   + "Descricao: " + _RESET + _BRANCO   + despesa[1]      + _RESET)
    print(_CINZA   + "Valor: "     + _RESET + _VERMELHO + str(despesa[2]) + " EUR" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
