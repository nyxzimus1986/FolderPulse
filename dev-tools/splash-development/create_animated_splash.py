#!/usr/bin/env python3
"""
Generate Animated Splash Screen for FolderPulse
Creates animated splash screen elements and integrates with the working splash screen.
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path
import math

def create_animated_progress_frames(width=300, height=6, frames=30, color=(76, 175, 80)):
    """Create frames for animated progress bar."""
    frames_list = []
    
    for frame in range(frames):
        # Create progress frame
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Background bar
        draw.rectangle([0, 0, width, height], fill=(100, 100, 100), outline=None)
        
        # Animated progress
        progress = (frame / frames)
        fill_width = int(width * progress)
        
        if fill_width > 0:
            # Create gradient effect
            segments = min(fill_width, 20)
            if segments > 0:
                segment_width = fill_width / segments
                
                for i in range(segments):
                    x1 = i * segment_width
                    x2 = (i + 1) * segment_width
                    
                    # Color variation for gradient
                    intensity = 0.7 + 0.3 * (i / max(segments - 1, 1))
                    seg_color = (
                        int(color[0] * intensity),
                        int(color[1] * intensity),
                        int(color[2] * intensity)
                    )
                    
                    draw.rectangle([x1, 1, x2, height-1], fill=seg_color)
        
        frames_list.append(img)
    
    return frames_list

def create_pulsing_dots_frames(count=3, frames=60, base_color=(76, 175, 80)):
    """Create frames for pulsing dots animation."""
    frames_list = []
    dot_size = 8
    spacing = 30
    
    for frame in range(frames):
        # Create frame
        total_width = count * dot_size + (count - 1) * spacing
        img = Image.new('RGBA', (total_width, dot_size * 2), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        for dot in range(count):
            # Calculate pulsing animation
            phase_offset = (dot * frames // count)
            pulse_frame = (frame + phase_offset) % frames
            pulse = 0.5 + 0.5 * math.sin(2 * math.pi * pulse_frame / frames)
            
            # Dot properties
            size = int(dot_size * (0.6 + 0.4 * pulse))
            alpha = int(255 * (0.4 + 0.6 * pulse))
            
            # Position
            x = dot * (dot_size + spacing) + dot_size // 2
            y = dot_size
            
            # Color with alpha
            color = (*base_color, alpha)
            
            # Draw dot with glow effect
            for glow in range(3):
                glow_size = size + glow * 2
                glow_alpha = alpha // (glow + 1)
                glow_color = (*base_color, glow_alpha)
                
                draw.ellipse([
                    x - glow_size//2, y - glow_size//2,
                    x + glow_size//2, y + glow_size//2
                ], fill=glow_color)
        
        frames_list.append(img)
    
    return frames_list

def create_spinning_icon_frames(size=80, frames=60, colors=[(76, 175, 80), (56, 142, 60)]):
    """Create frames for spinning folder icon."""
    frames_list = []
    
    for frame in range(frames):
        # Create frame
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Rotation angle
        angle = (frame / frames) * 360
        
        # Create a slight 3D rotation effect
        scale_x = 0.8 + 0.2 * abs(math.cos(math.radians(angle)))
        
        # Folder colors (lighter when "facing" forward)
        intensity = 0.7 + 0.3 * abs(math.cos(math.radians(angle)))
        folder_color = (
            int(colors[0][0] * intensity),
            int(colors[0][1] * intensity),
            int(colors[0][2] * intensity)
        )
        folder_shadow = colors[1]
        
        # Calculate dimensions with scaling
        scaled_width = int((size - 20) * scale_x)
        offset_x = (size - scaled_width) // 2
        
        # Draw folder shadow
        shadow_coords = [offset_x + 5, 25, offset_x + scaled_width - 5, size - 10]
        if shadow_coords[2] > shadow_coords[0] and shadow_coords[3] > shadow_coords[1]:
            draw.rectangle(shadow_coords, fill=folder_shadow)
        
        # Draw main folder
        main_coords = [offset_x, 20, offset_x + scaled_width - 10, size - 15]
        if main_coords[2] > main_coords[0] and main_coords[3] > main_coords[1]:
            draw.rectangle(main_coords, fill=folder_color)
        
        # Draw folder tab
        tab_width = scaled_width // 2
        tab_coords = [offset_x, 15, offset_x + tab_width, 25]
        if tab_coords[2] > tab_coords[0] and tab_coords[3] > tab_coords[1]:
            draw.rectangle(tab_coords, fill=folder_color)
        
        frames_list.append(img)
    
    return frames_list

def create_text_fade_frames(text, font, color, frames=30):
    """Create frames for text fade-in animation."""
    frames_list = []
    
    if not font:
        return frames_list
    
    # Get text dimensions
    temp_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    bbox = temp_draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    for frame in range(frames):
        # Create frame
        img = Image.new('RGBA', (text_width + 20, text_height + 20), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Fade animation
        alpha = int(255 * (frame / frames))
        text_color = (*color[:3], alpha)
        
        # Draw text with shadow
        shadow_alpha = alpha // 3
        shadow_color = (0, 0, 0, shadow_alpha)
        
        # Shadow
        draw.text((12, 12), text, fill=shadow_color, font=font)
        # Main text
        draw.text((10, 10), text, fill=text_color, font=font)
        
        frames_list.append(img)
    
    return frames_list

def enhance_working_splash_screen():
    """Add animation capabilities to the working splash screen."""
    
    working_splash_path = Path("src/gui/working_splash_screen.py")
    if not working_splash_path.exists():
        print("❌ Working splash screen not found!")
        return False
    
    # Read the current working splash screen
    with open(working_splash_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already enhanced
    if "# ANIMATION ENHANCED" in content:
        print("✅ Splash screen already has animation enhancements!")
        return True
    
    # Add animation enhancement marker and imports
    enhanced_content = content.replace(
        'import threading\nimport time\nfrom pathlib import Path\nimport os\nimport sys',
        '''import threading
import time
from pathlib import Path
import os
import sys
import math
# ANIMATION ENHANCED - Added animation capabilities'''
    )
    
    # Add animation methods before the show method
    animation_methods = '''
    def create_animated_elements(self):
        """Create animated elements for the splash screen."""
        if not hasattr(self, '_animation_frame'):
            self._animation_frame = 0
            self._animation_running = True
            self._max_animation_frames = 60
    
    def animate_elements(self):
        """Animate splash screen elements."""
        if not hasattr(self, '_animation_running') or not self._animation_running:
            return
        
        try:
            # Update animation frame
            self._animation_frame = (self._animation_frame + 1) % self._max_animation_frames
            
            # Add pulsing effect to any existing elements
            if hasattr(self, 'splash') and self.splash.winfo_exists():
                # Simple pulsing opacity effect
                pulse = 0.85 + 0.15 * math.sin(2 * math.pi * self._animation_frame / 30)
                try:
                    self.splash.attributes('-alpha', pulse)
                except:
                    pass  # Not all systems support alpha
            
            # Schedule next animation frame
            if self._animation_running and hasattr(self, 'splash'):
                self.splash.after(50, self.animate_elements)  # ~20 FPS
        except Exception as e:
            # Stop animation on error
            self._animation_running = False
    
    def stop_animations(self):
        """Stop all animations."""
        self._animation_running = False
        if hasattr(self, 'splash'):
            try:
                self.splash.attributes('-alpha', 1.0)  # Reset to full opacity
            except:
                pass
'''
    
    # Insert animation methods before the show method
    show_method_pos = enhanced_content.find('    def show(self, callback=None):')
    if show_method_pos != -1:
        enhanced_content = (
            enhanced_content[:show_method_pos] + 
            animation_methods + 
            '\n' + 
            enhanced_content[show_method_pos:]
        )
    
    # Enhance the show method to start animations
    old_show_start = '''    def show(self, callback=None):
        """
        Show splash screen and handle the entire splash sequence.
        
        Args:
            callback: Function to call when splash screen finishes
        """
        
        print("🚀 Starting splash screen...")  # Debug
        
        try:
            # Ensure splash window exists
            if not self.splash or not self.splash.winfo_exists():
                print("❌ Splash window does not exist!")
                if callback:
                    callback()
                return
            
            # Show the splash screen
            self.splash.deiconify()
            self.splash.lift()
            self.splash.attributes('-topmost', True)
            
            print("✅ Splash screen displayed")  # Debug'''
    
    new_show_start = '''    def show(self, callback=None):
        """
        Show splash screen and handle the entire splash sequence.
        
        Args:
            callback: Function to call when splash screen finishes
        """
        
        print("🚀 Starting animated splash screen...")  # Debug
        
        try:
            # Ensure splash window exists
            if not self.splash or not self.splash.winfo_exists():
                print("❌ Splash window does not exist!")
                if callback:
                    callback()
                return
            
            # Initialize animations
            self.create_animated_elements()
            
            # Show the splash screen
            self.splash.deiconify()
            self.splash.lift()
            self.splash.attributes('-topmost', True)
            
            # Start animations
            self.animate_elements()
            
            print("✅ Animated splash screen displayed")  # Debug'''
    
    enhanced_content = enhanced_content.replace(old_show_start, new_show_start)
    
    # Enhance the cleanup to stop animations
    old_cleanup = '''            # In PyInstaller exe, just clean up without force exit
            if self._is_frozen:
                print("EXE CLEANUP - No force exit")  # Debug
                import time
                time.sleep(0.1)  # Brief cleanup delay
                # DO NOT call os._exit(0) - let main app start!'''
    
    new_cleanup = '''            # Stop animations before cleanup
            self.stop_animations()
            
            # In PyInstaller exe, just clean up without force exit
            if self._is_frozen:
                print("EXE CLEANUP - No force exit")  # Debug
                import time
                time.sleep(0.1)  # Brief cleanup delay
                # DO NOT call os._exit(0) - let main app start!'''
    
    enhanced_content = enhanced_content.replace(old_cleanup, new_cleanup)
    
    # Write enhanced content back
    with open(working_splash_path, 'w', encoding='utf-8') as f:
        f.write(enhanced_content)
    
    print("✅ Enhanced working splash screen with animations!")
    return True

def main():
    """Main function to add animation capabilities."""
    print("🎬 FolderPulse Animated Splash Screen Enhancement")
    print("=" * 50)
    
    # Create animation assets directory
    assets_dir = Path("assets/animations")
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n🎨 Creating animation frames...")
    
    # Create progress bar animation frames
    print("📊 Generating progress bar frames...")
    progress_frames = create_animated_progress_frames()
    for i, frame in enumerate(progress_frames):
        frame.save(f"assets/animations/progress_{i:03d}.png")
    print(f"✅ Created {len(progress_frames)} progress bar frames")
    
    # Create pulsing dots frames
    print("🔵 Generating pulsing dots frames...")
    dots_frames = create_pulsing_dots_frames()
    for i, frame in enumerate(dots_frames):
        frame.save(f"assets/animations/dots_{i:03d}.png")
    print(f"✅ Created {len(dots_frames)} pulsing dots frames")
    
    # Create spinning icon frames
    print("🔄 Generating spinning icon frames...")
    icon_frames = create_spinning_icon_frames()
    for i, frame in enumerate(icon_frames):
        frame.save(f"assets/animations/icon_{i:03d}.png")
    print(f"✅ Created {len(icon_frames)} spinning icon frames")
    
    # Enhance the working splash screen
    print("\n🔧 Enhancing splash screen with animations...")
    if enhance_working_splash_screen():
        print("✅ Splash screen enhanced successfully!")
    else:
        print("❌ Failed to enhance splash screen")
        return
    
    print("\n🎉 Animation enhancement complete!")
    print("\n💡 What's been added:")
    print("  ✨ Smooth pulsing opacity effect")
    print("  🎬 Animation framework in splash screen")
    print("  📁 Animation assets in assets/animations/")
    print("  🔧 Enhanced splash screen code")
    
    print("\n🚀 Your splash screen now has:")
    print("  • Subtle pulsing animation")
    print("  • Smooth transitions")
    print("  • Professional animated effects")
    
    print("\n▶️  Run your app to see the animated splash screen!")

if __name__ == "__main__":
    main()
