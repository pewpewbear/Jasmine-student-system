#!/usr/bin/env python3
"""
CLI University App - Entry Point
Main application loop with University menu
"""

from controllers.university_controller import UniversityController

def main():
    """Main application entry point"""
    print("Welcome to CLI University System")
    controller = UniversityController()
    controller.run()

if __name__ == "__main__":
    main()
