# -*- coding: utf-8 -*-
"""
FILE HANDLER - FILE OPERATIONS AND MANAGEMENT
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import os
import json
import csv
import pickle
import shutil
import zipfile
import tarfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from utils.logger import Logger

class FileHandler:
    def __init__(self):
        self.logger = Logger("file_handler")
    
    def read_file(self, filepath: str, encoding: str = 'utf-8') -> Optional[str]:
        """Read text file"""
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read()
        except Exception as e:
            self.logger.error(f"Error reading file {filepath}: {e}")
            return None
    
    def write_file(self, filepath: str, content: str, 
                  encoding: str = 'utf-8', mode: str = 'w') -> bool:
        """Write text file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, mode, encoding=encoding) as f:
                f.write(content)
            
            self.logger.debug(f"File written: {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error writing file {filepath}: {e}")
            return False
    
    def read_json(self, filepath: str) -> Optional[Dict]:
        """Read JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error reading JSON file {filepath}: {e}")
            return None
    
    def write_json(self, filepath: str, data: Dict, 
                  indent: int = 2, ensure_ascii: bool = False) -> bool:
        """Write JSON file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)
            
            self.logger.debug(f"JSON file written: {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error writing JSON file {filepath}: {e}")
            return False
    
    def read_csv(self, filepath: str, delimiter: str = ',') -> List[Dict]:
        """Read CSV file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=delimiter)
                return list(reader)
        except Exception as e:
            self.logger.error(f"Error reading CSV file {filepath}: {e}")
            return []
    
    def write_csv(self, filepath: str, data: List[Dict], 
                 fieldnames: List[str] = None) -> bool:
        """Write CSV file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            if not fieldnames and data:
                fieldnames = list(data[0].keys())
            
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            self.logger.debug(f"CSV file written: {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error writing CSV file {filepath}: {e}")
            return False
    
    def read_pickle(self, filepath: str) -> Optional[Any]:
        """Read pickle file"""
        try:
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            self.logger.error(f"Error reading pickle file {filepath}: {e}")
            return None
    
    def write_pickle(self, filepath: str, data: Any) -> bool:
        """Write pickle file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'wb') as f:
                pickle.dump(data, f)
            
            self.logger.debug(f"Pickle file written: {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error writing pickle file {filepath}: {e}")
            return False
    
    def file_exists(self, filepath: str) -> bool:
        """Check if file exists"""
        return os.path.exists(filepath) and os.path.isfile(filepath)
    
    def directory_exists(self, dirpath: str) -> bool:
        """Check if directory exists"""
        return os.path.exists(dirpath) and os.path.isdir(dirpath)
    
    def create_directory(self, dirpath: str) -> bool:
        """Create directory"""
        try:
            os.makedirs(dirpath, exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(f"Error creating directory {dirpath}: {e}")
            return False
    
    def list_files(self, dirpath: str, pattern: str = '*') -> List[str]:
        """List files in directory"""
        try:
            import glob
            return glob.glob(os.path.join(dirpath, pattern))
        except Exception as e:
            self.logger.error(f"Error listing files in {dirpath}: {e}")
            return []
    
    def list_directories(self, dirpath: str) -> List[str]:
        """List directories in directory"""
        try:
            return [d for d in os.listdir(dirpath) 
                   if os.path.isdir(os.path.join(dirpath, d))]
        except Exception as e:
            self.logger.error(f"Error listing directories in {dirpath}: {e}")
            return []
    
    def get_file_info(self, filepath: str) -> Optional[Dict]:
        """Get file information"""
        try:
            stat = os.stat(filepath)
            
            return {
                'path': filepath,
                'filename': os.path.basename(filepath),
                'size_bytes': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime),
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'accessed': datetime.fromtimestamp(stat.st_atime),
                'is_file': os.path.isfile(filepath),
                'is_dir': os.path.isdir(filepath),
                'extension': os.path.splitext(filepath)[1]
            }
        except Exception as e:
            self.logger.error(f"Error getting file info {filepath}: {e}")
            return None
    
    def get_file_size(self, filepath: str) -> int:
        """Get file size in bytes"""
        try:
            return os.path.getsize(filepath)
        except:
            return 0
    
    def get_file_hash(self, filepath: str, algorithm: str = 'md5') -> Optional[str]:
        """Calculate file hash"""
        import hashlib
        
        try:
            hash_func = getattr(hashlib, algorithm)()
            
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_func.update(chunk)
            
            return hash_func.hexdigest()
            
        except Exception as e:
            self.logger.error(f"Error calculating hash for {filepath}: {e}")
            return None
    
    def copy_file(self, src: str, dst: str) -> bool:
        """Copy file"""
        try:
            # Ensure destination directory exists
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            
            shutil.copy2(src, dst)
            self.logger.debug(f"File copied: {src} -> {dst}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error copying file {src} to {dst}: {e}")
            return False
    
    def move_file(self, src: str, dst: str) -> bool:
        """Move/rename file"""
        try:
            # Ensure destination directory exists
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            
            shutil.move(src, dst)
            self.logger.debug(f"File moved: {src} -> {dst}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error moving file {src} to {dst}: {e}")
            return False
    
    def delete_file(self, filepath: str) -> bool:
        """Delete file"""
        try:
            os.remove(filepath)
            self.logger.debug(f"File deleted: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting file {filepath}: {e}")
            return False
    
    def delete_directory(self, dirpath: str, recursive: bool = False) -> bool:
        """Delete directory"""
        try:
            if recursive:
                shutil.rmtree(dirpath)
            else:
                os.rmdir(dirpath)
            
            self.logger.debug(f"Directory deleted: {dirpath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting directory {dirpath}: {e}")
            return False
    
    def archive_files(self, files: List[str], archive_path: str, 
                     format: str = 'zip') -> bool:
        """Create archive from files"""
        try:
            if format == 'zip':
                with zipfile.ZipFile(archive_path, 'w') as zipf:
                    for file in files:
                        if os.path.exists(file):
                            arcname = os.path.basename(file)
                            zipf.write(file, arcname=arcname)
            
            elif format == 'tar':
                with tarfile.open(archive_path, 'w') as tarf:
                    for file in files:
                        if os.path.exists(file):
                            arcname = os.path.basename(file)
                            tarf.add(file, arcname=arcname)
            
            elif format == 'tar.gz':
                with tarfile.open(archive_path, 'w:gz') as tarf:
                    for file in files:
                        if os.path.exists(file):
                            arcname = os.path.basename(file)
                            tarf.add(file, arcname=arcname)
            
            else:
                self.logger.error(f"Unsupported archive format: {format}")
                return False
            
            self.logger.debug(f"Archive created: {archive_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating archive {archive_path}: {e}")
            return False
    
    def extract_archive(self, archive_path: str, extract_dir: str, 
                       format: str = None) -> bool:
        """Extract archive"""
        try:
            # Ensure extract directory exists
            os.makedirs(extract_dir, exist_ok=True)
            
            if format is None:
                # Auto-detect format
                if archive_path.endswith('.zip'):
                    with zipfile.ZipFile(archive_path, 'r') as zipf:
                        zipf.extractall(extract_dir)
                
                elif archive_path.endswith('.tar.gz') or archive_path.endswith('.tgz'):
                    with tarfile.open(archive_path, 'r:gz') as tarf:
                        tarf.extractall(extract_dir)
                
                elif archive_path.endswith('.tar'):
                    with tarfile.open(archive_path, 'r') as tarf:
                        tarf.extractall(extract_dir)
                
                else:
                    self.logger.error(f"Unsupported archive format: {archive_path}")
                    return False
            
            else:
                if format == 'zip':
                    with zipfile.ZipFile(archive_path, 'r') as zipf:
                        zipf.extractall(extract_dir)
                
                elif format == 'tar':
                    with tarfile.open(archive_path, 'r') as tarf:
                        tarf.extractall(extract_dir)
                
                elif format == 'tar.gz':
                    with tarfile.open(archive_path, 'r:gz') as tarf:
                        tarf.extractall(extract_dir)
                
                else:
                    self.logger.error(f"Unsupported archive format: {format}")
                    return False
            
            self.logger.debug(f"Archive extracted: {archive_path} -> {extract_dir}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error extracting archive {archive_path}: {e}")
            return False
    
    def find_files(self, search_dir: str, pattern: str, 
                  recursive: bool = True) -> List[str]:
        """Find files matching pattern"""
        import fnmatch
        
        found_files = []
        
        try:
            if recursive:
                for root, dirs, files in os.walk(search_dir):
                    for file in files:
                        if fnmatch.fnmatch(file, pattern):
                            found_files.append(os.path.join(root, file))
            else:
                for file in os.listdir(search_dir):
                    if fnmatch.fnmatch(file, pattern):
                        found_files.append(os.path.join(search_dir, file))
            
            return found_files
            
        except Exception as e:
            self.logger.error(f"Error finding files in {search_dir}: {e}")
            return []
    
    def find_files_by_content(self, search_dir: str, search_text: str, 
                             file_pattern: str = '*', recursive: bool = True) -> List[str]:
        """Find files containing specific text"""
        found_files = []
        
        try:
            for root, dirs, files in os.walk(search_dir):
                if not recursive and root != search_dir:
                    continue
                
                for file in files:
                    if fnmatch.fnmatch(file, file_pattern):
                        filepath = os.path.join(root, file)
                        
                        try:
                            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                if search_text in content:
                                    found_files.append(filepath)
                        except:
                            # Skip binary files
                            continue
            
            return found_files
            
        except Exception as e:
            self.logger.error(f"Error finding files by content in {search_dir}: {e}")
            return []
    
    def backup_file(self, filepath: str, backup_dir: str = None, 
                   suffix: str = '.bak') -> Optional[str]:
        """Create backup of file"""
        try:
            if not self.file_exists(filepath):
                self.logger.warning(f"File does not exist for backup: {filepath}")
                return None
            
            if backup_dir is None:
                backup_dir = os.path.dirname(filepath)
            
            # Create backup directory if needed
            os.makedirs(backup_dir, exist_ok=True)
            
            # Generate backup filename
            filename = os.path.basename(filepath)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f"{filename}_{timestamp}{suffix}"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            # Copy file
            self.copy_file(filepath, backup_path)
            
            self.logger.debug(f"File backed up: {filepath} -> {backup_path}")
            return backup_path
            
        except Exception as e:
            self.logger.error(f"Error backing up file {filepath}: {e}")
            return None
    
    def cleanup_old_files(self, directory: str, pattern: str = '*', 
                         days_old: int = 30) -> int:
        """Cleanup files older than specified days"""
        try:
            from datetime import datetime, timedelta
            
            cutoff_date = datetime.now() - timedelta(days=days_old)
            deleted_count = 0
            
            for filepath in self.list_files(directory, pattern):
                file_info = self.get_file_info(filepath)
                if file_info and file_info['modified'] < cutoff_date:
                    if self.delete_file(filepath):
                        deleted_count += 1
            
            self.logger.debug(f"Cleaned up {deleted_count} old files in {directory}")
            return deleted_count
            
        except Exception as e:
            self.logger.error(f"Error cleaning up old files in {directory}: {e}")
            return 0
    
    def get_directory_size(self, directory: str) -> int:
        """Get total size of directory in bytes"""
        total_size = 0
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    filepath = os.path.join(root, file)
                    total_size += self.get_file_size(filepath)
            
            return total_size
            
        except Exception as e:
            self.logger.error(f"Error getting directory size for {directory}: {e}")
            return 0