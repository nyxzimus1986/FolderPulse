#!/usr/bin/env python3
"""
Generate Splash Screen for FolderPulse
Creates a professional splash screen image with custom branding.
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

def create_gradient_background(width, height, start_color, end_color):
    """Create a gradient background."""
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    
    # Create vertical gradient
    for y in range(height):
        # Calculate color interpolation
        ratio = y / height
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        
        # Draw horizontal line with interpolated color
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return image

def draw_rounded_rectangle(draw, coords, radius, fill, outline=None, width=1):
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = coords
    
    # Draw main rectangle
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill, outline=outline, width=width)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill, outline=outline, width=width)
    
    # Draw corners
    draw.pieslice([x1, y1, x1 + 2*radius, y1 + 2*radius], 180, 270, fill=fill, outline=outline, width=width)
    draw.pieslice([x2 - 2*radius, y1, x2, y1 + 2*radius], 270, 360, fill=fill, outline=outline, width=width)
    draw.pieslice([x1, y2 - 2*radius, x1 + 2*radius, y2], 90, 180, fill=fill, outline=outline, width=width)
    draw.pieslice([x2 - 2*radius, y2 - 2*radius, x2, y2], 0, 90, fill=fill, outline=outline, width=width)

def get_font(size, bold=False):
    """Get a font with fallback options."""
    font_paths = [
        "C:/Windows/Fonts/segoeui.ttf",  # Segoe UI
        "C:/Windows/Fonts/arial.ttf",   # Arial
        "C:/Windows/Fonts/calibri.ttf", # Calibri
    ]
    
    if bold:
        bold_paths = [
            "C:/Windows/Fonts/segoeuib.ttf",  # Segoe UI Bold
            "C:/Windows/Fonts/arialbd.ttf",   # Arial Bold
            "C:/Windows/Fonts/calibrib.ttf",  # Calibri Bold
        ]
        font_paths = bold_paths + font_paths
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                continue
    
    # Fallback to default font
    try:
        return ImageFont.load_default()
    except Exception:
        return None

def create_folder_icon(size=80):
    """Create a simple folder icon."""
    icon = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    
    # Folder colors
    folder_color = (76, 175, 80)  # Green
    folder_shadow = (56, 142, 60)  # Darker green
    
    # Draw folder shadow
    shadow_coords = [10, 25, size-5, size-10]
    draw_rounded_rectangle(draw, shadow_coords, 8, folder_shadow)
    
    # Draw main folder
    main_coords = [5, 20, size-10, size-15]
    draw_rounded_rectangle(draw, main_coords, 8, folder_color)
    
    # Draw folder tab
    tab_coords = [5, 15, size//2, 25]
    draw_rounded_rectangle(draw, tab_coords, 4, folder_color)
    
    return icon

def generate_splash_screen(
    width=600,
    height=400,
    title="FolderPulse",
    subtitle="Find and Manage Empty Folders",
    version="v1.0.0",
    output_path="assets/splash.png"
):
    """Generate a professional splash screen."""
    
    print(f"🎨 Generating splash screen ({width}x{height})...")
    
    # Color scheme
    bg_start = (26, 26, 26)      # Dark gray
    bg_end = (45, 45, 45)        # Slightly lighter gray
    accent_color = (76, 175, 80)  # Green accent
    text_primary = (255, 255, 255)  # White
    text_secondary = (200, 200, 200)  # Light gray
    text_version = (150, 150, 150)   # Gray
    
    # Create gradient background
    image = create_gradient_background(width, height, bg_start, bg_end)
    draw = ImageDraw.Draw(image)
    
    # Add subtle pattern/texture
    for i in range(0, width, 40):
        for j in range(0, height, 40):
            if (i + j) % 80 == 0:
                draw.ellipse([i-2, j-2, i+2, j+2], fill=(60, 60, 60))
    
    # Create content area with rounded rectangle
    content_padding = 60
    content_coords = [
        content_padding, 
        content_padding, 
        width - content_padding, 
        height - content_padding
    ]
    
    # Draw content background with transparency effect
    content_overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    content_draw = ImageDraw.Draw(content_overlay)
    
    draw_rounded_rectangle(
        content_draw, 
        content_coords, 
        20, 
        fill=(255, 255, 255, 30),  # Semi-transparent white
        outline=(255, 255, 255, 80),  # Semi-transparent border
        width=2
    )
    
    # Composite the overlay
    image = Image.alpha_composite(image.convert('RGBA'), content_overlay).convert('RGB')
    draw = ImageDraw.Draw(image)
    
    # Create and position folder icon
    folder_icon = create_folder_icon(80)
    icon_x = (width - 80) // 2
    icon_y = content_padding + 30
    
    # Paste icon with transparency
    image.paste(folder_icon, (icon_x, icon_y), folder_icon)
    
    # Get fonts
    title_font = get_font(36, bold=True)
    subtitle_font = get_font(16)
    version_font = get_font(12)
    
    # Calculate text positions
    title_y = icon_y + 100
    subtitle_y = title_y + 50
    version_y = height - content_padding - 30
    
    # Draw title with shadow effect
    title_shadow_offset = 2
    if title_font:
        # Get text size for centering
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (width - title_width) // 2
        
        # Draw shadow
        draw.text(
            (title_x + title_shadow_offset, title_y + title_shadow_offset), 
            title, 
            fill=(0, 0, 0, 180), 
            font=title_font
        )
        
        # Draw main text
        draw.text((title_x, title_y), title, fill=text_primary, font=title_font)
    
    # Draw subtitle
    if subtitle_font:
        subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        subtitle_x = (width - subtitle_width) // 2
        draw.text((subtitle_x, subtitle_y), subtitle, fill=text_secondary, font=subtitle_font)
    
    # Draw version
    if version_font:
        version_bbox = draw.textbbox((0, 0), version, font=version_font)
        version_width = version_bbox[2] - version_bbox[0]
        version_x = (width - version_width) // 2
        draw.text((version_x, version_y), version, fill=text_version, font=version_font)
    
    # Add decorative elements
    # Progress bar placeholder area
    progress_y = subtitle_y + 60
    progress_width = 300
    progress_x = (width - progress_width) // 2
    progress_height = 4
    
    # Progress bar background
    draw.rectangle(
        [progress_x, progress_y, progress_x + progress_width, progress_y + progress_height],
        fill=(100, 100, 100)
    )
    
    # Add some accent dots
    for i in range(3):
        dot_x = width // 2 - 30 + i * 30
        dot_y = progress_y + 30
        draw.ellipse([dot_x-3, dot_y-3, dot_x+3, dot_y+3], fill=accent_color)
    
    # Ensure output directory exists
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save the image
    image.save(output_path, 'PNG', quality=95)
    print(f"✅ Splash screen saved to: {output_path}")
    
    return str(output_path)

def create_variations():
    """Create different variations of the splash screen."""
    
    variations = [
        {
            'name': 'default',
            'width': 600,
            'height': 400,
            'output': 'assets/splash.png'
        },
        {
            'name': 'wide',
            'width': 800,
            'height': 400,
            'output': 'assets/splash_wide.png'
        },
        {
            'name': 'square',
            'width': 500,
            'height': 500,
            'output': 'assets/splash_square.png'
        },
        {
            'name': 'large',
            'width': 900,
            'height': 600,
            'output': 'assets/splash_large.png'
        }
    ]
    
    created_files = []
    
    for variation in variations:
        print(f"\n🎯 Creating {variation['name']} variation...")
        file_path = generate_splash_screen(
            width=variation['width'],
            height=variation['height'],
            output_path=variation['output']
        )
        created_files.append(file_path)
    
    return created_files

def main():
    """Main function to generate splash screens."""
    print("🚀 FolderPulse Splash Screen Generator")
    print("=" * 40)
    
    # Create assets directory if it doesn't exist
    Path("assets").mkdir(exist_ok=True)
    
    # Generate default splash screen
    default_splash = generate_splash_screen()
    
    # Ask if user wants variations
    create_more = input("\n🤔 Create additional size variations? (y/n): ").lower().strip()
    
    if create_more == 'y':
        print("\n🎨 Creating variations...")
        variations = create_variations()
        print(f"\n✅ Created {len(variations)} splash screen variations!")
        
        print("\n📁 Generated files:")
        for file_path in variations:
            print(f"  - {file_path}")
    else:
        print(f"\n✅ Created default splash screen: {default_splash}")
    
    print("\n🎉 Splash screen generation complete!")
    print("\n💡 Tips:")
    print("  - Use 'splash.png' as your main splash screen")
    print("  - Edit colors and text in this script to customize")
    print("  - Try different sizes for different display resolutions")

if __name__ == "__main__":
    main()
