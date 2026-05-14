import sys
import os

_pasta_src = os.path.dirname(os.path.abspath(__file__))
_raiz = os.path.dirname(_pasta_src)

if _raiz not in sys.path:
    sys.path.insert(0, _raiz)
if _pasta_src not in sys.path:
    sys.path.insert(0, _pasta_src)

try:
    from src.menu import menu_principal
    from src.planos import carregar_planos
    from src.clientes import carregar_clientes
    from src.despesas import carregar_despesas
    from src.pagamentos import carregar_pagamentos
    from src.ginasios import carregar_ginasios
except ImportError:
    from menu import menu_principal
    from planos import carregar_planos
    from clientes import carregar_clientes
    from despesas import carregar_despesas
    from pagamentos import carregar_pagamentos
    from ginasios import carregar_ginasios

if __name__ == "__main__":
    # Carrega dados existentes dos JSON (criados automaticamente após primeira execução)
    carregar_planos()
    carregar_clientes()
    carregar_despesas()
    carregar_pagamentos()
    carregar_ginasios()
    menu_principal()
