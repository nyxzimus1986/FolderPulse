"""
Core Application Manager
Handles the main application logic and coordination between components.
"""

import logging
import threading
from pathlib import Path
from typing import Dict, Any, Optional


class AppManager:
    """Central application manager for coordinating all components."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = {}
        self.running = False
        self.components = {}
        self._lock = threading.Lock()
    
    def initialize(self) -> bool:
        """Initialize the application manager."""
        try:
            self.logger.info("Initializing AppManager...")
            
            # Load configuration
            self.load_config()
            
            # Initialize components
            self.init_components()
            
            self.running = True
            self.logger.info("AppManager initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize AppManager: {e}")
            return False
    
    def load_config(self):
        """Load application configuration."""
        config_path = Path("config/config.json")
        if config_path.exists():
            import json
            try:
                with open(config_path, 'r') as f:
                    self.config = json.load(f)
                self.logger.info("Configuration loaded successfully")
            except Exception as e:
                self.logger.warning(f"Failed to load config: {e}")
                self.config = self.get_default_config()
        else:
            self.config = self.get_default_config()
            self.save_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "app_name": "FolderPulse",
            "version": "1.0.0",
            "debug": False,
            "auto_save": True,
            "theme": "default",
            "window": {
                "width": 800,
                "height": 600,
                "resizable": True
            },
            "logging": {
                "level": "INFO",
                "file": "logs/app.log"
            },
            "scanner": {
                "default_include_subdirs": True,
                "default_scan_hidden": False,
                "ignore_patterns": [
                    ".git",
                    "__pycache__",
                    ".vscode",
                    "node_modules",
                    ".DS_Store",
                    "Thumbs.db"
                ]
            }
        }
    
    def save_config(self):
        """Save current configuration."""
        try:
            import json
            config_path = Path("config/config.json")
            config_path.parent.mkdir(exist_ok=True)
            
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            
            self.logger.info("Configuration saved successfully")
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
    
    def init_components(self):
        """Initialize application components."""
        # This is where you would initialize various app components
        # like file monitors, data processors, web services, etc.
        pass
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set_config(self, key: str, value: Any):
        """Set configuration value."""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save_config()
    
    def start_background_tasks(self):
        """Start background tasks."""
        if not self.running:
            return
        
        # Start any background processing here
        pass
    
    def stop_background_tasks(self):
        """Stop background tasks."""
        self.running = False
        # Stop any background processing here
        pass
    
    def cleanup(self):
        """Cleanup resources."""
        try:
            self.logger.info("Cleaning up AppManager...")
            self.stop_background_tasks()
            
            # Cleanup components
            for component in self.components.values():
                if hasattr(component, 'cleanup'):
                    component.cleanup()
            
            self.logger.info("AppManager cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during AppManager cleanup: {e}")
