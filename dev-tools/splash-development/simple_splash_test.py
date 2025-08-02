#!/usr/bin/env python3
"""
Simple test to verify animated progress bar is working.
This will create a minimal splash screen that you can see.
"""

import tkinter as tk
from tkinter import messagebox
import sys
from pathlib import Path
import threading
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_progress_bar():
    """Test the progress bar animation directly."""
    try:
        from gui.splash_screen import SplashScreen
        
        root = tk.Tk()
        root.title("Testing Splash Screen")
        root.geometry("300x100")
        
        status_label = tk.Label(root, text="Click 'Test Splash' to see animated progress bar", wraplength=280)
        status_label.pack(pady=10)
        
        def start_splash_test():
            status_label.config(text="Splash screen should appear now!\nLook for animated blue progress bar...")
            
            def splash_complete():
                status_label.config(text="✅ Splash screen completed!\nDid you see the animated progress bar?")
            
            # Create splash screen
            splash = SplashScreen(duration=5.0, callback=splash_complete)
        
        test_button = tk.Button(root, text="Test Splash Screen", command=start_splash_test)
        test_button.pack(pady=10)
        
        quit_button = tk.Button(root, text="Quit", command=root.quit)
        quit_button.pack(pady=5)
        
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to test splash screen:\n{e}")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_progress_bar()
