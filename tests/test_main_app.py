"""
Test suite for VoidPulse application.
"""

import pytest
import tkinter as tk
import sys
from pathlib import Path
import tempfile
import shutil

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import VoidPulseApp
from core.app_manager import AppManager
from core.folder_scanner import EmptyFolderScanner
from utils.logger import setup_logger


class TestVoidPulseApp:
    """Test cases for the main VoidPulseApp class."""
    
    def test_app_creation(self):
        """Test that the app can be created without errors."""
        app = VoidPulseApp()
        assert app is not None
        assert app.app_manager is not None
        assert app.root is None  # Not initialized yet
    
    def test_app_manager_creation(self):
        """Test AppManager creation and basic functionality."""
        manager = AppManager()
        assert manager is not None
        assert manager.running is False
        assert isinstance(manager.config, dict)
    
    def test_default_config(self):
        """Test default configuration generation."""
        manager = AppManager()
        default_config = manager.get_default_config()
        
        assert "app_name" in default_config
        assert "version" in default_config
        assert "window" in default_config
        assert "logging" in default_config
        assert "scanner" in default_config
        
        assert default_config["app_name"] == "FolderPulse"
        assert default_config["version"] == "1.0.0"
        assert "ignore_patterns" in default_config["scanner"]
    
    def test_config_get_set(self):
        """Test configuration get/set operations."""
        manager = AppManager()
        
        # Test getting existing config
        app_name = manager.get_config("app_name")
        assert app_name == "FolderPulse"
        
        # Test getting nested config
        window_width = manager.get_config("window.width")
        assert window_width == 800
        
        # Test getting non-existent config with default
        non_existent = manager.get_config("non.existent.key", "default_value")
        assert non_existent == "default_value"
        
        # Test setting config
        manager.set_config("test.key", "test_value")
        assert manager.get_config("test.key") == "test_value"


class TestEmptyFolderScanner:
    """Test cases for the EmptyFolderScanner class."""
    
    def setup_method(self):
        """Set up test environment for each test."""
        self.scanner = EmptyFolderScanner()
        self.test_dir = None
    
    def teardown_method(self):
        """Clean up after each test."""
        if self.test_dir and self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def create_test_structure(self):
        """Create a test directory structure."""
        self.test_dir = Path(tempfile.mkdtemp(prefix="folderpulse_test_"))
        
        # Create empty folders
        empty_folders = [
            self.test_dir / "empty1",
            self.test_dir / "empty2",
            self.test_dir / "nested" / "empty_nested",
            self.test_dir / ".hidden_empty"
        ]
        
        for folder in empty_folders:
            folder.mkdir(parents=True, exist_ok=True)
        
        # Create non-empty folders
        non_empty_folders = [
            self.test_dir / "not_empty",
            self.test_dir / "nested" / "not_empty_nested"
        ]
        
        for folder in non_empty_folders:
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "test_file.txt").write_text("test content")
        
        return self.test_dir
    
    def test_scanner_creation(self):
        """Test scanner creation."""
        scanner = EmptyFolderScanner()
        assert scanner is not None
        assert scanner.empty_folders == []
    
    def test_basic_scan(self):
        """Test basic scanning functionality."""
        test_root = self.create_test_structure()
        
        empty_folders = self.scanner.scan_directory(
            str(test_root),
            include_subdirectories=True,
            scan_hidden=False
        )
        
        assert len(empty_folders) >= 2  # At least empty1 and empty2
        
        # Check that empty folders are detected
        folder_names = [f.name for f in empty_folders]
        assert "empty1" in folder_names
        assert "empty2" in folder_names
    
    def test_hidden_folder_scanning(self):
        """Test scanning with hidden folders."""
        test_root = self.create_test_structure()
        
        # Scan without hidden
        empty_folders_no_hidden = self.scanner.scan_directory(
            str(test_root),
            include_subdirectories=True,
            scan_hidden=False
        )
        
        # Scan with hidden
        empty_folders_with_hidden = self.scanner.scan_directory(
            str(test_root),
            include_subdirectories=True,
            scan_hidden=True
        )
        
        # Should find the same or more folders when including hidden
        assert len(empty_folders_with_hidden) >= len(empty_folders_no_hidden)
    
    def test_single_level_scan(self):
        """Test single level (non-recursive) scanning."""
        test_root = self.create_test_structure()
        
        # Recursive scan
        recursive_results = self.scanner.scan_directory(
            str(test_root),
            include_subdirectories=True,
            scan_hidden=False
        )
        
        # Single level scan  
        single_level_results = self.scanner.scan_directory(
            str(test_root),
            include_subdirectories=False,
            scan_hidden=False
        )
        
        # Single level should find fewer or equal folders
        assert len(single_level_results) <= len(recursive_results)
    
    def test_dry_run_deletion(self):
        """Test dry run deletion functionality."""
        test_root = self.create_test_structure()
        
        empty_folders = self.scanner.scan_directory(str(test_root))
        
        if empty_folders:
            deleted, failed = self.scanner.delete_empty_folders(
                empty_folders[:1],  # Try to delete one folder
                dry_run=True
            )
            
            assert len(deleted) >= 0
            assert len(failed) >= 0
            # In dry run, folder should still exist
            assert empty_folders[0].exists()
    
    def test_export_functionality(self):
        """Test export functionality."""
        test_root = self.create_test_structure()
        
        # Perform scan
        self.scanner.scan_directory(str(test_root))
        
        # Test export
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            result = self.scanner.export_results(tmp.name, "txt")
            assert result is True
            
            # Check file was created
            assert Path(tmp.name).exists()
            
            # Clean up
            Path(tmp.name).unlink()
    
    def test_scan_summary(self):
        """Test scan summary functionality."""
        test_root = self.create_test_structure()
        
        self.scanner.scan_directory(str(test_root))
        summary = self.scanner.get_scan_summary()
        
        assert isinstance(summary, dict)
        assert "total_folders" in summary
        assert "empty_folders" in summary
        assert "scan_time" in summary
        assert summary["total_folders"] >= 0
        assert summary["empty_folders"] >= 0


class TestLogger:
    """Test cases for logging utilities."""
    
    def test_logger_setup(self):
        """Test logger setup."""
        logger = setup_logger("test_logger")
        assert logger is not None
        assert logger.name == "test_logger"
    
    def test_logger_with_file(self):
        """Test logger with file output."""
        with tempfile.NamedTemporaryFile(suffix='.log', delete=False) as tmp:
            logger = setup_logger("file_logger", log_file=tmp.name)
            logger.info("Test message")
            assert logger is not None
            
            # Clean up
            Path(tmp.name).unlink()


@pytest.fixture
def temp_config_file():
    """Create a temporary configuration file for testing."""
    import json
    
    config = {
        "app_name": "TestApp",
        "version": "0.1.0",
        "debug": True,
        "scanner": {
            "default_include_subdirs": True,
            "ignore_patterns": [".git", "__pycache__"]
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config, f)
        return f.name


def test_integration_full_workflow():
    """Integration test for full workflow."""
    # Create scanner
    scanner = EmptyFolderScanner()
    
    # Create temporary test structure
    test_dir = Path(tempfile.mkdtemp(prefix="folderpulse_integration_"))
    
    try:
        # Create test folders
        empty1 = test_dir / "empty1"
        empty2 = test_dir / "empty2"
        not_empty = test_dir / "not_empty"
        
        empty1.mkdir()
        empty2.mkdir()
        not_empty.mkdir()
        (not_empty / "file.txt").write_text("content")
        
        # Scan
        empty_folders = scanner.scan_directory(str(test_dir))
        
        # Should find 2 empty folders
        assert len(empty_folders) == 2
        
        # Test dry run
        deleted, failed = scanner.delete_empty_folders(empty_folders, dry_run=True)
        assert len(deleted) == 2
        assert len(failed) == 0
        
        # Folders should still exist after dry run
        assert empty1.exists()
        assert empty2.exists()
        
        # Test actual deletion
        deleted, failed = scanner.delete_empty_folders([empty1], dry_run=False)
        assert len(deleted) == 1
        assert not empty1.exists()
        assert empty2.exists()  # Should still exist
        
    finally:
        # Clean up
        if test_dir.exists():
            shutil.rmtree(test_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
