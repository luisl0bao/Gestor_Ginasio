https://docs.google.com/document/d/1Nx-fcNj_ut2M3mUhvd3cojEs4aUEs7kzg3kj5qBhDJU/edit?usp=sharing

O projeto consiste no desenvolvimento de um sistema de gestão de ginásio, que permite administrar informações essenciais como clientes, planos de treino e despesas.

O objetivo é facilitar o controlo e organização do ginásio, permitindo:

Registar novos clientes
Associar clientes a planos de treino
Acompanhar datas e pagamentos
Controlar despesas do ginásio

Este sistema ajuda a melhorar a eficiência da gestão e a tomada de decisões.

🗄️ Base de Dados

A base de dados é estruturada de forma simples utilizando dicionários para armazenar a informação.

🔹 Entidade: Cliente

Cada cliente é armazenado num dicionário com:

ID (chave)
Nome
Data de nascimento
Número de telefone
ID do plano atual
Data de início do plano

📌 Exemplo:

clientes = {
    1: ("João Silva", "2000-05-10", "912345678", 1, "2026-01-01")
}

🔹 Entidade: Plano

Os planos de treino são armazenados num dicionário com:

ID do plano (chave)
Nome do plano
Número de treinos
Preço (mensal ou por treino)

📌 Exemplo:

planos = {
    101: ("Plano Mensal", 12, 30.0)
}

🔄 CRUD (Operações principais)

O sistema implementa operações básicas de gestão de dados:

➕ Create (Criar)

Permite adicionar novos clientes e planos.
Ex: registar um novo cliente ou criar um novo plano.

📖 Read (Ler)

Permite consultar dados existentes.
Ex: listar todos os clientes ou ver detalhes de um plano.

✏️ Update (Atualizar)

Permite modificar informações.
Ex: alterar o plano de um cliente ou atualizar o número de telefone.

❌ Delete (Eliminar)

Permite remover dados.
Ex: apagar um cliente ou eliminar um plano.
