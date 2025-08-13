"""
Text to Code Converter Module

This module handles the conversion of user text into Python code
using various predefined templates.
"""

import re
from datetime import datetime


class TextToCodeConverter:
    """Handles conversion of text to Python code using various templates."""
    
    def __init__(self):
        """Initialize the converter with template definitions."""
        self.templates = {
            1: self._create_print_statements,
            2: self._create_function_definition,
            3: self._create_class_definition,
            4: self._create_comment_block
        }
    
    def convert_text(self, text, template_type):
        """
        Convert text to Python code using the specified template.
        
        Args:
            text (str): The input text to convert
            template_type (int): Template type (1-4)
        
        Returns:
            str: Generated Python code
        
        Raises:
            ValueError: If template_type is invalid
        """
        if template_type not in self.templates:
            raise ValueError(f"Invalid template type: {template_type}")
        
        if not text.strip():
            raise ValueError("Input text cannot be empty")
        
        return self.templates[template_type](text)
    
    def _create_print_statements(self, text):
        """
        Convert text to print statements.
        Each sentence becomes a separate print statement.
        """
        # Split text into sentences
        sentences = self._split_into_sentences(text)
        
        code_lines = [
            "# Generated Print Statements",
            f"# Created on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ""
        ]
        
        for i, sentence in enumerate(sentences, 1):
            if sentence.strip():
                # Clean and escape the sentence for Python string
                clean_sentence = sentence.strip().replace('"', '\\"')
                code_lines.append(f'print("Statement {i}: {clean_sentence}")')
        
        code_lines.extend([
            "",
            "# End of generated print statements"
        ])
        
        return "\n".join(code_lines)
    
    def _create_function_definition(self, text):
        """
        Convert text to a function definition.
        The function name is derived from the first few words.
        """
        # Extract function name from first few words
        words = text.split()[:3]
        function_name = self._create_identifier("_".join(words))
        
        # Split text into logical parts for function body
        sentences = self._split_into_sentences(text)
        
        code_lines = [
            "# Generated Function Definition",
            f"# Created on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            f"def {function_name}():",
            '    """',
            f"    Function generated from user input:",
            f'    "{text[:60]}{"..." if len(text) > 60 else ""}"',
            '    """',
        ]
        
        # Add function body
        for sentence in sentences:
            if sentence.strip():
                clean_sentence = sentence.strip().replace('"', '\\"')
                code_lines.append(f'    print("{clean_sentence}")')
        
        code_lines.extend([
            "",
            "",
            "# Example usage:",
            f"if __name__ == '__main__':",
            f"    {function_name}()"
        ])
        
        return "\n".join(code_lines)
    
    def _create_class_definition(self, text):
        """
        Convert text to a class definition.
        The class name is derived from the first few words.
        """
        # Extract class name from first few words
        words = text.split()[:2]
        class_name = self._create_class_name("_".join(words))
        
        # Split text for methods
        sentences = self._split_into_sentences(text)
        
        code_lines = [
            "# Generated Class Definition",
            f"# Created on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            f"class {class_name}:",
            '    """',
            f"    Class generated from user input:",
            f'    "{text[:60]}{"..." if len(text) > 60 else ""}"',
            '    """',
            "",
            "    def __init__(self):",
            '        """Initialize the class instance."""',
            f'        self.description = "{text[:50]}{"..." if len(text) > 50 else ""}"',
            "",
            "    def display_info(self):",
            '        """Display information about this instance."""',
            '        print(f"Description: {self.description}")',
        ]
        
        # Add methods based on sentences
        for i, sentence in enumerate(sentences[:3], 1):  # Limit to 3 methods
            if sentence.strip():
                method_name = self._create_identifier(f"method_{i}")
                clean_sentence = sentence.strip().replace('"', '\\"')
                code_lines.extend([
                    "",
                    f"    def {method_name}(self):",
                    f'        """Method {i} generated from user input."""',
                    f'        print("{clean_sentence}")',
                    f'        return "{clean_sentence}"'
                ])
        
        code_lines.extend([
            "",
            "",
            "# Example usage:",
            f"if __name__ == '__main__':",
            f"    obj = {class_name}()",
            "    obj.display_info()",
            "    obj.method_1()" if len(sentences) > 0 else ""
        ])
        
        return "\n".join(filter(None, code_lines))
    
    def _create_comment_block(self, text):
        """
        Convert text to a well-formatted comment block.
        """
        lines = text.split('\n')
        max_width = 70
        
        code_lines = [
            '"""',
            f"Generated Comment Block - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * max_width,
            ""
        ]
        
        for line in lines:
            if line.strip():
                # Wrap long lines
                words = line.strip().split()
                current_line = ""
                
                for word in words:
                    if len(current_line + " " + word) <= max_width:
                        current_line += " " + word if current_line else word
                    else:
                        if current_line:
                            code_lines.append(current_line)
                        current_line = word
                
                if current_line:
                    code_lines.append(current_line)
                code_lines.append("")
        
        code_lines.extend([
            "=" * max_width,
            '"""',
            "",
            "# This is a comment block generated from your text",
            "# You can use this as documentation in your Python projects"
        ])
        
        return "\n".join(code_lines)
    
    def _split_into_sentences(self, text):
        """
        Split text into sentences using basic punctuation.
        
        Args:
            text (str): Input text
        
        Returns:
            list: List of sentences
        """
        # Basic sentence splitting on common punctuation
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _create_identifier(self, text):
        """
        Create a valid Python identifier from text.
        
        Args:
            text (str): Input text
        
        Returns:
            str: Valid Python identifier
        """
        # Remove non-alphanumeric characters and replace with underscores
        identifier = re.sub(r'[^a-zA-Z0-9_]', '_', text.lower())
        
        # Ensure it starts with a letter or underscore
        if identifier and identifier[0].isdigit():
            identifier = "func_" + identifier
        
        # Remove multiple consecutive underscores
        identifier = re.sub(r'_+', '_', identifier)
        
        # Remove trailing underscores
        identifier = identifier.strip('_')
        
        # Ensure minimum length
        if not identifier or len(identifier) < 3:
            identifier = "generated_item"
        
        return identifier
    
    def _create_class_name(self, text):
        """
        Create a valid Python class name from text (PascalCase).
        
        Args:
            text (str): Input text
        
        Returns:
            str: Valid Python class name
        """
        # Split and clean words
        words = re.findall(r'[a-zA-Z0-9]+', text)
        
        if not words:
            return "GeneratedClass"
        
        # Convert to PascalCase
        class_name = ''.join(word.capitalize() for word in words[:3])  # Limit to 3 words
        
        # Ensure it's a valid identifier
        if not class_name or not class_name[0].isalpha():
            class_name = "Generated" + class_name
        
        return class_name