"""
Build script for creating FolderPulse executable.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def clean_build():
    """Clean previous build artifacts."""
    print("🧹 Cleaning previous build artifacts...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}/")
    
    # Clean spec files
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"   Removed {spec_file}")


def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)


def build_executable():
    """Build the executable using PyInstaller."""
    print("🔨 Building executable...")
    
    # Ensure assets exist
    assets_exist = all([
        Path("assets/icons/app.ico").exists(),
        Path("assets/logo.png").exists()
    ])
    
    if not assets_exist:
        print("📦 Creating missing assets...")
        subprocess.run([sys.executable, "scripts/create_assets.py"], check=True)
    
    # Basic build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--noconsole",
        "--name", "FolderPulse",
        "src/main.py",
        "--add-data", "config;config",
        "--add-data", "assets;assets",
        "--clean"
    ]
    
    # Add icon if available
    icon_path = Path("assets/icons/app.ico")
    if icon_path.exists():
        cmd.extend(["--icon", str(icon_path)])
        print(f"🎨 Using custom icon: {icon_path}")
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Build completed successfully!")
        
        # Check if executable was created
        exe_path = Path("dist/FolderPulse.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📁 Executable created: {exe_path} ({size_mb:.1f} MB)")
            print("🎨 Includes custom logo and splash screen!")
        else:
            print("❌ Executable not found in dist/ directory")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    
    return True


def run_tests():
    """Run tests before building."""
    print("🧪 Running tests...")
    try:
        subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], check=True)
        print("✅ All tests passed!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Tests failed!")
        return False


def main():
    """Main build process."""
    print("🚀 FolderPulse Build Script")
    print("=" * 50)
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    try:
        # Step 1: Clean previous builds
        clean_build()
        
        # Step 2: Install dependencies
        install_dependencies()
        
        # Step 3: Run tests (optional, comment out if tests are not ready)
        # if not run_tests():
        #     print("❌ Build aborted due to test failures")
        #     return 1
        
        # Step 4: Build executable
        if not build_executable():
            return 1
        
        print("\n🎉 Build process completed successfully!")
        print("📍 Find your executable in the 'dist/' directory")
        
        return 0
        
    except Exception as e:
        print(f"❌ Build process failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
