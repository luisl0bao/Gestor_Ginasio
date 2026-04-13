from src.CoresANSII import AMARELO, VERMELHO_B, RESET

def _pedir_texto(mensagem):
    while True:
        try:
            valor = input(AMARELO + mensagem + RESET).strip()
            if valor == "":
                raise ValueError("Campo obrigatorio.")
            if any(char.isdigit() for char in valor):
                raise ValueError("Nao pode conter numeros.")
            return valor
        except ValueError as erro:
            print(VERMELHO_B + "Erro: " + str(erro) + RESET)

def _pedir_telefone(mensagem):
    while True:
        try:
            valor = input(AMARELO + mensagem + RESET).strip()
            if valor == "":
                raise ValueError("Campo obrigatorio.")
            if not valor.isdigit():
                raise ValueError("O telefone so pode conter digitos.")
            if len(valor) != 9:
                raise ValueError("O telefone tem de ter 9 digitos.")
            return valor
        except ValueError as erro:
            print(VERMELHO_B + "Erro: " + str(erro) + RESET)

def _pedir_inteiro_positivo(mensagem):
    while True:
        try:
            valor = input(AMARELO + mensagem + RESET).strip()
            if valor == "":
                raise ValueError("Campo obrigatorio.")
            numero = int(valor)
            if numero <= 0:
                raise ValueError("Tem de ser maior que zero.")
            return numero
        except ValueError as erro:
            print(VERMELHO_B + "Erro: " + str(erro) + RESET)

def _pedir_decimal_positivo(mensagem):
    while True:
        try:
            valor = input(AMARELO + mensagem + RESET).strip()
            if valor == "":
                raise ValueError("Campo obrigatorio.")
            numero = float(valor)
            if numero <= 0:
                raise ValueError("Tem de ser maior que zero.")
            return round(numero, 2)
        except ValueError as erro:
            print(VERMELHO_B + "Erro: " + str(erro) + RESET)

def _pedir_data(mensagem):
    while True:
        try:
            valor = input(AMARELO + mensagem + " (DD/MM/AAAA): " + RESET).strip()
            if valor == "":
                raise ValueError("Campo obrigatorio.")
            partes = valor.split("/")
            if len(partes) != 3:
                raise ValueError("Formato invalido. Usa DD/MM/AAAA.")
            dia = int(partes[0])
            mes = int(partes[1])
            ano = int(partes[2])
            if dia < 1 or dia > 31:
                raise ValueError("Dia invalido.")
            if mes < 1 or mes > 12:
                raise ValueError("Mes invalido.")
            if ano < 1900 or ano > 2025:
                raise ValueError("Ano invalido.")
            return valor
        except ValueError as erro:
            print(VERMELHO_B + "Erro: " + str(erro) + RESET)

def _pedir_confirmacao(mensagem):
    while True:
        try:
            valor = input(AMARELO + mensagem + " (s/n): " + RESET).strip().lower()
            if valor not in ("s", "n"):
                raise ValueError("Responde com 's' ou 'n'.")
            return valor == "s"
        except ValueError as erro:
            print(VERMELHO_B + "Erro: " + str(erro) + RESET)

def _pedir_id_valido(mensagem, ids_validos):
    while True:
        try:
            valor = input(AMARELO + mensagem + RESET).strip()
            if valor == "":
                raise ValueError("Campo obrigatorio.")
            numero = int(valor)
            if numero not in ids_validos:
                raise ValueError("ID invalido. Escolhe um da lista.")
            return numero
        except ValueError as erro:
            print(VERMELHO_B + "Erro: " + str(erro) + RESET)

def _pedir_nome_valido(mensagem, nomes_validos):
    while True:
        try:
            valor = input(AMARELO + mensagem + RESET).strip()
            if valor == "":
                raise ValueError("Campo obrigatorio.")
            if valor not in nomes_validos:
                raise ValueError("Nome nao encontrado.")
            return valor
        except ValueError as erro:
            print(VERMELHO_B + "Erro: " + str(erro) + RESET)
