#!/usr/bin/env python3
"""
Test script for enhanced splash screen with transparency and animated loading bar.
"""

import tkinter as tk
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from gui.splash_screen import SplashScreen


def splash_complete():
    """Callback when splash screen completes."""
    print("✅ Splash screen completed!")
    root.quit()


def test_enhanced_splash():
    """Test the enhanced splash screen."""
    global root
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    print("🚀 Testing Enhanced Splash Screen")
    print("Features:")
    print("  • Transparent top and bottom areas")
    print("  • Custom animated progress bar with gradient")
    print("  • Smooth progress animation with glow effects")
    print("  • Enhanced visual styling")
    print("  • Longer duration for better showcase")
    print("\n" + "="*50)
    
    # Create splash screen with longer duration for testing
    splash = SplashScreen(duration=5.0, callback=splash_complete)
    
    # Start GUI loop
    root.mainloop()
    
    print("="*50)
    print("🎉 Enhanced splash screen test completed!")


if __name__ == "__main__":
    test_enhanced_splash()
