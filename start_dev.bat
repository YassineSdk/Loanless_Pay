@echo off
echo ============================================
echo    Loanless Microloan Application
echo    Starting Development Servers...
echo ============================================
echo.

REM Start Backend Server
echo [1/2] Starting Flask Backend Server...
start "Flask Backend" cmd /k "cd /d "%~dp0" && .venv\Scripts\python.exe backend\app.py"
timeout /t 3 /nobreak >nul

echo [2/2] Starting React Frontend Server...
start "React Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ============================================
echo    Servers Starting...
echo ============================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:5173
echo.
echo Two new windows have been opened:
echo   1. Flask Backend Server
echo   2. React Frontend Server
echo.
echo Press Ctrl+C in each window to stop the servers
echo.
echo Default Accounts:
echo   Admin: admin / admin123
echo   User:  demo  / demo123
echo.
echo ============================================
echo Close this window when done.
pause
