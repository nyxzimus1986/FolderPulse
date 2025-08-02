"""
Demo script for FolderPulse empty folder scanner.
Creates some test folders and demonstrates the scanner functionality.
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.folder_scanner import EmptyFolderScanner


def create_test_structure():
    """Create a test directory structure with empty and non-empty folders."""
    test_root = Path("demo_test_folders")
    
    # Remove existing test structure
    if test_root.exists():
        import shutil
        shutil.rmtree(test_root)
    
    # Create test structure
    test_folders = [
        "demo_test_folders/empty1",
        "demo_test_folders/empty2", 
        "demo_test_folders/not_empty",
        "demo_test_folders/nested/empty_nested",
        "demo_test_folders/nested/not_empty_nested",
        "demo_test_folders/.hidden_empty",
        "demo_test_folders/.hidden_not_empty",
        "demo_test_folders/deep/nested/empty_deep"
    ]
    
    # Create folders
    for folder in test_folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
    
    # Add files to non-empty folders
    test_files = [
        "demo_test_folders/not_empty/file1.txt",
        "demo_test_folders/nested/not_empty_nested/file2.txt",
        "demo_test_folders/.hidden_not_empty/hidden_file.txt"
    ]
    
    for file_path in test_files:
        Path(file_path).write_text(f"Test content for {file_path}")
    
    print(f"✅ Created test structure in: {test_root.absolute()}")
    return test_root


def demo_scanner():
    """Demonstrate the empty folder scanner functionality."""
    print("🚀 FolderPulse Empty Folder Scanner Demo")
    print("=" * 50)
    
    # Create test structure
    test_root = create_test_structure()
    
    # Initialize scanner
    scanner = EmptyFolderScanner()
    
    # Demo 1: Basic scan (include subdirectories, ignore hidden)
    print("\n📁 Demo 1: Basic scan (subdirectories: YES, hidden: NO)")
    print("-" * 50)
    
    empty_folders = scanner.scan_directory(
        str(test_root),
        include_subdirectories=True,
        scan_hidden=False
    )
    
    print(f"Found {len(empty_folders)} empty folders:")
    for folder in empty_folders:
        print(f"  • {folder}")
    
    # Demo 2: Scan including hidden files
    print("\n📁 Demo 2: Scan including hidden files")
    print("-" * 50)
    
    empty_folders_with_hidden = scanner.scan_directory(
        str(test_root),
        include_subdirectories=True,
        scan_hidden=True
    )
    
    print(f"Found {len(empty_folders_with_hidden)} empty folders (including hidden):")
    for folder in empty_folders_with_hidden:
        print(f"  • {folder}")
    
    # Demo 3: Single level scan only
    print("\n📁 Demo 3: Single level scan (no subdirectories)")
    print("-" * 50)
    
    empty_folders_single = scanner.scan_directory(
        str(test_root),
        include_subdirectories=False,
        scan_hidden=False
    )
    
    print(f"Found {len(empty_folders_single)} empty folders (single level):")
    for folder in empty_folders_single:
        print(f"  • {folder}")
    
    # Demo 4: Dry run deletion
    print("\n🗑️  Demo 4: Dry run deletion preview")
    print("-" * 50)
    
    deleted, failed = scanner.delete_empty_folders(
        empty_folders[:2],  # Delete first 2 folders
        dry_run=True
    )
    
    print(f"Dry run results:")
    print(f"  Would delete: {len(deleted)} folders")
    print(f"  Would fail: {len(failed)} folders")
    
    # Demo 5: Export results
    print("\n💾 Demo 5: Export results")
    print("-" * 50)
    
    export_files = [
        ("demo_results.txt", "txt"),
        ("demo_results.csv", "csv"),
        ("demo_results.json", "json")
    ]
    
    for filename, format_type in export_files:
        if scanner.export_results(filename, format_type):
            print(f"  ✅ Exported to {filename}")
        else:
            print(f"  ❌ Failed to export to {filename}")
    
    # Show scan summary
    print("\n📊 Scan Summary")
    print("-" * 50)
    summary = scanner.get_scan_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print(f"\n🎉 Demo completed! Test files created in: {test_root.absolute()}")
    print("You can now run the full GUI application with: python src/main.py")


if __name__ == "__main__":
    try:
        demo_scanner()
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
