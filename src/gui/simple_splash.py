#!/usr/bin/env python3
"""
Simplified splash screen that definitely works.
"""

import tkinter as tk
from tkinter import ttk
import time

class SimpleSplash:
    """Simplified splash screen for FolderPulse."""
    
    def __init__(self, duration=3.0, callback=None, parent=None):
        self.duration = duration
        self.callback = callback
        self.parent = parent
        
        # Create window
        if parent:
            self.splash = tk.Toplevel(parent)
        else:
            self.splash = tk.Tk()
        
        self.setup_window()
        self.create_content()
        self.show()
    
    def setup_window(self):
        """Setup the splash window."""
        self.splash.overrideredirect(True)
        self.splash.geometry("500x350+300+200")  # Fixed position for visibility
        self.splash.configure(bg='#2c2c2c')
        self.splash.attributes('-topmost', True)
        
        # Add a border to make it more visible
        self.splash.configure(relief='solid', bd=2)
    
    def create_content(self):
        """Create splash content."""
        # Main frame
        main_frame = tk.Frame(self.splash, bg='#2c2c2c', padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo (emoji for now)
        logo_label = tk.Label(
            main_frame,
            text="📁",
            font=("Arial", 48),
            bg='#2c2c2c',
            fg='#4CAF50'
        )
        logo_label.pack(pady=(20, 10))
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="FolderPulse",
            font=("Arial", 24, "bold"),
            bg='#2c2c2c',
            fg='white'
        )
        title_label.pack(pady=(0, 5))
        
        # Subtitle
        subtitle_label = tk.Label(
            main_frame,
            text="Find and Manage Empty Folders",
            font=("Arial", 12),
            bg='#2c2c2c',
            fg='#cccccc'
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Loading text
        self.loading_label = tk.Label(
            main_frame,
            text="Loading...",
            font=("Arial", 10),
            bg='#2c2c2c',
            fg='#888888'
        )
        self.loading_label.pack(pady=(0, 15))
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            length=300,
            mode='indeterminate'
        )
        self.progress.pack(pady=(0, 20))
    
    def show(self):
        """Show the splash screen."""
        print("[SIMPLE SPLASH] Showing splash screen...")
        self.splash.deiconify()
        self.splash.lift()
        
        # Start progress bar
        self.progress.start(10)
        
        # Schedule close
        self.splash.after(int(self.duration * 1000), self.close)
        
        print(f"[SIMPLE SPLASH] Splash visible at {self.splash.geometry()}")
    
    def close(self):
        """Close the splash screen."""
        print("[SIMPLE SPLASH] Closing splash screen...")
        self.progress.stop()
        self.splash.destroy()
        
        if self.callback:
            self.callback()
