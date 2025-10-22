"""
Enrolment controller - handles subject enrollment and management
"""

import random
from models.subject import Subject
from services.grading_service import grade_from_mark
from services.id_service import new_subject_id
from services.auth_service import is_valid_password
from utils.ioutils import safe_input, print_error, print_success, print_info


class EnrolmentController:
    """Subject enrollment controller"""
    
    def run(self, student, db):
        """Subject enrollment main loop"""
        while True:
            self.show_menu()
            choice = safe_input("> ").lower()
            
            if choice == 'e':
                self.enrol_subject(student, db)
            elif choice == 'r':
                self.remove_subject(student, db)
            elif choice == 's':
                self.show_subjects(student)
            elif choice == 'c':
                self.change_password(student, db)
            elif choice == 'x':
                print("Returning to Student menu...")
                break
            else:
                print_error("Invalid option. Please choose c, e, r, s, or x.")
    
    def show_menu(self):
        """Display the enrollment menu"""
        print("\nSubject Enrolment System")
        print("(c) change")
        print("(e) enrol")
        print("(r) remove")
        print("(s) show")
        print("(x) exit")
    
    def enrol_subject(self, student, db):
        """Enroll student in a new subject"""
        if len(student.subjects) >= 4:
            print_error("Cannot enrol more than four (4) subjects.")
            return
        
        # Generate random mark between 25 and 100
        mark = random.randint(25, 100)
        grade = grade_from_mark(mark)
        subject_id = new_subject_id(student)
        
        subject = Subject(subject_id, mark, grade)
        student.add_subject(subject)
        db.upsert(student)
        
        current_count = len(student.subjects)
        print_success(f"Enrolled subject {subject_id} with mark {mark} (grade {grade}). [{current_count}/4]")
    
    def remove_subject(self, student, db):
        """Remove a subject by ID"""
        subject_id = safe_input("Enter subject id to remove: ")
        if not subject_id:
            print_error("Subject ID cannot be empty.")
            return
        
        if student.remove_subject_by_id(subject_id):
            db.upsert(student)
            print_success(f"Removed subject {subject_id}.")
        else:
            print_error("Subject not found.")
    
    def show_subjects(self, student):
        """Show all enrolled subjects with average and status"""
        if not student.subjects:
            print_info("No subjects enrolled.")
            return
        
        print_info("Subjects:")
        for subject in student.subjects:
            print(f"  {subject.id}  mark={subject.mark}  grade={subject.grade}")
        
        avg_mark = student.avg_mark()
        status = "PASS" if student.is_pass() else "FAIL"
        print(f"Average: {avg_mark}  Status: {status}")
    
    def change_password(self, student, db):
        """Change student password"""
        new_password = safe_input("Enter new password: ")
        if not is_valid_password(new_password):
            print_error("Invalid password format. Must start with uppercase, have at least 5 letters, then at least 3 digits.")
            return
        
        confirm_password = safe_input("Confirm new password: ")
        if new_password != confirm_password:
            print_error("Passwords do not match.")
            return
        
        student.change_password(new_password)
        db.upsert(student)
        print_success("Password changed.")
