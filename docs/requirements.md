# Соответствие заданию

Автор: Комаров В.Ю. Группа: ИКБО-41-25. Вариант: 8.

Основание — предоставленный файл «ИКБО-41-25.pdf»: требования
к организации проекта на страницах 4–7, вариант 8 на страницах 29–31.

| Требование | Реализация | Проверка |
| --- | --- | --- |
| Графический интерфейс; имя VFS в заголовке | `src/gui.py` | `tests/test_gui.py` |
| Команды с одинарными и двойными кавычками | `src/parser.py` | `tests/test_repl.py` |
| Заглушки `ls`, `cd`, завершение `exit` на первом этапе | Тег `stage-1`, `src/shell.py` | Тесты в соответствующем коммите |
| Позиционные параметры VFS и стартового сценария; отладочный вывод | `src/config.py`, `src/main.py` | `tests/test_config.py`, `scripts/run_parameters.bat` и три Bash-сценария запуска |
| Последовательные команды сценария; продолжение после ошибки | `src/startup.py` | `tests/test_config.py`, `examples/startup_stage2.txt` |
| JSON VFS, бинарные данные в base64, работа в памяти | `src/vfs.py` | `tests/test_vfs.py` |
| Минимальная VFS, несколько файлов, не менее трёх уровней вложенности | `examples/vfs_minimal.json`, `vfs_files.json`, `vfs.json` | `scripts/run_vfs_variants.sh` и `.bat` |
| Основные команды `ls`, `cd` | `src/commands.py` | `tests/test_commands.py` |
| Дополнительные команды `find`, `cal`, `who` | `src/commands.py` | `tests/test_commands.py`, `examples/startup_stage4.txt` |
| Изменяющие команды `mkdir`, `chmod` | `src/mutations.py`, `permissions.py`, `access.py` | `tests/test_mutations.py`, `examples/startup_stage5.txt` |
| Не менять входную VFS и не распаковывать её на диск | Изменяются только объекты `Node` в памяти | Проверка неизменности исходного JSON и повторной загрузки в `tests/test_mutations.py` |
| Демонстрация режимов команд и ошибок | `examples/startup_stage4.txt`, `startup_stage5.txt` | OS-сценарии этапов 4 и 5 |
| Отдельный коммит для каждого этапа | Пять коммитов и тегов `stage-1` … `stage-5` | `git log --reverse --format=fuller` |
| README с настройками, запуском, тестами и примерами | `README.md` | Просмотр README |
| Исходники, тесты, скрипты запуска и игнорирование служебных файлов | `src`, `tests`, `run.sh`, `run.bat`, `.gitignore` | Просмотр отслеживаемых файлов Git |
| Ограничения оформления Python | Небольшие функции с docstring и именованными константами | `scripts/check_quality.py` |

Поддерживаемые режимы команд и границы учебной модели прав описаны
в README. `--headless` добавлен для автоматических проверок;
обычный запуск открывает графическое окно.
