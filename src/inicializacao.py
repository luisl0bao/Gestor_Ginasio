from src.planos import adicionar_plano
from clientes import adicionar_cliente
from despesas import adicionar_despesa

def carregar_dados():
    adicionar_plano("Basico", 8, 3.50)
    adicionar_plano("Standard", 12, 3.00)
    adicionar_plano("Premium", 20, 2.50)

    adicionar_despesa("Agua e Luz", 90.00)
    adicionar_despesa("Equipamentos", 160.00)

    adicionar_cliente("Joao Silva", "15/03/2002", "912345678", 1, "01/01/2025")
    adicionar_cliente("Ana Ferreira", "22/07/1996", "923456789", 2, "01/01/2025")
    adicionar_cliente("Carlos Sousa", "05/11/1989", "934567890", 1, "01/02/2025")
    adicionar_cliente("Marta Oliveira", "30/09/2005", "945678901", 2, "01/02/2025")
    adicionar_cliente("Rui Costa", "14/04/1982", "956789012", 1, "01/03/2025")
    adicionar_cliente("Sofia Martins", "08/12/1998", "967890123", 3, "01/03/2025")
    adicionar_cliente("Pedro Rodrigues", "19/06/1993", "978901234", 1, "01/01/2025")
    adicionar_cliente("Ines Almeida", "27/01/2000", "989012345", 2, "01/04/2025")
    adicionar_cliente("Tiago Lopes", "03/08/1986", "910123456", 1, "01/04/2025")
    adicionar_cliente("Beatriz Nunes", "11/05/2003", "921234567", 3, "01/05/2025")