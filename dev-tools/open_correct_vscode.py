#!/usr/bin/env python3
"""
Script to open VS Code in the correct FolderPulse_Main directory
"""

import subprocess
import os
from pathlib import Path

def open_vscode_in_correct_directory():
    """Open VS Code in the FolderPulse_Main directory."""
    
    # Get the correct directory path
    current_dir = Path(__file__).parent
    correct_main_py = current_dir / "src" / "main.py"
    
    print(f"🔍 Current directory: {current_dir}")
    print(f"📁 Correct main.py path: {correct_main_py}")
    print(f"✅ Main.py exists: {correct_main_py.exists()}")
    
    if correct_main_py.exists():
        print("🚀 Opening VS Code in the correct directory...")
        try:
            # Change to the correct directory and open VS Code
            os.chdir(current_dir)
            subprocess.run(["code", ".", str(correct_main_py)], check=True)
            print("✅ VS Code opened successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to open VS Code: {e}")
            print("💡 Try running: code . src/main.py")
        except FileNotFoundError:
            print("❌ VS Code 'code' command not found in PATH")
            print("💡 Please open VS Code manually and navigate to:")
            print(f"   Directory: {current_dir}")
            print(f"   File: {correct_main_py}")
    else:
        print("❌ Could not find the correct main.py file")
        print(f"   Expected at: {correct_main_py}")

if __name__ == "__main__":
    open_vscode_in_correct_directory()
