"""Независимое от интерфейса ядро эмулятора."""

import getpass
import socket
from dataclasses import dataclass

from parser import parse_command


@dataclass
class CommandResult:
    """Результат команды и признаки ошибки или завершения."""

    output: str = ''
    error: bool = False
    exit_requested: bool = False


class Shell:
    """Выполнять команды и сохранять состояние сеанса."""

    def __init__(self, vfs_name='memory'):
        """Создать сеанс с указанным именем виртуальной системы."""
        self.vfs_name = vfs_name
        self.cwd = '/'
        self.user = getpass.getuser()
        self.host = socket.gethostname()

    @property
    def prompt(self):
        """Сформировать приглашение для текущего каталога."""
        return f'{self.user}@{self.host}:{self.cwd}$ '

    def execute(self, line):
        """Выполнить строку, возвращая ошибки без исключений в GUI."""
        try:
            tokens = parse_command(line)
            if not tokens:
                return CommandResult()
            name, *args = tokens
            if name == 'exit':
                return self._exit(args)
            if name in ('ls', 'cd'):
                return CommandResult(f'{name}: аргументы = {args!r}')
            return CommandResult(f'{name}: команда не найдена', error=True)
        except ValueError as error:
            return CommandResult(f'Ошибка: {error}', error=True)

    def _exit(self, args):
        """Завершить сеанс, если команда вызвана без аргументов."""
        if args:
            raise ValueError('exit не принимает аргументы')
        return CommandResult('Сеанс завершён.', exit_requested=True)
