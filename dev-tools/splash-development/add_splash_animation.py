#!/usr/bin/env python3
"""
Simple Splash Animation Enhancement
Adds smooth animations to the existing splash screen.
"""

import os
from pathlib import Path

def add_animation_to_splash():
    """Add animation capabilities to the working splash screen."""
    
    working_splash_path = Path("src/gui/working_splash_screen.py")
    if not working_splash_path.exists():
        print("Working splash screen not found!")
        return False
    
    # Read the current working splash screen
    with open(working_splash_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already enhanced
    if "ANIMATION_ENHANCED" in content:
        print("Splash screen already has animations!")
        return True
    
    # Add animation imports
    import_section = """import threading
import time
from pathlib import Path
import os
import sys
import math  # ANIMATION_ENHANCED - Added for animations"""
    
    content = content.replace(
        "import threading\nimport time\nfrom pathlib import Path\nimport os\nimport sys",
        import_section
    )
    
    # Add animation methods to the class
    animation_code = '''
    def init_animations(self):
        """Initialize animation variables."""
        self._animation_frame = 0
        self._animation_running = True
        self._pulse_direction = 1
        self._current_alpha = 0.9
    
    def animate_splash(self):
        """Create smooth pulsing animation."""
        if not hasattr(self, '_animation_running') or not self._animation_running:
            return
        
        try:
            if hasattr(self, 'splash') and self.splash and self.splash.winfo_exists():
                # Smooth pulsing effect
                self._animation_frame += 1
                pulse = 0.8 + 0.2 * abs(math.sin(self._animation_frame * 0.1))
                
                try:
                    self.splash.attributes('-alpha', pulse)
                except:
                    pass  # Some systems don't support alpha
                
                # Continue animation
                if self._animation_running:
                    self.splash.after(50, self.animate_splash)
        except:
            self._animation_running = False
    
    def stop_animation(self):
        """Stop the animation and restore normal appearance."""
        self._animation_running = False
        if hasattr(self, 'splash') and self.splash:
            try:
                self.splash.attributes('-alpha', 1.0)
            except:
                pass
'''
    
    # Find where to insert the animation methods (before the show method)
    show_method_pos = content.find("    def show(self, callback=None):")
    if show_method_pos == -1:
        print("Could not find show method in splash screen!")
        return False
    
    # Insert animation methods
    content = content[:show_method_pos] + animation_code + "\n" + content[show_method_pos:]
    
    # Modify the show method to start animations
    old_show_line = "        print(\"🚀 Starting splash screen...\")  # Debug"
    new_show_line = """        print("🚀 Starting animated splash screen...")  # Debug
        
        # Initialize animations
        self.init_animations()"""
    
    content = content.replace(old_show_line, new_show_line)
    
    # Add animation start after splash is shown
    old_display_line = "        print(\"✅ Splash screen displayed\")  # Debug"
    new_display_line = """        print("✅ Animated splash screen displayed")  # Debug
        
        # Start smooth animations
        self.animate_splash()"""
    
    content = content.replace(old_display_line, new_display_line)
    
    # Add animation stop before cleanup
    cleanup_line = "            print(\"EXE CLEANUP - No force exit\")  # Debug"
    new_cleanup_line = """            # Stop animations before cleanup
            self.stop_animation()
            print("EXE CLEANUP - No force exit")  # Debug"""
    
    content = content.replace("            print(\"EXE CLEANUP - No force exit\")  # Debug", new_cleanup_line)
    
    # Write the enhanced version
    with open(working_splash_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Enhanced splash screen with smooth animations!")
    return True

def main():
    """Main function."""
    print("🎬 Adding Smooth Animations to Splash Screen")
    print("=" * 45)
    
    if add_animation_to_splash():
        print("\n🎉 Animation enhancement complete!")
        print("\n✨ Your splash screen now has:")
        print("  • Smooth pulsing opacity animation")
        print("  • Professional fade effects")
        print("  • Seamless transitions")
        print("\n▶️  Run your app to see the animated splash!")
    else:
        print("\n❌ Failed to enhance splash screen")

if __name__ == "__main__":
    main()
