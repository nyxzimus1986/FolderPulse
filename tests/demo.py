"""
Simple demo script to test FolderPulse functionality.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from core.app_manager import AppManager
    from utils.logger import setup_logger
    
    def demo():
        """Run a simple demo of FolderPulse functionality."""
        print("🎯 FolderPulse Demo")
        print("=" * 40)
        
        # Set up logger
        logger = setup_logger("demo", console=True)
        logger.info("Starting FolderPulse demo...")
        
        # Create app manager
        app_manager = AppManager()
        logger.info("Created AppManager")
        
        # Show configuration
        config = app_manager.get_default_config()
        print(f"\n📋 Default Configuration:")
        print(f"   App Name: {config['app_name']}")
        print(f"   Version: {config['version']}")
        print(f"   Window Size: {config['window']['width']}x{config['window']['height']}")
        
        # Test config operations
        app_manager.set_config("demo.test", "Hello World")
        test_value = app_manager.get_config("demo.test")
        print(f"   Test Config: {test_value}")
        
        logger.info("Demo completed successfully!")
        print("\n✅ Demo completed! You can now run 'python src/main.py' to start the GUI.")
    
    if __name__ == "__main__":
        demo()

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the project root directory.")
    print("Try: cd C:\\Users\\nyxzi\\Python\\scripts\\FolderPulse")
except Exception as e:
    print(f"❌ Error: {e}")
