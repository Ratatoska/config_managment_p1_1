"""Восьмеричные и символические режимы команды chmod."""

import re

from vfs import MODE_PATTERN, parse_mode


SHIFTS = {'u': 6, 'g': 3, 'o': 0}
RIGHTS = {'r': 4, 'w': 2, 'x': 1}
PERMISSION_MASK = 0o7
CHANGE_PATTERN = r'([ugoa]*)([+=-])([rwx]*)'


def change_mode(old, value):
    """Применить восьмеричное значение либо список изменений ugoa/rwx."""
    if re.fullmatch(MODE_PATTERN, value):
        return parse_mode(value)
    for part in value.split(','):
        match = re.fullmatch(CHANGE_PATTERN, part)
        if match is None:
            raise ValueError('chmod: неверный режим прав')
        who, operation, rights = match.groups()
        groups = 'ugo' if not who or 'a' in who else who
        bits = sum(RIGHTS[right] for right in set(rights))
        old = apply_change(old, groups, operation, bits)
    return old


def apply_change(mode, groups, operation, bits):
    """Добавить, удалить или заменить биты выбранных классов."""
    for group in set(groups):
        shift = SHIFTS[group]
        selected = bits << shift
        if operation == '+':
            mode |= selected
        elif operation == '-':
            mode &= ~selected
        else:
            mode = (mode & ~(PERMISSION_MASK << shift)) | selected
    return mode
