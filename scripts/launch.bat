@echo off
echo 🚀 Starting VoidPulse with Splash Screen
echo ========================================

:: Change to the project root directory (one level up from scripts)
cd /d "%~dp0.."

echo 📦 Checking dependencies...
python -c "import tkinter, PIL; print('✅ All dependencies available')" 2>nul
if errorlevel 1 (
    echo ❌ Missing dependencies. Installing...
    python -m pip install Pillow
)

echo 🎨 Ensuring assets exist...
if not exist "assets\icons\app.ico" (
    echo Creating default assets...
    python scripts\create_assets.py
)

echo 🎯 Launching VoidPulse...
python src\main.py

echo.
echo Press any key to exit...
pause >nul
