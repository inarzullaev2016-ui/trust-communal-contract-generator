from __future__ import annotations

import tkinter as tk

from app.paths import ensure_runtime_dirs
from app.ui import ContractGeneratorApp


def main() -> None:
    ensure_runtime_dirs()
    root = tk.Tk()
    ContractGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
