"""Последовательное выполнение команд стартового сценария."""


def run_lines(shell, lines, emit):
    """Показывать ввод и вывод, продолжая работу после ошибок."""
    for number, line in enumerate(lines, start=1):
        line = line.rstrip('\r\n')
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        emit(shell.prompt + line)
        result = shell.execute(line)
        if result.error:
            emit(f'Строка {number}: {result.output}')
        elif result.output:
            emit(result.output)
        if result.exit_requested:
            return True
    return False


def run_startup(shell, path, emit):
    """Прочитать UTF-8 сценарий и выполнить его команды."""
    try:
        with path.open(encoding='utf-8') as stream:
            return run_lines(shell, stream, emit)
    except (OSError, UnicodeError) as error:
        raise ValueError(f'Не удалось прочитать сценарий: {error}') from error
