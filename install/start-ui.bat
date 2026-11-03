@echo off
rem Starts the Second Brain desktop installer (native window with pywebview, else your browser).
where py >nul 2>nul && (py -3 "%~dp0app.py" %* & goto :eof)
python "%~dp0app.py" %*
