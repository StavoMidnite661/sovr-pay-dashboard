@echo off
REM SOVR Pay Historic Transaction Monitor
REM Windows batch script for transaction monitoring

echo Starting SOVR Pay Historic Transaction Monitor...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Start the transaction monitor
echo Starting transaction monitoring service...
cd /d "%~dp0"
python scripts\start_all_services.py

echo.
echo Press any key to stop services...
pause >nul
