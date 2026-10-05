"""Разбор команд оболочки с поддержкой кавычек."""

import shlex


def parse_command(line):
    """Вернуть токены, сохранив пробелы внутри кавычек."""
    return shlex.split(line, comments=False, posix=True)
