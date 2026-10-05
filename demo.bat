@echo off
setlocal
cd /d "%~dp0"
call run.bat examples\vfs.json examples\startup_demo.txt
