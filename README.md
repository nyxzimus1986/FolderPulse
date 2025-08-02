# VoidPulse

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)]()

**Find and manage empty folders with ease!**

VoidPulse is a powerful Python application designed specifically for detecting and managing empty folders in your file system. Keep your storage organized and reclaim wasted space with an intuitive GUI interface.

## 🚀 Features

- **🔍 Smart Empty Folder Detection**: Find empty folders quickly and accurately
- **📁 Recursive Scanning**: Include or exclude subdirectories based on your needs  
- **👁️ Hidden File Support**: Choose whether to consider hidden files when determining if folders are empty
- **🗑️ Safe Deletion**: Preview deletions with dry-run mode before making changes
- **📊 Export Results**: Save scan results in TXT, CSV, or JSON formats
- **🖥️ Professional GUI**: Clean, intuitive interface with custom splash screen
- **🎨 Customizable Branding**: Custom logos, icons, and splash screen
- **⚡ Fast Performance**: Optimized scanning algorithms for quick results
- **🔒 Safe Operation**: Built-in safeguards to prevent accidental data loss

## Quick Start

### Prerequisites

- Python 3.8 or higher
- tkinter (usually included with Python)

### Installation & Usage

1. **Download VoidPulse**
   ```bash
   cd C:\Users\nyxzi\Python\scripts\VoidPulse
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   # With animated splash screen (recommended)
   python src/main.py
   
   # Or use the launcher scripts
   scripts\launch.bat
   scripts\run.bat
   ```

4. **Build executable** (optional)
   ```bash
   python scripts\build.py
   ```

5. **Try the demo first**
   ```bash
   python demo.py
   ```

### How to Use

1. **Launch VoidPulse** and click "Scan for Empty Folders" on the home screen
2. **Select a directory** to scan for empty folders
3. **Configure options**:
   - ✅ **Include subdirectories**: Scan all nested folders recursively
   - ✅ **Consider hidden files**: Include hidden files when checking if folders are empty
4. **Click "Start Scan"** to find empty folders
5. **Review results** in the tree view
6. **Select folders** you want to delete (or use "Select All")
7. **Preview deletion** with "Dry Run" to see what would be deleted
8. **Delete selected folders** when you're ready

## Screenshots

The application features:
- **Professional Splash Screen**: Custom animated loading screen with your logo
- **Home Tab**: Quick access to main functions
- **Scanner Tab**: Detailed scanning interface with results tree view
- **Settings Tab**: Customize application behavior

## Customization

VoidPulse supports full visual customization:

### Custom Logos and Icons
- **Window Icon**: Replace `assets/icons/app.ico` with your custom icon
- **Splash Logo**: Replace `assets/logo.png` with your custom logo (256x256 PNG)
- **Create Assets**: Run `python scripts/create_assets.py` to generate defaults

### Splash Screen
- Animated loading with progress bar
- Custom logo display
- Configurable duration and messages
- Professional appearance with company branding

### Quick Customization
```bash
# Create default assets
python scripts/create_assets.py

# Edit the generated files in assets/ folder
# Then restart the application
```

See `docs/CUSTOMIZATION_GUIDE.md` for detailed customization instructions.

## Configuration Options

### Scan Options
- **Recursive scanning**: Include all subdirectories
- **Hidden file handling**: Consider hidden files when determining emptiness
- **Ignore patterns**: Skip common system folders (`.git`, `__pycache__`, etc.)

### Safety Features
- **Dry run mode**: Preview deletions without making changes
- **Confirmation dialogs**: Double-check before deleting folders
- **Error handling**: Graceful handling of permission issues

## Use Cases

- **🧹 Disk Cleanup**: Remove empty folders left behind by uninstalled programs
- **📂 Project Organization**: Clean up development projects with empty directories
- **💾 Storage Management**: Identify and remove unnecessary empty folders
- **🔄 System Maintenance**: Regular cleanup of temporary and cache directories
- **📱 Media Organization**: Clean up empty folders in photo/music libraries

## Export Formats

Save your scan results in multiple formats:
- **TXT**: Human-readable text format with summary
- **CSV**: Spreadsheet-compatible format for analysis  
- **JSON**: Machine-readable format for automation

## Development

### Project Structure

```
VoidPulse/
├── src/
│   ├── main.py                 # Application entry point
│   ├── core/
│   │   ├── app_manager.py      # Application management
│   │   └── folder_scanner.py   # Empty folder detection logic
│   ├── gui/
│   │   └── main_window.py      # Main user interface
│   └── utils/
│       └── logger.py           # Logging utilities
├── config/
│   └── config.json             # Application configuration
├── demo.py                     # Demo script
└── README.md                   # This file
```

### Running Tests

```bash
# Create test structure and run scanner demo
python demo.py

# The demo creates sample folders and demonstrates all features
```

### Building Executable

```bash
# Use the build script
python scripts/build.py

# Or run PyInstaller directly
pyinstaller --onefile --noconsole --name VoidPulse src/main.py
```

## Development

### Adding New Features

1. **Core Logic**: Add business logic to `src/core/`
2. **GUI Components**: Add interface elements to `src/gui/`
3. **Utilities**: Add helper functions to `src/utils/`
4. **Configuration**: Update `config/config.json` schema
5. **Tests**: Add tests to `tests/`

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings for all public functions
- Include proper error handling
- Use the centralized logging system

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_main_app.py
```

## Logging

The application uses a comprehensive logging system:

- **Console output**: Real-time feedback during development
- **File logging**: Persistent logs with rotation
- **Multiple levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Structured format**: Timestamps, logger names, and detailed messages

Log files are stored in the `logs/` directory with automatic rotation.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## Troubleshooting

### Common Issues

**Import Errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version compatibility (3.8+)

**GUI Not Displaying**
- Verify Tkinter is available: `python -c "import tkinter"`
- On Linux, install: `sudo apt-get install python3-tk`

**Permission Errors**
- Run as administrator if monitoring system directories
- Check file permissions for log and config directories

### Debug Mode

Enable debug mode by modifying `config/config.json`:
```json
{
  "debug": true,
  "logging": {
    "level": "DEBUG"
  }
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, bug reports, or feature requests:
- Create an issue in the repository
- Check the documentation in the `docs/` folder
- Review the logs in the `logs/` directory for error details

---

**VoidPulse** - Professional file system monitoring made simple.
