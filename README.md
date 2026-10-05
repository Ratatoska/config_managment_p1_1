# Эмулятор командной строки

**Вариант 8 · Комаров В.Ю. · ИКБО-41-25**

Практическая работа № 1 по конфигурационному управлению.
Графический терминал на Python и Tkinter.

## Что сделано — этапы 1 и 2

- Окно с именем VFS в заголовке.
- Парсер с поддержкой одинарных и двойных кавычек.
- Заглушки `ls` и `cd` выводят имя команды и аргументы.
- `exit` завершает сеанс.
- Ошибки команд и кавычек выводятся в терминал.
- Пути к VFS и стартовому скрипту задаются при запуске.
- Все параметры выводятся при старте.
- Стартовый скрипт показывает ввод и вывод и пропускает ошибки.
- Для OS-скриптов и проверок доступен режим `--headless`.

## Запуск

Нужен Python 3.10 или новее с Tkinter. Сборка не требуется.
Внешние библиотеки не используются.

```bash
python src/main.py
python src/main.py examples/vfs.json examples/startup_stage2.txt
python src/main.py examples/vfs.json examples/startup_stage2.txt --headless
```

Linux и Git Bash: `bash run.sh`. Windows: `run.bat`.
VFS на этапе 2 обозначается путём, её содержимое ещё не загружается.

## Параметры

```text
main.py [путь_VFS] [путь_стартового_скрипта] [--headless]
```

По умолчанию путь VFS — `examples/vfs.json` внутри проекта.
Сценарий необязателен; в GUI команды вводятся вручную, а `--headless`
читает stdin. Строки, начинающиеся с `#`, и пустые строки пропускаются.
`exit` прекращает выполнение сценария и закрывает GUI.

## Тесты

```bash
python -m unittest discover -s tests -v
```

Проверка параметров средствами ОС:

```bash
bash scripts/run_no_args.sh
bash scripts/run_with_vfs.sh
bash scripts/run_with_script.sh
```

В Windows: `scripts\run_parameters.bat`.

## Интерактивная демонстрация

Введите в окне:

```text
ls -la "my folder"
cd "my folder"
unknown
ls "broken
exit now
exit
```

Заглушки показывают аргументы; ошибки не закрывают окно.
После `exit` окно закрывается.

## Структура

```text
src/       ядро, парсер, GUI и точка входа
tests/     автоматические проверки
run.sh     запуск в Linux или Git Bash
run.bat    запуск в Windows
```
