#!/usr/bin/env python3
"""
Very simple splash screen test to debug the display issue.
"""

import tkinter as tk
import time
import threading

def test_simple_splash():
    """Test the simplest possible splash screen."""
    print("Creating simple splash test...")
    
    # Create root window
    root = tk.Tk()
    root.withdraw()  # Hide root
    
    # Create splash window
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    splash.geometry("400x300+200+200")  # Fixed position
    splash.configure(bg='red')  # Bright red to make it obvious
    splash.attributes('-topmost', True)
    
    # Add some text
    label = tk.Label(
        splash,
        text="SPLASH SCREEN TEST",
        font=("Arial", 20, "bold"),
        bg='red',
        fg='white'
    )
    label.pack(expand=True)
    
    print("Showing splash...")
    splash.deiconify()
    splash.lift()
    splash.focus_force()
    
    def close_splash():
        print("Closing splash...")
        splash.destroy()
        root.quit()
    
    # Close after 3 seconds
    root.after(3000, close_splash)
    
    print("Starting mainloop...")
    root.mainloop()
    print("Test complete.")

if __name__ == "__main__":
    test_simple_splash()
