"""Виртуальная файловая система, хранимая только в памяти."""

import base64
import binascii
import getpass
import json
import posixpath
import re
from dataclasses import dataclass


DIRECTORY_MODE = 0o755
FILE_MODE = 0o644
MODE_PATTERN = r'0?[0-7]{3}'


@dataclass
class Node:
    """Каталог либо файл с содержимым и виртуальными правами."""

    kind: str
    mode: int
    owner: str
    content: bytes = b''


class Vfs:
    """Хранить узлы и разрешать UNIX-пути без доступа к диску."""

    def __init__(self, name='memory', nodes=None):
        """Создать систему с корневым каталогом."""
        self.name = name
        self.nodes = nodes if nodes is not None else {
            '/': Node('dir', DIRECTORY_MODE, getpass.getuser()),
        }

    def resolve(self, path, cwd='/'):
        """Нормализовать абсолютный или относительный путь внутри VFS."""
        if not path or '\x00' in path:
            raise ValueError('Некорректный виртуальный путь')
        if path == '~' or path.startswith('~/'):
            path = '/' + path.removeprefix('~').lstrip('/')
        joined = posixpath.join(cwd, path)
        return '/' + posixpath.normpath(joined).lstrip('/')

    def get(self, path, cwd='/'):
        """Получить узел или сообщить об отсутствующем пути."""
        resolved = self.resolve(path, cwd)
        if resolved not in self.nodes:
            raise ValueError(f'Путь не найден: {resolved}')
        return self.nodes[resolved]

    def children(self, path):
        """Вернуть пути непосредственных потомков каталога."""
        node = self.get(path)
        if node.kind != 'dir':
            raise ValueError(f'Не каталог: {path}')
        return sorted(key for key in self.nodes
                      if key != path and posixpath.dirname(key) == path)

    def walk(self, path):
        """Вернуть узел и все вложенные пути в устойчивом порядке."""
        self.get(path)
        prefix = path.rstrip('/') + '/'
        return sorted(key for key in self.nodes
                      if key == path or key.startswith(prefix))


def parse_mode(value):
    """Проверить трёхзначные восьмеричные права от 000 до 777."""
    if not isinstance(value, str) or not re.fullmatch(MODE_PATTERN, value):
        raise ValueError('Права должны иметь вид 755 или 0755')
    return int(value, 8)


def parse_entry(entry):
    """Проверить одну запись JSON и декодировать содержимое файла."""
    if not isinstance(entry, dict):
        raise ValueError('Запись VFS должна быть объектом')
    path, kind = entry.get('path'), entry.get('type')
    validate_entry_path(path)
    if kind not in ('dir', 'file'):
        raise ValueError(f'Неизвестный тип узла: {kind}')
    default = '755' if kind == 'dir' else '644'
    mode = parse_mode(entry.get('mode', default))
    owner = entry.get('owner', getpass.getuser())
    if not isinstance(owner, str) or not owner:
        raise ValueError('owner должен быть непустой строкой')
    content = decode_content(entry.get('content', ''))
    if kind == 'dir' and content:
        raise ValueError('У каталога не должно быть содержимого')
    return path, Node(kind, mode, owner, content)


def validate_entry_path(path):
    """Отклонить некорректные или ненормализованные пути JSON."""
    if not isinstance(path, str) or not path.startswith('/'):
        raise ValueError('path должен быть абсолютным UNIX-путём')
    if '\x00' in path or Vfs().resolve(path) != path:
        raise ValueError(f'Путь должен быть нормализован: {path!r}')


def decode_content(content):
    """Декодировать строгий base64; текст и двоичные данные равноправны."""
    if not isinstance(content, str):
        raise ValueError('content должен быть строкой base64')
    try:
        return base64.b64decode(content, validate=True)
    except (binascii.Error, ValueError) as error:
        raise ValueError('Некорректный base64 в content') from error


def validate_tree(nodes):
    """Проверить корень и существование всех родительских каталогов."""
    if '/' not in nodes or nodes['/'].kind != 'dir':
        raise ValueError('VFS должна содержать корневой каталог /')
    for path in nodes:
        if path == '/':
            continue
        parent = posixpath.dirname(path)
        if parent not in nodes or nodes[parent].kind != 'dir':
            raise ValueError(f'Не найден родительский каталог: {parent}')


def load_vfs(path):
    """Загрузить JSON без распаковки и изменения физической системы."""
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(data, dict):
            raise ValueError('JSON VFS должен быть объектом')
        name, entries = data.get('name'), data.get('entries')
        if not isinstance(name, str) or not name.strip():
            raise ValueError('VFS должна иметь непустое имя name')
        if not isinstance(entries, list):
            raise ValueError('entries должен быть массивом')
        nodes = {}
        for entry in entries:
            key, node = parse_entry(entry)
            if key in nodes:
                raise ValueError(f'Повторяющийся путь: {key}')
            nodes[key] = node
        validate_tree(nodes)
        return Vfs(name, nodes)
    except (OSError, UnicodeError, ValueError) as error:
        raise ValueError(f'Ошибка загрузки VFS: {error}') from error
