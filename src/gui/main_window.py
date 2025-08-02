"""
Main Window GUI
The primary user interface for the VoidPulse application.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import logging
import threading
from pathlib import Path
from typing import Optional, List
from core.folder_scanner import EmptyFolderScanner


class MainWindow:
    """Main application window."""
    
    def __init__(self, root: tk.Tk, app_manager):
        self.root = root
        self.app_manager = app_manager
        self.logger = logging.getLogger(__name__)
        
        # Initialize scanner
        self.scanner = EmptyFolderScanner()
        self.scan_results = []
        self.selected_folders = []
        
        # Initialize UI components
        self.setup_ui()
        self.setup_menu()
        self.setup_events()
    
    def setup_ui(self):
        """Set up the main user interface."""
        # Configure modern styling
        self.setup_modern_styles()
        
        # Configure main frame with modern padding
        self.main_frame = ttk.Frame(self.root, style="Modern.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create modern notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame, style="Modern.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_home_tab()
        self.create_scanner_tab()
        self.create_settings_tab()
        
        # Modern status bar
        self.create_status_bar()
    
    def setup_modern_styles(self):
        """Configure modern UI styles."""
        style = ttk.Style()
        
        # Configure modern button styles
        try:
            style.configure("Accent.TButton",
                          font=("Segoe UI", 9, "bold"),
                          padding=(10, 5))
            
            style.configure("Modern.TCheckbutton",
                          font=("Segoe UI", 9))
            
            style.configure("Modern.TFrame",
                          relief="flat")
            
            style.configure("Modern.TNotebook",
                          tabposition="n")
            
            style.configure("Modern.TNotebook.Tab",
                          font=("Segoe UI", 10),
                          padding=(15, 8))
        except Exception as e:
            # Fallback if theme doesn't support custom styles
            self.logger.debug(f"Could not apply custom styles: {e}")
    
    def create_home_tab(self):
        """Create the home tab."""
        home_frame = ttk.Frame(self.notebook)
        self.notebook.add(home_frame, text="Dashboard")
        
        # Create main container with padding
        main_container = ttk.Frame(home_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section with modern styling
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # App title with modern font
        title_label = ttk.Label(
            header_frame,
            text="VoidPulse",
            font=("Segoe UI", 24, "bold")
        )
        title_label.pack(anchor=tk.W)
        
        # Subtitle
        subtitle_label = ttk.Label(
            header_frame,
            text="Intelligent folder management and cleanup tool",
            font=("Segoe UI", 11),
            foreground="gray"
        )
        subtitle_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Main actions grid
        actions_container = ttk.Frame(main_container)
        actions_container.pack(fill=tk.BOTH, expand=True)
        
        # Primary action cards
        self.create_action_card(
            actions_container,
            "🔍 Start Scan",
            "Scan directories for empty folders",
            self.quick_scan,
            row=0, column=0, primary=True
        )
        
        self.create_action_card(
            actions_container,
            "📊 View Results",
            "Review your last scan results",
            lambda: self.notebook.select(1),
            row=0, column=1
        )
        
        self.create_action_card(
            actions_container,
            "⚙️ Settings",
            "Configure scan preferences",
            lambda: self.notebook.select(2),
            row=1, column=0
        )
        
        self.create_action_card(
            actions_container,
            "📁 Quick Access",
            "Browse and manage folders",
            self.browse_scan_path,
            row=1, column=1
        )
        
        # Configure grid weights for responsive layout
        actions_container.grid_columnconfigure(0, weight=1)
        actions_container.grid_columnconfigure(1, weight=1)
    
    def create_action_card(self, parent, title, description, command, row, column, primary=False):
        """Create a modern action card."""
        # Card frame with padding
        card_frame = ttk.Frame(parent)
        card_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
        
        # Inner frame for card content
        inner_frame = ttk.LabelFrame(card_frame, text="", padding=20)
        inner_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_font = ("Segoe UI", 12, "bold") if primary else ("Segoe UI", 11, "bold")
        title_label = ttk.Label(inner_frame, text=title, font=title_font)
        title_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Description
        desc_label = ttk.Label(
            inner_frame,
            text=description,
            font=("Segoe UI", 9),
            foreground="gray",
            wraplength=200
        )
        desc_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Action button
        button_style = "Accent.TButton" if primary else "TButton"
        action_button = ttk.Button(
            inner_frame,
            text="Launch" if primary else "Open",
            command=command,
            style=button_style
        )
        action_button.pack(anchor=tk.W)
    
    def create_scanner_tab(self):
        """Create the empty folder scanner tab."""
        scanner_frame = ttk.Frame(self.notebook)
        self.notebook.add(scanner_frame, text="Scanner")
        
        # Create main container with modern layout
        main_container = ttk.Frame(scanner_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header section
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            header_frame,
            text="Empty Folder Scanner",
            font=("Segoe UI", 16, "bold")
        )
        title_label.pack(anchor=tk.W)
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Find and manage empty directories in your system",
            font=("Segoe UI", 10),
            foreground="gray"
        )
        subtitle_label.pack(anchor=tk.W, pady=(2, 0))
        
        # Modern scan controls
        control_frame = ttk.LabelFrame(main_container, text="Scan Configuration", padding=15)
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Path selection with modern styling
        path_frame = ttk.Frame(control_frame)
        path_frame.pack(fill=tk.X, pady=(0, 10))
        
        path_label = ttk.Label(path_frame, text="Target Directory", font=("Segoe UI", 10, "bold"))
        path_label.pack(anchor=tk.W, pady=(0, 5))
        
        path_input_frame = ttk.Frame(path_frame)
        path_input_frame.pack(fill=tk.X)
        
        self.path_var = tk.StringVar()
        path_entry = ttk.Entry(
            path_input_frame,
            textvariable=self.path_var,
            font=("Segoe UI", 10)
        )
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_button = ttk.Button(
            path_input_frame,
            text="📁 Browse",
            command=self.browse_scan_path,
            width=12
        )
        browse_button.pack(side=tk.RIGHT)
        
        # Modern scan options
        options_label = ttk.Label(control_frame, text="Scan Options", font=("Segoe UI", 10, "bold"))
        options_label.pack(anchor=tk.W, pady=(15, 5))
        
        options_frame = ttk.Frame(control_frame)
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.include_subdirs_var = tk.BooleanVar(value=True)
        subdirs_check = ttk.Checkbutton(
            options_frame,
            text="🔄 Include subdirectories (recursive scan)",
            variable=self.include_subdirs_var,
            style="Modern.TCheckbutton"
        )
        subdirs_check.pack(anchor=tk.W, pady=2)
        
        self.scan_hidden_var = tk.BooleanVar(value=False)
        hidden_check = ttk.Checkbutton(
            options_frame,
            text="👁️ Scan hidden files and folders",
            variable=self.scan_hidden_var,
            style="Modern.TCheckbutton"
        )
        hidden_check.pack(anchor=tk.W, pady=2)
        
        # Modern control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(pady=(10, 0))
        
        self.scan_button = ttk.Button(
            button_frame,
            text="🔍 Start Scan",
            command=self.start_scan,
            style="Accent.TButton",
            width=15
        )
        self.scan_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = ttk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_scan_results,
            width=12
        )
        clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        export_button = ttk.Button(
            button_frame,
            text="📤 Export",
            command=self.export_results,
            width=12
        )
        export_button.pack(side=tk.LEFT)
        
        # Modern results area
        results_frame = ttk.LabelFrame(main_container, text="Results", padding=15)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Results header with status
        results_header = ttk.Frame(results_frame)
        results_header.pack(fill=tk.X, pady=(0, 10))
        
        self.summary_var = tk.StringVar(value="Ready to scan - Select a directory above")
        summary_label = ttk.Label(
            results_header,
            textvariable=self.summary_var,
            font=("Segoe UI", 10)
        )
        summary_label.pack(side=tk.LEFT)
        
        # Modern progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            results_header,
            variable=self.progress_var,
            mode='indeterminate',
            length=200
        )
        
        # Modern results tree view
        tree_container = ttk.Frame(results_frame)
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        # Create modern treeview
        style = ttk.Style()
        style.configure("Modern.Treeview", font=("Segoe UI", 9))
        style.configure("Modern.Treeview.Heading", font=("Segoe UI", 9, "bold"))
        
        self.results_tree = ttk.Treeview(
            tree_container,
            columns=('size', 'modified', 'type'),
            show='tree headings',
            selectmode='extended',
            style="Modern.Treeview"
        )
        
        # Configure modern columns
        self.results_tree.heading('#0', text='📁 Empty Folder Path')
        self.results_tree.heading('size', text='📊 Size')
        self.results_tree.heading('modified', text='🕒 Modified')
        self.results_tree.heading('type', text='🏷️ Type')
        
        self.results_tree.column('#0', width=400, minwidth=200)
        self.results_tree.column('size', width=80, minwidth=60)
        self.results_tree.column('modified', width=150, minwidth=100)
        self.results_tree.column('type', width=100, minwidth=80)
        
        # Modern scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.results_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL, command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout for better control
        self.results_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        tree_container.grid_columnconfigure(0, weight=1)
        tree_container.grid_rowconfigure(0, weight=1)
        
        # Modern deletion controls
        delete_frame = ttk.LabelFrame(main_container, text="🗑️ Folder Management", padding=15)
        delete_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Information section
        info_label = ttk.Label(
            delete_frame,
            text="Select folders from the results above to manage or delete them",
            font=("Segoe UI", 9),
            foreground="gray"
        )
        info_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Selection controls
        selection_frame = ttk.Frame(delete_frame)
        selection_frame.pack(fill=tk.X, pady=(0, 10))
        
        selection_label = ttk.Label(selection_frame, text="Selection", font=("Segoe UI", 10, "bold"))
        selection_label.pack(anchor=tk.W, pady=(0, 5))
        
        selection_buttons = ttk.Frame(selection_frame)
        selection_buttons.pack(anchor=tk.W)
        
        ttk.Button(
            selection_buttons,
            text="✅ Select All",
            command=self.select_all_results,
            width=12
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            selection_buttons,
            text="❌ Clear Selection",
            command=self.select_none_results,
            width=15
        ).pack(side=tk.LEFT)
        
        # Action controls
        action_frame = ttk.Frame(delete_frame)
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        action_label = ttk.Label(action_frame, text="Actions", font=("Segoe UI", 10, "bold"))
        action_label.pack(anchor=tk.W, pady=(0, 5))
        
        action_buttons = ttk.Frame(action_frame)
        action_buttons.pack(anchor=tk.W)
        
        ttk.Button(
            action_buttons,
            text="👁️ Preview Delete",
            command=self.preview_delete,
            width=15
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            action_buttons,
            text="🗑️ Delete Selected",
            command=self.delete_selected,
            style="Accent.TButton",
            width=15
        ).pack(side=tk.LEFT)
    
    def create_settings_tab(self):
        """Create the settings tab."""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Main container with modern layout
        main_container = ttk.Frame(settings_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        title_label = ttk.Label(
            header_frame,
            text="Application Settings",
            font=("Segoe UI", 16, "bold")
        )
        title_label.pack(anchor=tk.W)
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Customize your FolderPulse experience",
            font=("Segoe UI", 10),
            foreground="gray"
        )
        subtitle_label.pack(anchor=tk.W, pady=(2, 0))
        
        # Modern settings sections
        # Appearance section
        appearance_frame = ttk.LabelFrame(main_container, text="🎨 Appearance", padding=15)
        appearance_frame.pack(fill=tk.X, pady=(0, 15))
        
        theme_label = ttk.Label(appearance_frame, text="Theme", font=("Segoe UI", 10, "bold"))
        theme_label.pack(anchor=tk.W, pady=(0, 5))
        
        theme_frame = ttk.Frame(appearance_frame)
        theme_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.theme_var = tk.StringVar(value=self.app_manager.get_config("theme", "default"))
        theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=["🌟 Default", "🌙 Dark", "☀️ Light"],
            state="readonly",
            font=("Segoe UI", 10),
            width=20
        )
        theme_combo.pack(side=tk.LEFT)
        
        theme_desc = ttk.Label(
            theme_frame,
            text="Choose your preferred visual theme",
            font=("Segoe UI", 9),
            foreground="gray"
        )
        theme_desc.pack(side=tk.LEFT, padx=(10, 0))
        
        # Behavior section
        behavior_frame = ttk.LabelFrame(main_container, text="⚡ Behavior", padding=15)
        behavior_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.auto_save_var = tk.BooleanVar(value=self.app_manager.get_config("auto_save", True))
        auto_save_check = ttk.Checkbutton(
            behavior_frame,
            text="💾 Auto-save settings on change",
            variable=self.auto_save_var,
            style="Modern.TCheckbutton"
        )
        auto_save_check.pack(anchor=tk.W, pady=(0, 10))
        
        self.remember_window_var = tk.BooleanVar(value=self.app_manager.get_config("remember_window", True))
        remember_window_check = ttk.Checkbutton(
            behavior_frame,
            text="🪟 Remember window size and position",
            variable=self.remember_window_var,
            style="Modern.TCheckbutton"
        )
        remember_window_check.pack(anchor=tk.W)
        
        # Actions section
        actions_frame = ttk.Frame(main_container)
        actions_frame.pack(fill=tk.X, pady=(20, 0))
        
        save_button = ttk.Button(
            actions_frame,
            text="💾 Save Settings",
            command=self.save_settings,
            style="Accent.TButton",
            width=20
        )
        save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        reset_button = ttk.Button(
            actions_frame,
            text="🔄 Reset to Defaults",
            command=self.reset_settings,
            width=20
        )
        reset_button.pack(side=tk.LEFT)
    
    def create_status_bar(self):
        """Create the modern status bar."""
        # Status bar container
        status_container = ttk.Frame(self.root)
        status_container.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Status bar with modern styling
        self.status_var = tk.StringVar(value="🟢 Ready")
        status_bar = ttk.Label(
            status_container,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            relief=tk.FLAT,
            anchor=tk.W,
            padding=(10, 5)
        )
        status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Optional: Add version info or additional status elements
        version_label = ttk.Label(
            status_container,
            text="FolderPulse v1.0",
            font=("Segoe UI", 8),
            foreground="gray",
            anchor=tk.E,
            padding=(5, 5)
        )
        version_label.pack(side=tk.RIGHT)
    
    def setup_menu(self):
        """Set up the application menu."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Scan Directory...", command=self.quick_scan)
        file_menu.add_command(label="Export Results...", command=self.export_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Scan menu
        scan_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Scan", menu=scan_menu)
        scan_menu.add_command(label="Start Scan", command=self.start_scan)
        scan_menu.add_command(label="Clear Results", command=self.clear_scan_results)
        scan_menu.add_separator()
        scan_menu.add_command(label="Select All Results", command=self.select_all_results)
        scan_menu.add_command(label="Select None", command=self.select_none_results)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Refresh Results", command=self.refresh_view)
        view_menu.add_command(label="Scanner Tab", command=lambda: self.notebook.select(1))
        view_menu.add_command(label="Settings Tab", command=lambda: self.notebook.select(2))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def setup_events(self):
        """Set up event handlers."""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    # Event handlers
    def quick_scan(self):
        """Quick scan with folder selection."""
        folder = filedialog.askdirectory(title="Select Folder to Scan for Empty Folders")
        if folder:
            self.path_var.set(folder)
            self.notebook.select(1)  # Switch to scanner tab
            self.start_scan()
    
    def browse_scan_path(self):
        """Browse for a path to scan."""
        folder = filedialog.askdirectory(title="Select Folder to Scan")
        if folder:
            self.path_var.set(folder)
    
    def start_scan(self):
        """Start scanning for empty folders."""
        path = self.path_var.get()
        if not path:
            messagebox.showwarning("Warning", "Please select a directory to scan.")
            return
        
        if not Path(path).exists():
            messagebox.showerror("Error", "Selected directory does not exist.")
            return
        
        # Disable scan button and show progress
        self.scan_button.config(state=tk.DISABLED, text="Scanning...")
        self.progress_bar.pack(side=tk.RIGHT, padx=(10, 0))
        self.progress_bar.start()
        self.summary_var.set("Scanning in progress...")
        
        # Clear previous results
        self.clear_scan_results(update_summary=False)
        
        # Start scan in background thread
        scan_thread = threading.Thread(target=self._perform_scan, args=(path,))
        scan_thread.daemon = True
        scan_thread.start()
    
    def _perform_scan(self, path: str):
        """Perform the actual scan in background thread."""
        try:
            include_subdirs = self.include_subdirs_var.get()
            scan_hidden = self.scan_hidden_var.get()
            
            # Perform scan
            empty_folders = self.scanner.scan_directory(
                path,
                include_subdirectories=include_subdirs,
                scan_hidden=scan_hidden
            )
            
            # Update UI in main thread
            self.root.after(0, self._scan_completed, empty_folders)
            
        except Exception as e:
            self.root.after(0, self._scan_error, str(e))
    
    def _scan_completed(self, empty_folders: List[Path]):
        """Handle scan completion in main thread."""
        self.scan_results = empty_folders
        
        # Update UI
        self.scan_button.config(state=tk.NORMAL, text="Start Scan")
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        
        # Update summary
        scan_summary = self.scanner.get_scan_summary()
        summary_text = (
            f"Found {len(empty_folders)} empty folders "
            f"(scanned {scan_summary['total_folders']} total folders in "
            f"{scan_summary['scan_time']:.1f}s)"
        )
        self.summary_var.set(summary_text)
        
        # Populate results tree
        self._populate_results_tree(empty_folders)
        
        self.status_var.set(f"Scan completed: {len(empty_folders)} empty folders found")
        
        if empty_folders:
            self.logger.info(f"Scan completed: found {len(empty_folders)} empty folders")
        else:
            messagebox.showinfo("Scan Complete", "No empty folders found!")
    
    def _scan_error(self, error_message: str):
        """Handle scan error in main thread."""
        self.scan_button.config(state=tk.NORMAL, text="Start Scan")
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.summary_var.set("Scan failed")
        
        messagebox.showerror("Scan Error", f"Failed to scan directory:\n{error_message}")
        self.status_var.set("Scan failed")
    
    def _populate_results_tree(self, empty_folders: List[Path]):
        """Populate the results tree with empty folders."""
        import datetime
        import os
        
        for folder in empty_folders:
            try:
                # Get folder stats
                stats = folder.stat()
                modified_time = datetime.datetime.fromtimestamp(stats.st_mtime)
                modified_str = modified_time.strftime("%Y-%m-%d %H:%M")
                
                # Insert into tree
                self.results_tree.insert(
                    '',
                    'end',
                    text=str(folder),
                    values=('0 bytes', modified_str)
                )
            except Exception as e:
                # If we can't get stats, still show the folder
                self.results_tree.insert(
                    '',
                    'end',
                    text=str(folder),
                    values=('Unknown', 'Unknown')
                )
    
    def clear_scan_results(self, update_summary: bool = True):
        """Clear the scan results."""
        # Clear tree view
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Clear internal results
        self.scan_results = []
        self.selected_folders = []
        
        if update_summary:
            self.summary_var.set("No scan performed yet")
            self.status_var.set("Ready")
    
    def select_all_results(self):
        """Select all items in the results tree."""
        for item in self.results_tree.get_children():
            self.results_tree.selection_add(item)
    
    def select_none_results(self):
        """Deselect all items in the results tree."""
        self.results_tree.selection_remove(self.results_tree.selection())
    
    def get_selected_folders(self) -> List[Path]:
        """Get the currently selected folders from the tree."""
        selected_items = self.results_tree.selection()
        selected_folders = []
        
        for item in selected_items:
            folder_path = self.results_tree.item(item, 'text')
            selected_folders.append(Path(folder_path))
        
        return selected_folders
    
    def preview_delete(self):
        """Preview which folders would be deleted (dry run)."""
        selected_folders = self.get_selected_folders()
        
        if not selected_folders:
            messagebox.showwarning("No Selection", "Please select folders to preview deletion.")
            return
        
        # Perform dry run
        deleted, failed = self.scanner.delete_empty_folders(selected_folders, dry_run=True)
        
        # Show preview dialog
        preview_text = f"Dry Run Results:\n\n"
        preview_text += f"Would delete {len(deleted)} folders:\n"
        for folder in deleted[:10]:  # Show first 10
            preview_text += f"  • {folder}\n"
        
        if len(deleted) > 10:
            preview_text += f"  ... and {len(deleted) - 10} more\n"
        
        if failed:
            preview_text += f"\nWould fail to delete {len(failed)} folders:\n"
            for folder, error in failed[:5]:  # Show first 5 failures
                preview_text += f"  • {folder}: {error}\n"
        
        messagebox.showinfo("Delete Preview", preview_text)
    
    def delete_selected(self):
        """Delete the selected empty folders."""
        selected_folders = self.get_selected_folders()
        
        if not selected_folders:
            messagebox.showwarning("No Selection", "Please select folders to delete.")
            return
        
        # Confirmation dialog
        confirm_text = (
            f"Are you sure you want to delete {len(selected_folders)} empty folders?\n\n"
            "This action cannot be undone!"
        )
        
        if not messagebox.askyesno("Confirm Deletion", confirm_text):
            return
        
        # Perform actual deletion
        try:
            deleted, failed = self.scanner.delete_empty_folders(selected_folders, dry_run=False)
            
            # Show results
            result_text = f"Deletion completed:\n\n"
            result_text += f"Successfully deleted: {len(deleted)} folders\n"
            
            if failed:
                result_text += f"Failed to delete: {len(failed)} folders\n\n"
                result_text += "Failed deletions:\n"
                for folder, error in failed[:5]:
                    result_text += f"  • {folder}: {error}\n"
            
            messagebox.showinfo("Deletion Results", result_text)
            
            # Remove deleted items from tree
            for item in self.results_tree.selection():
                folder_path = Path(self.results_tree.item(item, 'text'))
                if folder_path in deleted:
                    self.results_tree.delete(item)
            
            # Update summary
            remaining_count = len(self.results_tree.get_children())
            self.summary_var.set(f"Remaining empty folders: {remaining_count}")
            self.status_var.set(f"Deleted {len(deleted)} folders")
            
        except Exception as e:
            messagebox.showerror("Deletion Error", f"Error during deletion:\n{e}")
    
    def export_results(self):
        """Export scan results to file."""
        if not self.scan_results:
            messagebox.showwarning("No Results", "No scan results to export.")
            return
        
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            title="Export Scan Results",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("CSV files", "*.csv"),
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Determine format from extension
                file_ext = Path(file_path).suffix.lower()
                format_map = {'.txt': 'txt', '.csv': 'csv', '.json': 'json'}
                format_type = format_map.get(file_ext, 'txt')
                
                # Export results
                if self.scanner.export_results(file_path, format_type):
                    messagebox.showinfo("Export Complete", f"Results exported to:\n{file_path}")
                    self.status_var.set("Results exported")
                else:
                    messagebox.showerror("Export Failed", "Failed to export results.")
            
            except Exception as e:
                messagebox.showerror("Export Error", f"Error exporting results:\n{e}")
    
    def save_settings(self):
        """Save application settings."""
        self.app_manager.set_config("theme", self.theme_var.get())
        self.app_manager.set_config("auto_save", self.auto_save_var.get())
        if hasattr(self, 'remember_window_var'):
            self.app_manager.set_config("remember_window", self.remember_window_var.get())
        
        messagebox.showinfo("Settings Saved", "✅ Your settings have been saved successfully!")
        self.status_var.set("Settings saved")
    
    def reset_settings(self):
        """Reset settings to default values."""
        if messagebox.askyesno("Reset Settings", "🔄 Are you sure you want to reset all settings to defaults?"):
            # Reset to default values
            self.theme_var.set("🌟 Default")
            self.auto_save_var.set(True)
            if hasattr(self, 'remember_window_var'):
                self.remember_window_var.set(True)
            
            # Save the reset values
            self.save_settings()
            self.status_var.set("Settings reset to defaults")
    
    def view_logs(self):
        """View application logs."""
        log_path = Path("logs/app.log")
        if log_path.exists():
            # Simple log viewer - could be enhanced with a dedicated window
            messagebox.showinfo("Logs", f"Log file location:\n{log_path.absolute()}")
        else:
            messagebox.showinfo("Logs", "No log file found.")
    
    def refresh_view(self):
        """Refresh the current view."""
        self.status_var.set("View refreshed")
        # Could add logic to refresh the current tab's content
    
    def show_about(self):
        """Show about dialog."""
        about_text = (
            "FolderPulse v1.0.0\n\n"
            "Find and manage empty folders in your file system.\n\n"
            "Features:\n"
            "• Scan directories for empty folders\n"
            "• Include/exclude subdirectories\n"
            "• Handle hidden files properly\n"
            "• Safe deletion with preview\n"
            "• Export results to multiple formats\n\n"
            "Built with Python and Tkinter"
        )
        messagebox.showinfo("About FolderPulse", about_text)
    
    def on_closing(self):
        """Handle window closing event."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.app_manager.cleanup()
            self.root.destroy()
