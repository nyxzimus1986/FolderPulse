#!/usr/bin/env python3
"""
Minimal splash screen test to isolate the issue.
"""

import tkinter as tk
from tkinter import ttk
import threading
import time

class MinimalSplash:
    """Minimal splash screen for testing."""
    
    def __init__(self, duration=5.0):
        self.duration = duration
        self.root = tk.Tk()
        self.root.withdraw()  # Hide root
        
        # Create splash as Toplevel
        self.splash = tk.Toplevel(self.root)
        self.setup_window()
        self.create_content()
        self.show()
    
    def setup_window(self):
        """Setup window properties."""
        self.splash.overrideredirect(True)
        self.splash.geometry("400x300+100+100")  # Fixed position for testing
        self.splash.configure(bg='#2d2d2d')
        self.splash.attributes('-topmost', True)
        print(f"Window created at: {self.splash.geometry()}")
    
    def create_content(self):
        """Create simple content."""
        # Title
        title = tk.Label(
            self.splash,
            text="FolderPulse",
            font=("Arial", 24, "bold"),
            bg='#2d2d2d',
            fg='white'
        )
        title.pack(pady=50)
        
        # Loading text
        self.loading_label = tk.Label(
            self.splash,
            text="Loading...",
            font=("Arial", 12),
            bg='#2d2d2d',
            fg='#cccccc'
        )
        self.loading_label.pack(pady=20)
        
        # Simple progress bar
        self.progress = ttk.Progressbar(
            self.splash,
            length=300,
            mode='indeterminate'
        )
        self.progress.pack(pady=20)
        
        print("Content created")
    
    def show(self):
        """Show splash and start timer."""
        print("Showing splash screen...")
        self.splash.deiconify()
        self.splash.lift()
        self.splash.focus_force()
        
        # Start progress animation
        self.progress.start(10)
        
        # Start loading sequence
        threading.Thread(target=self.loading_sequence, daemon=True).start()
        
        print("Starting mainloop...")
        self.root.mainloop()
    
    def loading_sequence(self):
        """Simple loading sequence."""
        steps = ["Initializing...", "Loading modules...", "Almost ready...", "Ready!"]
        step_time = self.duration / len(steps)
        
        for step in steps:
            print(f"Loading step: {step}")
            self.splash.after(0, lambda text=step: self.loading_label.config(text=text))
            time.sleep(step_time)
        
        print("Loading complete, closing splash...")
        self.splash.after(0, self.close)
    
    def close(self):
        """Close splash screen."""
        print("Closing splash screen...")
        self.progress.stop()
        self.splash.destroy()
        self.root.quit()

if __name__ == "__main__":
    print("Starting minimal splash test...")
    try:
        splash = MinimalSplash(duration=3.0)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    print("Test complete.")
