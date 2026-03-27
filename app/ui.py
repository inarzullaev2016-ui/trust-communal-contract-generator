from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from pathlib import Path

from app.storage import load_json, save_json
from app.template_service import TemplateService
from app.contract_service import ContractService


LANDLORD_FIELDS = [
    ("landlord_name", "Наименование арендодателя"),
    ("landlord_director", "ФИО руководителя"),
    ("landlord_basis", "Основание действий"),
    ("landlord_address", "Адрес"),
    ("landlord_details", "Реквизиты"),
]

CONTRACT_FIELDS = [
    ("contract_number", "Номер договора"),
    ("contract_date", "Дата договора"),
    ("tenant_name", "Наименование арендатора"),
    ("tenant_director", "ФИО руководителя арендатора"),
    ("tenant_basis", "Основание действий арендатора"),
    ("tenant_address", "Адрес арендатора"),
    ("object_address", "Адрес объекта"),
    ("area_sq_m", "Площадь, м²"),
    ("rent_amount", "Сумма аренды (числом)"),
    ("term_text", "Срок договора"),
]


class ContractGeneratorApp:
    def __init__(
        self,
        root: tk.Tk,
        templates_dir: Path,
        settings_dir: Path,
        generated_dir: Path,
    ) -> None:
        self.root = root
        self.root.title("TRUST COMMUNAL — Генератор договоров")
        self.root.geometry("980x700")

        self.template_service = TemplateService(templates_dir)
        self.contract_service = ContractService(generated_dir)
        self.landlord_file = settings_dir / "landlord.json"

        self.landlord_values = load_json(
            self.landlord_file,
            {
                "landlord_name": "",
                "landlord_director": "",
                "landlord_basis": "",
                "landlord_address": "",
                "landlord_details": "",
            },
        )

        self.landlord_entries: dict[str, tk.Entry] = {}
        self.contract_entries: dict[str, tk.Entry] = {}

        self._build_ui()
        self._refresh_templates()

    def _build_ui(self) -> None:
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_landlord = ttk.Frame(notebook)
        self.tab_templates = ttk.Frame(notebook)
        self.tab_generate = ttk.Frame(notebook)

        notebook.add(self.tab_landlord, text="Мои реквизиты")
        notebook.add(self.tab_templates, text="Шаблоны договоров")
        notebook.add(self.tab_generate, text="Создать договор")

        self._build_landlord_tab()
        self._build_templates_tab()
        self._build_generate_tab()

    def _build_landlord_tab(self) -> None:
        frame = ttk.Frame(self.tab_landlord, padding=16)
        frame.pack(fill="both", expand=True)

        for row, (key, label_text) in enumerate(LANDLORD_FIELDS):
            ttk.Label(frame, text=label_text).grid(row=row, column=0, sticky="w", pady=6)
            entry = ttk.Entry(frame, width=90)
            entry.grid(row=row, column=1, sticky="ew", pady=6, padx=8)
            entry.insert(0, self.landlord_values.get(key, ""))
            self.landlord_entries[key] = entry

        frame.columnconfigure(1, weight=1)

        ttk.Button(
            frame,
            text="Сохранить реквизиты",
            command=self._save_landlord,
        ).grid(row=len(LANDLORD_FIELDS), column=1, sticky="e", pady=12)

    def _build_templates_tab(self) -> None:
        wrapper = ttk.Frame(self.tab_templates, padding=16)
        wrapper.pack(fill="both", expand=True)

        left = ttk.Frame(wrapper)
        left.pack(side="left", fill="y", padx=(0, 12))

        ttk.Label(left, text="Список шаблонов").pack(anchor="w")
        self.templates_listbox = tk.Listbox(left, width=35, height=25)
        self.templates_listbox.pack(fill="y", pady=8)
        self.templates_listbox.bind("<<ListboxSelect>>", self._on_template_select)

        ttk.Button(left, text="Новый", command=self._new_template).pack(fill="x", pady=2)
        ttk.Button(left, text="Сохранить", command=self._save_template).pack(fill="x", pady=2)
        ttk.Button(left, text="Удалить", command=self._delete_template).pack(fill="x", pady=2)

        right = ttk.Frame(wrapper)
        right.pack(side="left", fill="both", expand=True)

        self.current_template_name = tk.StringVar()
        name_frame = ttk.Frame(right)
        name_frame.pack(fill="x", pady=(0, 8))

        ttk.Label(name_frame, text="Имя файла шаблона (.txt)").pack(side="left")
        ttk.Entry(name_frame, textvariable=self.current_template_name, width=45).pack(
            side="left", padx=8
        )

        ttk.Label(
            right,
            text="Доступные переменные: {contract_number}, {contract_date}, {tenant_name}, {tenant_director},\n"
            "{tenant_basis}, {tenant_address}, {object_address}, {area_sq_m}, {rent_amount}, {rent_amount_words},\n"
            "{term_text}, {landlord_name}, {landlord_director}, {landlord_basis}, {landlord_address}, {landlord_details}",
            justify="left",
        ).pack(anchor="w", pady=(0, 8))

        self.template_text = tk.Text(right, wrap="word")
        self.template_text.pack(fill="both", expand=True)

    def _build_generate_tab(self) -> None:
        frame = ttk.Frame(self.tab_generate, padding=16)
        frame.pack(fill="both", expand=True)

        top = ttk.Frame(frame)
        top.pack(fill="x")

        ttk.Label(top, text="Шаблон").pack(side="left")
        self.template_for_generation = tk.StringVar()
        self.template_combo = ttk.Combobox(
            top,
            textvariable=self.template_for_generation,
            state="readonly",
            width=45,
        )
        self.template_combo.pack(side="left", padx=8)

        fields_container = ttk.Frame(frame)
        fields_container.pack(fill="both", expand=True, pady=(14, 0))

        for row, (key, label_text) in enumerate(CONTRACT_FIELDS):
            ttk.Label(fields_container, text=label_text).grid(
                row=row, column=0, sticky="w", pady=4
            )
            entry = ttk.Entry(fields_container, width=80)
            entry.grid(row=row, column=1, sticky="ew", pady=4, padx=8)
            self.contract_entries[key] = entry

        fields_container.columnconfigure(1, weight=1)

        self.status_var = tk.StringVar(value="Готово")
        ttk.Label(frame, textvariable=self.status_var).pack(anchor="w", pady=8)

        ttk.Button(
            frame,
            text="Сформировать .docx",
            command=self._generate_contract,
        ).pack(anchor="e", pady=8)

    def _save_landlord(self) -> None:
        for key in self.landlord_entries:
            self.landlord_values[key] = self.landlord_entries[key].get().strip()
        save_json(self.landlord_file, self.landlord_values)
        messagebox.showinfo("Готово", "Реквизиты сохранены.")

    def _refresh_templates(self) -> None:
        templates = self.template_service.list_templates()
        self.templates_listbox.delete(0, tk.END)
        for name in templates:
            self.templates_listbox.insert(tk.END, name)

        self.template_combo["values"] = templates
        if templates and not self.template_for_generation.get():
            self.template_for_generation.set(templates[0])

    def _on_template_select(self, _event: object) -> None:
        selection = self.templates_listbox.curselection()
        if not selection:
            return
        file_name = self.templates_listbox.get(selection[0])
        self.current_template_name.set(file_name)
        content = self.template_service.load_template(file_name)
        self.template_text.delete("1.0", tk.END)
        self.template_text.insert("1.0", content)

    def _new_template(self) -> None:
        name = simpledialog.askstring(
            "Новый шаблон",
            "Введите имя шаблона (без .txt):",
            parent=self.root,
        )
        if not name:
            return
        file_name = f"{name.strip()}.txt"
        self.current_template_name.set(file_name)
        self.template_text.delete("1.0", tk.END)
        self.template_text.insert("1.0", "Введите текст шаблона договора")

    def _save_template(self) -> None:
        file_name = self.current_template_name.get().strip()
        if not file_name:
            messagebox.showwarning("Ошибка", "Укажите имя файла шаблона.")
            return
        if not file_name.endswith(".txt"):
            file_name += ".txt"

        content = self.template_text.get("1.0", tk.END).strip()
        self.template_service.save_template(file_name, content)
        self._refresh_templates()
        messagebox.showinfo("Готово", f"Шаблон {file_name} сохранён.")

    def _delete_template(self) -> None:
        file_name = self.current_template_name.get().strip()
        if not file_name:
            messagebox.showwarning("Ошибка", "Выберите шаблон для удаления.")
            return
        if messagebox.askyesno("Подтверждение", f"Удалить шаблон {file_name}?"):
            self.template_service.delete_template(file_name)
            self.current_template_name.set("")
            self.template_text.delete("1.0", tk.END)
            self._refresh_templates()

    def _collect_values(self) -> dict[str, str]:
        values = {key: entry.get().strip() for key, entry in self.contract_entries.items()}
        values.update(self.landlord_values)
        return values

    def _generate_contract(self) -> None:
        template_name = self.template_for_generation.get().strip()
        if not template_name:
            messagebox.showwarning("Ошибка", "Выберите шаблон.")
            return

        template_text = self.template_service.load_template(template_name)
        if not template_text:
            messagebox.showwarning("Ошибка", "Шаблон пустой или не найден.")
            return

        values = self._collect_values()

        try:
            output_path = self.contract_service.generate_docx(template_text, values)
        except ValueError:
            messagebox.showerror(
                "Ошибка", "Некорректная сумма аренды. Используйте формат 10000 или 10000.50"
            )
            return

        self.status_var.set(f"Договор создан: {output_path.name}")
        messagebox.showinfo("Готово", f"Файл создан:\n{output_path}")
