@echo off
setlocal
cd /d "%~dp0.."
for %%F in (vfs_minimal.json vfs_files.json vfs.json) do (
    call run.bat examples\%%F examples\startup_stage3.txt --headless
)
call run.bat examples\missing.json --headless < NUL
call run.bat examples\vfs_invalid.json --headless < NUL
