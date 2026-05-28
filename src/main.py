import sys
import os

_pasta_src = os.path.dirname(os.path.abspath(__file__))
_raiz = os.path.dirname(_pasta_src)
if _raiz not in sys.path:
    sys.path.insert(0, _raiz)
if _pasta_src not in sys.path:
    sys.path.insert(0, _pasta_src)

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import date

try:
    from src.inicializacao import carregar_dados
    from src import dados
    from src.dados import clientes, planos, despesas
    from src.planos import (
        adicionar_plano, mostrar_planos, mostrar_plano,
        modificar_plano, remover_plano, _ids_planos, _resumo_planos,
    )
    from src.clientes import (
        adicionar_cliente, mostrar_clientes, mostrar_cliente,
        modificar_cliente, remover_cliente, pesquisar_cliente, _ids_clientes,
    )
    from src.despesas import adicionar_despesa, mostrar_despesas, mostrar_despesa, remover_despesa
    from src.pagamentos import (
        criar_pagamento, listar_pagamentos, apagar_pagamento,
        atualizar_pagamento, gerar_pagamentos_fim_do_mes,
    )
    from src.relatorios import (
        mostrar_relatorio_financeiro, mostrar_estatisticas, simular_mes,
        _calcular_receita_mensal, _calcular_total_despesas, _calcular_saldo,
    )
except ImportError:
    from inicializacao import carregar_dados
    import dados
    from dados import clientes, planos, despesas
    from planos import (
        adicionar_plano, mostrar_planos, mostrar_plano,
        modificar_plano, remover_plano, _ids_planos, _resumo_planos,
    )
    from clientes import (
        adicionar_cliente, mostrar_clientes, mostrar_cliente,
        modificar_cliente, remover_cliente, pesquisar_cliente, _ids_clientes,
    )
    from despesas import adicionar_despesa, mostrar_despesas, mostrar_despesa, remover_despesa
    from pagamentos import (
        criar_pagamento, listar_pagamentos, apagar_pagamento,
        atualizar_pagamento, gerar_pagamentos_fim_do_mes,
    )
    from relatorios import (
        mostrar_relatorio_financeiro, mostrar_estatisticas, simular_mes,
        _calcular_receita_mensal, _calcular_total_despesas, _calcular_saldo,
    )

# ─────────────────────────── Paleta de cores ────────────────────────────────
BG        = "#1e1e2e"
BG2       = "#2a2a3e"
BG3       = "#313145"
ACCENT    = "#a6e3a1"
ACCENT2   = "#89b4fa"
DANGER    = "#f38ba8"
WARNING   = "#f9e2af"
TEXT      = "#cdd6f4"
TEXT_DIM  = "#6c7086"
BORDER    = "#45475a"
SUCCESS   = "#a6e3a1"


def _ar(v):
    return round(v, 2)


# ─────────────────────────── Janela de diálogo genérica ─────────────────────
class FormDialog(tk.Toplevel):
    """Janela de formulário reutilizável com campos texto."""

    def __init__(self, parent, title, fields, values=None):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=BG)
        self.resizable(False, False)
        self.grab_set()
        self.result = None
        self._entries = {}

        tk.Label(self, text=title, bg=BG, fg=ACCENT, font=("Segoe UI", 13, "bold"),
                 pady=10).pack(fill="x", padx=20)

        frame = tk.Frame(self, bg=BG)
        frame.pack(padx=20, pady=6, fill="x")

        for i, (key, label) in enumerate(fields):
            tk.Label(frame, text=label, bg=BG, fg=TEXT_DIM,
                     font=("Segoe UI", 10), anchor="w").grid(row=i, column=0, sticky="w", pady=4)
            e = tk.Entry(frame, bg=BG2, fg=TEXT, insertbackground=TEXT,
                         relief="flat", font=("Segoe UI", 10), width=30,
                         highlightthickness=1, highlightbackground=BORDER,
                         highlightcolor=ACCENT2)
            e.grid(row=i, column=1, padx=(10, 0), pady=4, sticky="ew")
            if values and key in values:
                e.insert(0, str(values[key]))
            self._entries[key] = e

        frame.columnconfigure(1, weight=1)

        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(pady=12)
        tk.Button(btn_frame, text="Confirmar", bg=ACCENT, fg=BG,
                  font=("Segoe UI", 10, "bold"), relief="flat", padx=16, pady=6,
                  cursor="hand2", command=self._confirm).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Cancelar", bg=BG3, fg=TEXT,
                  font=("Segoe UI", 10), relief="flat", padx=16, pady=6,
                  cursor="hand2", command=self.destroy).pack(side="left", padx=6)

        self.bind("<Return>", lambda e: self._confirm())
        self.bind("<Escape>", lambda e: self.destroy())
        self._center(parent)

    def _confirm(self):
        self.result = {k: e.get().strip() for k, e in self._entries.items()}
        self.destroy()

    def _center(self, parent):
        self.update_idletasks()
        pw, ph = parent.winfo_width(), parent.winfo_height()
        px, py = parent.winfo_rootx(), parent.winfo_rooty()
        w, h = self.winfo_width(), self.winfo_height()
        self.geometry(f"+{px + pw//2 - w//2}+{py + ph//2 - h//2}")


class SelectDialog(tk.Toplevel):
    """Diálogo para seleccionar um item de uma lista."""

    def __init__(self, parent, title, items):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=BG)
        self.resizable(False, False)
        self.grab_set()
        self.result = None

        tk.Label(self, text=title, bg=BG, fg=ACCENT,
                 font=("Segoe UI", 12, "bold"), pady=8).pack(fill="x", padx=20)

        lb_frame = tk.Frame(self, bg=BG)
        lb_frame.pack(padx=20, pady=4, fill="both", expand=True)

        sb = tk.Scrollbar(lb_frame)
        sb.pack(side="right", fill="y")
        self._lb = tk.Listbox(lb_frame, bg=BG2, fg=TEXT, selectbackground=ACCENT2,
                              selectforeground=BG, font=("Segoe UI", 10),
                              relief="flat", yscrollcommand=sb.set,
                              activestyle="none", height=min(len(items), 12))
        self._lb.pack(side="left", fill="both", expand=True)
        sb.config(command=self._lb.yview)

        self._ids = []
        for id_, label in items:
            self._lb.insert("end", f"  [{id_}]  {label}")
            self._ids.append(id_)

        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Seleccionar", bg=ACCENT2, fg=BG,
                  font=("Segoe UI", 10, "bold"), relief="flat", padx=14, pady=5,
                  cursor="hand2", command=self._select).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Cancelar", bg=BG3, fg=TEXT,
                  font=("Segoe UI", 10), relief="flat", padx=14, pady=5,
                  cursor="hand2", command=self.destroy).pack(side="left", padx=6)

        self._lb.bind("<Double-Button-1>", lambda e: self._select())
        self._center(parent)

    def _select(self):
        sel = self._lb.curselection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona um item.", parent=self)
            return
        self.result = self._ids[sel[0]]
        self.destroy()

    def _center(self, parent):
        self.update_idletasks()
        pw, ph = parent.winfo_width(), parent.winfo_height()
        px, py = parent.winfo_rootx(), parent.winfo_rooty()
        w, h = self.winfo_width(), self.winfo_height()
        self.geometry(f"+{px + pw//2 - w//2}+{py + ph//2 - h//2}")


# ─────────────────────────── Painel de conteúdo base ────────────────────────
class BasePanel(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app

    def _table(self, parent, columns, rows, height=12):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                        background=BG2, foreground=TEXT,
                        fieldbackground=BG2, rowheight=28,
                        font=("Segoe UI", 10), borderwidth=0)
        style.configure("Custom.Treeview.Heading",
                        background=BG3, foreground=ACCENT2,
                        font=("Segoe UI", 10, "bold"), relief="flat")
        style.map("Custom.Treeview",
                  background=[("selected", ACCENT2)],
                  foreground=[("selected", BG)])

        frame = tk.Frame(parent, bg=BG)
        frame.pack(fill="both", expand=True, pady=6)

        sb = ttk.Scrollbar(frame, orient="vertical")
        sb.pack(side="right", fill="y")

        tree = ttk.Treeview(frame, columns=columns, show="headings",
                            style="Custom.Treeview", height=height,
                            yscrollcommand=sb.set)
        sb.config(command=tree.yview)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=120, minwidth=60)
        tree.pack(side="left", fill="both", expand=True)

        for row in rows:
            tree.insert("", "end", values=row)

        return tree

    def _btn(self, parent, text, cmd, color=ACCENT2):
        return tk.Button(parent, text=text, bg=color, fg=BG,
                         font=("Segoe UI", 10, "bold"), relief="flat",
                         padx=12, pady=6, cursor="hand2", command=cmd)

    def _danger_btn(self, parent, text, cmd):
        return self._btn(parent, text, cmd, DANGER)

    def _section(self, text):
        tk.Label(self, text=text, bg=BG, fg=ACCENT,
                 font=("Segoe UI", 14, "bold"), anchor="w",
                 pady=10).pack(fill="x", padx=24)
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=24)


# ─────────────────────────── PAINEL: CLIENTES ────────────────────────────────
class ClientesPanel(BasePanel):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._section("👤  Clientes")
        self._toolbar()
        self._tree_frame = tk.Frame(self, bg=BG)
        self._tree_frame.pack(fill="both", expand=True, padx=24, pady=6)
        self._tree = None
        self._load()

    def _toolbar(self):
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=24, pady=8)
        self._btn(bar, "+ Novo cliente", self._criar).pack(side="left", padx=4)
        self._btn(bar, "✏ Editar", self._editar).pack(side="left", padx=4)
        self._danger_btn(bar, "🗑 Remover", self._remover).pack(side="left", padx=4)
        self._btn(bar, "🔍 Pesquisar", self._pesquisar).pack(side="left", padx=4)
        self._btn(bar, "↺ Actualizar", self._load, ACCENT).pack(side="right", padx=4)

    def _load(self):
        for w in self._tree_frame.winfo_children():
            w.destroy()
        cols = ("ID", "Nome", "Nascimento", "Telefone", "Plano", "Início")
        rows = []
        for cid, c in clientes.items():
            p = planos.get(c["id_plano"])
            nome_plano = p[0] if p else "—"
            rows.append((cid, c["nome"], c["data_nascimento"],
                         c["telefone"], nome_plano, c["data_inicio"]))
        self._tree = self._table(self._tree_frame, cols, rows)
        tk.Label(self._tree_frame, text=f"Total: {len(clientes)} clientes",
                 bg=BG, fg=TEXT_DIM, font=("Segoe UI", 9)).pack(anchor="e", padx=4)

    def _sel_id(self):
        sel = self._tree.selection() if self._tree else []
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona um cliente.")
            return None
        return self._tree.item(sel[0])["values"][0]

    def _criar(self):
        if not planos:
            messagebox.showerror("Erro", "Cria um plano primeiro.")
            return
        items = [(pid, f"{p[0]}  ({p[1]} treinos · {_ar(p[1]*p[2])} EUR/mês)")
                 for pid, p in planos.items()]
        d = FormDialog(self.app.root, "Novo Cliente", [
            ("nome", "Nome *"),
            ("nasc", "Data de nascimento (DD/MM/AAAA) *"),
            ("tel",  "Telefone (9 dígitos) *"),
        ])
        self.app.root.wait_window(d)
        if not d.result:
            return
        sel = SelectDialog(self.app.root, "Selecciona o Plano", items)
        self.app.root.wait_window(sel)
        if sel.result is None:
            return
        r = d.result
        data_inicio = str(date.today()).replace("-", "/")
        _, codigo = adicionar_cliente(r["nome"], r["nasc"], r["tel"],
                                      sel.result, data_inicio)
        if codigo == 201:
            messagebox.showinfo("Sucesso", f"Cliente '{r['nome']}' adicionado.")
        elif codigo == 409:
            messagebox.showerror("Conflito", "Já existe um cliente com esse nome.")
        elif codigo == 404:
            messagebox.showerror("Erro", "Plano não encontrado.")
        else:
            messagebox.showerror("Erro", "Dados inválidos.")
        self._load()

    def _editar(self):
        cid = self._sel_id()
        if cid is None:
            return
        c = clientes.get(cid)
        if not c:
            return
        d = FormDialog(self.app.root, "Editar Cliente", [
            ("nome", "Nome"),
            ("nasc", "Data nascimento (DD/MM/AAAA)"),
            ("tel",  "Telefone"),
            ("inicio", "Data início (DD/MM/AAAA)"),
        ], values={"nome": c["nome"], "nasc": c["data_nascimento"],
                   "tel": c["telefone"], "inicio": c["data_inicio"]})
        self.app.root.wait_window(d)
        if not d.result:
            return

        id_plano_str = ""
        if planos:
            items = [(pid, f"{p[0]}  ({p[1]} treinos · {_ar(p[1]*p[2])} EUR/mês)")
                     for pid, p in planos.items()]
            if messagebox.askyesno("Plano", "Deseja alterar o plano?"):
                sel = SelectDialog(self.app.root, "Selecciona o Plano", items)
                self.app.root.wait_window(sel)
                if sel.result is not None:
                    id_plano_str = str(sel.result)

        r = d.result
        _, codigo = modificar_cliente(cid, r["nome"], r["nasc"], r["tel"],
                                      id_plano_str, r["inicio"])
        if codigo == 200:
            messagebox.showinfo("Sucesso", "Cliente actualizado.")
        elif codigo == 409:
            messagebox.showerror("Conflito", "Nome já existe.")
        else:
            messagebox.showerror("Erro", f"Erro {codigo}.")
        self._load()

    def _remover(self):
        cid = self._sel_id()
        if cid is None:
            return
        nome = clientes.get(cid, {}).get("nome", cid)
        if not messagebox.askyesno("Confirmar", f"Remover o cliente '{nome}'?"):
            return
        _, codigo = remover_cliente(cid)
        if codigo == 200:
            messagebox.showinfo("Sucesso", "Cliente removido.")
        else:
            messagebox.showerror("Erro", "Cliente não encontrado.")
        self._load()

    def _pesquisar(self):
        termo = simpledialog.askstring("Pesquisar", "Nome a pesquisar:", parent=self.app.root)
        if not termo:
            return
        encontrados, codigo = pesquisar_cliente(termo)
        if codigo == 404 or not encontrados:
            messagebox.showinfo("Resultado", "Nenhum cliente encontrado.")
            return
        texto = "\n".join(f"• {c['nome']}" for c in encontrados)
        messagebox.showinfo(f"Resultados ({len(encontrados)})", texto)


# ─────────────────────────── PAINEL: PLANOS ──────────────────────────────────
class PlanosPanel(BasePanel):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._section("📋  Planos de Treino")
        self._toolbar()
        self._tree_frame = tk.Frame(self, bg=BG)
        self._tree_frame.pack(fill="both", expand=True, padx=24, pady=6)
        self._tree = None
        self._load()

    def _toolbar(self):
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=24, pady=8)
        self._btn(bar, "+ Novo plano", self._criar).pack(side="left", padx=4)
        self._btn(bar, "✏ Editar", self._editar).pack(side="left", padx=4)
        self._danger_btn(bar, "🗑 Remover", self._remover).pack(side="left", padx=4)
        self._btn(bar, "↺ Actualizar", self._load, ACCENT).pack(side="right", padx=4)

    def _load(self):
        for w in self._tree_frame.winfo_children():
            w.destroy()
        cols = ("ID", "Nome", "Treinos/mês", "Preço/treino (€)", "Total mensal (€)", "Clientes")
        rows = []
        for pid, p in planos.items():
            tc = sum(1 for c in clientes.values() if c["id_plano"] == pid)
            rows.append((pid, p[0], p[1], p[2], _ar(p[1]*p[2]), tc))
        self._tree = self._table(self._tree_frame, cols, rows)

    def _sel_id(self):
        sel = self._tree.selection() if self._tree else []
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona um plano.")
            return None
        return self._tree.item(sel[0])["values"][0]

    def _criar(self):
        d = FormDialog(self.app.root, "Novo Plano", [
            ("nome",    "Nome do plano *"),
            ("treinos", "Nº de treinos por mês *"),
            ("preco",   "Preço por treino (€) *"),
        ])
        self.app.root.wait_window(d)
        if not d.result:
            return
        r = d.result
        try:
            nt = int(r["treinos"])
            pt = float(r["preco"])
        except ValueError:
            messagebox.showerror("Erro", "Treinos e preço devem ser números válidos.")
            return
        _, codigo = adicionar_plano(r["nome"], nt, pt)
        if codigo == 201:
            messagebox.showinfo("Sucesso", f"Plano '{r['nome']}' adicionado.")
        else:
            messagebox.showerror("Erro", "Dados inválidos.")
        self._load()

    def _editar(self):
        pid = self._sel_id()
        if pid is None:
            return
        p = planos.get(pid)
        if not p:
            return
        d = FormDialog(self.app.root, "Editar Plano", [
            ("nome",    "Nome"),
            ("treinos", "Nº treinos/mês"),
            ("preco",   "Preço/treino (€)"),
        ], values={"nome": p[0], "treinos": p[1], "preco": p[2]})
        self.app.root.wait_window(d)
        if not d.result:
            return
        r = d.result
        _, codigo = modificar_plano(pid, r["nome"], r["treinos"], r["preco"])
        if codigo == 200:
            messagebox.showinfo("Sucesso", "Plano actualizado.")
        elif codigo == 400:
            messagebox.showerror("Erro", "Dados inválidos.")
        else:
            messagebox.showerror("Erro", f"Erro {codigo}.")
        self._load()

    def _remover(self):
        pid = self._sel_id()
        if pid is None:
            return
        nome = planos.get(pid, ("?",))[0]
        if not messagebox.askyesno("Confirmar", f"Remover o plano '{nome}'?"):
            return
        _, codigo = remover_plano(pid)
        if codigo == 200:
            messagebox.showinfo("Sucesso", "Plano removido.")
        elif codigo == 409:
            messagebox.showerror("Conflito", "Existem clientes com este plano.")
        else:
            messagebox.showerror("Erro", "Plano não encontrado.")
        self._load()


# ─────────────────────────── PAINEL: DESPESAS ────────────────────────────────
class DespesasPanel(BasePanel):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._section("💸  Despesas")
        self._toolbar()
        self._tree_frame = tk.Frame(self, bg=BG)
        self._tree_frame.pack(fill="both", expand=True, padx=24, pady=6)
        self._tree = None
        self._load()

    def _toolbar(self):
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=24, pady=8)
        self._btn(bar, "+ Nova despesa", self._criar).pack(side="left", padx=4)
        self._danger_btn(bar, "🗑 Remover", self._remover).pack(side="left", padx=4)
        self._btn(bar, "↺ Actualizar", self._load, ACCENT).pack(side="right", padx=4)

    def _load(self):
        for w in self._tree_frame.winfo_children():
            w.destroy()
        cols = ("ID", "Descrição", "Valor (€)", "Data")
        rows = [(d[0], d[1], d[2], d[3] if len(d) > 3 else "—") for d in despesas]
        self._tree = self._table(self._tree_frame, cols, rows)
        total = _ar(sum(d[2] for d in despesas))
        tk.Label(self._tree_frame, text=f"Total despesas: {total} €",
                 bg=BG, fg=DANGER, font=("Segoe UI", 10, "bold")).pack(anchor="e", padx=4, pady=4)

    def _sel_id(self):
        sel = self._tree.selection() if self._tree else []
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona uma despesa.")
            return None
        return self._tree.item(sel[0])["values"][0]

    def _criar(self):
        d = FormDialog(self.app.root, "Nova Despesa", [
            ("desc",  "Descrição *"),
            ("valor", "Valor (€) *"),
            ("data",  "Data (DD/MM/AAAA, vazio = hoje)"),
        ])
        self.app.root.wait_window(d)
        if not d.result:
            return
        r = d.result
        try:
            v = float(r["valor"])
        except ValueError:
            messagebox.showerror("Erro", "Valor deve ser um número.")
            return
        data = r["data"] if r["data"] else None
        _, codigo = adicionar_despesa(r["desc"], v, data)
        if codigo == 201:
            messagebox.showinfo("Sucesso", "Despesa adicionada.")
        else:
            messagebox.showerror("Erro", "Dados inválidos.")
        self._load()

    def _remover(self):
        did = self._sel_id()
        if did is None:
            return
        if not messagebox.askyesno("Confirmar", f"Remover despesa ID {did}?"):
            return
        _, codigo = remover_despesa(did)
        if codigo == 200:
            messagebox.showinfo("Sucesso", "Despesa removida.")
        else:
            messagebox.showerror("Erro", "Despesa não encontrada.")
        self._load()


# ─────────────────────────── PAINEL: PAGAMENTOS ──────────────────────────────
class PagamentosPanel(BasePanel):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._section("💳  Pagamentos")
        self._toolbar()
        self._tree_frame = tk.Frame(self, bg=BG)
        self._tree_frame.pack(fill="both", expand=True, padx=24, pady=6)
        self._tree = None
        self._load()

    def _toolbar(self):
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=24, pady=8)
        self._btn(bar, "+ Novo pagamento", self._criar).pack(side="left", padx=4)
        self._danger_btn(bar, "🗑 Remover", self._remover).pack(side="left", padx=4)
        self._btn(bar, "↺ Actualizar", self._load, ACCENT).pack(side="right", padx=4)

    def _load(self):
        for w in self._tree_frame.winfo_children():
            w.destroy()
        pags = listar_pagamentos()
        cols = ("ID", "Cliente", "Plano", "Valor (€)", "Data")
        rows = [(p["id"], p["nome_cliente"], p["plano"],
                 p["valor"], p["dia_pagamento"]) for p in pags]
        self._tree = self._table(self._tree_frame, cols, rows)
        total = _ar(sum(p["valor"] for p in pags))
        tk.Label(self._tree_frame, text=f"Total recebido: {total} €",
                 bg=BG, fg=SUCCESS, font=("Segoe UI", 10, "bold")).pack(anchor="e", padx=4, pady=4)

    def _sel_id(self):
        sel = self._tree.selection() if self._tree else []
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona um pagamento.")
            return None
        return self._tree.item(sel[0])["values"][0]

    def _criar(self):
        if not clientes:
            messagebox.showerror("Erro", "Não existem clientes registados.")
            return
        items = [(cid, c["nome"]) for cid, c in clientes.items()]
        sel = SelectDialog(self.app.root, "Selecciona o Cliente", items)
        self.app.root.wait_window(sel)
        if sel.result is None:
            return
        cid = sel.result
        c = clientes[cid]
        p = planos.get(c["id_plano"])
        nome_plano   = p[0] if p else "Sem plano"
        valor_suger  = _ar(p[1] * p[2]) if p else 0.0

        d = FormDialog(self.app.root, "Novo Pagamento", [
            ("plano", "Plano"),
            ("valor", "Valor (€)"),
            ("data",  "Data (DD/MM/AAAA, vazio = hoje)"),
        ], values={"plano": nome_plano, "valor": valor_suger})
        self.app.root.wait_window(d)
        if not d.result:
            return
        r = d.result
        try:
            v = float(r["valor"])
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido.")
            return
        data = r["data"] if r["data"] else None
        res = criar_pagamento(cid, v, r["plano"] or nome_plano, data)
        if res:
            messagebox.showinfo("Sucesso", "Pagamento adicionado.")
        else:
            messagebox.showerror("Erro", "Erro ao criar pagamento.")
        self._load()

    def _remover(self):
        pid = self._sel_id()
        if pid is None:
            return
        if not messagebox.askyesno("Confirmar", f"Remover pagamento ID {pid}?"):
            return
        if apagar_pagamento(pid):
            messagebox.showinfo("Sucesso", "Pagamento removido.")
        else:
            messagebox.showerror("Erro", "Pagamento não encontrado.")
        self._load()


# ─────────────────────────── PAINEL: RELATÓRIOS ──────────────────────────────
class RelatoriosPanel(BasePanel):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._section("📊  Relatório Financeiro")
        self._build()

    def _build(self):
        self._body = tk.Frame(self, bg=BG)
        self._body.pack(fill="both", expand=True, padx=24, pady=10)

        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=24, pady=8)
        self._btn(bar, "↺ Actualizar", self._refresh, ACCENT).pack(side="left", padx=4)
        self._btn(bar, "▶ Simular Mês", self._simular).pack(side="left", padx=4)

        self._refresh()

    def _refresh(self):
        for w in self._body.winfo_children():
            w.destroy()

        receita    = _calcular_receita_mensal()
        desp_total = _calcular_total_despesas()
        saldo      = _calcular_saldo()

        cards = [
            ("Receita Mensal",      f"{receita} €",         ACCENT),
            ("Total Despesas",      f"{desp_total} €",      DANGER),
            ("Lucro Mensal",        f"{saldo} €",           ACCENT if saldo >= 0 else DANGER),
            ("Lucro Acumulado",     f"{dados.saldo_acumulado} €",
             ACCENT if dados.saldo_acumulado >= 0 else DANGER),
            ("Total Clientes",      str(len(clientes)),     ACCENT2),
            ("Total Planos",        str(len(planos)),       ACCENT2),
        ]

        grid = tk.Frame(self._body, bg=BG)
        grid.pack(fill="x", pady=10)
        for i, (titulo, valor, cor) in enumerate(cards):
            card = tk.Frame(grid, bg=BG2, padx=18, pady=14,
                            highlightthickness=1, highlightbackground=BORDER)
            card.grid(row=i//3, column=i%3, padx=8, pady=8, sticky="nsew")
            tk.Label(card, text=titulo, bg=BG2, fg=TEXT_DIM,
                     font=("Segoe UI", 9)).pack(anchor="w")
            tk.Label(card, text=valor, bg=BG2, fg=cor,
                     font=("Segoe UI", 16, "bold")).pack(anchor="w")
        for col in range(3):
            grid.columnconfigure(col, weight=1)

        # Tabela despesas
        tk.Label(self._body, text="Despesas registadas", bg=BG, fg=TEXT_DIM,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(14, 2))
        cols = ("ID", "Descrição", "Valor (€)", "Data")
        rows = [(d[0], d[1], d[2], d[3] if len(d) > 3 else "—") for d in despesas]
        self._table(self._body, cols, rows, height=6)

    def _simular(self):
        if not messagebox.askyesno("Simular Mês",
                                   "Confirmas a simulação do próximo mês?\n"
                                   "Serão gerados pagamentos para todos os clientes."):
            return
        _, codigo = simular_mes()
        if codigo == 200:
            messagebox.showinfo("Simulação concluída",
                                f"Mês {dados.proximo_mes - 1} simulado.\n"
                                f"Lucro acumulado: {dados.saldo_acumulado} €")
            self._refresh()
        else:
            messagebox.showerror("Erro", "Erro interno ao simular mês.")


# ─────────────────────────── APLICAÇÃO PRINCIPAL ─────────────────────────────
class App:
    PANELS = [
        ("👤 Clientes",       ClientesPanel),
        ("📋 Planos",          PlanosPanel),
        ("💸 Despesas",        DespesasPanel),
        ("💳 Pagamentos",      PagamentosPanel),
        ("📊 Relatórios",      RelatoriosPanel),
    ]

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gestor de Ginásio")
        self.root.geometry("1100x700")
        self.root.configure(bg=BG)
        self.root.minsize(900, 600)

        self._build_ui()
        self._show_panel(0)

    def _build_ui(self):
        # ── Cabeçalho ──────────────────────────────────────────────────────
        header = tk.Frame(self.root, bg=BG2, height=56)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🏋  Gestor de Ginásio", bg=BG2, fg=ACCENT,
                 font=("Segoe UI", 15, "bold"), padx=20).pack(side="left", pady=10)

        self._status_var = tk.StringVar()
        self._update_status()
        tk.Label(header, textvariable=self._status_var, bg=BG2, fg=TEXT_DIM,
                 font=("Segoe UI", 9), padx=20).pack(side="right", pady=10)

        # ── Layout principal ───────────────────────────────────────────────
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True)

        # Sidebar
        sidebar = tk.Frame(main, bg=BG2, width=190)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="MENU", bg=BG2, fg=TEXT_DIM,
                 font=("Segoe UI", 8, "bold"), pady=18).pack(fill="x", padx=16)

        self._nav_btns = []
        for i, (label, _) in enumerate(self.PANELS):
            b = tk.Button(sidebar, text=label, bg=BG2, fg=TEXT,
                          font=("Segoe UI", 10), relief="flat",
                          anchor="w", padx=16, pady=10, cursor="hand2",
                          activebackground=BG3, activeforeground=ACCENT,
                          command=lambda idx=i: self._show_panel(idx))
            b.pack(fill="x")
            self._nav_btns.append(b)

        # Área de conteúdo
        self._content = tk.Frame(main, bg=BG)
        self._content.pack(side="left", fill="both", expand=True)

        self._panels = {}

    def _update_status(self):
        receita = _calcular_receita_mensal()
        saldo   = _calcular_saldo()
        cor     = "↑" if saldo >= 0 else "↓"
        self._status_var.set(
            f"Receita: {receita} €   |   Lucro mensal: {cor} {saldo} €   |   "
            f"Lucro acumulado: {dados.saldo_acumulado} €"
        )
        self.root.after(5000, self._update_status)

    def _show_panel(self, idx):
        for w in self._content.winfo_children():
            w.pack_forget()

        for i, b in enumerate(self._nav_btns):
            b.configure(bg=BG3 if i == idx else BG2,
                        fg=ACCENT if i == idx else TEXT)

        label, PanelClass = self.PANELS[idx]
        if idx not in self._panels:
            p = PanelClass(self._content, self)
            self._panels[idx] = p
        self._panels[idx].pack(fill="both", expand=True)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    carregar_dados()
    App().run()
