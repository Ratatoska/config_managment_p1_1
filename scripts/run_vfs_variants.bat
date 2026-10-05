@echo off
setlocal
cd /d "%~dp0.."
set "failures=0"
for %%F in (vfs_minimal.json vfs_files.json vfs.json) do (
    call run.bat examples\%%F examples\startup_stage3.txt --headless
    if errorlevel 1 set "failures=1"
)
call run.bat examples\missing.json --headless < NUL
if not errorlevel 1 set "failures=1"
call run.bat examples\vfs_invalid.json --headless < NUL
if not errorlevel 1 set "failures=1"
exit /b %failures%
