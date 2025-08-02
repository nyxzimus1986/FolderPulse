# FolderPulse Project Structure

## 📁 Directory Organization

```
FolderPulse_Main/
├── 📂 src/                    # Source code
│   ├── main.py               # Application entry point
│   ├── core/                 # Core business logic
│   │   ├── app_manager.py    # Central application manager
│   │   └── folder_scanner.py # Empty folder scanning engine
│   ├── gui/                  # User interface components
│   │   ├── main_window.py    # Main Tkinter interface
│   │   ├── splash_screen.py  # Original splash screen
│   │   └── working_splash_screen.py # Enhanced animated splash
│   └── utils/                # Utility modules
│       └── logger.py         # Logging utilities
│
├── 📂 assets/                 # Application assets
│   ├── splash.png           # Custom splash screen image
│   ├── logo.png             # Application logo
│   ├── splash_bg.png        # Background assets
│   └── icons/               # Application icons
│       └── app.ico          # Main application icon
│
├── 📂 config/                 # Configuration files
│   └── config.json          # Application settings
│
├── 📂 docs/                   # Documentation
│   └── CUSTOMIZATION_GUIDE.md # User customization guide
│
├── 📂 scripts/                # Build and utility scripts
│   ├── build.py             # Application builder
│   ├── create_assets.py     # Asset generation utilities
│   ├── build.bat            # Windows build script
│   ├── launch.bat           # Application launcher
│   ├── launch_no_splash.bat # Launcher without splash
│   └── run.bat              # Quick run script
│
├── 📂 tests/                  # Unit tests
│   ├── test_main_app.py     # Main application tests
│   └── demo.py              # Demo and testing utilities
│
├── 📂 logs/                   # Application logs
│   └── app.log              # Runtime logs
│
├── 📂 dev-tools/              # Development utilities (not in production)
│   ├── splash-development/   # Splash screen development files
│   │   ├── add_splash_animation.py
│   │   ├── generate_splash.py
│   │   ├── *test*.py        # Various test scripts
│   │   └── *.md             # Development documentation
│   ├── test-data/           # Test data and demo files
│   │   ├── demo.py
│   │   ├── demo_results.*
│   │   └── demo_test_folders/
│   └── open_correct_vscode.py # VSCode utility
│
├── 📂 .github/                # GitHub configuration
├── 📂 .vscode/                # VSCode settings
├── .gitignore                # Git ignore rules
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup
└── STRUCTURE.md              # This file
```

## 🎯 Key Directories

### **Production Code**
- `src/` - All production source code
- `assets/` - Images, icons, and media files
- `config/` - Configuration files
- `scripts/` - Build and deployment scripts

### **Development & Testing**
- `tests/` - Unit tests and integration tests
- `dev-tools/` - Development utilities and experimental code
- `logs/` - Runtime logs and debugging information
- `docs/` - Project documentation

### **Configuration**
- `.github/` - GitHub Actions and repository settings
- `.vscode/` - Visual Studio Code workspace settings

## 🧹 Cleanup Benefits

✅ **Organized Structure**: Clear separation between production and development code
✅ **Reduced Clutter**: Moved test files and development scripts to dedicated folders
✅ **Better Navigation**: Logical grouping of related files
✅ **Professional Layout**: Industry-standard project organization
✅ **Maintainable**: Easy to find and modify specific components

## 🚀 Quick Start

1. **Run Application**: `python src/main.py`
2. **Build Executable**: `python scripts/build.py`
3. **Run Tests**: `python -m pytest tests/`
4. **Generate Assets**: `python scripts/create_assets.py`

## 📝 Notes

- The `dev-tools/` directory contains development utilities and should not be included in production builds
- All splash screen development files are organized in `dev-tools/splash-development/`
- Test data and demo files are in `dev-tools/test-data/`
- Build scripts in `scripts/` handle packaging and distribution
