#!/usr/bin/env python3
"""
FolderPulse - Main Application Entry Point
Find and manage empty folders with a professional GUI interface.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.app_manager import AppManager
from gui.main_window import MainWindow
from gui.working_splash_screen import SplashScreen  # Using working splash from CodePulse
from utils.logger import setup_logger


class FolderPulseApp:
    """Main application class for FolderPulse."""
    
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.app_manager = AppManager()
        self.root = None
        self.main_window = None
        self.splash = None
    
    def initialize(self, root_window=None):
        """Initialize the application."""
        try:
            self.logger.info("Initializing FolderPulse application...")
            
            # Use provided root or create new one
            if root_window:
                self.root = root_window
                self.root.deiconify()  # Show if hidden
            else:
                self.root = tk.Tk()
            
            # Configure main window
            self.setup_main_window()
            
            # Initialize main window
            self.main_window = MainWindow(self.root, self.app_manager)
            
            self.logger.info("Application initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize application: {e}")
            messagebox.showerror("Error", f"Failed to initialize application:\n{e}")
            return False
    
    def setup_main_window(self):
        """Configure the main application window."""
        self.root.title("FolderPulse - Empty Folder Manager")
        
        # Get window size from config
        config_width = self.app_manager.get_config("window.width", 900)
        config_height = self.app_manager.get_config("window.height", 700)
        self.root.geometry(f"{config_width}x{config_height}")
        
        # Center window on screen
        if self.app_manager.get_config("window.center_on_startup", True):
            self.center_window()
        
        # Set window icon
        self.set_window_icon()
        
        # Configure window behavior
        self.root.minsize(600, 500)  # Minimum size
        if self.app_manager.get_config("window.resizable", True):
            self.root.resizable(True, True)
    
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def set_window_icon(self):
        """Set the window icon."""
        # Try multiple icon paths
        icon_paths = [
            Path("assets/icons/app.ico"),
            Path("assets/icon.ico"),
            Path("../assets/icons/app.ico"),
            Path("../assets/icon.ico")
        ]
        
        for icon_path in icon_paths:
            if icon_path.exists():
                try:
                    self.root.iconbitmap(icon_path)
                    self.logger.info(f"Window icon set: {icon_path}")
                    return
                except Exception as e:
                    self.logger.warning(f"Failed to set icon {icon_path}: {e}")
        
        self.logger.info("No custom icon found, using default")
    
    def show_splash_and_run(self):
        """Show splash screen then start main application."""
        print("[DEBUG] Starting show_splash_and_run...")
        
        # Create hidden root window for main app
        self.root = tk.Tk()
        self.root.withdraw()  # Hide initially
        print("[DEBUG] Root window created and hidden")
        
        # Show splash screen with root as parent
        print("[DEBUG] Creating splash screen...")
        try:
            self.splash = SplashScreen(  # Using working splash from CodePulse
                duration=4.0,  # Reasonable duration
                splash_image_path="assets/splash.png"  # Use our custom splash image
            )
            print("[DEBUG] Splash screen created successfully")
            
            # Show splash with callback
            print("[DEBUG] Showing splash screen...")
            self.splash.show(callback=self.start_main_application)
            print("[DEBUG] Splash show() called")
            
        except Exception as e:
            print(f"[DEBUG] Error creating splash screen: {e}")
            import traceback
            traceback.print_exc()
        
        print("[DEBUG] Starting mainloop...")
        # Start the GUI event loop
        self.root.mainloop()
        print("[DEBUG] Mainloop ended")
    
    def start_main_application(self):
        """Start the main application (called after splash)."""
        try:
            # Initialize main application
            if self.initialize(self.root):
                self.logger.info("Main application started successfully")
            else:
                self.logger.error("Failed to start main application")
                self.root.quit()
                
        except Exception as e:
            self.logger.error(f"Error starting main application: {e}")
            messagebox.showerror("Startup Error", f"Failed to start application:\n{e}")
            self.root.quit()
    
    def run(self):
        """Run the application with splash screen."""
        try:
            self.logger.info("Starting FolderPulse with splash screen...")
            self.show_splash_and_run()
        except KeyboardInterrupt:
            self.logger.info("Application interrupted by user")
        except Exception as e:
            self.logger.error(f"Application error: {e}")
            messagebox.showerror("Error", f"Application error:\n{e}")
        finally:
            self.cleanup()
    
    def run_without_splash(self):
        """Run the application without splash screen."""
        try:
            self.logger.info("Starting FolderPulse (no splash)...")
            if self.initialize():
                self.root.mainloop()
        except KeyboardInterrupt:
            self.logger.info("Application interrupted by user")
        except Exception as e:
            self.logger.error(f"Application error: {e}")
            messagebox.showerror("Error", f"Application error:\n{e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources before exit."""
        try:
            self.logger.info("Cleaning up application resources...")
            if self.app_manager:
                self.app_manager.cleanup()
            self.logger.info("Cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")


def main():
    """Main entry point."""
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="FolderPulse - Empty Folder Manager")
    parser.add_argument(
        "--no-splash", 
        action="store_true", 
        help="Skip splash screen and start directly"
    )
    args = parser.parse_args()
    
    # Create and run application
    app = FolderPulseApp()
    
    if args.no_splash:
        app.run_without_splash()
    else:
        app.run()


if __name__ == "__main__":
    main()
