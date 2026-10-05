@echo off
setlocal
if defined PYTHON goto custom
python -c "import sys; sys.exit(sys.version_info < (3, 10))" >NUL 2>&1
if not errorlevel 1 goto python
py -3 -c "import sys; sys.exit(sys.version_info < (3, 10))" >NUL 2>&1
if not errorlevel 1 goto launcher
echo Python 3.10 or newer is required. Set PYTHON to its executable. 1>&2
exit /b 1

:custom
"%PYTHON%" -c "import sys; sys.exit(sys.version_info < (3, 10))" >NUL 2>&1
if errorlevel 1 (
    echo PYTHON must point to a working Python 3.10+ executable. 1>&2
    exit /b 1
)
"%PYTHON%" -X utf8 "%~dp0src\main.py" %*
exit /b %errorlevel%

:python
python -X utf8 "%~dp0src\main.py" %*
exit /b %errorlevel%

:launcher
py -3 -X utf8 "%~dp0src\main.py" %*
exit /b %errorlevel%
