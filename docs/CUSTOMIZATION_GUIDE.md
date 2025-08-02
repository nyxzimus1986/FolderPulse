# 🎨 FolderPulse Customization Guide

## Custom Logos and Splash Screen

FolderPulse supports full customization of its visual appearance including logos, icons, and splash screen. This guide shows you how to customize these elements.

## 📁 Asset File Locations

### Required Assets
- **Application Icon**: `assets/icons/app.ico` (Windows icon file)
- **Logo**: `assets/logo.png` (PNG image for splash screen)
- **Splash Background**: `assets/splash_bg.png` (Optional background image)

### Asset Specifications

#### Application Icon (`app.ico`)
- **Format**: ICO (Windows Icon)
- **Sizes**: Multiple sizes (16x16, 32x32, 48x48, 64x64)
- **Usage**: Window title bar, taskbar, system tray
- **Tool**: Use online ICO converters or tools like GIMP

#### Logo (`logo.png`)
- **Format**: PNG with transparency support
- **Recommended Size**: 256x256 pixels
- **Usage**: Splash screen, about dialog
- **Background**: Transparent or solid color

#### Splash Background (`splash_bg.png`)
- **Format**: PNG or JPG
- **Size**: 500x350 pixels (matches splash window)
- **Usage**: Background image for splash screen
- **Optional**: If not provided, uses solid color background

## 🛠️ Customization Methods

### Method 1: Replace Default Assets

1. **Create Your Assets**
   ```bash
   # Generate default assets first (if needed)
   python scripts/create_assets.py
   ```

2. **Replace with Your Custom Files**
   - Replace `assets/icons/app.ico` with your custom icon
   - Replace `assets/logo.png` with your custom logo
   - Replace `assets/splash_bg.png` with your custom background (optional)

3. **Test Your Changes**
   ```bash
   python src/main.py
   ```

### Method 2: Modify Asset Creation Script

Edit `scripts/create_assets.py` to customize the programmatically generated assets:

```python
# Customize colors
primary_color = (44, 62, 80)    # Your primary color
accent_color = (52, 152, 219)   # Your accent color
highlight_color = (241, 196, 15) # Your highlight color

# Customize sizes
icon_size = (64, 64)
logo_size = (256, 256)
splash_size = (500, 350)
```

## 🎨 Splash Screen Customization

### Basic Customization

Edit `src/gui/splash_screen.py` to customize:

#### Colors
```python
# In setup_window method
self.splash.configure(bg='#YourColor')  # Background color

# In create_title_section method  
title_label = tk.Label(
    title_frame,
    text="Your App Name",
    font=("Your Font", 28, "bold"),
    bg='#YourBgColor',
    fg='#YourTextColor'
)
```

#### Text Content
```python
# App title
text="Your Application Name"

# Subtitle  
text="Your Custom Subtitle"

# Version
text="Version X.Y.Z"

# Loading messages
loading_messages = [
    "Starting your app...",
    "Loading your modules...",
    "Preparing interface...",
    "Almost ready..."
]
```

#### Timing
```python
# Splash duration (seconds)
duration = 4.0  # Show splash for 4 seconds

# Message timing
message_duration = self.duration / len(loading_messages)
```

### Advanced Customization

#### Custom Logo Loading
```python
def create_logo_section(self, parent):
    logo_path = Path("assets/your_custom_logo.png")
    if logo_path.exists():
        image = Image.open(logo_path)
        image = image.resize((120, 120), Image.Resampling.LANCZOS)
        self.logo_image = ImageTk.PhotoImage(image)
        # ... rest of logo setup
```

#### Custom Background Image
```python
def setup_window(self):
    # Add background image
    bg_path = Path("assets/splash_bg.png")
    if bg_path.exists():
        bg_image = Image.open(bg_path)
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(self.splash, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
```

## 🖼️ Creating Custom Assets

### Using Design Software

#### Professional Tools
- **Adobe Illustrator/Photoshop**: Vector/raster graphics
- **GIMP**: Free alternative to Photoshop
- **Inkscape**: Free vector graphics editor
- **Canva**: Online design tool

#### Asset Templates
Create templates with these dimensions:
- **Icon**: 64x64px, save as ICO with multiple sizes
- **Logo**: 256x256px, PNG with transparency
- **Splash**: 500x350px, PNG or JPG

### Using Online Tools

#### Icon Creation
- **Favicon.io**: Convert PNG to ICO
- **IconArchive**: Free icon resources
- **FlatIcon**: Icon marketplace

#### Logo Creation
- **LogoMaker**: Online logo generator
- **Canva**: Logo templates
- **Hatchful**: Free logo maker

## 📋 Asset Checklist

### Before Customizing
- [ ] Backup original assets
- [ ] Test with default assets first
- [ ] Understand file format requirements

### Asset Requirements
- [ ] Icon: ICO format, multiple sizes
- [ ] Logo: PNG format, square aspect ratio
- [ ] Background: Matches splash dimensions
- [ ] All files: Reasonable file sizes (<1MB each)

### After Customization
- [ ] Test splash screen appearance
- [ ] Check window icon display
- [ ] Verify logo scaling
- [ ] Test on different screen resolutions

## 🚀 Quick Start Examples

### Example 1: Simple Color Change
```python
# In splash_screen.py
self.splash.configure(bg='#1a237e')  # Deep blue background

# Update text colors to match
fg='#ffffff'  # White text
```

### Example 2: Corporate Branding
```python
# Use your company colors
primary_color = '#003366'    # Corporate blue
accent_color = '#00cc66'     # Corporate green
text_color = '#ffffff'       # White text

# Update company name
text="YourCompany FileManager"
```

### Example 3: Custom Font
```python
# In create_title_section method
try:
    font = ImageFont.truetype("path/to/your/font.ttf", 28)
except:
    font = ("Arial", 28, "bold")  # Fallback
```

## 🔧 Command Line Options

Run FolderPulse with different options:

```bash
# Normal startup with splash
python src/main.py

# Skip splash screen
python src/main.py --no-splash

# Create new default assets
python scripts/create_assets.py
```

## 🐛 Troubleshooting

### Common Issues

**Icon Not Showing**
- Check file exists: `assets/icons/app.ico`
- Verify ICO format (not just renamed PNG)
- Try absolute path in code

**Logo Not Loading**  
- Check file exists: `assets/logo.png`
- Verify PNG format with transparency
- Check file permissions

**Splash Screen Issues**
- Verify Pillow is installed: `pip install Pillow`
- Check image dimensions match code
- Ensure images are not corrupted

### Debug Mode
Enable debug logging to troubleshoot:
```python
# In config/config.json
"debug": true,
"logging": {
    "level": "DEBUG"
}
```

## 📝 Notes

- **Performance**: Keep asset files reasonably sized
- **Compatibility**: Test on different Windows versions
- **Backup**: Always backup original assets before customizing
- **Format Support**: PNG, ICO supported; JPG for backgrounds only

---

**🎨 Happy Customizing!** Make FolderPulse uniquely yours with custom branding and visual elements.
