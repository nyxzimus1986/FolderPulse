# 🎨 FolderPulse - Custom Logo & Splash Screen Features

## ✨ New Features Added

### 🚀 Professional Splash Screen
- **Animated Loading**: Progress bar with loading messages
- **Custom Logo Display**: Shows your custom logo prominently
- **Professional Design**: Modern UI with smooth animations
- **Configurable Duration**: Adjustable splash screen timing
- **Skip Option**: `--no-splash` command line argument

### 🎨 Customizable Branding
- **Window Icon**: Custom ICO file for taskbar and title bar
- **Splash Logo**: PNG logo for splash screen (supports transparency)
- **Brand Colors**: Easily customizable color scheme
- **Company Info**: Custom text, version, and copyright

### 🛠️ Asset Management
- **Auto-Generation**: Creates default professional assets
- **Easy Replacement**: Drop-in custom logo/icon support
- **Multiple Formats**: ICO, PNG support with proper sizing
- **Build Integration**: Assets included in executable builds

## 📁 File Structure

```
FolderPulse/
├── src/
│   ├── main.py                 # Updated with splash screen support
│   └── gui/
│       ├── main_window.py      # Main interface
│       └── splash_screen.py    # NEW: Custom splash screen
├── assets/
│   ├── icons/
│   │   └── app.ico            # NEW: Application icon
│   ├── logo.png               # NEW: Splash screen logo
│   └── splash_bg.png          # NEW: Optional background
├── scripts/
│   └── create_assets.py       # NEW: Asset generation tool
├── docs/
│   └── CUSTOMIZATION_GUIDE.md # NEW: Detailed customization guide
├── launch.bat                 # NEW: Easy launcher with splash
└── launch_no_splash.bat       # NEW: Direct launcher
```

## 🚀 Usage Examples

### Standard Launch (with Splash)
```bash
python src/main.py
# or
launch.bat
```

### Quick Launch (no Splash)
```bash
python src/main.py --no-splash
# or  
launch_no_splash.bat
```

### Create Custom Assets
```bash
python scripts/create_assets.py
```

### Build with Custom Branding
```bash
python scripts/build.py
# Automatically includes your custom assets
```

## 🎨 Customization Quick Start

### 1. Generate Default Assets
```bash
python scripts/create_assets.py
```

### 2. Replace with Your Assets
- Replace `assets/icons/app.ico` with your icon
- Replace `assets/logo.png` with your logo
- Optionally replace `assets/splash_bg.png`

### 3. Test Your Changes
```bash
python src/main.py
```

### 4. Build Executable
```bash
python scripts/build.py
```

## 🔧 Technical Details

### Splash Screen Features
- **Duration**: 3 seconds (configurable)
- **Animation**: Smooth progress bar and text updates
- **Logo Support**: PNG with transparency, auto-resizing
- **Responsive**: Centers on screen, works on all resolutions
- **Thread-Safe**: Non-blocking loading with callback system

### Asset Specifications
- **Icon**: ICO format, multiple sizes (16x16 to 64x64)
- **Logo**: PNG format, recommended 256x256 pixels
- **Background**: PNG/JPG, 500x350 pixels for splash

### Dependencies Added
- **Pillow**: For image processing and logo display
- **Threading**: For non-blocking splash screen

## 🎯 Key Benefits

1. **Professional Appearance**: Custom branding throughout
2. **User Experience**: Smooth loading with progress feedback
3. **Easy Customization**: Simple file replacement system
4. **Build Integration**: Assets automatically included in executables
5. **Flexible Options**: Can skip splash for development

## 🐛 Troubleshooting

### Common Issues
- **Missing Pillow**: Run `pip install Pillow`
- **Asset Not Loading**: Check file paths and formats
- **Icon Not Showing**: Ensure ICO format (not renamed PNG)

### Debug Mode
```bash
# Enable debug logging in config/config.json
"debug": true,
"logging": {"level": "DEBUG"}
```

---

**🎉 Your FolderPulse application now has professional branding and a custom splash screen!**

The application maintains all its core empty folder detection functionality while adding a polished, customizable user interface that can be branded for personal or corporate use.
