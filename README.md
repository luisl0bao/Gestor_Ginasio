# 🏋️‍♂️ Sistema de Gestão de Ginásio

## 📌 **Descrição do Projeto**

Este projeto consiste no desenvolvimento de um sistema de gestão de ginásio, criado para facilitar a administração de informações essenciais como:

- Clientes  
- Planos de treino  
- Pagamentos  
- Despesas  

O principal objetivo é melhorar a organização, o controlo e a eficiência na gestão do ginásio, apoiando também uma melhor tomada de decisões.

---

## 🎯 **Funcionalidades**

O sistema permite:

- ✅ Registar novos clientes  
- ✅ Associar clientes a planos de treino  
- ✅ Acompanhar datas e pagamentos  
- ✅ Controlar despesas do ginásio  

---

## 🗄️ **Base de Dados**

A base de dados é estruturada de forma simples, utilizando dicionários em Python para armazenar a informação.

### 🔹 **Entidade: Cliente**

Cada cliente é representado por um dicionário com os seguintes dados:

- ID (chave)  
- Nome  
- Data de nascimento  
- Número de telefone  
- ID do plano atual  
- Data de início do plano  

📌 **Exemplo:**

```python
clientes = {
    1: ("João Silva", "2000-05-10", "912345678", 1, "2026-01-01")
}
🔹 Entidade: Plano

Os planos de treino também são armazenados em dicionários com:

ID do plano (chave)
Nome do plano
Número de treinos
Preço (mensal ou por treino)

📌 Exemplo:

planos = {
    101: ("Plano Mensal", 12, 30.0)
}
🔄 Operações CRUD

O sistema implementa as principais operações de gestão de dados:

➕ Create (Criar)

Permite adicionar novos dados ao sistema.
Exemplo:

Registar um novo cliente
Criar um novo plano
📖 Read (Ler)

Permite consultar informações existentes.
Exemplo:

Listar todos os clientes
Ver detalhes de um plano
✏️ Update (Atualizar)

Permite modificar dados já existentes.
Exemplo:

Alterar o plano de um cliente
Atualizar o número de telefone
❌ Delete (Eliminar)

Permite remover dados do sistema.
Exemplo:

Apagar um cliente
Eliminar um plano
