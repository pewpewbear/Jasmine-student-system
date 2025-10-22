#!/usr/bin/env python3
"""
University Student System Launcher
Choose between CLI and GUI interfaces
"""

import sys
import os

def main():
    """Main launcher function"""
    print("=" * 50)
    print("University Student System")
    print("=" * 50)
    print()
    print("Choose your interface:")
    print("1. Command Line Interface (CLI)")
    print("2. Desktop GUI (tkinter)")
    print("3. Web GUI (browser-based)")
    print("4. Exit")
    print()
    
    while True:
        try:
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == '1':
                print("\nStarting CLI interface...")
                print("-" * 30)
                # Import and run CLI app
                sys.path.append(os.path.join(os.path.dirname(__file__), 'cliuniapp'))
                from cliuniapp.app import main as cli_main
                cli_main()
                break
                
            elif choice == '2':
                print("\nStarting Desktop GUI interface...")
                try:
                    # Import and run GUI app
                    sys.path.append(os.path.join(os.path.dirname(__file__), 'cliuniapp'))
                    from cliuniapp.gui_app import UniversityGUI
                    app = UniversityGUI()
                    app.run()
                    break
                except ImportError as e:
                    print(f"Desktop GUI not available: {e}")
                    print("Please try the Web GUI option instead.")
                    continue
                
            elif choice == '3':
                print("\nStarting Web GUI interface...")
                print("The web interface will open in your browser at http://localhost:8000")
                print("Press Ctrl+C to stop the server")
                # Import and run Web GUI app
                sys.path.append(os.path.join(os.path.dirname(__file__), 'cliuniapp'))
                from cliuniapp.web_gui import run_web_server
                run_web_server()
                break
                
            elif choice == '4':
                print("\nGoodbye!")
                break
                
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()
