try:
    from src import dados
    from src.dados import clientes
    from src.planos import obter_plano
except ImportError:
    import dados
    from dados import clientes
    from planos import obter_plano

# Cores ANSI inline
_RESET      = "\033[0m"
_BOLD       = "\033[1m"
_BRANCO     = "\033[97m"
_CINZA      = "\033[90m"
_VERDE      = "\033[32m"
_VERDE_B    = "\033[92m"
_AMARELO    = "\033[33m"
_VERMELHO_B = "\033[91m"
_MAGENTA    = "\033[35m"

# ---------- Helpers ----------

def _arredondar(valor):
    return round(valor, 2)

def _ids_clientes():
    return list(clientes.keys())

# ---------- CRUD ----------

def adicionar_cliente(nome, data_nascimento, telefone, id_plano, data_inicio):
    """[HTTP 201/400/409] Adiciona um novo cliente."""
    try:
        if not nome:
            raise ValueError("[HTTP 400] Nome invalido.")
        for id_c in clientes:
            if clientes[id_c]["nome"] == nome:
                raise ValueError("[HTTP 409] Ja existe um cliente com esse nome.")
        if obter_plano(id_plano) is None:
            raise ValueError("[HTTP 404] Plano nao existe.")
        clientes[dados.proximo_id_cliente] = {
            "nome": nome,
            "data_nascimento": data_nascimento,
            "telefone": telefone,
            "id_plano": id_plano,
            "data_inicio": data_inicio
        }
        dados.proximo_id_cliente = dados.proximo_id_cliente + 1
        print(_VERDE_B + "[HTTP 201] Cliente adicionado." + _RESET)
    except ValueError as erro:
        print(_VERMELHO_B + "Erro: " + str(erro) + _RESET)

def obter_cliente(id_cliente):
    """[HTTP 200/404] Devolve o cliente ou None se nao existir."""
    return clientes.get(id_cliente)

def modificar_cliente(id_cliente, nome, data_nascimento, telefone, id_plano_str, data_inicio):
    """[HTTP 200/400/404/409] Atualiza os dados de um cliente."""
    try:
        if id_cliente not in clientes:
            raise ValueError("[HTTP 404] Cliente nao encontrado.")
        dados_cliente = clientes[id_cliente]
        if nome != "":
            for id_c in clientes:
                if id_c != id_cliente and clientes[id_c]["nome"] == nome:
                    raise ValueError("[HTTP 409] Ja existe um cliente com esse nome.")
            dados_cliente["nome"] = nome
        if data_nascimento != "":
            dados_cliente["data_nascimento"] = data_nascimento
        if telefone != "":
            dados_cliente["telefone"] = telefone
        if id_plano_str != "":
            try:
                novo_id = int(id_plano_str)
            except (ValueError, TypeError):
                raise ValueError("[HTTP 400] ID do plano invalido.")
            if obter_plano(novo_id) is None:
                raise ValueError("[HTTP 404] Plano nao existe.")
            dados_cliente["id_plano"] = novo_id
        if data_inicio != "":
            dados_cliente["data_inicio"] = data_inicio
        print(_VERDE_B + "[HTTP 200] Cliente atualizado." + _RESET)
    except ValueError as erro:
        print(_VERMELHO_B + "Erro: " + str(erro) + _RESET)

def remover_cliente(id_cliente):
    """[HTTP 200/404] Remove um cliente."""
    try:
        if id_cliente not in clientes:
            raise ValueError("[HTTP 404] Cliente nao encontrado.")
        del clientes[id_cliente]
        print(_VERDE_B + "[HTTP 200] Cliente removido." + _RESET)
    except ValueError as erro:
        print(_VERMELHO_B + "Erro: " + str(erro) + _RESET)

# ---------- Listagem ----------

def mostrar_clientes():
    """[HTTP 200/204] Lista todos os clientes."""
    if len(clientes) == 0:
        print(_AMARELO + "[HTTP 204] Nenhum cliente registado." + _RESET)
        return
    print()
    print(_VERDE + _BOLD + "[ CLIENTES ]" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    for id_cliente, dados_cliente in clientes.items():
        plano = obter_plano(dados_cliente["id_plano"])
        if plano:
            nome_plano, num_treinos, preco_treino = plano
            preco_mensal = _arredondar(num_treinos * preco_treino)
        else:
            nome_plano, preco_mensal = "Sem plano", 0.0
        print(_AMARELO + "ID: "           + _RESET + _BRANCO  + str(id_cliente)                  + _RESET)
        print(_CINZA   + "Nome: "         + _RESET + _BRANCO  + dados_cliente["nome"]            + _RESET)
        print(_CINZA   + "Nascimento: "   + _RESET           + dados_cliente["data_nascimento"])
        print(_CINZA   + "Telefone: "     + _RESET           + dados_cliente["telefone"])
        print(_CINZA   + "Plano: "        + _RESET + _MAGENTA + nome_plano                       + _RESET)
        print(_CINZA   + "Inicio plano: " + _RESET           + dados_cliente["data_inicio"])
        print(_CINZA   + "Mensalidade: "  + _RESET + _VERDE   + str(preco_mensal) + " EUR"       + _RESET)
        print(_CINZA + "-" * 40 + _RESET)

def mostrar_cliente(id_cliente):
    """[HTTP 200/404] Mostra detalhes de um cliente."""
    if id_cliente not in clientes:
        print(_VERMELHO_B + "[HTTP 404] Cliente nao encontrado." + _RESET)
        return
    dados_cliente = clientes[id_cliente]
    plano = obter_plano(dados_cliente["id_plano"])
    if plano:
        nome_plano, num_treinos, preco_treino = plano
        preco_mensal = _arredondar(num_treinos * preco_treino)
    else:
        nome_plano, num_treinos, preco_treino, preco_mensal = "Sem plano", 0, 0.0, 0.0
    print()
    print(_VERDE + _BOLD + "[ CLIENTE ]" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    print(_AMARELO + "ID: "           + _RESET + _BRANCO  + str(id_cliente)                  + _RESET)
    print(_CINZA   + "Nome: "         + _RESET + _BRANCO  + dados_cliente["nome"]            + _RESET)
    print(_CINZA   + "Nascimento: "   + _RESET           + dados_cliente["data_nascimento"])
    print(_CINZA   + "Telefone: "     + _RESET           + dados_cliente["telefone"])
    print(_CINZA   + "Plano: "        + _RESET + _MAGENTA + nome_plano                       + _RESET)
    print(_CINZA   + "Treinos/mes: "  + _RESET           + str(num_treinos))
    print(_CINZA   + "Preco/treino: " + _RESET + _VERDE   + str(preco_treino) + " EUR"       + _RESET)
    print(_CINZA   + "Mensalidade: "  + _RESET + _VERDE   + str(preco_mensal) + " EUR"       + _RESET)
    print(_CINZA   + "Inicio plano: " + _RESET           + dados_cliente["data_inicio"])
    print(_CINZA + "-" * 40 + _RESET)

def pesquisar_cliente(pesquisa):
    """[HTTP 200/404] Pesquisa clientes pelo nome."""
    try:
        if not pesquisa:
            raise ValueError("[HTTP 400] Termo de pesquisa vazio.")
        print()
        print(_VERDE + _BOLD + "[ RESULTADOS ]" + _RESET)
        print(_CINZA + "-" * 40 + _RESET)
        encontrou = False
        for id_cliente, dados_cliente in clientes.items():
            if pesquisa.lower() in dados_cliente["nome"].lower():
                plano = obter_plano(dados_cliente["id_plano"])
                nome_plano = plano[0] if plano else "Sem plano"
                print(_AMARELO + "ID: "    + _RESET + _BRANCO  + str(id_cliente)       + _RESET)
                print(_CINZA   + "Nome: "  + _RESET + _BRANCO  + dados_cliente["nome"] + _RESET)
                print(_CINZA   + "Plano: " + _RESET + _MAGENTA + nome_plano            + _RESET)
                print(_CINZA + "-" * 40 + _RESET)
                encontrou = True
        if not encontrou:
            print(_AMARELO + "[HTTP 404] Nenhum cliente encontrado." + _RESET)
    except ValueError as erro:
        print(_VERMELHO_B + "Erro: " + str(erro) + _RESET)
