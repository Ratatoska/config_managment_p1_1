"""Точка входа графического и проверочного режимов."""

import sys

from config import parse_args
from shell import Shell
from startup import run_lines, run_startup
from vfs import load_vfs


def run_headless(shell, config):
    """Выполнить команды без GUI для автоматических проверок."""
    if config.startup_path:
        run_startup(shell, config.startup_path, print)
    else:
        run_lines(shell, sys.stdin, print)


def run_gui(shell, config):
    """Создать окно и выполнить стартовый сценарий после открытия."""
    import tkinter as tk
    from gui import TerminalWindow

    root = tk.Tk()
    window = TerminalWindow(root, shell)
    window.write(config.describe())
    if config.startup_path:
        root.after_idle(window.run_script, config.startup_path)
    root.mainloop()


def main(argv=None):
    """Разобрать параметры и запустить выбранный интерфейс."""
    config = parse_args(argv)
    print(config.describe())
    try:
        shell = Shell(vfs=load_vfs(config.vfs_path))
        if config.headless:
            run_headless(shell, config)
        else:
            run_gui(shell, config)
    except (ValueError, OSError) as error:
        print(f'Ошибка запуска: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
