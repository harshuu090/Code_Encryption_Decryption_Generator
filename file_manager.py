"""
File Manager Module

This module handles file operations for saving and loading
encrypted and decrypted code.
"""

import os
import datetime


class FileManager:
    """Handles file operations for the Text to Code Generator."""
    
    def __init__(self, base_directory="generated_files"):
        """
        Initialize the file manager.
        
        Args:
            base_directory (str): Base directory for saving files
        """
        self.base_directory = base_directory
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self):
        """Create the base directory if it doesn't exist."""
        try:
            if not os.path.exists(self.base_directory):
                os.makedirs(self.base_directory)
        except Exception as e:
            raise Exception(f"Failed to create directory '{self.base_directory}': {e}")
    
    def save_code(self, code, code_type="generated"):
        """
        Save code to a file with timestamp.
        
        Args:
            code (str): Code content to save
            code_type (str): Type of code (generated, encrypted, decrypted)
        
        Returns:
            str: Filename of the saved file
        
        Raises:
            ValueError: If code is empty
            Exception: If file cannot be saved
        """
        if not code.strip():
            raise ValueError("Cannot save empty code")
        
        # Generate filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{code_type}_code_{timestamp}.py"
        filepath = os.path.join(self.base_directory, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                # Add header comment
                header = self._generate_file_header(code_type)
                file.write(header)
                file.write(code)
                
                # Add footer comment
                footer = self._generate_file_footer()
                file.write(footer)
            
            return filename
        except Exception as e:
            raise Exception(f"Failed to save file '{filename}': {e}")
    
    def load_code(self, filename):
        """
        Load code from a file.
        
        Args:
            filename (str): Name of the file to load
        
        Returns:
            str: Content of the file
        
        Raises:
            FileNotFoundError: If file doesn't exist
            Exception: If file cannot be read
        """
        if not filename:
            raise ValueError("Filename cannot be empty")
        
        # Check if filename includes path, if not, use base directory
        if not os.path.dirname(filename):
            filepath = os.path.join(self.base_directory, filename)
        else:
            filepath = filename
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Remove header and footer if present
            content = self._remove_file_headers_footers(content)
            return content
        
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filename}' not found")
        except Exception as e:
            raise Exception(f"Failed to read file '{filename}': {e}")
    
    def list_files(self, code_type=None):
        """
        List all files in the base directory.
        
        Args:
            code_type (str, optional): Filter by code type (generated, encrypted, decrypted)
        
        Returns:
            list: List of filenames
        """
        try:
            all_files = os.listdir(self.base_directory)
            
            # Filter Python files
            python_files = [f for f in all_files if f.endswith('.py')]
            
            # Filter by code type if specified
            if code_type:
                python_files = [f for f in python_files if f.startswith(code_type)]
            
            # Sort by modification time (newest first)
            python_files.sort(key=lambda x: os.path.getmtime(
                os.path.join(self.base_directory, x)
            ), reverse=True)
            
            return python_files
        
        except Exception as e:
            print(f"Error listing files: {e}")
            return []
    
    def delete_file(self, filename):
        """
        Delete a file.
        
        Args:
            filename (str): Name of the file to delete
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not filename:
            return False
        
        # Check if filename includes path, if not, use base directory
        if not os.path.dirname(filename):
            filepath = os.path.join(self.base_directory, filename)
        else:
            filepath = filename
        
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            else:
                return False
        except Exception as e:
            print(f"Error deleting file '{filename}': {e}")
            return False
    
    def get_file_info(self, filename):
        """
        Get information about a file.
        
        Args:
            filename (str): Name of the file
        
        Returns:
            dict: File information or None if file doesn't exist
        """
        if not filename:
            return None
        
        # Check if filename includes path, if not, use base directory
        if not os.path.dirname(filename):
            filepath = os.path.join(self.base_directory, filename)
        else:
            filepath = filename
        
        try:
            if os.path.exists(filepath):
                stat = os.stat(filepath)
                return {
                    'filename': filename,
                    'size': stat.st_size,
                    'created': datetime.datetime.fromtimestamp(stat.st_ctime),
                    'modified': datetime.datetime.fromtimestamp(stat.st_mtime),
                    'is_readable': os.access(filepath, os.R_OK),
                    'is_writable': os.access(filepath, os.W_OK)
                }
            else:
                return None
        except Exception as e:
            print(f"Error getting file info for '{filename}': {e}")
            return None
    
    def backup_file(self, filename):
        """
        Create a backup copy of a file.
        
        Args:
            filename (str): Name of the file to backup
        
        Returns:
            str: Backup filename if successful, None otherwise
        """
        if not filename:
            return None
        
        # Check if filename includes path, if not, use base directory
        if not os.path.dirname(filename):
            filepath = os.path.join(self.base_directory, filename)
        else:
            filepath = filename
        
        try:
            if os.path.exists(filepath):
                # Generate backup filename
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                name, ext = os.path.splitext(filename)
                backup_filename = f"{name}_backup_{timestamp}{ext}"
                backup_filepath = os.path.join(self.base_directory, backup_filename)
                
                # Copy file
                with open(filepath, 'r', encoding='utf-8') as original:
                    content = original.read()
                
                with open(backup_filepath, 'w', encoding='utf-8') as backup:
                    backup.write(content)
                
                return backup_filename
            else:
                return None
        except Exception as e:
            print(f"Error creating backup for '{filename}': {e}")
            return None
    
    def _generate_file_header(self, code_type):
        """Generate a header comment for saved files."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f'''"""
Text to Code Generator - {code_type.title()} Code
Generated on: {timestamp}
=====================================

This file was automatically generated by the Text to Code Generator
with Encryption tool. 

Code Type: {code_type.title()}
"""


'''
        return header
    
    def _generate_file_footer(self):
        """Generate a footer comment for saved files."""
        footer = '''


"""
End of generated code
=====================

This file was created by Text to Code Generator with Encryption.
For more information about this tool, check the main.py file.
"""
'''
        return footer
    
    def _remove_file_headers_footers(self, content):
        """Remove automatically generated headers and footers from file content."""
        lines = content.split('\n')
        
        # Remove header (between first """ and next """)
        start_remove = -1
        end_remove = -1
        quote_count = 0
        
        for i, line in enumerate(lines):
            if '"""' in line:
                quote_count += 1
                if quote_count == 1:
                    start_remove = i
                elif quote_count == 2:
                    end_remove = i
                    break
        
        if start_remove != -1 and end_remove != -1:
            # Remove header section
            lines = lines[:start_remove] + lines[end_remove + 1:]
        
        # Remove footer (last """ section)
        quote_count = 0
        start_remove = -1
        
        for i in range(len(lines) - 1, -1, -1):
            if '"""' in lines[i]:
                quote_count += 1
                if quote_count == 1:
                    start_remove = i
                elif quote_count == 2:
                    lines = lines[:i] + lines[start_remove + 1:]
                    break
        
        # Remove empty lines at the beginning and end
        while lines and not lines[0].strip():
            lines.pop(0)
        
        while lines and not lines[-1].strip():
            lines.pop()
        
        return '\n'.join(lines)