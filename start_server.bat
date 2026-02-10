@echo off
echo ========================================
echo   Starting Gym Tracker Server
echo ========================================
echo.

cd /d "%~dp0"

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting Django server on port 8080...
echo Open your browser to: http://127.0.0.1:8080/
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python manage.py runserver 8080

pause
