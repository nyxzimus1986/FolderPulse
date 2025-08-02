@echo off
echo 🚀 Starting FolderPulse - Empty Folder Scanner
echo ============================================

:: Change to the project root directory (one level up from scripts)
cd /d "%~dp0.."

echo 📁 Launching FolderPulse GUI...
python src\main.py

if errorlevel 1 (
    echo.
    echo ❌ Error: Failed to start FolderPulse
    echo 💡 Make sure Python is installed and available in PATH
    echo.
    pause
) else (
    echo.
    echo ✅ FolderPulse closed successfully
)
