"""Интеграционные проверки графического терминала."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

import tkinter as tk
from gui import TerminalWindow
from shell import Shell


class GuiTests(unittest.TestCase):
    """Проверить реальное окно без показа на экране."""

    def prepare(self):
        """Создать скрытое окно, если Tk доступен."""
        try:
            self.root = tk.Tk()
        except tk.TclError as error:
            self.skipTest(str(error))
        self.addCleanup(self.root.destroy)
        self.root.withdraw()
        self.window = TerminalWindow(self.root, Shell('test-vfs'))


    def test_title(self):
        """Имя VFS включено в заголовок."""
        self.prepare()
        self.assertIn('test-vfs', self.root.title())

    def test_command_error_is_visible(self):
        """Ошибочный ввод отображается и очищает поле ввода."""
        self.prepare()
        self.window.entry.insert(0, 'unknown')
        self.window.submit()
        text = self.window.output.get('1.0', 'end')
        self.assertIn('unknown', text)
        self.assertIn('команда не найдена', text)
        self.assertEqual(self.window.entry.get(), '')


if __name__ == '__main__':
    unittest.main()
