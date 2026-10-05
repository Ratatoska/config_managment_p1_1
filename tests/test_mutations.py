"""Проверки изменения состояния VFS без записи на диск."""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from permissions import change_mode
from shell import Shell
from vfs import load_vfs


class MutationTests(unittest.TestCase):
    """Проверить создание каталогов, права и неизменность источника."""

    def prepare(self):
        """Загрузить независимую файловую систему."""
        self.shell = Shell(vfs=load_vfs(ROOT / 'examples/vfs.json'))

    def test_mkdir_parents_and_spaces(self):
        """-p создаёт родителей и допускает существующий каталог."""
        self.prepare()
        result = self.shell.execute('mkdir -p "/work/my folder/deep"')
        self.assertFalse(result.error, result.output)
        self.assertEqual(self.shell.vfs.get('/work/my folder').kind, 'dir')
        self.assertFalse(self.shell.execute('mkdir -p /work').error)
        self.assertTrue(self.shell.execute('mkdir /work').error)

    def test_mkdir_missing_parent(self):
        """Без -p отсутствующий родитель вызывает ошибку."""
        self.prepare()
        self.assertTrue(self.shell.execute('mkdir /missing/a').error)
        self.assertNotIn('/missing', self.shell.vfs.nodes)

    def test_numeric_chmod_and_display(self):
        """Права меняются и отображаются командой ls -l."""
        self.prepare()
        self.shell.execute('chmod 600 /docs/readme.txt')
        self.assertEqual(self.shell.vfs.get('/docs/readme.txt').mode, 0o600)
        text = self.shell.execute('ls -l /docs/readme.txt').output
        self.assertIn('-rw-------', text)
        self.assertTrue(self.shell.execute('chmod 888 /docs').error)

    def test_symbolic_chmod(self):
        """Символические операции добавляют, убирают и заменяют биты."""
        self.prepare()
        self.assertEqual(change_mode(0o644, 'u+x,g-w,o='), 0o740)
        self.assertEqual(change_mode(0o700, 'a=rx'), 0o555)
        self.assertEqual(change_mode(0o644, '+x'), 0o755)
        with self.assertRaises(ValueError):
            change_mode(0o644, 'u+z')

    def test_recursive_chmod(self):
        """-R изменяет каталог и всех потомков."""
        self.prepare()
        self.assertFalse(self.shell.execute('chmod -R 700 /docs').error)
        self.assertEqual(self.shell.vfs.get('/docs/notes/lab').mode, 0o700)
        self.assertEqual(self.shell.vfs.get('/docs/readme.txt').mode, 0o700)

    def test_permissions_affect_commands(self):
        """Отсутствие виртуальных прав препятствует чтению и переходу."""
        self.prepare()
        self.shell.execute('chmod 000 /docs')
        self.assertTrue(self.shell.execute('cd /docs').error)
        self.assertTrue(self.shell.execute('ls /docs').error)
        self.assertTrue(self.shell.execute('mkdir /docs/new').error)
        self.assertFalse(self.shell.execute('chmod 755 /docs').error)
        self.assertFalse(self.shell.execute('cd /docs').error)

    def test_json_and_host_remain_unchanged(self):
        """mkdir и chmod не меняют исходный JSON или файлы хоста."""
        self.prepare()
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'vfs.json'
            before = (ROOT / 'examples/vfs.json').read_bytes()
            path.write_bytes(before)
            shell = Shell(vfs=load_vfs(path))
            shell.execute('mkdir /host_must_not_change')
            shell.execute('chmod 700 /docs')
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(list(Path(folder).iterdir()), [path])
            self.assertNotIn('/host_must_not_change', load_vfs(path).nodes)


if __name__ == '__main__':
    unittest.main()
