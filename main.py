#!/usr/bin/env python3
"""
Text to Code Generator with Encryption
Main CLI interface for the application

This module provides the main command-line interface for users to:
- Convert text to Python code
- Encrypt and decrypt generated code
- Save results to files
"""

import sys
from text_to_code import TextToCodeConverter
from encryption import CaesarCipher
from file_manager import FileManager


class TextToCodeApp:
    """Main application class that handles the CLI interface and coordinates between modules."""
    
    def __init__(self):
        """Initialize the application with necessary components."""
        self.converter = TextToCodeConverter()
        self.cipher = CaesarCipher()
        self.file_manager = FileManager()
        self.generated_code = ""
        self.encrypted_code = ""
    
    def display_menu(self):
        """Display the main menu options to the user."""
        print("\n" + "="*50)
        print("  TEXT TO CODE GENERATOR WITH ENCRYPTION")
        print("="*50)
        print("1. Convert Text to Python Code")
        print("2. Encrypt Generated Code")
        print("3. Decrypt Code")
        print("4. Save Code to File")
        print("5. Load and Decrypt from File")
        print("6. View Current Code")
        print("7. Clear All Data")
        print("8. Exit")
        print("-"*50)
    
    def get_user_choice(self):
        """Get and validate user menu choice."""
        try:
            choice = input("Enter your choice (1-8): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
                return int(choice)
            else:
                print("❌ Invalid choice! Please enter a number between 1-8.")
                return None
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error reading input: {e}")
            return None
    
    def convert_text_to_code(self):
        """Handle text to code conversion with template selection."""
        print("\n📝 TEXT TO CODE CONVERSION")
        print("-"*30)
        
        # Get user text
        text = input("Enter your text: ").strip()
        if not text:
            print("❌ Empty text provided!")
            return
        
        # Show template options
        print("\nAvailable templates:")
        print("1. Print Statements")
        print("2. Function Definition")
        print("3. Class Definition")
        print("4. Comment Block")
        
        try:
            template_choice = int(input("Choose template (1-4): ").strip())
            if template_choice not in [1, 2, 3, 4]:
                print("❌ Invalid template choice!")
                return
        except ValueError:
            print("❌ Please enter a valid number!")
            return
        
        # Convert text to code
        try:
            self.generated_code = self.converter.convert_text(text, template_choice)
            print("\n✅ Code generated successfully!")
            print("\nGenerated Code:")
            print("-"*40)
            print(self.generated_code)
            print("-"*40)
        except Exception as e:
            print(f"❌ Error generating code: {e}")
    
    def encrypt_code(self):
        """Handle code encryption."""
        if not self.generated_code:
            print("❌ No code to encrypt! Please generate code first.")
            return
        
        print("\n🔒 CODE ENCRYPTION")
        print("-"*20)
        
        try:
            shift = int(input("Enter Caesar cipher shift value (1-25): ").strip())
            if not (1 <= shift <= 25):
                print("❌ Shift value must be between 1 and 25!")
                return
        except ValueError:
            print("❌ Please enter a valid number!")
            return
        
        try:
            self.encrypted_code = self.cipher.encrypt(self.generated_code, shift)
            print("✅ Code encrypted successfully!")
            print(f"Encryption shift used: {shift}")
        except Exception as e:
            print(f"❌ Error encrypting code: {e}")
    
    def decrypt_code(self):
        """Handle code decryption."""
        print("\n🔓 CODE DECRYPTION")
        print("-"*20)
        
        # Check if we have encrypted code or need to input it
        if not self.encrypted_code:
            print("No encrypted code in memory. Please enter encrypted code:")
            encrypted_input = input("Encrypted code: ").strip()
            if not encrypted_input:
                print("❌ Empty encrypted code provided!")
                return
        else:
            encrypted_input = self.encrypted_code
            print("Using encrypted code from memory.")
        
        try:
            shift = int(input("Enter Caesar cipher shift value used for encryption: ").strip())
            if not (1 <= shift <= 25):
                print("❌ Shift value must be between 1 and 25!")
                return
        except ValueError:
            print("❌ Please enter a valid number!")
            return
        
        try:
            decrypted_code = self.cipher.decrypt(encrypted_input, shift)
            print("\n✅ Code decrypted successfully!")
            print("\nDecrypted Code:")
            print("-"*40)
            print(decrypted_code)
            print("-"*40)
        except Exception as e:
            print(f"❌ Error decrypting code: {e}")
    
    def save_code_to_file(self):
        """Handle saving code to file."""
        print("\n💾 SAVE CODE TO FILE")
        print("-"*22)
        print("1. Save Generated Code")
        print("2. Save Encrypted Code")
        
        try:
            save_choice = int(input("Choose what to save (1-2): ").strip())
        except ValueError:
            print("❌ Please enter a valid number!")
            return
        
        if save_choice == 1:
            if not self.generated_code:
                print("❌ No generated code to save!")
                return
            try:
                filename = self.file_manager.save_code(self.generated_code, "generated")
                print(f"✅ Generated code saved to: {filename}")
            except Exception as e:
                print(f"❌ Error saving generated code: {e}")
        
        elif save_choice == 2:
            if not self.encrypted_code:
                print("❌ No encrypted code to save!")
                return
            try:
                filename = self.file_manager.save_code(self.encrypted_code, "encrypted")
                print(f"✅ Encrypted code saved to: {filename}")
            except Exception as e:
                print(f"❌ Error saving encrypted code: {e}")
        
        else:
            print("❌ Invalid choice!")
    
    def load_and_decrypt_from_file(self):
        """Handle loading encrypted code from file and decrypting it."""
        print("\n📂 LOAD AND DECRYPT FROM FILE")
        print("-"*35)
        
        filename = input("Enter filename to load: ").strip()
        if not filename:
            print("❌ Empty filename provided!")
            return
        
        try:
            loaded_code = self.file_manager.load_code(filename)
            print("✅ File loaded successfully!")
            
            shift = int(input("Enter Caesar cipher shift value: ").strip())
            if not (1 <= shift <= 25):
                print("❌ Shift value must be between 1 and 25!")
                return
            
            decrypted_code = self.cipher.decrypt(loaded_code, shift)
            print("\n✅ Code decrypted successfully!")
            print("\nDecrypted Code:")
            print("-"*40)
            print(decrypted_code)
            print("-"*40)
            
        except FileNotFoundError:
            print(f"❌ File '{filename}' not found!")
        except ValueError:
            print("❌ Please enter a valid shift number!")
        except Exception as e:
            print(f"❌ Error loading/decrypting file: {e}")
    
    def view_current_code(self):
        """Display current generated and encrypted code."""
        print("\n👁️  CURRENT CODE STATUS")
        print("-"*25)
        
        if self.generated_code:
            print("Generated Code:")
            print("-"*15)
            print(self.generated_code)
            print()
        else:
            print("No generated code available.")
        
        if self.encrypted_code:
            print("Encrypted Code:")
            print("-"*15)
            print(self.encrypted_code[:100] + "..." if len(self.encrypted_code) > 100 else self.encrypted_code)
            print()
        else:
            print("No encrypted code available.")
    
    def clear_all_data(self):
        """Clear all generated and encrypted code from memory."""
        confirm = input("Are you sure you want to clear all data? (y/N): ").strip().lower()
        if confirm == 'y':
            self.generated_code = ""
            self.encrypted_code = ""
            print("✅ All data cleared!")
        else:
            print("Operation cancelled.")
    
    def run(self):
        """Main application loop."""
        print("🚀 Welcome to Text to Code Generator with Encryption!")
        
        while True:
            try:
                self.display_menu()
                choice = self.get_user_choice()
                
                if choice is None:
                    continue
                
                if choice == 1:
                    self.convert_text_to_code()
                elif choice == 2:
                    self.encrypt_code()
                elif choice == 3:
                    self.decrypt_code()
                elif choice == 4:
                    self.save_code_to_file()
                elif choice == 5:
                    self.load_and_decrypt_from_file()
                elif choice == 6:
                    self.view_current_code()
                elif choice == 7:
                    self.clear_all_data()
                elif choice == 8:
                    print("\n👋 Thank you for using Text to Code Generator!")
                    break
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                input("Press Enter to continue...")


def main():
    """Entry point of the application."""
    app = TextToCodeApp()
    app.run()


if __name__ == "__main__":
    main()