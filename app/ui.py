from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox

from app.document_service import build_context, generate_docx
from app.landlord_service import LandlordDetails, load_landlord_details, save_landlord_details
from app.template_service import delete_template, list_templates, read_template, save_template


TEMPLATE_HINT = """Пример шаблона:\n\nДОГОВОР № {contract_number}\nот {contract_date}\n\nАрендодатель: {landlord_name}\nАрендатор: {tenant_name}\nСумма аренды: {rent_amount} ({rent_amount_words})\n"""


class ContractGeneratorApp(ttk.Frame):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root, padding=12)
        self.root = root
        self.root.title("TRUST COMMUNAL — Генератор договоров")
        self.root.geometry("980x700")
        self.pack(fill=tk.BOTH, expand=True)

        self.landlord_vars: dict[str, tk.StringVar] = {}
        self.contract_vars: dict[str, tk.StringVar] = {}

        self._build_ui()
        self._load_landlord_details()
        self._refresh_templates()

    def _build_ui(self) -> None:
        tabs = ttk.Notebook(self)
        tabs.pack(fill=tk.BOTH, expand=True)

        landlord_tab = ttk.Frame(tabs, padding=10)
        templates_tab = ttk.Frame(tabs, padding=10)
        generate_tab = ttk.Frame(tabs, padding=10)

        tabs.add(landlord_tab, text="Мои реквизиты")
        tabs.add(templates_tab, text="Шаблоны договоров")
        tabs.add(generate_tab, text="Генерация договора")

        self._build_landlord_tab(landlord_tab)
        self._build_templates_tab(templates_tab)
        self._build_generate_tab(generate_tab)

    def _build_landlord_tab(self, parent: ttk.Frame) -> None:
        fields = [
            ("landlord_name", "Название арендодателя"),
            ("landlord_director", "Руководитель"),
            ("landlord_basis", "Основание действия"),
            ("landlord_address", "Адрес"),
            ("landlord_details", "Реквизиты"),
        ]

        for idx, (key, label) in enumerate(fields):
            ttk.Label(parent, text=label).grid(row=idx, column=0, sticky="w", padx=4, pady=6)
            var = tk.StringVar()
            ttk.Entry(parent, textvariable=var, width=90).grid(row=idx, column=1, sticky="ew", padx=4, pady=6)
            self.landlord_vars[key] = var

        parent.columnconfigure(1, weight=1)
        ttk.Button(parent, text="Сохранить реквизиты", command=self._save_landlord_details).grid(
            row=len(fields), column=1, sticky="e", pady=12
        )

    def _build_templates_tab(self, parent: ttk.Frame) -> None:
        left = ttk.Frame(parent)
        right = ttk.Frame(parent)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.templates_list = tk.Listbox(left, height=25, width=35)
        self.templates_list.pack(fill=tk.Y, expand=False)
        self.templates_list.bind("<<ListboxSelect>>", self._on_template_selected)

        buttons = ttk.Frame(left)
        buttons.pack(fill=tk.X, pady=8)
        ttk.Button(buttons, text="Обновить", command=self._refresh_templates).pack(fill=tk.X, pady=2)
        ttk.Button(buttons, text="Удалить", command=self._delete_current_template).pack(fill=tk.X, pady=2)

        ttk.Label(right, text="Название шаблона").pack(anchor="w")
        self.template_name_var = tk.StringVar()
        ttk.Entry(right, textvariable=self.template_name_var).pack(fill=tk.X, pady=4)

        ttk.Label(right, text="Текст шаблона").pack(anchor="w")
        self.template_text = tk.Text(right, wrap=tk.WORD, height=24)
        self.template_text.pack(fill=tk.BOTH, expand=True, pady=4)

        actions = ttk.Frame(right)
        actions.pack(fill=tk.X, pady=8)
        ttk.Button(actions, text="Новый шаблон", command=self._new_template).pack(side=tk.LEFT)
        ttk.Button(actions, text="Сохранить шаблон", command=self._save_template).pack(side=tk.RIGHT)

    def _build_generate_tab(self, parent: ttk.Frame) -> None:
        form = ttk.Frame(parent)
        form.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form, text="Шаблон договора").grid(row=0, column=0, sticky="w", padx=4, pady=6)
        self.template_combo = ttk.Combobox(form, state="readonly")
        self.template_combo.grid(row=0, column=1, sticky="ew", padx=4, pady=6)

        fields = [
            ("contract_number", "Номер договора"),
            ("contract_date", "Дата договора"),
            ("tenant_name", "Название арендатора"),
            ("tenant_director", "Руководитель арендатора"),
            ("tenant_basis", "Основание арендатора"),
            ("tenant_address", "Адрес арендатора"),
            ("object_address", "Адрес объекта"),
            ("area_sq_m", "Площадь (кв.м.)"),
            ("rent_amount", "Сумма аренды"),
            ("term_text", "Срок аренды"),
        ]

        for idx, (key, label) in enumerate(fields, start=1):
            ttk.Label(form, text=label).grid(row=idx, column=0, sticky="w", padx=4, pady=6)
            var = tk.StringVar()
            ttk.Entry(form, textvariable=var, width=75).grid(row=idx, column=1, sticky="ew", padx=4, pady=6)
            self.contract_vars[key] = var

        form.columnconfigure(1, weight=1)
        ttk.Button(form, text="Сгенерировать .docx", command=self._generate_document).grid(
            row=len(fields) + 1, column=1, sticky="e", pady=14
        )

    def _load_landlord_details(self) -> None:
        details = load_landlord_details()
        for key, value in details.__dict__.items():
            if key in self.landlord_vars:
                self.landlord_vars[key].set(value)

    def _save_landlord_details(self) -> None:
        payload = {key: var.get().strip() for key, var in self.landlord_vars.items()}
        save_landlord_details(LandlordDetails(**payload))
        messagebox.showinfo("Готово", "Реквизиты сохранены")

    def _refresh_templates(self) -> None:
        templates = list_templates()
        self.templates_list.delete(0, tk.END)
        for item in templates:
            self.templates_list.insert(tk.END, item)

        self.template_combo["values"] = templates
        if templates and not self.template_combo.get():
            self.template_combo.set(templates[0])

    def _on_template_selected(self, _: object = None) -> None:
        selection = self.templates_list.curselection()
        if not selection:
            return
        name = self.templates_list.get(selection[0])
        self.template_name_var.set(name)
        self.template_text.delete("1.0", tk.END)
        self.template_text.insert("1.0", read_template(name))

    def _new_template(self) -> None:
        self.template_name_var.set("")
        self.template_text.delete("1.0", tk.END)
        self.template_text.insert("1.0", TEMPLATE_HINT)

    def _save_template(self) -> None:
        name = self.template_name_var.get().strip()
        if not name:
            messagebox.showwarning("Ошибка", "Введите название шаблона")
            return

        body = self.template_text.get("1.0", tk.END).strip()
        saved_name = save_template(name, body)
        self.template_name_var.set(saved_name)
        self._refresh_templates()
        messagebox.showinfo("Готово", "Шаблон сохранён")

    def _delete_current_template(self) -> None:
        selection = self.templates_list.curselection()
        if not selection:
            messagebox.showwarning("Ошибка", "Выберите шаблон для удаления")
            return

        name = self.templates_list.get(selection[0])
        if not messagebox.askyesno("Подтверждение", f"Удалить шаблон '{name}'?"):
            return

        delete_template(name)
        self._refresh_templates()
        self._new_template()

    def _generate_document(self) -> None:
        template_name = self.template_combo.get().strip()
        if not template_name:
            messagebox.showwarning("Ошибка", "Выберите шаблон")
            return

        template_text = read_template(template_name)
        if not template_text:
            messagebox.showwarning("Ошибка", "Шаблон пустой")
            return

        contract_data = {key: var.get().strip() for key, var in self.contract_vars.items()}
        landlord_data = {key: var.get().strip() for key, var in self.landlord_vars.items()}
        context = build_context(contract_data, landlord_data)

        output = generate_docx(template_text, context, contract_data.get("contract_number", "contract"))
        messagebox.showinfo("Готово", f"Документ сохранён:\n{output}")
