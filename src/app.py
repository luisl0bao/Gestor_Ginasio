#codigo do tkinter
import sys
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import date

_pasta_src = os.path.dirname(os.path.abspath(__file__))
_raiz = os.path.dirname(_pasta_src)
if _raiz not in sys.path:
    sys.path.insert(0, _raiz)
if _pasta_src not in sys.path:
    sys.path.insert(0, _pasta_src)

try:
    from src.inicializacao import carregar_dados
    from src import dados
    from src.dados import clientes, planos, despesas
    from src.planos import adicionar_plano, modificar_plano, remover_plano
    from src.clientes import adicionar_cliente, modificar_cliente, remover_cliente, pesquisar_cliente
    from src.despesas import adicionar_despesa, remover_despesa
    from src.pagamentos import criar_pagamento, listar_pagamentos, apagar_pagamento
    from src.relatorios import _calcular_receita_mensal, _calcular_total_despesas, _calcular_saldo, simular_mes
except ImportError:
    from inicializacao import carregar_dados
    import dados
    from dados import clientes, planos, despesas
    from planos import adicionar_plano, modificar_plano, remover_plano
    from clientes import adicionar_cliente, modificar_cliente, remover_cliente, pesquisar_cliente
    from despesas import adicionar_despesa, remover_despesa
    from pagamentos import criar_pagamento, listar_pagamentos, apagar_pagamento
    from relatorios import _calcular_receita_mensal, _calcular_total_despesas, _calcular_saldo, simular_mes

# ── janela principal ──────────────────────────────────────────────────────────
janela = tk.Tk()
janela.title("Gestor de Ginásio")
janela.geometry("860x560")
janela.resizable(False, False)

# ── frame do lado esquerdo (menu) ─────────────────────────────────────────────
frame_menu = tk.Frame(janela, bg="#2c2c2c", width=160)
frame_menu.pack(side="left", fill="y")
frame_menu.pack_propagate(False)

# ── frame do lado direito (conteúdo) ─────────────────────────────────────────
frame_conteudo = tk.Frame(janela, bg="#1e1e1e")
frame_conteudo.pack(side="left", fill="both", expand=True)

# ─────────────────────────── funções auxiliares ───────────────────────────────

def limpar_conteudo():
    for widget in frame_conteudo.winfo_children():
        widget.destroy()

def titulo(texto):
    tk.Label(frame_conteudo, text=texto, bg="#1e1e1e", fg="#a6e3a1",
             font=("Arial", 14, "bold"), anchor="w", padx=16, pady=10).pack(fill="x")
    tk.Frame(frame_conteudo, bg="#444", height=1).pack(fill="x", padx=16)

def botao_acao(parent, texto, comando, cor="#89b4fa"):
    tk.Button(parent, text=texto, bg=cor, fg="#1e1e1e",
              font=("Arial", 9, "bold"), relief="flat",
              padx=10, pady=5, cursor="hand2",
              command=comando).pack(side="left", padx=4)

def listbox_com_scroll(parent, altura=14):
    frame = tk.Frame(parent, bg="#1e1e1e")
    frame.pack(fill="both", expand=True, padx=16, pady=8)
    sb = tk.Scrollbar(frame)
    sb.pack(side="right", fill="y")
    lb = tk.Listbox(frame, bg="#2c2c2c", fg="#cdd6f4", selectbackground="#89b4fa",
                    selectforeground="#1e1e1e", font=("Courier", 10),
                    relief="flat", height=altura, yscrollcommand=sb.set,
                    activestyle="none")
    lb.pack(side="left", fill="both", expand=True)
    sb.config(command=lb.yview)
    return lb

def pedir_id_listbox(lb, dados_dict):
    """Devolve a chave (int) do item seleccionado na listbox, ou None."""
    sel = lb.curselection()
    if not sel:
        messagebox.showwarning("Aviso", "Selecciona um item da lista.")
        return None
    linha = lb.get(sel[0])
    try:
        return int(linha.split("|")[0].strip())
    except (ValueError, IndexError):
        return None

def pedir_id_listbox_lista(lb, lista):
    """Para listas (despesas/pagamentos) — devolve o id pelo índice."""
    sel = lb.curselection()
    if not sel:
        messagebox.showwarning("Aviso", "Selecciona um item da lista.")
        return None
    linha = lb.get(sel[0])
    try:
        return int(linha.split("|")[0].strip())
    except (ValueError, IndexError):
        return None

# ═══════════════════════════ CLIENTES ════════════════════════════════════════

def mostrar_clientes():
    limpar_conteudo()
    titulo("👤  Clientes")

    barra = tk.Frame(frame_conteudo, bg="#1e1e1e")
    barra.pack(fill="x", padx=16, pady=6)

    lb = listbox_com_scroll(frame_conteudo)

    def recarregar():
        lb.delete(0, "end")
        for cid, c in clientes.items():
            p = planos.get(c["id_plano"])
            nome_plano = p[0] if p else "Sem plano"
            lb.insert("end", f"{cid:<4}| {c['nome']:<20}| {c['data_nascimento']:<12}| {c['telefone']:<12}| {nome_plano}")

    def criar():
        if not planos:
            messagebox.showerror("Erro", "Cria um plano primeiro.")
            return
        nome  = simpledialog.askstring("Novo Cliente", "Nome:", parent=janela)
        if not nome:
            return
        nasc  = simpledialog.askstring("Novo Cliente", "Data de nascimento (DD/MM/AAAA):", parent=janela)
        tel   = simpledialog.askstring("Novo Cliente", "Telefone:", parent=janela)
        # escolher plano
        opcoes = "\n".join(f"{pid}: {p[0]} ({p[1]} treinos, {round(p[1]*p[2],2)} EUR/mês)" for pid, p in planos.items())
        pid_str = simpledialog.askstring("Plano", f"Planos disponíveis:\n{opcoes}\n\nID do plano:", parent=janela)
        if not pid_str:
            return
        try:
            pid = int(pid_str)
        except ValueError:
            messagebox.showerror("Erro", "ID inválido.")
            return
        inicio = str(date.today().strftime("%d/%m/%Y"))
        _, codigo = adicionar_cliente(nome, nasc, tel, pid, inicio)
        if codigo == 201:
            messagebox.showinfo("Sucesso", f"Cliente '{nome}' adicionado.")
        elif codigo == 409:
            messagebox.showerror("Erro", "Já existe um cliente com esse nome.")
        elif codigo == 404:
            messagebox.showerror("Erro", "Plano não encontrado.")
        else:
            messagebox.showerror("Erro", "Dados inválidos.")
        recarregar()

    def remover():
        cid = pedir_id_listbox(lb, clientes)
        if cid is None:
            return
        nome = clientes.get(cid, {}).get("nome", "?")
        if not messagebox.askyesno("Confirmar", f"Remover cliente '{nome}'?"):
            return
        _, codigo = remover_cliente(cid)
        if codigo == 200:
            messagebox.showinfo("Sucesso", "Cliente removido.")
        else:
            messagebox.showerror("Erro", "Cliente não encontrado.")
        recarregar()

    def pesquisar():
        termo = simpledialog.askstring("Pesquisar", "Nome:", parent=janela)
        if not termo:
            return
        encontrados, codigo = pesquisar_cliente(termo)
        if codigo == 404 or not encontrados:
            messagebox.showinfo("Resultado", "Nenhum cliente encontrado.")
        else:
            nomes = "\n".join(f"• {c['nome']}" for c in encontrados)
            messagebox.showinfo(f"{len(encontrados)} resultado(s)", nomes)

    botao_acao(barra, "+ Adicionar", criar)
    botao_acao(barra, "🗑 Remover", remover, "#f38ba8")
    botao_acao(barra, "🔍 Pesquisar", pesquisar, "#f9e2af")
    botao_acao(barra, "↺ Actualizar", recarregar, "#a6e3a1")

    recarregar()

# ═══════════════════════════ PLANOS ══════════════════════════════════════════

def mostrar_planos():
    limpar_conteudo()
    titulo("📋  Planos de Treino")

    barra = tk.Frame(frame_conteudo, bg="#1e1e1e")
    barra.pack(fill="x", padx=16, pady=6)

    lb = listbox_com_scroll(frame_conteudo)

    def recarregar():
        lb.delete(0, "end")
        for pid, p in planos.items():
            total = round(p[1] * p[2], 2)
            n_cli = sum(1 for c in clientes.values() if c["id_plano"] == pid)
            lb.insert("end", f"{pid:<4}| {p[0]:<20}| {p[1]} treinos | {p[2]} EUR/treino | {total} EUR/mês | {n_cli} clientes")

    def criar():
        nome = simpledialog.askstring("Novo Plano", "Nome do plano:", parent=janela)
        if not nome:
            return
        treinos_str = simpledialog.askstring("Novo Plano", "Nº de treinos por mês:", parent=janela)
        preco_str   = simpledialog.askstring("Novo Plano", "Preço por treino (€):", parent=janela)
        try:
            treinos = int(treinos_str)
            preco   = float(preco_str)
        except (ValueError, TypeError):
            messagebox.showerror("Erro", "Treinos deve ser inteiro e preço um número.")
            return
        _, codigo = adicionar_plano(nome, treinos, preco)
        if codigo == 201:
            messagebox.showinfo("Sucesso", f"Plano '{nome}' adicionado.")
        else:
            messagebox.showerror("Erro", "Dados inválidos.")
        recarregar()

    def remover():
        pid = pedir_id_listbox(lb, planos)
        if pid is None:
            return
        nome = planos.get(pid, ("?",))[0]
        if not messagebox.askyesno("Confirmar", f"Remover plano '{nome}'?"):
            return
        _, codigo = remover_plano(pid)
        if codigo == 200:
            messagebox.showinfo("Sucesso", "Plano removido.")
        elif codigo == 409:
            messagebox.showerror("Erro", "Existem clientes com este plano.")
        else:
            messagebox.showerror("Erro", "Plano não encontrado.")
        recarregar()

    botao_acao(barra, "+ Adicionar", criar)
    botao_acao(barra, "🗑 Remover", remover, "#f38ba8")
    botao_acao(barra, "↺ Actualizar", recarregar, "#a6e3a1")

    recarregar()

# ═══════════════════════════ DESPESAS ════════════════════════════════════════

def mostrar_despesas():
    limpar_conteudo()
    titulo("💸  Despesas")

    barra = tk.Frame(frame_conteudo, bg="#1e1e1e")
    barra.pack(fill="x", padx=16, pady=6)

    lb = listbox_com_scroll(frame_conteudo)

    def recarregar():
        lb.delete(0, "end")
        for d in despesas:
            data = d[3] if len(d) > 3 else "—"
            lb.insert("end", f"{d[0]:<4}| {d[1]:<25}| {d[2]} EUR | {data}")
        total = round(sum(d[2] for d in despesas), 2)
        tk.Label(frame_conteudo, text=f"Total: {total} EUR",
                 bg="#1e1e1e", fg="#f38ba8", font=("Arial", 10, "bold")).pack(anchor="e", padx=20)

    def criar():
        desc = simpledialog.askstring("Nova Despesa", "Descrição:", parent=janela)
        if not desc:
            return
        valor_str = simpledialog.askstring("Nova Despesa", "Valor (€):", parent=janela)
        try:
            valor = float(valor_str)
        except (ValueError, TypeError):
            messagebox.showerror("Erro", "Valor inválido.")
            return
        _, codigo = adicionar_despesa(desc, valor)
        if codigo == 201:
            messagebox.showinfo("Sucesso", "Despesa adicionada.")
        else:
            messagebox.showerror("Erro", "Dados inválidos.")
        recarregar()

    def remover():
        did = pedir_id_listbox_lista(lb, despesas)
        if did is None:
            return
        if not messagebox.askyesno("Confirmar", f"Remover despesa ID {did}?"):
            return
        _, codigo = remover_despesa(did)
        if codigo == 200:
            messagebox.showinfo("Sucesso", "Despesa removida.")
        else:
            messagebox.showerror("Erro", "Despesa não encontrada.")
        recarregar()

    botao_acao(barra, "+ Adicionar", criar)
    botao_acao(barra, "🗑 Remover", remover, "#f38ba8")
    botao_acao(barra, "↺ Actualizar", recarregar, "#a6e3a1")

    recarregar()

# ═══════════════════════════ PAGAMENTOS ══════════════════════════════════════

def mostrar_pagamentos():
    limpar_conteudo()
    titulo("💳  Pagamentos")

    barra = tk.Frame(frame_conteudo, bg="#1e1e1e")
    barra.pack(fill="x", padx=16, pady=6)

    lb = listbox_com_scroll(frame_conteudo)

    def recarregar():
        lb.delete(0, "end")
        pags = listar_pagamentos()
        for p in pags:
            lb.insert("end", f"{p['id']:<4}| {p['nome_cliente']:<20}| {p['plano']:<15}| {p['valor']} EUR | {p['dia_pagamento']}")
        total = round(sum(p["valor"] for p in pags), 2)
        tk.Label(frame_conteudo, text=f"Total recebido: {total} EUR",
                 bg="#1e1e1e", fg="#a6e3a1", font=("Arial", 10, "bold")).pack(anchor="e", padx=20)

    def criar():
        if not clientes:
            messagebox.showerror("Erro", "Não existem clientes.")
            return
        opcoes = "\n".join(f"{cid}: {c['nome']}" for cid, c in clientes.items())
        cid_str = simpledialog.askstring("Novo Pagamento", f"Clientes:\n{opcoes}\n\nID do cliente:", parent=janela)
        if not cid_str:
            return
        try:
            cid = int(cid_str)
        except ValueError:
            messagebox.showerror("Erro", "ID inválido.")
            return
        if cid not in clientes:
            messagebox.showerror("Erro", "Cliente não encontrado.")
            return
        c = clientes[cid]
        p = planos.get(c["id_plano"])
        nome_plano  = p[0] if p else "Sem plano"
        valor_sug   = round(p[1] * p[2], 2) if p else 0.0
        valor_str = simpledialog.askstring("Novo Pagamento",
                                           f"Valor sugerido: {valor_sug} EUR\nValor (Enter = sugerido):",
                                           parent=janela)
        valor = float(valor_str) if valor_str else valor_sug
        res = criar_pagamento(cid, valor, nome_plano)
        if res:
            messagebox.showinfo("Sucesso", "Pagamento adicionado.")
        else:
            messagebox.showerror("Erro", "Erro ao criar pagamento.")
        recarregar()

    def remover():
        pid = pedir_id_listbox_lista(lb, [])
        if pid is None:
            return
        if not messagebox.askyesno("Confirmar", f"Remover pagamento ID {pid}?"):
            return
        if apagar_pagamento(pid):
            messagebox.showinfo("Sucesso", "Pagamento removido.")
        else:
            messagebox.showerror("Erro", "Pagamento não encontrado.")
        recarregar()

    botao_acao(barra, "+ Adicionar", criar)
    botao_acao(barra, "🗑 Remover", remover, "#f38ba8")
    botao_acao(barra, "↺ Actualizar", recarregar, "#a6e3a1")

    recarregar()

# ═══════════════════════════ RELATÓRIO ═══════════════════════════════════════

def mostrar_relatorio():
    limpar_conteudo()
    titulo("📊  Relatório Financeiro")

    receita    = _calcular_receita_mensal()
    total_desp = _calcular_total_despesas()
    saldo      = _calcular_saldo()

    info = tk.Frame(frame_conteudo, bg="#1e1e1e")
    info.pack(fill="x", padx=16, pady=14)

    def cartao(parent, label, valor, cor):
        f = tk.Frame(parent, bg="#2c2c2c", padx=16, pady=12)
        f.pack(side="left", padx=8, expand=True, fill="both")
        tk.Label(f, text=label, bg="#2c2c2c", fg="#888", font=("Arial", 9)).pack(anchor="w")
        tk.Label(f, text=valor, bg="#2c2c2c", fg=cor, font=("Arial", 15, "bold")).pack(anchor="w")

    cartao(info, "Receita Mensal",  f"{receita} EUR",    "#a6e3a1")
    cartao(info, "Total Despesas",  f"{total_desp} EUR", "#f38ba8")
    cor_saldo = "#a6e3a1" if saldo >= 0 else "#f38ba8"
    cartao(info, "Lucro Mensal",    f"{saldo} EUR",      cor_saldo)
    cor_acum = "#a6e3a1" if dados.saldo_acumulado >= 0 else "#f38ba8"
    cartao(info, "Lucro Acumulado", f"{dados.saldo_acumulado} EUR", cor_acum)

    # lista de despesas
    tk.Label(frame_conteudo, text="Despesas registadas:", bg="#1e1e1e", fg="#aaa",
             font=("Arial", 10, "bold"), anchor="w", padx=16).pack(fill="x", pady=(10, 2))
    lb = listbox_com_scroll(frame_conteudo, altura=6)
    for d in despesas:
        data = d[3] if len(d) > 3 else "—"
        lb.insert("end", f"{d[0]:<4}| {d[1]:<25}| {d[2]} EUR | {data}")

    barra = tk.Frame(frame_conteudo, bg="#1e1e1e")
    barra.pack(fill="x", padx=16, pady=8)

    def simular():
        if not messagebox.askyesno("Simular Mês", "Confirmas a simulação do próximo mês?"):
            return
        _, codigo = simular_mes()
        if codigo == 200:
            messagebox.showinfo("Simulação concluída",
                                f"Lucro acumulado: {dados.saldo_acumulado} EUR")
            mostrar_relatorio()
        else:
            messagebox.showerror("Erro", "Erro ao simular mês.")

    botao_acao(barra, "▶ Simular Mês", simular, "#f9e2af")
    botao_acao(barra, "↺ Actualizar", mostrar_relatorio, "#a6e3a1")

# ═══════════════════════════ MENU LATERAL ════════════════════════════════════

tk.Label(frame_menu, text="GINÁSIO", bg="#2c2c2c", fg="#a6e3a1",
         font=("Arial", 11, "bold"), pady=20).pack(fill="x")

botoes_menu = [
    ("👤 Clientes",    mostrar_clientes),
    ("📋 Planos",      mostrar_planos),
    ("💸 Despesas",    mostrar_despesas),
    ("💳 Pagamentos",  mostrar_pagamentos),
    ("📊 Relatório",   mostrar_relatorio),
]

for texto, comando in botoes_menu:
    tk.Button(frame_menu, text=texto, bg="#2c2c2c", fg="#cdd6f4",
              font=("Arial", 10), relief="flat", anchor="w",
              padx=14, pady=10, cursor="hand2",
              activebackground="#3c3c3c", activeforeground="#a6e3a1",
              command=comando).pack(fill="x")

# ── arranque ──────────────────────────────────────────────────────────────────
carregar_dados()
mostrar_clientes()
janela.mainloop()