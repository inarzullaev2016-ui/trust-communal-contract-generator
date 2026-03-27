from __future__ import annotations

import tkinter as tk

from app.path_utils import get_app_root, ensure_project_dirs
from app.ui import ContractGeneratorApp


def main() -> None:
    app_root = get_app_root()
    dirs = ensure_project_dirs(app_root)

    root = tk.Tk()
    ContractGeneratorApp(
        root=root,
        templates_dir=dirs["templates"],
        settings_dir=dirs["settings"],
        generated_dir=dirs["generated"],
    )
    root.mainloop()


if __name__ == "__main__":
    main()
