"""
Student controller - handles registration and login
"""

import random
from models.database import Database
from models.student import Student
from services.auth_service import is_valid_email, is_valid_password, authenticate
from services.id_service import new_student_id
from controllers.enrolment_controller import EnrolmentController
from utils.ioutils import safe_input, print_error, print_success


class StudentController:
    """Student system controller for registration and login"""
    
    def __init__(self):
        self.db = Database()
        self.enrolment_controller = EnrolmentController()
    
    def run(self):
        """Student system main loop"""
        while True:
            self.show_menu()
            choice = safe_input("> ").lower()
            
            if choice == 'l':
                self.login()
            elif choice == 'r':
                self.register()
            elif choice == 'x':
                print("Returning to University menu...")
                break
            else:
                print_error("Invalid option. Please choose l, r, or x.")
    
    def show_menu(self):
        """Display the student menu"""
        print("\nStudent System")
        print("(l) login")
        print("(r) register")
        print("(x) exit")
    
    def register(self):
        """Register a new student"""
        name = safe_input("Enter name: ")
        if not name:
            print_error("Name cannot be empty.")
            return
        
        email = safe_input("Enter email: ")
        if not is_valid_email(email):
            print_error("Invalid email format. Must end with @anything.uts.edu.au")
            return
        
        # Check if email already exists
        if self.db.find_by_email(email):
            print_error("Email already registered.")
            return
        
        password = safe_input("Enter password: ")
        if not is_valid_password(password):
            print_error("Invalid password format. Must start with uppercase, have at least 5 letters, then at least 3 digits.")
            return
        
        # Create new student
        student_id = new_student_id(self.db)
        student = Student(student_id, name, email, password)
        self.db.upsert(student)
        
        print_success(f"Registered successfully. Your student id is {student_id}.")
    
    def login(self):
        """Login an existing student"""
        email = safe_input("Email: ")
        password = safe_input("Password: ")
        
        student = authenticate(email, password, self.db)
        if student:
            print_success("Login successful.")
            self.enrolment_controller.run(student, self.db)
        else:
            print_error("Invalid credentials.")
