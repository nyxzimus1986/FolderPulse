#!/usr/bin/env python3
"""
Debug splash screen test to see what's happening.
"""

import tkinter as tk
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def debug_splash():
    """Debug the splash screen issues."""
    print("🔍 Debugging Splash Screen Issues")
    print("=" * 50)
    
    # Test 1: Check if enhanced splash screen is loaded
    try:
        from gui.splash_screen import SplashScreen
        print("✅ SplashScreen imported successfully")
        
        # Check if it has the enhanced features
        splash_instance = None
        def test_callback():
            print("✅ Splash callback called!")
            if root:
                root.quit()
        
        root = tk.Tk()
        root.withdraw()
        
        print("🎬 Creating splash screen...")
        splash_instance = SplashScreen(duration=3.0, callback=test_callback)
        
        # Check attributes
        print(f"✅ Has progress_value: {hasattr(splash_instance, 'progress_value')}")
        print(f"✅ Progress value: {getattr(splash_instance, 'progress_value', 'Not found')}")
        print(f"✅ Has animation_running: {hasattr(splash_instance, 'animation_running')}")
        print(f"✅ Animation running: {getattr(splash_instance, 'animation_running', 'Not found')}")
        print(f"✅ Has progress_canvas: {hasattr(splash_instance, 'progress_canvas')}")
        
        # Test the canvas
        if hasattr(splash_instance, 'progress_canvas'):
            print("✅ Progress canvas exists")
            print(f"   Canvas size: {splash_instance.progress_canvas.winfo_reqwidth()}x{splash_instance.progress_canvas.winfo_reqheight()}")
        else:
            print("❌ Progress canvas missing!")
        
        print("🎬 Starting GUI loop...")
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_splash()
