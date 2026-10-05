"""Параметры запуска эмулятора."""

import argparse
from dataclasses import dataclass
from pathlib import Path


DEFAULT_VFS = Path(__file__).resolve().parents[1] / 'examples/vfs.json'


@dataclass(frozen=True)
class Config:
    """Пути входных файлов и выбор режима без окна."""

    vfs_path: Path = DEFAULT_VFS
    startup_path: Path | None = None
    headless: bool = False

    def describe(self):
        """Вернуть все параметры в виде ключ-значение."""
        startup = self.startup_path or '(не задан)'
        return (f'vfs={self.vfs_path}\nstartup={startup}\n'
                f'headless={self.headless}')


def parse_args(argv=None):
    """Прочитать необязательные пути VFS и стартового сценария."""
    parser = argparse.ArgumentParser(description='Эмулятор, вариант 8')
    parser.add_argument('vfs', nargs='?', type=Path, default=DEFAULT_VFS)
    parser.add_argument('startup', nargs='?', type=Path)
    parser.add_argument('--headless', action='store_true',
                        help='выполнить сценарий или stdin без окна')
    args = parser.parse_args(argv)
    return Config(args.vfs, args.startup, args.headless)
