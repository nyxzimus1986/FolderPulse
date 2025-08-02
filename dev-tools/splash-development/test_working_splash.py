#!/usr/bin/env python3
"""
Test the working splash screen from CodePulse.
"""

import tkinter as tk
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from gui.working_splash_screen import SplashScreen

def test_working_splash():
    """Test the working splash screen."""
    print("🚀 Testing working splash screen...")
    
    def callback():
        print("✅ Splash screen callback executed!")
        print("🎉 Test completed successfully!")
        root.quit()
    
    # Create root window (hidden)
    root = tk.Tk()
    root.withdraw()
    
    try:
        # Create splash screen
        print("📋 Creating splash screen...")
        splash = SplashScreen(duration=3.0)
        print("✅ Splash screen created")
        
        # Show splash screen with callback
        print("🎬 Showing splash screen...")
        splash.show(callback=callback)
        print("✅ Splash show() called")
        
        # Start mainloop
        print("🔄 Starting mainloop...")
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_working_splash()
