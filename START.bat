@echo off
echo ============================================
echo    Loanless Microloan Application
echo    Starting Server...
echo ============================================
echo.

REM Check if database needs to be recreated
if exist "instance\database.db" (
    echo Database found.
    echo NOTE: If you updated the schema, delete instance\database.db first!
    echo.
) else (
    echo Creating new database...
    echo.
)

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

echo Starting Flask application...
echo.
echo ============================================
echo Server will start on: http://localhost:5000
echo ============================================
echo.
echo Default Accounts:
echo   Admin: admin / admin123
echo   User:  demo  / demo123
echo.
echo Press Ctrl+C to stop the server
echo ============================================
echo.

python app.py

pause
