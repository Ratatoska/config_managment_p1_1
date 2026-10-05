"""Проверки параметров запуска и стартового сценария."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from config import parse_args
from shell import Shell
from startup import run_lines, run_startup


class ConfigTests(unittest.TestCase):
    """Проверить передачу параметров и обработку сценария."""

    def test_parameters(self):
        """Оба пути передаются через командную строку."""
        config = parse_args(['my vfs.json', 'startup.txt', '--headless'])
        self.assertEqual(config.vfs_path, Path('my vfs.json'))
        self.assertEqual(config.startup_path, Path('startup.txt'))
        self.assertTrue(config.headless)
        self.assertIn('startup=startup.txt', config.describe())

    def test_script_continues_after_errors(self):
        """Ошибочная команда не препятствует следующей строке."""
        output = []
        run_lines(Shell(), ['unknown', 'ls /'], output.append)
        self.assertIn('Строка 1:', '\n'.join(output))
        self.assertIn('ls /', '\n'.join(output))

    def test_exit_stops_script(self):
        """После exit следующие команды не исполняются."""
        output = []
        self.assertTrue(run_lines(Shell(), ['exit', 'ls'], output.append))
        self.assertFalse(any('ls' in line for line in output))

    def test_comments_and_blank_lines(self):
        """Пустые строки и полнострочные комментарии пропускаются."""
        output = []
        run_lines(Shell(), ['', ' # comment', 'exit'], output.append)
        self.assertEqual(len(output), 2)

    def test_missing_script(self):
        """Отсутствующий сценарий сообщает понятную ошибку."""
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'missing.txt'
            with self.assertRaisesRegex(ValueError, 'сценарий'):
                run_startup(Shell(), path, print)


if __name__ == '__main__':
    unittest.main()
