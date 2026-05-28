import sys
import os
import json
#teste comit
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src import dados
    from src.dados import clientes
    from src.planos import obter_plano
    from src.logger import obter_logger
    log = obter_logger("clientes")
except ImportError:
    log.error("Falha ao importar")


_PASTA             = os.path.dirname(os.path.abspath(__file__))
_FICHEIRO_CLIENTES = os.path.join(_PASTA, "clientes.json")

_RESET      = "\033[0m"
_BOLD       = "\033[1m"
_BRANCO     = "\033[97m"
_CINZA      = "\033[90m"
_VERDE      = "\033[32m"
_VERDE_B    = "\033[92m"
_AMARELO    = "\033[33m"
_VERMELHO_B = "\033[91m"
_MAGENTA    = "\033[35m"


def _arredondar(valor):
    return round(valor, 2)

def _ids_clientes():
    return list(clientes.keys())


# ---------------------------------------------------------------------------
# Persistência
# ---------------------------------------------------------------------------

def guardar_clientes():
    log.info("A guardar clientes em %s", _FICHEIRO_CLIENTES)
    payload = {
        "clientes":           {str(k): v for k, v in clientes.items()},
        "proximo_id_cliente": dados.proximo_id_cliente,
    }
    try:
        with open(_FICHEIRO_CLIENTES, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        log.info("Clientes guardados com sucesso (%d registos)", len(clientes))
    except OSError as e:
        log.critical("Erro ao guardar clientes: %s", e)


def carregar_clientes():
    if not os.path.exists(_FICHEIRO_CLIENTES):
        log.warning("Ficheiro %s nao encontrado — a iniciar sem dados", _FICHEIRO_CLIENTES)
        return False
    log.info("A carregar clientes de %s", _FICHEIRO_CLIENTES)
    try:
        with open(_FICHEIRO_CLIENTES, "r", encoding="utf-8") as f:
            payload = json.load(f)
        clientes.clear()
        for k, v in payload["clientes"].items():
            clientes[int(k)] = v
        dados.proximo_id_cliente = payload["proximo_id_cliente"]
        log.info("Clientes carregados com sucesso (%d registos)", len(clientes))
        return True
    except (OSError, json.JSONDecodeError, KeyError) as e:
        log.error("Erro ao carregar clientes: %s", e)
        return False


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------

def adicionar_cliente(nome, data_nascimento, telefone, id_plano, data_inicio):
    log.info("Tentativa de adicionar cliente: nome='%s' id_plano=%s", nome, id_plano)
    carregar_clientes()
    if not nome:
        log.warning("Nome vazio — cliente nao criado")
        return None, 400
    for id_c in clientes:
        if clientes[id_c]["nome"] == nome:
            log.warning("Cliente duplicado: nome='%s' ja existe (id=%d)", nome, id_c)
            return None, 409
    plano, codigo = obter_plano(id_plano)
    if codigo == 404:
        log.error("Plano id=%s nao encontrado ao adicionar cliente '%s'", id_plano, nome)
        return None, 404
    novo_id = dados.proximo_id_cliente
    clientes[novo_id] = {
        "nome": nome,
        "data_nascimento":data_nascimento,
        "telefone": telefone,
        "id_plano": id_plano,
        "data_inicio": data_inicio
    }
    dados.proximo_id_cliente += 1
    guardar_clientes()
    log.info("Cliente criado com sucesso: id=%d nome='%s'", novo_id, nome)
    return clientes[novo_id], 201


def obter_cliente(id_cliente):
    log.info("A obter cliente id=%d", id_cliente)
    carregar_clientes()
    cliente = clientes.get(id_cliente)
    if cliente is None:
        log.error("Cliente id=%d nao encontrado", id_cliente)
        return None, 404
    return cliente, 200


def modificar_cliente(id_cliente, nome, data_nascimento, telefone, id_plano_str, data_inicio):
    log.info("Tentativa de modificar cliente id=%d", id_cliente)
    carregar_clientes()
    if id_cliente not in clientes:
        log.error("Cliente id=%d nao encontrado para modificacao", id_cliente)
        return None, 404
    dados_cliente = clientes[id_cliente]
    if nome != "":
        for id_c in clientes:
            if id_c != id_cliente and clientes[id_c]["nome"] == nome:
                log.warning("Nome duplicado '%s' ao modificar cliente id=%d", nome, id_cliente)
                return None, 409
        dados_cliente["nome"] = nome
    if data_nascimento != "":
        dados_cliente["data_nascimento"] = data_nascimento
    if telefone != "":
        dados_cliente["telefone"] = telefone
    if id_plano_str != "":
        try:
            novo_id = int(id_plano_str)
        except (ValueError, TypeError):
            log.error("id_plano invalido '%s' ao modificar cliente id=%d", id_plano_str, id_cliente)
            return None, 400
        plano, codigo = obter_plano(novo_id)
        if codigo == 404:
            log.error("Plano id=%s nao encontrado ao modificar cliente id=%d", id_plano_str, id_cliente)
            return None, 404
        dados_cliente["id_plano"] = novo_id
    if data_inicio != "":
        dados_cliente["data_inicio"] = data_inicio
    guardar_clientes()
    log.info("Cliente id=%d modificado com sucesso", id_cliente)
    return dados_cliente, 200


def remover_cliente(id_cliente):
    log.info("Tentativa de remover cliente id=%d", id_cliente)
    carregar_clientes()
    if id_cliente not in clientes:
        log.warning("Cliente id=%d nao encontrado para remocao", id_cliente)
        return None, 404
    nome = clientes[id_cliente]["nome"]
    del clientes[id_cliente]
    guardar_clientes()
    log.info("Cliente id=%d nome='%s' removido com sucesso", id_cliente, nome)
    return id_cliente, 200


def mostrar_clientes():
    log.info("A listar todos os clientes")
    carregar_clientes()
    if len(clientes) == 0:
        log.info("Nenhum cliente encontrado")
        return [], 204
    print()
    print(_VERDE + _BOLD + "[ CLIENTES ]" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    for id_cliente, dados_cliente in clientes.items():
        plano, _ = obter_plano(dados_cliente["id_plano"])
        if plano:
            nome_plano, num_treinos, preco_treino = plano
            preco_mensal = _arredondar(num_treinos * preco_treino)
        else:
            nome_plano, preco_mensal = "Sem plano", 0.0
        print(_AMARELO + "ID: "           + _RESET + _BRANCO  + str(id_cliente)                + _RESET)
        print(_CINZA   + "Nome: "         + _RESET + _BRANCO  + dados_cliente["nome"]          + _RESET)
        print(_CINZA   + "Nascimento: "   + _RESET           + dados_cliente["data_nascimento"])
        print(_CINZA   + "Telefone: "     + _RESET           + dados_cliente["telefone"])
        print(_CINZA   + "Plano: "        + _RESET + _MAGENTA + nome_plano                     + _RESET)
        print(_CINZA   + "Inicio plano: " + _RESET           + dados_cliente["data_inicio"])
        print(_CINZA   + "Mensalidade: "  + _RESET + _VERDE   + str(preco_mensal) + " EUR"     + _RESET)
        print(_CINZA + "-" * 40 + _RESET)
    log.info("Listagem concluida: %d clientes apresentados", len(clientes))
    return list(clientes.values()), 200


def mostrar_cliente(id_cliente):
    log.info("A mostrar cliente id=%d", id_cliente)
    carregar_clientes()
    if id_cliente not in clientes:
        log.error("Cliente id=%d nao encontrado para mostrar", id_cliente)
        return None, 404
    dados_cliente = clientes[id_cliente]
    plano, _ = obter_plano(dados_cliente["id_plano"])
    if plano:
        nome_plano, num_treinos, preco_treino = plano
        preco_mensal = _arredondar(num_treinos * preco_treino)
    else:
        nome_plano, num_treinos, preco_treino, preco_mensal = "Sem plano", 0, 0.0, 0.0
    print()
    print(_VERDE + _BOLD + "[ CLIENTE ]" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    print(_AMARELO + "ID: "           + _RESET + _BRANCO  + str(id_cliente)                + _RESET)
    print(_CINZA   + "Nome: "         + _RESET + _BRANCO  + dados_cliente["nome"]          + _RESET)
    print(_CINZA   + "Nascimento: "   + _RESET           + dados_cliente["data_nascimento"])
    print(_CINZA   + "Telefone: "     + _RESET           + dados_cliente["telefone"])
    print(_CINZA   + "Plano: "        + _RESET + _MAGENTA + nome_plano                     + _RESET)
    print(_CINZA   + "Treinos/mes: "  + _RESET           + str(num_treinos))
    print(_CINZA   + "Preco/treino: " + _RESET + _VERDE   + str(preco_treino) + " EUR"     + _RESET)
    print(_CINZA   + "Mensalidade: "  + _RESET + _VERDE   + str(preco_mensal) + " EUR"     + _RESET)
    print(_CINZA   + "Inicio plano: " + _RESET           + dados_cliente["data_inicio"])
    print(_CINZA + "-" * 40 + _RESET)
    return dados_cliente, 200


def pesquisar_cliente(pesquisa):
    log.info("Pesquisa de cliente: termo='%s'", pesquisa)
    carregar_clientes()
    if not pesquisa:
        log.warning("Termo de pesquisa vazio")
        return None, 400
    print()
    print(_VERDE + _BOLD + "[ RESULTADOS ]" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    encontrados = []
    for id_cliente, dados_cliente in clientes.items():
        if pesquisa.lower() in dados_cliente["nome"].lower():
            plano, _ = obter_plano(dados_cliente["id_plano"])
            nome_plano = plano[0] if plano else "Sem plano"
            print(_AMARELO + "ID: "    + _RESET + _BRANCO  + str(id_cliente)       + _RESET)
            print(_CINZA   + "Nome: "  + _RESET + _BRANCO  + dados_cliente["nome"] + _RESET)
            print(_CINZA   + "Plano: " + _RESET + _MAGENTA + nome_plano            + _RESET)
            print(_CINZA + "-" * 40 + _RESET)
            encontrados.append(dados_cliente)
    if not encontrados:
        log.error("Nenhum cliente encontrado para termo='%s'", pesquisa)
        return [], 404
    log.info("Pesquisa concluida: %d resultado(s) para termo='%s'", len(encontrados), pesquisa)
    return encontrados, 200
