"""
Splash Screen Module

Professional splash screen for CodePulse Monitor application.
Optimized for both development and PyInstaller executable environments.
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
from pathlib import Path
import os
import sys
import math  # ANIMATION_ENHANCED - Added for animations

# Try to import PIL, fall back gracefully if not available
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class SplashScreen:
    """Splash                  # In PyInstaller exe, just clean up without force exit
            if self._is_frozen:
                # Stop animations before cleanup
            self.stop_animation()
            print("EXE CLEANUP - No force exit")  # Debug
                import time
                time.sleep(0.1)  # Brief cleanup delay
                # DO NOT call os._exit(0) - let main app start!
        
        # DO NOT schedule force exit - let program continue normallyPyInstaller exe, just clean up without force exit
            if self._is_frozen:
                # Stop animations before cleanup
            self.stop_animation()
            print("EXE CLEANUP - No force exit")  # Debug
                import time
                time.sleep(0.1)  # Brief cleanup delay
                # DO NOT call os._exit(0) - let main app start!for application startup."""
    
    def __init__(self, duration=3.0, splash_image_path=None, scale_mode="stretch"):
        """
        Initialize splash screen.
        
        Args:
            duration: How long to show splash screen in seconds
            splash_image_path: Path to custom splash screen image (PNG, JPG, etc.)
                              If provided, this image will be used as the entire splash screen background
            scale_mode: How to scale the image ("stretch", "fit", "crop")
                       - "stretch": Stretch to fill (may distort aspect ratio)
                       - "fit": Scale to fit with letterboxing (preserves aspect ratio)
                       - "crop": Scale to fill and crop excess (preserves aspect ratio)
        """
        self.duration = duration
        self.splash_image_path = splash_image_path
        self.scale_mode = scale_mode
        self.splash = None
        self.progress_var = None
        self.status_var = None
        self.splash_photo = None
        self._animation_running = False
        self._is_frozen = getattr(sys, 'frozen', False)  # Check if running as PyInstaller exe
        self._animation_steps = []
        self._current_step = 0
        

    def init_animations(self):
        """Initialize animation variables."""
        self._animation_frame = 0
        self._animation_running = True
        self._pulse_direction = 1
        self._current_alpha = 0.9
    
    def animate_splash(self):
        """Create smooth pulsing animation."""
        if not hasattr(self, '_animation_running') or not self._animation_running:
            return
        
        try:
            if hasattr(self, 'splash') and self.splash and self.splash.winfo_exists():
                # Smooth pulsing effect
                self._animation_frame += 1
                pulse = 0.8 + 0.2 * abs(math.sin(self._animation_frame * 0.1))
                
                try:
                    self.splash.attributes('-alpha', pulse)
                except:
                    pass  # Some systems don't support alpha
                
                # Continue animation
                if self._animation_running:
                    self.splash.after(50, self.animate_splash)
        except:
            self._animation_running = False
    
    def stop_animation(self):
        """Stop the animation and restore normal appearance."""
        self._animation_running = False
        if hasattr(self, 'splash') and self.splash:
            try:
                self.splash.attributes('-alpha', 1.0)
            except:
                pass

    def show(self, callback=None):
        """
        Show the splash screen.
        
        Args:
            callback: Function to call when splash screen finishes
        """
        # Create splash window
        self.splash = tk.Toplevel()
        self.splash.title("CodePulse Monitor")
        self.splash.geometry("500x350")
        self.splash.resizable(False, False)
        self.splash.configure(bg="#2c3e50")
        
        # Remove window decorations and make it stay on top
        self.splash.overrideredirect(True)
        self.splash.attributes("-topmost", True)
        
        # Center the splash screen
        self.center_window()
        
        # Create the splash content
        self.create_splash_content()
        
        # Force window to be visible and update
        self.splash.deiconify()
        self.splash.lift()
        self.splash.focus_force()
        self.splash.update()
        
        # Initialize and start animations
        self.init_animations()
        self.animate_splash()
        print("✅ Animated splash screen displayed")  # Debug
        
        # Set up a safety timeout to force close if animation fails
        max_duration = int((self.duration + 2.0) * 1000)  # Add 2 seconds safety margin
        self.splash.after(max_duration, lambda: self._force_timeout_close(callback))
        
        # Start the loading animation
        self.start_loading_animation(callback)
    
    def _force_timeout_close(self, callback):
        """Force close splash screen if it takes too long (safety mechanism)."""
        print("⚠️  SAFETY TIMEOUT TRIGGERED!")  # Debug
        if self.splash and self.splash.winfo_exists():
            print("🚨 Force closing stuck splash screen!")  # Debug
            self.stop_animation()  # Stop animations before closing
            self._animation_running = False
            try:
                self.splash.destroy()
                self.splash = None
                print("✅ Force close successful")  # Debug
            except:
                print("⚠️  Force close failed, setting to None")  # Debug
                self.splash = None
            
            if callback:
                print("🔄 Executing callback after force close...")  # Debug
                try:
                    callback()
                    print("✅ Force callback executed!")  # Debug
                except Exception as e:
                    print(f"❌ Force callback error: {e}")  # Debug
        
    def center_window(self):
        """Center the splash screen on the display."""
        # Get screen dimensions
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - 500) // 2
        y = (screen_height - 350) // 2
        
        self.splash.geometry(f"500x350+{x}+{y}")
    
    def scale_image(self, pil_image, target_width=500, target_height=350):
        """
        Scale image according to the specified scale mode.
        
        Args:
            pil_image: PIL Image object
            target_width: Target width in pixels
            target_height: Target height in pixels
            
        Returns:
            Scaled PIL Image object
        """
        original_width, original_height = pil_image.size
        target_ratio = target_width / target_height
        original_ratio = original_width / original_height
        
        if self.scale_mode == "stretch":
            # Stretch to fill (may distort)
            return pil_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        elif self.scale_mode == "fit":
            # Scale to fit with letterboxing (preserves aspect ratio)
            if original_ratio > target_ratio:
                # Image is wider - fit to width
                new_width = target_width
                new_height = int(target_width / original_ratio)
            else:
                # Image is taller - fit to height
                new_height = target_height
                new_width = int(target_height * original_ratio)
            
            # Resize the image
            scaled_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Create a new image with the target size and paste the scaled image centered
            final_image = Image.new('RGB', (target_width, target_height), (44, 62, 80))  # Dark blue background
            paste_x = (target_width - new_width) // 2
            paste_y = (target_height - new_height) // 2
            final_image.paste(scaled_image, (paste_x, paste_y))
            
            return final_image
            
        elif self.scale_mode == "crop":
            # Scale to fill and crop excess (preserves aspect ratio)
            if original_ratio > target_ratio:
                # Image is wider - fit to height and crop sides
                new_height = target_height
                new_width = int(target_height * original_ratio)
                crop_x = (new_width - target_width) // 2
                crop_y = 0
            else:
                # Image is taller - fit to width and crop top/bottom
                new_width = target_width
                new_height = int(target_width / original_ratio)
                crop_x = 0
                crop_y = (new_height - target_height) // 2
            
            # Resize the image
            scaled_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Crop to target size
            cropped_image = scaled_image.crop((crop_x, crop_y, crop_x + target_width, crop_y + target_height))
            
            return cropped_image
        
        else:
            # Default to stretch if unknown mode
            return pil_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    def create_splash_content(self):
        """Create the visual content of the splash screen."""
        # Check if we should use a custom splash image and PIL is available
        if (self.splash_image_path and os.path.exists(self.splash_image_path) and PIL_AVAILABLE):
            try:
                self.create_image_splash()
            except Exception as e:
                print(f"Failed to load custom splash image: {e}")
                self.create_default_splash()
        else:
            self.create_default_splash()
    
    def create_image_splash(self):
        """Create splash screen with custom background image."""
        if not PIL_AVAILABLE:
            self.create_default_splash()
            return
            
        try:
            # Load and scale the splash image
            pil_image = Image.open(self.splash_image_path)
            scaled_image = self.scale_image(pil_image, 500, 350)
            self.splash_photo = ImageTk.PhotoImage(scaled_image)
            
            # Create a label with the background image that fills the entire splash
            bg_label = tk.Label(self.splash, image=self.splash_photo, bd=0, highlightthickness=0)
            bg_label.place(x=0, y=0, width=500, height=350)
            
            # Create a minimal progress bar at the very bottom
            self.progress_var = tk.DoubleVar()
            progress_bar = ttk.Progressbar(
                self.splash,
                variable=self.progress_var,
                maximum=100,
                length=300,
                style="Minimal.Horizontal.TProgressbar"
            )
            progress_bar.place(x=250, y=330, anchor="center")
            
            # Configure minimal progress bar style
            style = ttk.Style()
            style.configure(
                "Minimal.Horizontal.TProgressbar",
                troughcolor="#ffffff",
                background="#000000",
                borderwidth=0,
                lightcolor="#000000",
                darkcolor="#000000"
            )
            
            # Store status variable but don't display it
            self.status_var = tk.StringVar(value="Initializing...")
            
        except Exception as e:
            print(f"Failed to load splash image: {e}")
            # Fall back to default splash
            self.create_default_splash()
    
    def create_default_splash(self):
        """Create the default splash screen design."""
        # Main frame with gradient-like background
        main_frame = tk.Frame(self.splash, bg="#2c3e50", width=500, height=350)
        main_frame.pack(fill="both", expand=True)
        main_frame.pack_propagate(False)
        
        # Header section
        header_frame = tk.Frame(main_frame, bg="#34495e", height=80)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        # Application logo/icon area
        logo_frame = tk.Frame(header_frame, bg="#34495e", width=60, height=60)
        logo_frame.pack(side="left", padx=(10, 20), pady=10)
        logo_frame.pack_propagate(False)
        
        # Removed logo - just empty space
        # logo_label = tk.Label(
        #     logo_frame, 
        #     text="⚡", 
        #     font=("Arial", 32), 
        #     fg="#e74c3c", 
        #     bg="#34495e"
        # )
        # logo_label.pack(expand=True)
        
        # Title and version
        title_frame = tk.Frame(header_frame, bg="#34495e")
        title_frame.pack(side="left", fill="both", expand=True, pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="CodePulse Monitor",
            font=("Arial", 24, "bold"),
            fg="#ecf0f1",
            bg="#34495e"
        )
        title_label.pack(anchor="w")
        
        version_label = tk.Label(
            title_frame,
            text="Version 1.0.0",
            font=("Arial", 12),
            fg="#bdc3c7",
            bg="#34495e"
        )
        version_label.pack(anchor="w")
        
        # Description section
        desc_frame = tk.Frame(main_frame, bg="#2c3e50", height=80)
        desc_frame.pack(fill="x", padx=20, pady=10)
        desc_frame.pack_propagate(False)
        
        desc_label = tk.Label(
            desc_frame,
            text="Python File Monitoring & Auto-Reload System",
            font=("Arial", 14),
            fg="#95a5a6",
            bg="#2c3e50"
        )
        desc_label.pack(pady=10)
        
        features_label = tk.Label(
            desc_frame,
            text="• Real-time file monitoring  • Automatic script reloading  • Process management",
            font=("Arial", 11),
            fg="#7f8c8d",
            bg="#2c3e50"
        )
        features_label.pack(pady=5)
        
        # Progress section
        progress_frame = tk.Frame(main_frame, bg="#2c3e50", height=100)
        progress_frame.pack(fill="x", padx=20, pady=10)
        progress_frame.pack_propagate(False)
        
        # Status text
        self.status_var = tk.StringVar(value="Initializing...")
        status_label = tk.Label(
            progress_frame,
            textvariable=self.status_var,
            font=("Arial", 12),
            fg="#ecf0f1",
            bg="#2c3e50"
        )
        status_label.pack(pady=(10, 5))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=400,
            style="Splash.Horizontal.TProgressbar"
        )
        progress_bar.pack(pady=10)
        
        # Configure progress bar style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Splash.Horizontal.TProgressbar",
            troughcolor="#34495e",
            background="#e74c3c",
            borderwidth=0,
            lightcolor="#e74c3c",
            darkcolor="#c0392b"
        )
        
        # Footer
        footer_frame = tk.Frame(main_frame, bg="#2c3e50", height=40)
        footer_frame.pack(fill="x", side="bottom", padx=20, pady=10)
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(
            footer_frame,
            text="Loading application components...",
            font=("Arial", 10),
            fg="#7f8c8d",
            bg="#2c3e50"
        )
        footer_label.pack(pady=10)
    
    def start_loading_animation(self, callback=None):
        """Start the loading animation and progress updates."""
        self._animation_running = True
        self._animation_steps = [
            ("Loading configuration...", 15),
            ("Initializing file monitor...", 30),
            ("Setting up process manager...", 50),
            ("Loading GUI components...", 70),
            ("Preparing user interface...", 85),
            ("Starting application...", 100)
        ]
        self._current_step = 0
        
        # Calculate timing - use shorter intervals for PyInstaller
        step_duration = int((self.duration * 1000) / len(self._animation_steps))  # Convert to milliseconds
        
        if self._is_frozen:
            # In PyInstaller, use after() instead of threading for better reliability
            self._animate_step_scheduled(callback, step_duration)
        else:
            # In development, use threading
            def animate():
                try:
                    for i, (status, progress) in enumerate(self._animation_steps):
                        if not self._animation_running:
                            return
                            
                        try:
                            if self.splash and self.splash.winfo_exists():
                                self.status_var.set(status)
                                
                                # Animate progress to target value
                                current_progress = self.progress_var.get()
                                steps_to_target = 10
                                increment = (progress - current_progress) / steps_to_target
                                
                                for step in range(steps_to_target):
                                    if not self._animation_running:
                                        return
                                        
                                    try:
                                        if self.splash and self.splash.winfo_exists():
                                            new_progress = current_progress + (increment * (step + 1))
                                            self.progress_var.set(new_progress)
                                            self.splash.update()
                                            time.sleep((step_duration / 1000) / steps_to_target)
                                        else:
                                            return
                                    except tk.TclError:
                                        return
                            else:
                                return
                        except tk.TclError:
                            return
                    
                    # Hold at 100% briefly  
                    if self._animation_running:
                        time.sleep(0.3)
                    
                    # Finish
                    self._finish_splash(callback)
                        
                except Exception as e:
                    print(f"Animation error: {e}")
                    if callback:
                        try:
                            callback()
                        except:
                            pass
            
            # Run animation in a separate thread
            animation_thread = threading.Thread(target=animate, daemon=True)
            animation_thread.start()
    
    def _animate_step_scheduled(self, callback, step_duration):
        """Animate a single step using Tkinter's after() method (for PyInstaller)."""
        print(f"🎬 Animate step {self._current_step}/{len(self._animation_steps)}")  # Debug
        
        if not self._animation_running or self._current_step >= len(self._animation_steps):
            print("🎯 Animation complete, finishing splash...")  # Debug
            # Animation complete, finish immediately in exe mode
            self._finish_splash_immediately(callback)
            return
        
        try:
            if self.splash and self.splash.winfo_exists():
                status, target_progress = self._animation_steps[self._current_step]
                self.status_var.set(status)
                self.progress_var.set(target_progress)
                self.splash.update_idletasks()
                print(f"✅ Step {self._current_step}: {status} ({target_progress}%)")  # Debug
                
                self._current_step += 1
                
                # Schedule next step immediately for faster animation in exe
                if self._current_step < len(self._animation_steps):
                    self.splash.after(step_duration // 2, lambda: self._animate_step_scheduled(callback, step_duration))
                else:
                    # Final step, finish after brief delay
                    self.splash.after(200, lambda: self._finish_splash_immediately(callback))
            else:
                print("⚠️  Splash window gone during animation")  # Debug
                if callback:
                    callback()
        except tk.TclError as e:
            print(f"⚠️  TclError in animate step: {e}")  # Debug
            if callback:
                callback()
    
    def _finish_splash_immediately(self, callback):
        """Immediate finish for exe environment with OS-level force exit."""
        print("IMMEDIATE FINISH - Clean splash close")  # Debug
        
        # Stop animation
        self._animation_running = False
        
        # Execute callback directly (no threading to avoid main loop issues)
        if callback:
            print("Executing callback directly...")  # Debug
            try:
                callback()
                print("Callback executed successfully!")  # Debug
            except Exception as e:
                print(f"Callback error: {e}")  # Debug
        
        # Force destroy splash with OS-level exit after brief delay
        def force_exit():
            try:
                if self.splash:
                    print("🗑️  Destroying splash window...")  # Debug
                    self.splash.destroy()
                    self.splash = None
                    print("✅ Splash destroyed!")  # Debug
            except:
                print("⚠️  Error destroying splash")  # Debug
            
            # In PyInstaller exe, force terminate this process after callback
            if self._is_frozen:
                print("� FORCE EXIT - PyInstaller exe environment")  # Debug
                import time
                time.sleep(0.5)  # Give callback time to execute
                import os
                os._exit(0)  # Nuclear option - terminate this process
        
        # Schedule force exit
        import threading
        exit_thread = threading.Thread(target=force_exit, daemon=True)
        exit_thread.start()
    
    # def _animate_progress_to_target(self, start_progress, target_progress, callback, step_duration, current_sub_step, total_sub_steps):
    #     """Smoothly animate progress bar to target value."""
    #     # DISABLED: This complex animation was causing issues in PyInstaller exe
    #     # Using simpler direct progress updates instead
    #     pass
    
    def _finish_splash(self, callback):
        """Finish splash screen and call callback on main thread."""
        print("🔄 Finishing splash screen...")  # Debug message
        
        # Stop animation first
        self._animation_running = False
        
        try:
            # Force final update to show 100%
            if self.splash and self.splash.winfo_exists():
                self.progress_var.set(100)
                self.status_var.set("Ready!")
                self.splash.update_idletasks()
                print("✅ Final splash update complete")  # Debug message
                
                # Always close immediately - no delay needed
                self._close_and_callback(callback)
            else:
                print("⚠️  Splash window not found, calling callback directly")  # Debug message
                # Window already gone, just call callback
                if callback:
                    callback()
        except tk.TclError as e:
            print(f"⚠️  TclError in finish_splash: {e}, calling callback directly")  # Debug message
            # Window already destroyed, just call callback
            if callback:
                callback()
    
    def _close_and_callback(self, callback):
        """Close splash and execute callback."""
        print("🔄 Closing splash and executing callback...")  # Debug message
        
        try:
            if self.splash and self.splash.winfo_exists():
                print("🗑️  Destroying splash window...")  # Debug message
                self.splash.withdraw()  # Hide first
                self.splash.destroy()   # Then destroy
                self.splash = None
                print("✅ Splash window destroyed")  # Debug message
        except tk.TclError as e:
            print(f"⚠️  TclError during close: {e}")  # Debug message
            self.splash = None
        
        # Call the callback function if provided
        if callback:
            print("🔄 Executing splash callback...")  # Debug message
            try:
                callback()
                print("✅ Splash callback executed successfully")  # Debug message
            except Exception as e:
                print(f"❌ Error in splash callback: {e}")
        else:
            print("⚠️  No callback provided")  # Debug message
    
    def close(self):
        """Close the splash screen immediately."""
        print("🔄 Force closing splash screen...")  # Debug message
        
        # Stop animation
        self._animation_running = False
        
        try:
            if self.splash and self.splash.winfo_exists():
                print("🗑️  Force destroying splash window...")  # Debug message
                self.splash.withdraw()  # Hide first
                self.splash.destroy()   # Then destroy
                self.splash = None
                print("✅ Splash force closed successfully")  # Debug message
        except tk.TclError as e:
            print(f"⚠️  TclError during force close: {e}")  # Debug message
            self.splash = None
    
    def is_visible(self):
        """Check if splash screen is still visible."""
        try:
            return self.splash and self.splash.winfo_exists()
        except tk.TclError:
            return False

def show_splash_screen(duration=3.0, callback=None, splash_image_path=None, scale_mode="stretch"):
    """
    Convenience function to show splash screen.
    
    Args:
        duration: How long to show splash screen in seconds
        callback: Function to call when splash screen finishes
        splash_image_path: Path to custom splash screen image (full background)
        scale_mode: How to scale the image ("stretch", "fit", "crop")
                   - "stretch": Stretch to fill (may distort aspect ratio)
                   - "fit": Scale to fit with letterboxing (preserves aspect ratio)
                   - "crop": Scale to fill and crop excess (preserves aspect ratio)
    
    Returns:
        SplashScreen instance for manual control if needed
    """
    print(f"🎬 Creating splash screen (duration: {duration}s)...")  # Debug message
    
    splash = SplashScreen(duration, splash_image_path, scale_mode)
    
    # Simple callback wrapper that just executes the callback
    def wrapped_callback():
        print("Splash callback wrapper executing...")  # Debug message
        # Execute the original callback directly - splash should already be closed
        if callback:
            try:
                print("Calling original callback...")  # Debug message
                callback()
                print("Original callback completed")  # Debug message
            except Exception as e:
                print(f"Error in callback: {e}")
                # Don't retry - let any errors propagate
    
    splash.show(wrapped_callback)
    print("🎬 Splash screen shown, returning instance")  # Debug message
    return splash
