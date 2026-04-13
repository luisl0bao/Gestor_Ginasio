from src import dados
from src.dados import despesas
from src.CoresANSII import VERDE_B, VERMELHO_B, AMARELO, BRANCO, CINZA, BOLD, RESET, VERMELHO, VERDE

# __Crud_____

def _arredondar(valor):
    return round(valor, 2)

def adicionar_despesa(descricao, valor):
    despesas.append((dados.proximo_id_despesa, descricao, _arredondar(valor)))
    dados.proximo_id_despesa = dados.proximo_id_despesa + 1
    print(VERDE_B + "Despesa registada." + RESET)

def obter_despesa(id_despesa):
    for despesa in despesas:
        if despesa[0] == id_despesa:
            return despesa
    return None

def remover_despesa(id_despesa):
    for despesa in despesas:
        if despesa[0] == id_despesa:
            despesas.remove(despesa)
            print(VERDE_B + "Despesa removida." + RESET)
            return
    print(VERMELHO_B + "Despesa nao encontrada." + RESET)

def mostrar_despesas():
    if len(despesas) == 0:
        print(AMARELO + "Nenhuma despesa registada." + RESET)
        return
    print()
    print(VERDE + BOLD + "[ DESPESAS ]" + RESET)
    print(CINZA + "-" * 40 + RESET)
    for despesa in despesas:
        print(AMARELO + "ID: "        + RESET + BRANCO   + str(despesa[0]) + RESET)
        print(CINZA   + "Descricao: " + RESET + BRANCO   + despesa[1]      + RESET)
        print(CINZA   + "Valor: "     + RESET + VERMELHO + str(despesa[2]) + " EUR" + RESET)
        print(CINZA + "-" * 40 + RESET)

def mostrar_despesa(id_despesa):
    despesa = obter_despesa(id_despesa)
    if despesa is None:
        print(VERMELHO_B + "Despesa nao encontrada." + RESET)
        return
    print()
    print(VERDE + BOLD + "[ DESPESA ]" + RESET)
    print(CINZA + "-" * 40 + RESET)
    print(AMARELO + "ID: "        + RESET + BRANCO   + str(despesa[0]) + RESET)
    print(CINZA   + "Descricao: " + RESET + BRANCO   + despesa[1]      + RESET)
    print(CINZA   + "Valor: "     + RESET + VERMELHO + str(despesa[2]) + " EUR" + RESET)
    print(CINZA + "-" * 40 + RESET)
