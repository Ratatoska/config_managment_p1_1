"""Проверки этапа REPL."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from parser import parse_command
from shell import Shell


class ReplTests(unittest.TestCase):
    """Проверить кавычки, заглушки и обработку ошибок."""

    def test_quotes(self):
        """Пробелы в кавычках остаются частью одного аргумента."""
        self.assertEqual(parse_command('cd "my folder"'),
                         ['cd', 'my folder'])

    def test_empty_argument(self):
        """Пустые кавычки создают пустой аргумент."""
        self.assertEqual(parse_command("ls ''"), ['ls', ''])

    def test_stubs(self):
        """Заглушка сообщает имя и аргументы."""
        self.assertIn("['my folder']", Shell().execute(
            'cd "my folder"').output)

    def test_unknown_command(self):
        """Неизвестная команда возвращает ошибку."""
        self.assertTrue(Shell().execute('unknown').error)

    def test_unclosed_quote(self):
        """Незакрытая кавычка не завершает сеанс аварийно."""
        self.assertTrue(Shell().execute('ls "broken').error)

    def test_exit(self):
        """exit без аргументов запрашивает завершение."""
        self.assertTrue(Shell().execute('exit').exit_requested)
        self.assertTrue(Shell().execute('exit now').error)

    def test_blank_line(self):
        """Пустая строка не является ошибкой."""
        self.assertFalse(Shell().execute(' ').error)


if __name__ == '__main__':
    unittest.main()
