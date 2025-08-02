"""
Icon and Logo Creator for FolderPulse
Creates default icons and logos programmatically using PIL.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os


def create_default_icon(size=(64, 64), output_path="assets/icons/app.ico"):
    """Create a default application icon."""
    # Create new image with transparent background
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Define colors
    folder_color = (52, 152, 219)  # Blue
    accent_color = (241, 196, 15)  # Yellow
    
    # Draw folder shape
    margin = size[0] // 8
    folder_width = size[0] - 2 * margin
    folder_height = size[1] - 2 * margin
    
    # Folder tab
    tab_width = folder_width // 3
    tab_height = folder_height // 4
    
    # Draw folder tab
    draw.rectangle([
        margin, 
        margin + tab_height, 
        margin + tab_width, 
        margin + 2 * tab_height
    ], fill=folder_color)
    
    # Draw main folder body
    draw.rectangle([
        margin, 
        margin + tab_height, 
        margin + folder_width, 
        margin + folder_height
    ], fill=folder_color)
    
    # Add search/pulse icon
    center_x = margin + folder_width // 2
    center_y = margin + folder_height // 2 + tab_height // 2
    pulse_radius = min(folder_width, folder_height) // 6
    
    # Draw pulse circles
    for i in range(3):
        radius = pulse_radius + i * 3
        draw.ellipse([
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius
        ], outline=accent_color, width=2)
    
    # Save as ICO file
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create multiple sizes for ICO
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
    images = []
    
    for icon_size in sizes:
        resized = img.resize(icon_size, Image.Resampling.LANCZOS)
        images.append(resized)
    
    images[0].save(output_path, format='ICO', sizes=[(img.width, img.height) for img in images])
    print(f"✅ Created icon: {output_path}")
    
    return output_path


def create_default_logo(size=(256, 256), output_path="assets/logo.png"):
    """Create a default application logo."""
    # Create new image with transparent background
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Define colors
    primary_color = (44, 62, 80)    # Dark blue-gray
    accent_color = (52, 152, 219)   # Blue
    highlight_color = (241, 196, 15) # Yellow
    
    # Draw background circle
    margin = 20
    circle_radius = (size[0] - 2 * margin) // 2
    center = (size[0] // 2, size[1] // 2)
    
    # Background circle
    draw.ellipse([
        center[0] - circle_radius,
        center[1] - circle_radius,
        center[0] + circle_radius,
        center[1] + circle_radius
    ], fill=primary_color)
    
    # Draw folder icon in center
    folder_size = circle_radius
    folder_margin = folder_size // 4
    
    # Folder dimensions
    folder_width = folder_size - 2 * folder_margin
    folder_height = int(folder_width * 0.7)
    
    # Folder position (centered)
    folder_x = center[0] - folder_width // 2
    folder_y = center[1] - folder_height // 2
    
    # Draw folder tab
    tab_width = folder_width // 3
    tab_height = folder_height // 4
    
    draw.rectangle([
        folder_x,
        folder_y,
        folder_x + tab_width,
        folder_y + tab_height
    ], fill=accent_color)
    
    # Draw main folder
    draw.rectangle([
        folder_x,
        folder_y + tab_height // 2,
        folder_x + folder_width,
        folder_y + folder_height
    ], fill=accent_color)
    
    # Add "pulse" effect - concentric circles
    pulse_center = (center[0] + folder_width // 4, center[1] - folder_height // 4)
    
    for i in range(3):
        radius = 8 + i * 6
        draw.ellipse([
            pulse_center[0] - radius,
            pulse_center[1] - radius,
            pulse_center[0] + radius,
            pulse_center[1] + radius
        ], outline=highlight_color, width=3)
    
    # Add text below if there's space
    if size[1] > 200:
        try:
            # Try to use a nice font
            font_size = max(16, size[0] // 12)
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            text = "FolderPulse"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            
            text_x = center[0] - text_width // 2
            text_y = center[1] + circle_radius + 20
            
            draw.text((text_x, text_y), text, fill=primary_color, font=font)
            
        except Exception:
            pass  # Skip text if font loading fails
    
    # Save PNG
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, format='PNG')
    print(f"✅ Created logo: {output_path}")
    
    return output_path


def create_splash_background(size=(600, 400), output_path="assets/splash_bg.png"):
    """Create an enhanced background image for splash screen with transparency."""
    # Create gradient background with alpha channel
    img = Image.new('RGBA', size, (26, 26, 26, 255))
    draw = ImageDraw.Draw(img)
    
    # Create subtle vertical gradient
    for y in range(size[1]):
        # Gradient with slight variation
        base_color = 26
        variation = int(15 * (y / size[1]))
        alpha = 255
        
        # Special handling for transparent areas
        if y < 60:  # Top transparent area
            alpha = int(255 * (y / 60))
        elif y > size[1] - 60:  # Bottom transparent area
            alpha = int(255 * ((size[1] - y) / 60))
        
        color = (base_color + variation, base_color + variation, base_color + variation, alpha)
        draw.line([(0, y), (size[0], y)], fill=color)
    
    # Add subtle decorative elements
    accent_color = (0, 212, 255, 30)  # Semi-transparent cyan
    
    # Draw some subtle geometric shapes
    for i in range(3):
        x = (i * size[0] // 4) + size[0] // 8
        y = size[1] // 3 + (i % 2) * size[1] // 6
        radius = 40 + i * 15
        
        # Create circle overlay
        circle_img = Image.new('RGBA', size, (0, 0, 0, 0))
        circle_draw = ImageDraw.Draw(circle_img)
        circle_draw.ellipse([
            x - radius, y - radius,
            x + radius, y + radius
        ], fill=accent_color)
        
        img = Image.alpha_composite(img, circle_img)
    
    # Add some geometric lines for modern look
    line_color = (0, 212, 255, 20)
    for i in range(0, size[0], 80):
        line_img = Image.new('RGBA', size, (0, 0, 0, 0))
        line_draw = ImageDraw.Draw(line_img)
        line_draw.line([(i, 80), (i + 40, size[1] - 80)], fill=line_color, width=1)
        img = Image.alpha_composite(img, line_img)
    
    # Save background
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, format='PNG')
    print(f"✅ Created enhanced splash background: {output_path}")
    
    return output_path


def main():
    """Create all default assets."""
    print("🎨 Creating FolderPulse assets...")
    
    try:
        # Create default assets
        create_default_icon()
        create_default_logo()
        create_splash_background()
        
        print("\n✅ All assets created successfully!")
        print("\nCustomization tips:")
        print("- Replace 'assets/logo.png' with your custom logo (recommended: 256x256 PNG)")
        print("- Replace 'assets/icons/app.ico' with your custom icon")
        print("- Replace 'assets/splash_bg.png' with custom splash background")
        
    except ImportError:
        print("❌ PIL (Pillow) is required to create assets.")
        print("Install with: pip install Pillow")
    except Exception as e:
        print(f"❌ Error creating assets: {e}")


if __name__ == "__main__":
    main()
