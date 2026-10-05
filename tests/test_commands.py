"""Функциональные проверки основных команд."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from shell import Shell
from vfs import load_vfs


class CommandTests(unittest.TestCase):
    """Проверить результаты команд и сохранность состояния при ошибках."""

    def prepare(self):
        """Загрузить независимую VFS для каждого теста."""
        self.shell = Shell(vfs=load_vfs(ROOT / 'examples/vfs.json'))

    def test_ls_hidden_and_long(self):
        """Флаги управляют скрытыми файлами и форматом прав."""
        self.prepare()
        self.assertNotIn('.hidden', self.shell.execute('ls').output)
        text = self.shell.execute('ls -la').output
        self.assertIn('.hidden', text)
        self.assertIn('drwxr-xr-x', text)
        self.assertIn('-rw-r--r--', text)

    def test_ls_file_and_error(self):
        """Можно вывести файл, неизвестный флаг возвращает ошибку."""
        self.prepare()
        self.assertEqual(self.shell.execute('ls /docs/readme.txt').output,
                         'readme.txt')
        self.assertTrue(self.shell.execute('ls -z').error)
        self.assertTrue(self.shell.execute('ls /missing').error)

    def test_cd_relative_and_previous(self):
        """Переходы по относительным путям обновляют приглашение."""
        self.prepare()
        self.shell.execute('cd /docs')
        self.shell.execute('cd notes/lab')
        self.assertEqual(self.shell.cwd, '/docs/notes/lab')
        self.assertEqual(self.shell.execute('cd -').output, '/docs')
        self.assertIn(':/docs$ ', self.shell.prompt)

    def test_failed_cd_preserves_directory(self):
        """Ошибочный переход не меняет cwd."""
        self.prepare()
        self.shell.execute('cd /docs')
        self.assertTrue(self.shell.execute('cd readme.txt').error)
        self.assertEqual(self.shell.cwd, '/docs')
        self.shell.execute('cd')
        self.assertEqual(self.shell.cwd, '/')

    def test_find_name_type_and_depth(self):
        """find рекурсивно фильтрует имена и тип узла."""
        self.prepare()
        text = self.shell.execute('find / -name "*.txt" -type f').output
        self.assertIn('/docs/notes/lab/task.txt', text)
        self.assertNotIn('/binary.bin', text)
        self.assertTrue(self.shell.execute('find / -type x').error)

    def test_cal(self):
        """Календарь содержит ожидаемый месяц и отклоняет неверные даты."""
        self.prepare()
        text = self.shell.execute('cal 10 2026').output
        self.assertIn('October 2026', text)
        self.assertIn('31', text)
        self.assertIn('December', self.shell.execute('cal 2026').output)
        self.assertTrue(self.shell.execute('cal 13 2026').error)
        self.assertTrue(self.shell.execute('cal abc').error)

    def test_who(self):
        """who выводит реальные данные текущего пользователя и узла."""
        self.prepare()
        text = self.shell.execute('who').output
        self.assertIn(self.shell.user, text)
        self.assertIn(self.shell.host, text)
        self.assertTrue(self.shell.execute('who extra').error)


if __name__ == '__main__':
    unittest.main()
