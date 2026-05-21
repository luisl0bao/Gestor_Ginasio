import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src import dados
    from src.dados import planos
    from src.logger import obter_logger
except ImportError:
    import dados
    from dados import planos
    from logger import obter_logger

log = obter_logger("planos")

_PASTA           = os.path.dirname(os.path.abspath(__file__))
_FICHEIRO_PLANOS = os.path.join(_PASTA, "planos.json")

_RESET      = "\033[0m"
_BOLD       = "\033[1m"
_BRANCO     = "\033[97m"
_CINZA      = "\033[90m"
_VERDE      = "\033[32m"
_VERDE_B    = "\033[92m"
_AMARELO    = "\033[33m"
_VERMELHO_B = "\033[91m"


def _arredondar(valor):
    return round(valor, 2)

def _ids_planos():
    return list(planos.keys())


# ---------------------------------------------------------------------------
# Persistência
# ---------------------------------------------------------------------------

def guardar_planos():
    log.info("A guardar planos em %s", _FICHEIRO_PLANOS)
    payload = {
        "planos":           {str(k): list(v) for k, v in planos.items()},
        "proximo_id_plano": dados.proximo_id_plano,
    }
    try:
        with open(_FICHEIRO_PLANOS, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        log.info("Planos guardados com sucesso (%d registos)", len(planos))
    except OSError as e:
        log.critical("Erro ao guardar planos: %s", e)


def carregar_planos():
    if not os.path.exists(_FICHEIRO_PLANOS):
        log.warning("Ficheiro %s nao encontrado — a iniciar sem dados", _FICHEIRO_PLANOS)
        return False
    log.info("A carregar planos de %s", _FICHEIRO_PLANOS)
    try:
        with open(_FICHEIRO_PLANOS, "r", encoding="utf-8") as f:
            payload = json.load(f)
        planos.clear()
        for k, v in payload["planos"].items():
            planos[int(k)] = tuple(v)
        dados.proximo_id_plano = payload["proximo_id_plano"]
        log.info("Planos carregados com sucesso (%d registos)", len(planos))
        return True
    except (OSError, json.JSONDecodeError, KeyError) as e:
        log.error("Erro ao carregar planos: %s", e)
        return False


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------

def adicionar_plano(nome, num_treinos, preco_por_treino):
    log.info("Tentativa de adicionar plano: nome='%s' treinos=%s preco=%s", nome, num_treinos, preco_por_treino)
    carregar_planos()
    if not nome or not isinstance(nome, str):
        log.warning("Nome invalido ao adicionar plano: '%s'", nome)
        return None, 400
    if not isinstance(num_treinos, int) or num_treinos <= 0:
        log.warning("num_treinos invalido: %s", num_treinos)
        return None, 400
    if not isinstance(preco_por_treino, (int, float)) or preco_por_treino <= 0:
        log.warning("preco_por_treino invalido: %s", preco_por_treino)
        return None, 400
    novo_id = dados.proximo_id_plano
    planos[novo_id] = (nome, num_treinos, _arredondar(preco_por_treino))
    dados.proximo_id_plano += 1
    guardar_planos()
    log.info("Plano criado com sucesso: id=%d nome='%s'", novo_id, nome)
    return planos[novo_id], 201


def obter_plano(id_plano):
    log.info("A obter plano id=%s", id_plano)
    carregar_planos()
    plano = planos.get(id_plano)
    if plano is None:
        log.warning("Plano id=%s nao encontrado", id_plano)
        return None, 404
    return plano, 200


def modificar_plano(id_plano, nome, num_treinos, preco_por_treino):
    log.info("Tentativa de modificar plano id=%d", id_plano)
    carregar_planos()
    if id_plano not in planos:
        log.warning("Plano id=%d nao encontrado para modificacao", id_plano)
        return None, 404
    plano_atual = planos[id_plano]
    if nome == "":
        nome = plano_atual[0]
    if num_treinos == "":
        num_treinos = plano_atual[1]
    else:
        try:
            num_treinos = int(num_treinos)
            if num_treinos <= 0:
                log.warning("num_treinos invalido ao modificar plano id=%d: %s", id_plano, num_treinos)
                return None, 400
        except (TypeError, ValueError):
            log.error("num_treinos nao e inteiro ao modificar plano id=%d: '%s'", id_plano, num_treinos)
            return None, 400
    if preco_por_treino == "":
        preco_por_treino = plano_atual[2]
    else:
        try:
            preco_por_treino = _arredondar(float(preco_por_treino))
            if preco_por_treino <= 0:
                log.warning("preco invalido ao modificar plano id=%d: %s", id_plano, preco_por_treino)
                return None, 400
        except (TypeError, ValueError):
            log.error("preco nao e numero ao modificar plano id=%d: '%s'", id_plano, preco_por_treino)
            return None, 400
    planos[id_plano] = (nome, num_treinos, preco_por_treino)
    guardar_planos()
    log.info("Plano id=%d modificado com sucesso", id_plano)
    return planos[id_plano], 200


def remover_plano(id_plano):
    log.info("Tentativa de remover plano id=%d", id_plano)
    carregar_planos()
    if id_plano not in planos:
        log.warning("Plano id=%d nao encontrado para remocao", id_plano)
        return None, 404
    try:
        from src.dados import clientes as _clientes
    except ImportError:
        from dados import clientes as _clientes
    for id_cliente in _clientes:
        if _clientes[id_cliente]["id_plano"] == id_plano:
            log.warning("Plano id=%d nao pode ser removido — esta associado ao cliente id=%d", id_plano, id_cliente)
            return None, 409
    nome = planos[id_plano][0]
    del planos[id_plano]
    guardar_planos()
    log.info("Plano id=%d nome='%s' removido com sucesso", id_plano, nome)
    return id_plano, 200


def mostrar_planos():
    log.info("A listar todos os planos")
    carregar_planos()
    if len(planos) == 0:
        log.info("Nenhum plano encontrado")
        return [], 204
    try:
        from src.dados import clientes as _clientes
    except ImportError:
        from dados import clientes as _clientes
    print()
    print(_VERDE + _BOLD + "[ PLANOS ]" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    for id_plano, dados_plano in planos.items():
        total_clientes = sum(1 for c in _clientes.values() if c["id_plano"] == id_plano)
        preco_mensal = _arredondar(dados_plano[1] * dados_plano[2])
        print(_AMARELO + "ID: "           + _RESET + _BRANCO  + str(id_plano)       + _RESET)
        print(_CINZA   + "Nome: "         + _RESET + _BRANCO  + dados_plano[0]      + _RESET)
        print(_CINZA   + "Treinos/mes: "  + _RESET + str(dados_plano[1]))
        print(_CINZA   + "Preco/treino: " + _RESET + _VERDE   + str(dados_plano[2]) + " EUR" + _RESET)
        print(_CINZA   + "Total mensal: " + _RESET + _VERDE   + str(preco_mensal)   + " EUR" + _RESET)
        print(_CINZA   + "Clientes: "     + _RESET + _AMARELO + str(total_clientes) + _RESET)
        print(_CINZA + "-" * 40 + _RESET)
    log.info("Listagem concluida: %d planos apresentados", len(planos))
    return list(planos.values()), 200


def mostrar_plano(id_plano):
    log.info("A mostrar plano id=%d", id_plano)
    carregar_planos()
    if id_plano not in planos:
        log.warning("Plano id=%d nao encontrado para mostrar", id_plano)
        return None, 404
    dados_plano  = planos[id_plano]
    preco_mensal = _arredondar(dados_plano[1] * dados_plano[2])
    print()
    print(_VERDE + _BOLD + "[ PLANO ]" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    print(_AMARELO + "ID: "           + _RESET + _BRANCO + str(id_plano)       + _RESET)
    print(_CINZA   + "Nome: "         + _RESET + _BRANCO + dados_plano[0]      + _RESET)
    print(_CINZA   + "Treinos/mes: "  + _RESET + str(dados_plano[1]))
    print(_CINZA   + "Preco/treino: " + _RESET + _VERDE  + str(dados_plano[2]) + " EUR" + _RESET)
    print(_CINZA   + "Total mensal: " + _RESET + _VERDE  + str(preco_mensal)   + " EUR" + _RESET)
    print(_CINZA + "-" * 40 + _RESET)
    return dados_plano, 200


def _resumo_planos():
    log.info("A gerar resumo de planos")
    carregar_planos()
    if len(planos) == 0:
        log.info("Nenhum plano disponivel para resumo")
        return [], 204
    print(_CINZA + "Planos disponiveis:" + _RESET)
    for id_plano, dados_plano in planos.items():
        preco_mensal = _arredondar(dados_plano[1] * dados_plano[2])
        print(_AMARELO + "[" + str(id_plano) + "] " + _RESET +
              _BRANCO + dados_plano[0] + _RESET +
              _CINZA + " - " + str(dados_plano[1]) + " treinos - " + str(preco_mensal) + " EUR/mes" + _RESET)
    return list(planos.values()), 200
