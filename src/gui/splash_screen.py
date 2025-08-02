"""
Enhanced Splash Screen for VoidPulse
Custom splash screen with animated loading bar and transparency effects.
"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path
import threading
import time
from PIL import Image, ImageTk, ImageDraw
import logging
import math


class SplashScreen:
    """Enhanced splash screen for VoidPulse application with animated loading bar."""
    
    def __init__(self, duration=3.0, callback=None, parent=None):
        """
        Initialize splash screen.
        
        Args:
            duration: How long to show the splash screen (seconds)
            callback: Function to call when splash is complete
            parent: Parent window (optional)
        """
        print(f"[SPLASH DEBUG] Initializing splash screen, duration={duration}")
        self.duration = duration
        self.callback = callback
        self.parent = parent
        self.logger = logging.getLogger(__name__)
        
        # Animation variables
        self.progress_value = 0
        self.animation_running = False
        self.progress_bar_width = 400
        self.progress_bar_height = 8
        
        print("[SPLASH DEBUG] Creating splash window...")
        try:
            # Create splash window
            if parent:
                self.splash = tk.Toplevel(parent)
                print("[SPLASH DEBUG] Created as Toplevel with parent")
            else:
                # Create standalone window if no parent
                self.splash = tk.Tk()
                print("[SPLASH DEBUG] Created as standalone Tk window")
            self.splash.withdraw()  # Hide initially
            
            # Configure splash window
            print("[SPLASH DEBUG] Setting up window...")
            self.setup_window()
            print("[SPLASH DEBUG] Creating content...")
            self.create_content()
            
            # Start splash sequence
            print("[SPLASH DEBUG] Starting splash sequence...")
            self.show_splash()
            print("[SPLASH DEBUG] Splash screen initialization complete")
            
        except Exception as e:
            print(f"[SPLASH DEBUG] Error in splash screen init: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def setup_window(self):
        """Configure the splash window properties with transparency."""
        # Remove window decorations
        self.splash.overrideredirect(True)
        
        # Set window size
        window_width = 600
        window_height = 400
        
        # Center on screen
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.splash.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.logger.info(f"Splash window geometry set to: {window_width}x{window_height}+{x}+{y}")
        
        # Set background - make it more visible
        self.splash.configure(bg='#1a1a1a')
        
        # Make window topmost and more visible
        self.splash.attributes('-topmost', True)
        self.splash.attributes('-alpha', 1.0)  # Full opacity for visibility
        
        # Add a border to make it more visible
        self.splash.configure(relief='raised', bd=2)
    
    def create_content(self):
        """Create splash screen content with transparent edges."""
        # Top transparent area
        top_frame = tk.Frame(self.splash, bg='#000001', height=60)  # Transparent color
        top_frame.pack(fill=tk.X)
        top_frame.pack_propagate(False)
        
        # Main content area
        main_frame = tk.Frame(self.splash, bg='#1a1a1a', padx=40, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo section
        self.create_logo_section(main_frame)
        
        # Title section
        self.create_title_section(main_frame)
        
        # Animated loading section
        self.create_animated_loading_section(main_frame)
        
        # Footer section
        self.create_footer_section(main_frame)
        
        # Bottom transparent area
        bottom_frame = tk.Frame(self.splash, bg='#000001', height=60)  # Transparent color
        bottom_frame.pack(fill=tk.X)
        bottom_frame.pack_propagate(False)
    
    def create_logo_section(self, parent):
        """Create the logo section."""
        logo_frame = tk.Frame(parent, bg='#1a1a1a')
        logo_frame.pack(pady=(10, 20))
        
        # Use simple text logo for reliability
        self.create_default_logo(logo_frame)
        
        # Optionally try to load custom logo (but don't fail if it doesn't work)
        # logo_path = Path("assets/logo.png")
        # if logo_path.exists():
        #     try:
        #         # Load and resize logo
        #         image = Image.open(logo_path)
        #         image = image.resize((100, 100), Image.Resampling.LANCZOS)
        #         self.logo_image = ImageTk.PhotoImage(image)
        #         
        #         logo_label = tk.Label(
        #             logo_frame, 
        #             image=self.logo_image,
        #             bg='#1a1a1a'
        #         )
        #         logo_label.pack()
        #         
        #     except Exception as e:
        #         self.logger.warning(f"Could not load logo: {e}")
        #         self.create_default_logo(logo_frame)
        # else:
        #     self.create_default_logo(logo_frame)
    
    def create_default_logo(self, parent):
        """Create a default logo if custom logo is not available."""
        # Create a simple text-based logo with gradient effect
        logo_label = tk.Label(
            parent,
            text="📁",
            font=("Arial", 56),
            bg='#1a1a1a',
            fg='#00d4ff'
        )
        logo_label.pack()
    
    def create_title_section(self, parent):
        """Create the title section."""
        title_frame = tk.Frame(parent, bg='#1a1a1a')
        title_frame.pack(pady=(0, 30))
        
        # App title with glow effect
        title_label = tk.Label(
            title_frame,
            text="VoidPulse",
            font=("Arial", 32, "bold"),
            bg='#1a1a1a',
            fg='#ffffff'
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(
            title_frame,
            text="Find and Manage Empty Folders",
            font=("Arial", 13),
            bg='#1a1a1a',
            fg='#b0b0b0'
        )
        subtitle_label.pack(pady=(8, 0))
        
        # Version
        version_label = tk.Label(
            title_frame,
            text="Version 1.0.0",
            font=("Arial", 10),
            bg='#1a1a1a',
            fg='#808080'
        )
        version_label.pack(pady=(12, 0))
    
    def create_animated_loading_section(self, parent):
        """Create the animated loading section with custom progress bar."""
        loading_frame = tk.Frame(parent, bg='#1a1a1a')
        loading_frame.pack(pady=(0, 20), fill=tk.X)
        
        # Loading text
        self.loading_label = tk.Label(
            loading_frame,
            text="Initializing...",
            font=("Arial", 11),
            bg='#1a1a1a',
            fg='#ffffff'
        )
        self.loading_label.pack(pady=(0, 15))
        
        # Custom animated progress bar container
        progress_container = tk.Frame(loading_frame, bg='#1a1a1a')
        progress_container.pack()
        
        # Create canvas for custom progress bar
        self.progress_canvas = tk.Canvas(
            progress_container,
            width=self.progress_bar_width,
            height=self.progress_bar_height + 10,
            bg='#1a1a1a',
            highlightthickness=0
        )
        self.progress_canvas.pack()
        
        # Draw initial progress bar background
        self.draw_progress_bar()
    
    def draw_progress_bar(self):
        """Draw the animated progress bar."""
        # Clear canvas
        self.progress_canvas.delete("all")
        
        # Background bar
        bg_x1, bg_y1 = 0, 5
        bg_x2, bg_y2 = self.progress_bar_width, bg_y1 + self.progress_bar_height
        
        self.progress_canvas.create_rectangle(
            bg_x1, bg_y1, bg_x2, bg_y2,
            fill='#333333',
            outline='#555555',
            width=1
        )
        
        # Progress bar fill
        if self.progress_value > 0:
            fill_width = int((self.progress_value / 100) * (self.progress_bar_width - 2))
            if fill_width > 0:
                # Create gradient effect
                num_segments = min(fill_width, 20)
                segment_width = fill_width / num_segments if num_segments > 0 else 0
                
                for i in range(num_segments):
                    x1 = bg_x1 + 1 + (i * segment_width)
                    x2 = x1 + segment_width
                    
                    # Calculate color based on position for gradient effect
                    ratio = i / max(num_segments - 1, 1)
                    blue_val = int(255 * (1 - ratio * 0.3))  # Fade from bright to darker blue
                    color = f"#{0:02x}{int(200 + ratio * 55):02x}{blue_val:02x}"  # Blue gradient
                    
                    self.progress_canvas.create_rectangle(
                        x1, bg_y1 + 1, x2, bg_y2 - 1,
                        fill=color,
                        outline=""
                    )
        
        # Add animated glow effect
        if self.animation_running and self.progress_value > 0:
            # Create moving highlight
            highlight_pos = (time.time() * 100) % self.progress_bar_width
            highlight_width = 40
            
            fill_width = int((self.progress_value / 100) * (self.progress_bar_width - 2))
            if highlight_pos < fill_width:
                self.progress_canvas.create_rectangle(
                    max(1, highlight_pos - highlight_width/2), bg_y1 + 1,
                    min(fill_width, highlight_pos + highlight_width/2), bg_y2 - 1,
                    fill='#66ccff',
                    outline="",
                    stipple="gray25"
                )
    
    def create_footer_section(self, parent):
        """Create the footer section."""
        footer_frame = tk.Frame(parent, bg='#1a1a1a')
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        
        # Copyright or additional info
        footer_label = tk.Label(
            footer_frame,
            text="© 2025 FolderPulse Team",
            font=("Arial", 9),
            bg='#1a1a1a',
            fg='#666666'
        )
        footer_label.pack()
    
    def show_splash(self):
        """Show the splash screen and start loading animation."""
        print("[SPLASH DEBUG] show_splash() called")
        self.logger.info("Showing splash screen...")
        
        print(f"[SPLASH DEBUG] Making splash visible, geometry: {self.splash.geometry()}")
        self.splash.deiconify()  # Show window
        self.splash.lift()  # Bring to front
        self.splash.focus_force()  # Force focus
        self.animation_running = True
        
        self.logger.info(f"Splash screen visible, size: {self.splash.geometry()}")
        print(f"[SPLASH DEBUG] Splash should now be visible!")
        
        # Start progress animation in a separate thread
        print("[SPLASH DEBUG] Starting animation thread...")
        threading.Thread(target=self._animate_progress, daemon=True).start()
        
        # Start loading sequence
        print("[SPLASH DEBUG] Starting loading sequence thread...")
        threading.Thread(target=self._loading_sequence, daemon=True).start()
        
        print("[SPLASH DEBUG] show_splash() complete")
    
    def _animate_progress(self):
        """Animate the progress bar continuously."""
        while self.animation_running:
            try:
                # Update progress bar animation
                self.splash.after(0, self.draw_progress_bar)
                time.sleep(0.05)  # 20 FPS
            except Exception:
                break
    
    def _loading_sequence(self):
        """Loading sequence with text updates and progress."""
        self.logger.info("Starting loading sequence...")
        loading_messages = [
            ("Initializing FolderPulse...", 0),
            ("Loading core modules...", 20),
            ("Setting up scanner engine...", 40),
            ("Preparing user interface...", 65),
            ("Configuring settings...", 85),
            ("Almost ready...", 95),
            ("Ready!", 100)
        ]
        
        total_time = self.duration
        step_time = total_time / len(loading_messages)
        
        for i, (message, progress) in enumerate(loading_messages):
            self.logger.info(f"Loading step {i+1}: {message} ({progress}%)")
            # Update loading message and progress in main thread
            self.splash.after(0, lambda msg=message, prog=progress: self._update_loading(msg, prog))
            
            # Wait for step duration (except for last step)
            if i < len(loading_messages) - 1:
                time.sleep(step_time)
            else:
                time.sleep(0.5)  # Short pause on "Ready!"
        
        # Close splash screen
        self.logger.info("Loading sequence complete, closing splash...")
        self.splash.after(0, self.close_splash)
    
    def _update_loading(self, message, progress):
        """Update loading message and progress value."""
        if hasattr(self, 'loading_label'):
            self.loading_label.config(text=message)
        self.progress_value = progress
    
    def close_splash(self):
        """Close splash screen and call callback."""
        try:
            self.logger.info("Closing splash screen...")
            self.animation_running = False
            time.sleep(0.1)  # Allow animation thread to finish
            self.splash.destroy()
            
            # Call callback if provided
            if self.callback:
                self.logger.info("Calling splash completion callback...")
                self.callback()
            else:
                self.logger.info("No callback provided")
                
        except Exception as e:
            self.logger.error(f"Error closing splash screen: {e}")
    
    def update_message(self, message, progress=None):
        """Update the loading message and optionally progress."""
        if hasattr(self, 'loading_label'):
            self.loading_label.config(text=message)
        if progress is not None:
            self.progress_value = progress
    
    def force_close(self):
        """Force close splash screen (emergency)."""
        try:
            self.animation_running = False
            if hasattr(self, 'splash') and self.splash.winfo_exists():
                self.splash.destroy()
        except Exception:
            pass


def show_splash_screen(duration=3.0, callback=None):
    """
    Show splash screen (convenience function).
    
    Args:
        duration: Duration to show splash screen
        callback: Function to call when complete
    
    Returns:
        SplashScreen instance
    """
    return SplashScreen(duration=duration, callback=callback)


def test_splash_screen():
    """Test the splash screen standalone."""
    print("Testing splash screen...")
    
    def test_callback():
        print("Splash screen test completed!")
    
    root = tk.Tk()
    root.withdraw()
    
    splash = SplashScreen(
        duration=5.0,
        callback=test_callback,
        parent=root
    )
    
    root.mainloop()


if __name__ == "__main__":
    # Test mode when run directly
    test_splash_screen()
