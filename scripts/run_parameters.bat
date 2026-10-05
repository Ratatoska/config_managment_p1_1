@echo off
setlocal
cd /d "%~dp0.."
call run.bat --headless < NUL
call run.bat examples\vfs.json --headless < NUL
call run.bat examples\vfs.json examples\startup_stage2.txt --headless
