"""
Encryption Module

This module provides Caesar Cipher encryption and decryption functionality
for the generated Python code.
"""

import string


class CaesarCipher:
    """Implements Caesar Cipher encryption and decryption."""
    
    def __init__(self):
        """Initialize the cipher with character sets."""
        # Define the character set for encryption (letters, digits, and common symbols)
        self.charset = string.ascii_letters + string.digits + string.punctuation + ' \n\t'
    
    def encrypt(self, text, shift):
        """
        Encrypt text using Caesar cipher.
        
        Args:
            text (str): Text to encrypt
            shift (int): Number of positions to shift (1-25)
        
        Returns:
            str: Encrypted text
        
        Raises:
            ValueError: If shift is not in valid range
        """
        if not (1 <= shift <= 25):
            raise ValueError("Shift must be between 1 and 25")
        
        if not text:
            raise ValueError("Text cannot be empty")
        
        encrypted_chars = []
        
        for char in text:
            if char in self.charset:
                # Find position of character in charset
                old_index = self.charset.index(char)
                # Calculate new position with wrap-around
                new_index = (old_index + shift) % len(self.charset)
                encrypted_chars.append(self.charset[new_index])
            else:
                # Keep characters not in charset unchanged
                encrypted_chars.append(char)
        
        return ''.join(encrypted_chars)
    
    def decrypt(self, encrypted_text, shift):
        """
        Decrypt text using Caesar cipher.
        
        Args:
            encrypted_text (str): Text to decrypt
            shift (int): Number of positions that were shifted (1-25)
        
        Returns:
            str: Decrypted text
        
        Raises:
            ValueError: If shift is not in valid range
        """
        if not (1 <= shift <= 25):
            raise ValueError("Shift must be between 1 and 25")
        
        if not encrypted_text:
            raise ValueError("Encrypted text cannot be empty")
        
        decrypted_chars = []
        
        for char in encrypted_text:
            if char in self.charset:
                # Find position of character in charset
                old_index = self.charset.index(char)
                # Calculate original position with wrap-around
                new_index = (old_index - shift) % len(self.charset)
                decrypted_chars.append(self.charset[new_index])
            else:
                # Keep characters not in charset unchanged
                decrypted_chars.append(char)
        
        return ''.join(decrypted_chars)
    
    def brute_force_decrypt(self, encrypted_text):
        """
        Attempt to decrypt text by trying all possible shift values.
        
        Args:
            encrypted_text (str): Text to decrypt
        
        Returns:
            dict: Dictionary with shift values as keys and decrypted text as values
        """
        if not encrypted_text:
            raise ValueError("Encrypted text cannot be empty")
        
        results = {}
        
        for shift in range(1, 26):
            try:
                decrypted = self.decrypt(encrypted_text, shift)
                results[shift] = decrypted
            except Exception as e:
                results[shift] = f"Error: {e}"
        
        return results
    
    def analyze_encrypted_text(self, encrypted_text):
        """
        Provide analysis of encrypted text.
        
        Args:
            encrypted_text (str): Text to analyze
        
        Returns:
            dict: Analysis results including character frequency and statistics
        """
        if not encrypted_text:
            return {"error": "Empty text provided"}
        
        analysis = {
            "length": len(encrypted_text),
            "unique_chars": len(set(encrypted_text)),
            "char_frequency": {},
            "most_common_char": None,
            "printable_chars": 0,
            "non_printable_chars": 0
        }
        
        # Count character frequencies
        for char in encrypted_text:
            analysis["char_frequency"][char] = analysis["char_frequency"].get(char, 0) + 1
            
            if char in string.printable:
                analysis["printable_chars"] += 1
            else:
                analysis["non_printable_chars"] += 1
        
        # Find most common character
        if analysis["char_frequency"]:
            most_common = max(analysis["char_frequency"].items(), key=lambda x: x[1])
            analysis["most_common_char"] = {
                "char": most_common[0],
                "count": most_common[1],
                "percentage": round((most_common[1] / len(encrypted_text)) * 100, 2)
            }
        
        return analysis
    
    def validate_shift(self, shift):
        """
        Validate if shift value is within acceptable range.
        
        Args:
            shift (int): Shift value to validate
        
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            return isinstance(shift, int) and (1 <= shift <= 25)
        except:
            return False
    
    def generate_shift_suggestions(self, text_sample):
        """
        Generate suggestions for shift values based on common English patterns.
        
        Args:
            text_sample (str): Sample of text to analyze
        
        Returns:
            list: Suggested shift values based on pattern analysis
        """
        if not text_sample:
            return [1, 3, 5, 13]  # Default suggestions
        
        suggestions = []
        
        # Look for common English patterns and suggest shifts
        common_patterns = [
            ('def ', 3),      # Python function definitions
            ('class ', 5),    # Python class definitions
            ('print(', 7),    # Python print statements
            ('import ', 11),  # Python imports
            ('if __name__', 13),  # Python main blocks
        ]
        
        for pattern, suggested_shift in common_patterns:
            if pattern.lower() in text_sample.lower():
                suggestions.append(suggested_shift)
        
        # Add some standard shifts if no patterns found
        if not suggestions:
            suggestions = [1, 3, 5, 7, 13, 17, 21, 25]
        
        # Remove duplicates and sort
        suggestions = sorted(list(set(suggestions)))
        
        return suggestions[:5]  # Return top 5 suggestions