# 🏋️ Sistema de Gestão de Ginásio

Projeto académico desenvolvido em Python para gestão administrativa de um ginásio, com suporte a múltiplas instalações.

---

## 📦 Estrutura de Dados

Os dados são geridos em memória com dicionários Python e persistidos automaticamente em ficheiros JSON por módulo.

**Cliente**
```python
clientes = {
    1: {
        "nome": "João Silva",
        "data_nascimento": "2000-05-10",
        "telefone": "912345678",
        "id_plano": 1,
        "data_inicio": "2026-01-01"
    }
}
```

**Plano de Treino**
```python
planos = {
    1: ("Plano Mensal", 12, 30.0)  # nome, treinos/mês, preço/treino
}
```

---

## ⚙️ Funcionalidades

- Gestão completa de clientes, planos, despesas e pagamentos (CRUD)
- Suporte a múltiplos ginásios com dados completamente isolados
- Relatórios financeiros e estatísticas mensais
- Simulação de fecho de mês com geração automática de pagamentos
- Persistência automática por módulo — cada alteração é guardada de imediato no ficheiro JSON correspondente

---

## 💾 Persistência

Cada módulo é responsável pelos seus próprios dados:

| Módulo | Ficheiro |
|---|---|
| `clientes.py` | `clientes.json` |
| `planos.py` | `planos.json` |
| `despesas.py` | `despesas.json` |
| `pagamentos.py` | `pagamentos.json` |
| `ginasios.py` | `ginasios.json` |

As funções de leitura carregam os dados do ficheiro antes de apresentar informação. As funções de escrita guardam os dados no ficheiro após qualquer alteração.

---

## 🗂️ Estrutura do Projeto
src/
├── main.py          # Ponto de entrada
├── menu.py          # Navegação e interface
├── dados.py         # Estado global partilhado
├── clientes.py      # Gestão de clientes
├── planos.py        # Gestão de planos de treino
├── despesas.py      # Gestão de despesas
├── pagamentos.py    # Gestão de pagamentos e transações
├── ginasios.py      # Gestão de ginásios adicionais
├── relatorios.py    # Relatórios financeiros
└── utils.py         # Utilitários de input

---

## 🚀 Como Executar

```bash
python src/main.py
```

Requer Python 3.8 ou superior. Sem dependências externas.
