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
except ImportError:
    from inicializacao import carregar_dados
    from menu import menu_principal

if __name__ == "__main__":
    carregar_dados()
    menu_principal()
