"""Точка входа графического эмулятора оболочки."""

import tkinter as tk

from gui import TerminalWindow
from shell import Shell


def main():
    """Запустить графический сеанс эмулятора."""
    root = tk.Tk()
    TerminalWindow(root, Shell())
    root.mainloop()


if __name__ == '__main__':
    main()
