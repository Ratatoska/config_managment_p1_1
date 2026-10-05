"""Проверки ограничений оформления из методички."""

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAX_LINES = 1000
MAX_WIDTH = 80
MAX_FUNCTION_LINES = 40
MAX_ARGUMENTS = 7
MAX_COMPLEXITY = 10


def complexity(function):
    """Оценить ветвления, циклы, логические операции и генераторы."""
    score = 1
    for node in ast.walk(function):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.IfExp,
                             ast.ExceptHandler, ast.Assert)):
            score += 1
        elif isinstance(node, ast.BoolOp):
            score += len(node.values) - 1
        elif isinstance(node, ast.comprehension):
            score += 1 + len(node.ifs)
    return score


def check_functions(tree, path):
    """Проверить длину, аргументы, docstring и ветвления функций."""
    errors = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        label = f'{path}:{node.lineno}: {node.name}'
        if node.end_lineno - node.lineno + 1 > MAX_FUNCTION_LINES:
            errors.append(f'{label}: функция длиннее 40 строк')
        count = len(node.args.args) + len(node.args.kwonlyargs)
        if count > MAX_ARGUMENTS:
            errors.append(f'{label}: более 7 аргументов')
        if ast.get_docstring(node) is None:
            errors.append(f'{label}: отсутствует docstring')
        score = complexity(node)
        if score > MAX_COMPLEXITY:
            errors.append(f'{label}: сложность {score} > 10')
    return errors


def check_file(path):
    """Проверить размер файла, строки и его Python-функции."""
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    relative = path.relative_to(ROOT)
    errors = []
    if len(lines) > MAX_LINES:
        errors.append(f'{relative}: файл длиннее 1000 строк')
    for number, line in enumerate(lines, start=1):
        if len(line) > MAX_WIDTH:
            errors.append(f'{relative}:{number}: строка длиннее 80 символов')
    tree = ast.parse(text)
    errors.extend(check_functions(tree, relative))
    return errors


def main():
    """Проверить Python-код проекта и вернуть код результата."""
    errors = []
    for directory in ('src', 'tests', 'scripts'):
        for path in sorted((ROOT / directory).glob('*.py')):
            errors.extend(check_file(path))
    if errors:
        print('\n'.join(errors))
        return 1
    print('Оформление Python-кода: все проверки пройдены.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
