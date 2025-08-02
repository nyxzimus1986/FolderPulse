#!/usr/bin/env python3
"""
Standalone test for splash screen debugging.
"""

import tkinter as tk
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_splash_direct():
    """Test splash screen directly without the main app."""
    print("=== SPLASH SCREEN DIRECT TEST ===")
    
    try:
        from gui.splash_screen import SplashScreen
        print("✓ SplashScreen imported successfully")
        
        def test_callback():
            print("✓ Splash callback called - test complete!")
            root.quit()
        
        print("Creating root window...")
        root = tk.Tk()
        root.withdraw()
        print("✓ Root window created and hidden")
        
        print("Creating splash screen...")
        splash = SplashScreen(
            duration=5.0,  # Longer for testing
            callback=test_callback,
            parent=root
        )
        print("✓ Splash screen created")
        
        print("Starting mainloop...")
        root.mainloop()
        print("✓ Test completed")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

def test_simple_window():
    """Test if basic Tkinter window works."""
    print("=== BASIC TKINTER TEST ===")
    
    root = tk.Tk()
    root.title("Basic Test")
    root.geometry("300x200+100+100")
    root.configure(bg='blue')
    
    label = tk.Label(root, text="Basic Tkinter Test", fg='white', bg='blue', font=('Arial', 16))
    label.pack(expand=True)
    
    def close_test():
        print("✓ Basic test window closing")
        root.quit()
    
    root.after(3000, close_test)
    print("✓ Basic window should be visible...")
    root.mainloop()
    print("✓ Basic test completed")

if __name__ == "__main__":
    print("Choose test:")
    print("1. Basic Tkinter window test")
    print("2. Splash screen direct test")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_simple_window()
    elif choice == "2":
        test_splash_direct()
    else:
        print("Running both tests...")
        test_simple_window()
        print("\n" + "="*50 + "\n")
        test_splash_direct()
