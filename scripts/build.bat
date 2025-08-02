@echo off
echo 🚀 FolderPulse Quick Build
echo ========================

:: Change to the project root directory (one level up from scripts)
cd /d "%~dp0.."

echo 📦 Installing dependencies...
python -m pip install -r requirements.txt

echo 🔨 Building executable...
python scripts/build.py

echo ✅ Build complete! Check the dist/ folder for your executable.
pause
