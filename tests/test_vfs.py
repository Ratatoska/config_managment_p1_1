"""Проверки загрузки и целостности виртуальной файловой системы."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from vfs import Vfs, load_vfs


class VfsTests(unittest.TestCase):
    """Проверить текст, base64, структуру и ошибки JSON."""

    def test_minimal(self):
        """Минимальная VFS состоит только из корня."""
        vfs = load_vfs(ROOT / 'examples/vfs_minimal.json')
        self.assertEqual(vfs.children('/'), [])

    def test_binary_data(self):
        """Двоичные данные base64 декодируются без потери байтов."""
        vfs = load_vfs(ROOT / 'examples/vfs_files.json')
        self.assertEqual(vfs.get('/data.bin').content, b'\x00\x01\x02\xff')

    def test_nested(self):
        """Поддерживается не менее трёх уровней каталогов."""
        vfs = load_vfs(ROOT / 'examples/vfs.json')
        self.assertEqual(vfs.get('/docs/notes/lab/task.txt').content,
                         b'Task 8\n')

    def test_path_normalization(self):
        """Относительные пути не выходят за виртуальный корень."""
        self.assertEqual(Vfs().resolve('../../x', '/docs'), '/x')
        self.assertEqual(Vfs().resolve('~/docs'), '/docs')

    def test_invalid_structure(self):
        """VFS без корня отклоняется."""
        with self.assertRaisesRegex(ValueError, 'корневой'):
            load_vfs(ROOT / 'examples/vfs_invalid.json')

    def test_missing_file(self):
        """Отсутствующий JSON даёт ошибку загрузки."""
        with self.assertRaisesRegex(ValueError, 'загрузки VFS'):
            load_vfs(ROOT / 'examples/missing.json')

    def test_duplicate_and_bad_base64(self):
        """Повторяющиеся пути и неправильный base64 отклоняются."""
        root = {'path': '/', 'type': 'dir'}
        bad = {'path': '/a', 'type': 'file', 'content': '%%%'}
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'test.json'
            for entries in ([root, root], [root, bad]):
                path.write_text(json.dumps({'name': 'x',
                                            'entries': entries}))
                with self.assertRaises(ValueError):
                    load_vfs(path)

    def test_source_unchanged(self):
        """Загрузка не меняет JSON на диске."""
        path = ROOT / 'examples/vfs.json'
        before = path.read_bytes()
        load_vfs(path)
        self.assertEqual(path.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
