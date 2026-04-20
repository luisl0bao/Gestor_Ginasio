"""
Ponto de entrada alternativo — execucao direta dentro da pasta src/.
Uso: python src/main.py  (a partir da raiz do projeto)
     python main.py      (a partir dentro da pasta src/)
"""
import sys
import os

# Garante que a pasta pai (raiz do projeto) esta no sys.path
# para que os imports "from src.xxx" funcionem quando chamado de dentro da src/
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
