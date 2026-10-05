"""Проверки виртуальных прав пользователя; права ОС не меняются."""

import posixpath


READ = 0o4
WRITE = 0o2
EXECUTE = 0o1
OWNER_SHIFT = 6
PERMISSION_MASK = 0o7


def require_access(vfs, path, user, required):
    """Проверить биты владельца либо остальных пользователей."""
    node = vfs.get(path)
    shift = OWNER_SHIFT if node.owner == user else 0
    permissions = (node.mode >> shift) & PERMISSION_MASK
    if permissions & required != required:
        raise ValueError(f'Доступ запрещён: {path}')


def require_traversal(vfs, path, user):
    """Проверить исполнение всех родительских каталогов пути."""
    parent = posixpath.dirname(path)
    while True:
        require_access(vfs, parent, user, EXECUTE)
        if parent == '/':
            return
        parent = posixpath.dirname(parent)
