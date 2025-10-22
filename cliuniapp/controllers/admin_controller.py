"""
Admin controller - handles administrative functions
"""

from models.database import Database
from utils.ioutils import safe_input, print_error, print_success, print_info


class AdminController:
    """Admin system controller"""
    
    def __init__(self):
        self.db = Database()
    
    def run(self):
        """Admin system main loop"""
        while True:
            self.show_menu()
            choice = safe_input("> ").lower()
            
            if choice == 's':
                self.show_all_students()
            elif choice == 'g':
                self.group_students()
            elif choice == 'p':
                self.partition_students()
            elif choice == 'r':
                self.remove_student()
            elif choice == 'c':
                self.clear_database()
            elif choice == 'x':
                print("Returning to University menu...")
                break
            else:
                print_error("Invalid option. Please choose c, g, p, r, s, or x.")
    
    def show_menu(self):
        """Display the admin menu"""
        print("\nAdmin System")
        print("(c) clear database")
        print("(g) group students")
        print("(p) partition students")
        print("(r) remove student")
        print("(s) show")
        print("(x) exit")
    
    def show_all_students(self):
        """Show all students with their details"""
        students = self.db.read_all()
        if not students:
            print_info("No students found.")
            return
        
        print_info("All Students:")
        for student in students:
            avg_mark = student.avg_mark()
            status = "PASS" if student.is_pass() else "FAIL"
            subject_count = len(student.subjects)
            print(f"  {student.id} {student.name} ({student.email}) avg={avg_mark} status={status} subjects={subject_count}")
    
    def group_students(self):
        """Group students by grade buckets"""
        students = self.db.read_all()
        if not students:
            print_info("No students found.")
            return
        
        grade_counts = {"HD": 0, "D": 0, "C": 0, "P": 0, "F": 0}
        
        for student in students:
            if not student.subjects:
                continue
            
            # Use highest grade among all subjects
            highest_grade = "F"
            for subject in student.subjects:
                if subject.grade == "HD":
                    highest_grade = "HD"
                elif subject.grade == "D" and highest_grade not in ["HD"]:
                    highest_grade = "D"
                elif subject.grade == "C" and highest_grade not in ["HD", "D"]:
                    highest_grade = "C"
                elif subject.grade == "P" and highest_grade not in ["HD", "D", "C"]:
                    highest_grade = "P"
            
            grade_counts[highest_grade] += 1
        
        print_info(f"HD: {grade_counts['HD']}  D: {grade_counts['D']}  C: {grade_counts['C']}  P: {grade_counts['P']}  F: {grade_counts['F']}")
    
    def partition_students(self):
        """Partition students into PASS/FAIL groups"""
        students = self.db.read_all()
        if not students:
            print_info("No students found.")
            return
        
        pass_students = []
        fail_students = []
        
        for student in students:
            if student.is_pass():
                pass_students.append(student)
            else:
                fail_students.append(student)
        
        print_info("PASS:")
        for student in pass_students:
            print(f"  {student.id} {student.name} (avg {student.avg_mark()})")
        
        print_info("FAIL:")
        for student in fail_students:
            print(f"  {student.id} {student.name} (avg {student.avg_mark()})")
    
    def remove_student(self):
        """Remove a student by ID"""
        student_id = safe_input("Enter student id to remove: ")
        if not student_id:
            print_error("Student ID cannot be empty.")
            return
        
        if len(student_id) != 6 or not student_id.isdigit():
            print_error("Student ID must be 6 digits.")
            return
        
        if self.db.remove_by_id(student_id):
            print_success(f"Removed student {student_id}.")
        else:
            print_error("Student not found.")
    
    def clear_database(self):
        """Clear all data from the database"""
        confirm = safe_input("Are you sure? (y/N): ").lower()
        if confirm == 'y':
            self.db.clear()
            print_success("All students removed.")
        else:
            print_info("Operation cancelled.")
