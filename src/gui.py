"""Графический терминал на Tkinter."""

import tkinter as tk
from tkinter import scrolledtext


class TerminalWindow:
    """Показывать историю ввода и вывода и принимать команды."""

    def __init__(self, root, shell):
        """Создать окно терминала с именем VFS в заголовке."""
        self.root = root
        self.shell = shell
        root.title(f'Эмулятор оболочки — {shell.vfs_name}')
        root.geometry('880x560')
        self.output = scrolledtext.ScrolledText(
            root, font=('Consolas', 11), bg='#17202a', fg='#ecf0f1',
            insertbackground='white', state='disabled', wrap='word',
        )
        self.output.pack(fill='both', expand=True, padx=12, pady=12)
        row = tk.Frame(root)
        row.pack(fill='x', padx=12, pady=(0, 12))
        self.prompt_label = tk.Label(row, text=shell.prompt)
        self.prompt_label.pack(side='left')
        self.entry = tk.Entry(row, font=('Consolas', 11))
        self.entry.pack(side='left', fill='x', expand=True)
        self.entry.bind('<Return>', self.submit)
        self.entry.focus_set()
        self.write('Введите команду. Для завершения: exit')

    def write(self, text):
        """Дополнить историю терминала и прокрутить её вниз."""
        if not text:
            return
        self.output.configure(state='normal')
        self.output.insert('end', text + '\n')
        self.output.configure(state='disabled')
        self.output.see('end')

    def submit(self, event=None):
        """Обработать Enter и закрыть окно по команде exit."""
        line = self.entry.get()
        self.entry.delete(0, 'end')
        self.write(self.shell.prompt + line)
        result = self.shell.execute(line)
        self.write(result.output)
        self.prompt_label.configure(text=self.shell.prompt)
        if result.exit_requested:
            self.root.destroy()
