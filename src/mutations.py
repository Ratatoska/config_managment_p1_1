"""Команды, изменяющие только объекты VFS в памяти."""

import posixpath

from access import EXECUTE, WRITE, require_access, require_traversal
from permissions import change_mode
from vfs import DIRECTORY_MODE, Node


MIN_CHMOD_ARGUMENTS = 2


def mkdir_arguments(args):
    """Выделить -p и список путей, поддержав разделитель --."""
    parents, paths, options = False, [], True
    for arg in args:
        if options and arg == '--':
            options = False
        elif options and arg == '-p':
            parents = True
        elif options and arg.startswith('-'):
            raise ValueError('mkdir: допустим только флаг -p')
        else:
            paths.append(arg)
    if not paths:
        raise ValueError('mkdir: [-p] путь [путь ...]')
    return parents, paths


def create_directory(vfs, path, user, parents):
    """Создать каталог, при -p предварительно создавая родителей."""
    if path in vfs.nodes:
        if parents and vfs.get(path).kind == 'dir':
            return
        raise ValueError(f'mkdir: путь уже существует: {path}')
    parent = posixpath.dirname(path)
    if parent not in vfs.nodes and parents:
        create_directory(vfs, parent, user, parents)
    if vfs.get(parent).kind != 'dir':
        raise ValueError(f'mkdir: родитель не каталог: {parent}')
    require_traversal(vfs, path, user)
    require_access(vfs, parent, user, WRITE | EXECUTE)
    vfs.nodes[path] = Node('dir', DIRECTORY_MODE, user)


class MutationCommands:
    """Реализовать mkdir и chmod для виртуальной системы."""

    def __init__(self, shell):
        """Сохранить состояние текущего сеанса."""
        self.shell = shell

    def mkdir(self, args):
        """Создать один или несколько виртуальных каталогов."""
        parents, paths = mkdir_arguments(args)
        for path in paths:
            path = self.shell.vfs.resolve(path, self.shell.cwd)
            create_directory(self.shell.vfs, path, self.shell.user, parents)
        return ''

    def chmod(self, args):
        """Изменить права путей, при -R включая вложенные узлы."""
        args = list(args)
        recursive = bool(args and args[0] == '-R')
        if recursive:
            args.pop(0)
        if args and args[0] == '--':
            args.pop(0)
        if len(args) < MIN_CHMOD_ARGUMENTS:
            raise ValueError('chmod: [-R] режим путь [путь ...]')
        mode, *paths = args
        change_mode(DIRECTORY_MODE, mode)
        for path in paths:
            self._chmod_path(path, mode, recursive)
        return ''

    def _chmod_path(self, path, mode, recursive):
        """Применить режим к выбранному пути и его потомкам."""
        vfs = self.shell.vfs
        path = vfs.resolve(path, self.shell.cwd)
        require_traversal(vfs, path, self.shell.user)
        paths = vfs.walk(path) if recursive else [path]
        for target in paths:
            node = vfs.get(target)
            if node.owner != self.shell.user:
                raise ValueError(f'chmod: пользователь не владелец: {target}')
            node.mode = change_mode(node.mode, mode)
