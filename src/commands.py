"""Основные команды UNIX-подобного эмулятора."""

import calendar
import fnmatch
import posixpath
import stat
from datetime import date


ONE_ARGUMENT = 1
TWO_ARGUMENTS = 2
MIN_MONTH = 1
MAX_MONTH = 12
MIN_YEAR = 1
MAX_YEAR = 9999


def ls_arguments(args):
    """Разобрать флаги -a, -l и один необязательный путь."""
    flags, paths = set(), []
    options = True
    for arg in args:
        if options and arg == '--':
            options = False
        elif options and arg.startswith('-') and arg != '-':
            if not set(arg[1:]) <= {'a', 'l'}:
                raise ValueError('ls: допустимы только -a и -l')
            flags.update(arg[1:])
        else:
            paths.append(arg)
    if len(paths) > ONE_ARGUMENT:
        raise ValueError('ls: укажите не более одного пути')
    return flags, paths[0] if paths else '.'


def find_arguments(args):
    """Разобрать путь, маску -name и тип -type f или d."""
    values = list(args)
    path = '.'
    if values and not values[0].startswith('-'):
        path = values.pop(0)
    options = {'-name': '*', '-type': None}
    while values:
        option = values.pop(0)
        if option not in options or not values:
            raise ValueError('find: путь [-name маска] [-type f|d]')
        options[option] = values.pop(0)
    if options['-type'] not in (None, 'f', 'd'):
        raise ValueError('find: -type должен быть f или d')
    return path, options['-name'], options['-type']


class BasicCommands:
    """Выполнять чтение VFS и информационные команды."""

    def __init__(self, shell):
        """Сохранить ссылку на состояние сеанса."""
        self.shell = shell

    def ls(self, args):
        """Показать содержимое каталога либо указанный файл."""
        flags, path = ls_arguments(args)
        path = self.shell.vfs.resolve(path, self.shell.cwd)
        node = self.shell.vfs.get(path)
        if node.kind == 'file':
            return self._ls_entry(path, posixpath.basename(path), flags)
        entries = [(key, posixpath.basename(key))
                   for key in self.shell.vfs.children(path)]
        if 'a' in flags:
            parent = self.shell.vfs.resolve('..', path)
            entries = [(path, '.'), (parent, '..')] + entries
        else:
            entries = [(key, name) for key, name in entries
                       if not name.startswith('.')]
        return '\n'.join(self._ls_entry(key, name, flags)
                         for key, name in entries)

    def _ls_entry(self, path, name, flags):
        """Оформить одно имя либо строку с правами, владельцем и размером."""
        if 'l' not in flags:
            return name
        node = self.shell.vfs.get(path)
        kind = stat.S_IFDIR if node.kind == 'dir' else stat.S_IFREG
        mode = stat.filemode(kind | node.mode)
        return f'{mode} {node.owner} {len(node.content):>5} {name}'

    def cd(self, args):
        """Изменить текущий каталог; поддержать /, .., ~ и cd -."""
        if len(args) > ONE_ARGUMENT:
            raise ValueError('cd: укажите не более одного пути')
        path = args[0] if args else '/'
        previous = path == '-'
        if previous:
            path = self.shell.previous_cwd
        path = self.shell.vfs.resolve(path, self.shell.cwd)
        if self.shell.vfs.get(path).kind != 'dir':
            raise ValueError(f'cd: не каталог: {path}')
        self.shell.previous_cwd, self.shell.cwd = self.shell.cwd, path
        return path if previous else ''

    def find(self, args):
        """Найти пути рекурсивно по имени и типу в VFS."""
        path, pattern, kind = find_arguments(args)
        path = self.shell.vfs.resolve(path, self.shell.cwd)
        matches = []
        for key in self.shell.vfs.walk(path):
            node = self.shell.vfs.get(key)
            if kind and node.kind[0] != kind:
                continue
            if fnmatch.fnmatchcase(posixpath.basename(key), pattern):
                matches.append(key)
        return '\n'.join(matches)

    def cal(self, args):
        """Показать текущий месяц, заданный месяц или весь год."""
        today = date.today()
        month, year = today.month, today.year
        if len(args) > TWO_ARGUMENTS:
            raise ValueError('cal: [год] или [месяц год]')
        if len(args) == ONE_ARGUMENT:
            year = int(args[0])
        elif len(args) == TWO_ARGUMENTS:
            month, year = map(int, args)
        if not MIN_YEAR <= year <= MAX_YEAR:
            raise ValueError('cal: год должен быть от 1 до 9999')
        if not MIN_MONTH <= month <= MAX_MONTH:
            raise ValueError('cal: месяц должен быть от 1 до 12')
        printer = calendar.TextCalendar(firstweekday=calendar.MONDAY)
        if len(args) == ONE_ARGUMENT:
            return printer.formatyear(year).rstrip()
        return printer.formatmonth(year, month).rstrip()

    def who(self, args):
        """Показать пользователя и узел текущего сеанса эмулятора."""
        if args:
            raise ValueError('who не принимает аргументы')
        return f'{self.shell.user}\t{self.shell.host}'
