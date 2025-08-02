#!/usr/bin/env python3
"""
Test script to debug splash screen issues.
"""

import tkinter as tk
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from gui.splash_screen import SplashScreen

def test_callback():
    """Test callback function."""
    print("Splash screen completed!")
    root.quit()

def test_splash_screen():
    """Test the splash screen in isolation."""
    global root
    
    print("Creating root window...")
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    print("Creating splash screen...")
    try:
        splash = SplashScreen(
            duration=2.0,  # Shorter duration for testing
            callback=test_callback,
            parent=root
        )
        print("Splash screen created successfully!")
        
        print("Starting mainloop...")
        root.mainloop()
        
    except Exception as e:
        print(f"Error creating splash screen: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Testing splash screen...")
    test_splash_screen()
    print("Test completed.")
