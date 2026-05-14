try:
    from src import dados as _dados_mod
except ImportError:
    import dados as _dados_mod
_AMARELO   = "\033[33m"
_VERMELHO_B = "\033[91m"
_RESET     = "\033[0m"
class ErroHTTP(Exception):
    def __init__(self, codigo, mensagem):
        self.codigo = codigo
        self.mensagem = mensagem
        super().__init__(f"[HTTP {codigo}] {mensagem}")

def _erro(codigo, mensagem):
    """Imprime um erro HTTP e lança a excepção correspondente."""
    raise ErroHTTP(codigo, mensagem)

def _pedir_texto(mensagem):
    while True:
        try:
            valor = input(_AMARELO + mensagem + _RESET).strip()
            if valor == "":
                raise ValueError("[HTTP 400] Campo obrigatorio.")
            if any(char.isdigit() for char in valor):
                raise ValueError("[HTTP 400] Nao pode conter numeros.")
            return valor
        except ValueError as erro:
            print(_VERMELHO_B + "Erro: " + str(erro) + _RESET)

def _pedir_telefone(mensagem):
    while True:
        try:
            valor = input(_AMARELO + mensagem + _RESET).strip()
            if valor == "":
                raise ValueError("[HTTP 400] Campo obrigatorio.")
            if not valor.isdigit():
                raise ValueError("[HTTP 400] O telefone so pode conter digitos.")
            if len(valor) != 9:
                raise ValueError("[HTTP 400] O telefone tem de ter 9 digitos.")
            return valor
        except ValueError as erro:
            print(_VERMELHO_B + "Erro: " + str(erro) + _RESET)

def _pedir_inteiro_positivo(mensagem):
    while True:
        try:
            valor = input(_AMARELO + mensagem + _RESET).strip()
            if valor == "":
                raise ValueError("[HTTP 400] Campo obrigatorio.")
            numero = int(valor)
            if numero <= 0:
                raise ValueError("[HTTP 400] Tem de ser maior que zero.")
            return numero
        except ValueError as erro:
            print(_VERMELHO_B + "Erro: " + str(erro) + _RESET)

def _pedir_decimal_positivo(mensagem):
    while True:
        try:
            valor = input(_AMARELO + mensagem + _RESET).strip()
            if valor == "":
                raise ValueError("[HTTP 400] Campo obrigatorio.")
            numero = float(valor)
            if numero <= 0:
                raise ValueError("[HTTP 400] Tem de ser maior que zero.")
            return round(numero, 2)
        except ValueError as erro:
            print(_VERMELHO_B + "Erro: " + str(erro) + _RESET)

def _pedir_data(mensagem):
    while True:
        try:
            valor = input(_AMARELO + mensagem + " (DD/MM/AAAA): " + _RESET).strip()
            if valor == "":
                raise ValueError("[HTTP 400] Campo obrigatorio.")
            partes = valor.split("/")
            if len(partes) != 3:
                raise ValueError("[HTTP 400] Formato invalido. Usa DD/MM/AAAA.")
            dia = int(partes[0])
            mes = int(partes[1])
            ano = int(partes[2])
            if dia < 1 or dia > 31:
                raise ValueError("[HTTP 400] Dia invalido.")
            if mes < 1 or mes > 12:
                raise ValueError("[HTTP 400] Mes invalido.")
            if ano < 1900 or ano > 2100:
                raise ValueError("[HTTP 400] Ano invalido.")
            return valor
        except ValueError as erro:
            print(_VERMELHO_B + "Erro: " + str(erro) + _RESET)

def _pedir_confirmacao(mensagem):
    while True:
        try:
            valor = input(_AMARELO + mensagem + " (s/n): " + _RESET).strip().lower()
            if valor not in ("s", "n"):
                raise ValueError("[HTTP 400] Responde com 's' ou 'n'.")
            return valor == "s"
        except ValueError as erro:
            print(_VERMELHO_B + "Erro: " + str(erro) + _RESET)

def _pedir_id_valido(mensagem, ids_validos):
    while True:
        try:
            valor = input(_AMARELO + mensagem + _RESET).strip()
            if valor == "":
                raise ValueError("[HTTP 400] Campo obrigatorio.")
            numero = int(valor)
            if numero not in ids_validos:
                raise ValueError("[HTTP 404] ID invalido. Escolhe um da lista.")
            return numero
        except ValueError as erro:
            print(_VERMELHO_B + "Erro: " + str(erro) + _RESET)

def _pedir_nome_valido(mensagem, nomes_validos):
    while True:
        try:
            valor = input(_AMARELO + mensagem + _RESET).strip()
            if valor == "":
                raise ValueError("[HTTP 400] Campo obrigatorio.")
            if valor not in nomes_validos:
                raise ValueError("[HTTP 404] Nome nao encontrado.")
            return valor
        except ValueError as erro:
            print(_VERMELHO_B + "Erro: " + str(erro) + _RESET)
