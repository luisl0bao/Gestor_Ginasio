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
    from src.menu import menu_principal
    from src.clientes import carregar_clientes
    from src.planos import carregar_planos
    from src.despesas import carregar_despesas
    from src.pagamentos import carregar_pagamentos
    from src.ginasios import carregar_ginasios
except ImportError:
    from inicializacao import carregar_dados
    from menu import menu_principal
    from clientes import carregar_clientes
    from planos import carregar_planos
    from despesas import carregar_despesas
    from pagamentos import carregar_pagamentos
    from ginasios import carregar_ginasios

_RESET   = "\033[0m"
_BOLD    = "\033[1m"
_VERDE_B = "\033[92m"
_AMARELO = "\033[33m"

if __name__ == "__main__":
    # Tentar carregar dados guardados de cada módulo
    carregou_algo = False
    carregou_algo |= carregar_clientes()
    carregou_algo |= carregar_planos()
    carregou_algo |= carregar_despesas()
    carregou_algo |= carregar_pagamentos()
    carregou_algo |= carregar_ginasios()

    if carregou_algo:
        print(_VERDE_B + _BOLD + "Dados carregados com sucesso." + _RESET)
    else:
        # Primeira execução: inicializar com dados de exemplo
        print(_AMARELO + "Primeiro arranque — a criar dados de exemplo..." + _RESET)
        carregar_dados()

    print()
    menu_principal()
