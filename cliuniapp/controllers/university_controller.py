"""
University controller - main menu system
"""

from controllers.student_controller import StudentController
from controllers.admin_controller import AdminController
from utils.ioutils import safe_input, print_error


class UniversityController:
    """Main university system controller"""
    
    def __init__(self):
        self.student_controller = StudentController()
        self.admin_controller = AdminController()
    
    def run(self):
        """Main application loop"""
        while True:
            self.show_menu()
            choice = safe_input("> ").upper()
            
            if choice == 'A':
                self.admin_controller.run()
            elif choice == 'S':
                self.student_controller.run()
            elif choice == 'X':
                print("Goodbye!")
                break
            else:
                print_error("Invalid option. Please choose A, S, or X.")
    
    def show_menu(self):
        """Display the university menu"""
        print("\nUniversity System")
        print("(A) Admin")
        print("(S) Student")
        print("(X) Exit")
