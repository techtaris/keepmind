@echo off
rem Second Brain prerequisites (Windows). Usage: install.bat [check|python|ollama|models|git|node|claude|codex|pywebview|all]
set "COMP=%~1"
if "%COMP%"=="" set "COMP=check"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" -Component %COMP% %2 %3 %4 %5
