import sys
import os

_pasta_src = os.path.dirname(os.path.abspath(__file__))
_raiz = os.path.dirname(_pasta_src)

if _raiz not in sys.path:
    sys.path.insert(0, _raiz)
if _pasta_src not in sys.path:
    sys.path.insert(0, _pasta_src)

try:
    from src.inicializacao import carregar_dados
    from src.menu import menu_principal, _carregar_dados, FICHEIRO_JSON
except ImportError:
    from inicializacao import carregar_dados
    from menu import menu_principal, _carregar_dados, FICHEIRO_JSON

_RESET   = "\033[0m"
_BOLD    = "\033[1m"
_VERDE_B = "\033[92m"
_CINZA   = "\033[90m"
_AMARELO = "\033[33m"

if __name__ == "__main__":
    # Tentar carregar dados guardados; se não existirem, inicializar com exemplos
    carregou = _carregar_dados()
    if carregou:
        print(_VERDE_B + _BOLD + "Dados carregados de: " + FICHEIRO_JSON + _RESET)
    else:
        print(_AMARELO + "Primeiro arranque — a criar Ginasio Default com dados de exemplo..." + _RESET)
        carregar_dados()
    print()

    # Executar menu principal
    menu_principal()
