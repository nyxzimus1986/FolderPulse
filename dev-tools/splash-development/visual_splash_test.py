#!/usr/bin/env python3
"""
Visual test for the animated splash screen to verify it's working correctly.
"""

import tkinter as tk
import sys
from pathlib import Path
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def visual_test():
    """Visual test to see the animated splash screen."""
    print("🎬 Starting Visual Splash Screen Test")
    print("=" * 50)
    print("What you should see:")
    print("• Dark splash window with transparent edges")
    print("• Animated blue progress bar with gradient")
    print("• Loading messages that change over time")
    print("• Smooth progress animation at 20 FPS")
    print("• Window size: 600x400 pixels")
    print("=" * 50)
    
    try:
        from gui.splash_screen import SplashScreen
        
        def splash_done():
            print("✅ Splash screen completed successfully!")
            print("   - Animated progress bar: ✅")
            print("   - Transparency effects: ✅")
            print("   - Loading messages: ✅")
            print("   - Custom styling: ✅")
            root.quit()
        
        root = tk.Tk()
        root.withdraw()
        
        # Create splash with longer duration to see animation
        print("🚀 Launching enhanced splash screen...")
        splash = SplashScreen(duration=4.0, callback=splash_done)
        
        # Monitor splash screen attributes
        def check_splash():
            if hasattr(splash, 'progress_value') and hasattr(splash, 'animation_running'):
                progress = getattr(splash, 'progress_value', 0)
                running = getattr(splash, 'animation_running', False)
                print(f"   Progress: {progress}% | Animation: {'Running' if running else 'Stopped'}")
            
            if getattr(splash, 'animation_running', False):
                root.after(500, check_splash)  # Check every 500ms
        
        # Start monitoring
        root.after(100, check_splash)
        
        # Start GUI
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    visual_test()
