"""
Empty Folder Scanner
Core functionality for detecting and managing empty folders.
"""

import os
import logging
from pathlib import Path
from typing import List, Set, Tuple, Optional
import stat


class EmptyFolderScanner:
    """Scanner for detecting empty folders with various options."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.empty_folders: List[Path] = []
        self.scan_results = {
            'total_folders': 0,
            'empty_folders': 0,
            'hidden_folders': 0,
            'scan_time': 0
        }
    
    def scan_directory(
        self,
        root_path: str,
        include_subdirectories: bool = True,
        scan_hidden: bool = False,
        ignore_patterns: Optional[List[str]] = None
    ) -> List[Path]:
        """
        Scan directory for empty folders.
        
        Args:
            root_path: Root directory to scan
            include_subdirectories: Whether to scan subdirectories recursively
            scan_hidden: Whether to include hidden files/folders in emptiness check
            ignore_patterns: List of patterns to ignore (e.g., ['.git', '__pycache__'])
        
        Returns:
            List of empty folder paths
        """
        import time
        start_time = time.time()
        
        self.logger.info(f"Starting empty folder scan: {root_path}")
        self.empty_folders.clear()
        
        # Default ignore patterns
        if ignore_patterns is None:
            ignore_patterns = ['.git', '__pycache__', '.vscode', 'node_modules']
        
        try:
            root = Path(root_path)
            if not root.exists():
                raise FileNotFoundError(f"Directory does not exist: {root_path}")
            
            if not root.is_dir():
                raise NotADirectoryError(f"Path is not a directory: {root_path}")
            
            # Scan directories
            if include_subdirectories:
                self._scan_recursive(root, scan_hidden, ignore_patterns)
            else:
                self._scan_single_level(root, scan_hidden, ignore_patterns)
            
            # Update scan results
            self.scan_results['scan_time'] = time.time() - start_time
            self.scan_results['empty_folders'] = len(self.empty_folders)
            
            self.logger.info(f"Scan completed. Found {len(self.empty_folders)} empty folders")
            return self.empty_folders.copy()
            
        except Exception as e:
            self.logger.error(f"Error during scan: {e}")
            raise
    
    def _scan_recursive(self, root: Path, scan_hidden: bool, ignore_patterns: List[str]):
        """Recursively scan directories."""
        for dirpath, dirnames, filenames in os.walk(root):
            current_path = Path(dirpath)
            
            # Skip ignored directories
            if self._should_ignore(current_path, ignore_patterns):
                continue
            
            # Check if directory is empty
            if self._is_directory_empty(current_path, scan_hidden, ignore_patterns):
                self.empty_folders.append(current_path)
                self.logger.debug(f"Found empty folder: {current_path}")
            
            self.scan_results['total_folders'] += 1
            
            # Track hidden folders
            if self._is_hidden(current_path):
                self.scan_results['hidden_folders'] += 1
    
    def _scan_single_level(self, root: Path, scan_hidden: bool, ignore_patterns: List[str]):
        """Scan only direct subdirectories."""
        try:
            for item in root.iterdir():
                if item.is_dir() and not self._should_ignore(item, ignore_patterns):
                    if self._is_directory_empty(item, scan_hidden, ignore_patterns):
                        self.empty_folders.append(item)
                        self.logger.debug(f"Found empty folder: {item}")
                    
                    self.scan_results['total_folders'] += 1
                    
                    if self._is_hidden(item):
                        self.scan_results['hidden_folders'] += 1
        except PermissionError as e:
            self.logger.warning(f"Permission denied accessing: {root} - {e}")
    
    def _is_directory_empty(self, path: Path, scan_hidden: bool, ignore_patterns: List[str]) -> bool:
        """
        Check if a directory is empty.
        
        Args:
            path: Directory path to check
            scan_hidden: Whether to consider hidden files
            ignore_patterns: Patterns to ignore when checking emptiness
        
        Returns:
            True if directory is empty, False otherwise
        """
        try:
            items = list(path.iterdir())
            
            # If no items at all, it's empty
            if not items:
                return True
            
            # Check each item
            for item in items:
                # Skip ignored patterns
                if self._should_ignore(item, ignore_patterns):
                    continue
                
                # If not scanning hidden files, skip hidden items
                if not scan_hidden and self._is_hidden(item):
                    continue
                
                # If we find any non-ignored, non-hidden item, it's not empty
                return False
            
            # All items were ignored or hidden (and we're not scanning hidden)
            return True
            
        except PermissionError:
            self.logger.warning(f"Permission denied checking: {path}")
            return False  # Can't determine, assume not empty
        except Exception as e:
            self.logger.error(f"Error checking directory {path}: {e}")
            return False
    
    def _is_hidden(self, path: Path) -> bool:
        """Check if a file or directory is hidden."""
        # On Windows, check file attributes
        if os.name == 'nt':
            try:
                attrs = os.stat(path).st_file_attributes
                return attrs & stat.FILE_ATTRIBUTE_HIDDEN
            except (AttributeError, OSError):
                pass
        
        # On Unix-like systems, check if name starts with dot
        return path.name.startswith('.')
    
    def _should_ignore(self, path: Path, ignore_patterns: List[str]) -> bool:
        """Check if path should be ignored based on patterns."""
        path_name = path.name.lower()
        
        for pattern in ignore_patterns:
            if pattern.lower() in path_name:
                return True
        
        return False
    
    def delete_empty_folders(
        self,
        folders_to_delete: Optional[List[Path]] = None,
        dry_run: bool = True
    ) -> Tuple[List[Path], List[Tuple[Path, str]]]:
        """
        Delete empty folders.
        
        Args:
            folders_to_delete: Specific folders to delete (None = use scan results)
            dry_run: If True, don't actually delete, just simulate
        
        Returns:
            Tuple of (successfully_deleted, failed_deletions_with_errors)
        """
        if folders_to_delete is None:
            folders_to_delete = self.empty_folders
        
        deleted = []
        failed = []
        
        self.logger.info(f"{'Simulating' if dry_run else 'Starting'} deletion of {len(folders_to_delete)} folders")
        
        for folder in folders_to_delete:
            try:
                if not folder.exists():
                    self.logger.warning(f"Folder no longer exists: {folder}")
                    continue
                
                if not dry_run:
                    folder.rmdir()  # Only removes empty directories
                    self.logger.info(f"Deleted: {folder}")
                else:
                    self.logger.debug(f"Would delete: {folder}")
                
                deleted.append(folder)
                
            except OSError as e:
                error_msg = f"Failed to delete {folder}: {e}"
                self.logger.error(error_msg)
                failed.append((folder, str(e)))
            except Exception as e:
                error_msg = f"Unexpected error deleting {folder}: {e}"
                self.logger.error(error_msg)
                failed.append((folder, str(e)))
        
        action = "Would delete" if dry_run else "Deleted"
        self.logger.info(f"{action} {len(deleted)} folders, {len(failed)} failed")
        
        return deleted, failed
    
    def get_scan_summary(self) -> dict:
        """Get summary of the last scan."""
        return self.scan_results.copy()
    
    def export_results(self, output_file: str, format_type: str = 'txt') -> bool:
        """
        Export scan results to file.
        
        Args:
            output_file: Output file path
            format_type: Format type ('txt', 'csv', 'json')
        
        Returns:
            True if successful, False otherwise
        """
        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            if format_type.lower() == 'txt':
                self._export_txt(output_path)
            elif format_type.lower() == 'csv':
                self._export_csv(output_path)
            elif format_type.lower() == 'json':
                self._export_json(output_path)
            else:
                raise ValueError(f"Unsupported format: {format_type}")
            
            self.logger.info(f"Results exported to: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export results: {e}")
            return False
    
    def _export_txt(self, output_path: Path):
        """Export results as text file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("FolderPulse - Empty Folder Scan Results\n")
            f.write("=" * 50 + "\n\n")
            
            # Summary
            f.write("SCAN SUMMARY:\n")
            f.write(f"Total folders scanned: {self.scan_results['total_folders']}\n")
            f.write(f"Empty folders found: {self.scan_results['empty_folders']}\n")
            f.write(f"Hidden folders: {self.scan_results['hidden_folders']}\n")
            f.write(f"Scan time: {self.scan_results['scan_time']:.2f} seconds\n\n")
            
            # Empty folders list
            f.write("EMPTY FOLDERS:\n")
            f.write("-" * 20 + "\n")
            for folder in self.empty_folders:
                f.write(f"{folder}\n")
    
    def _export_csv(self, output_path: Path):
        """Export results as CSV file."""
        import csv
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Path', 'Type', 'Size'])
            
            for folder in self.empty_folders:
                writer.writerow([str(folder), 'Empty Folder', '0'])
    
    def _export_json(self, output_path: Path):
        """Export results as JSON file."""
        import json
        data = {
            'scan_summary': self.scan_results,
            'empty_folders': [str(folder) for folder in self.empty_folders]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
