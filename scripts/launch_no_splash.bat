@echo off
echo 🚀 Starting FolderPulse (No Splash)
echo ================================

:: Change to the project root directory (one level up from scripts)
cd /d "%~dp0.."

echo 🎯 Launching FolderPulse directly...
python src\main.py --no-splash

echo.
echo Press any key to exit...
pause >nul
