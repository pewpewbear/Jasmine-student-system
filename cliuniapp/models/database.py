"""
Database persistence layer using pickle
"""

import pickle
import os
from typing import List, Optional
from .student import Student


class Database:
    """Database class for persisting student data using pickle"""
    
    def __init__(self, file_path: str = "io/students.data"):
        self.file_path = file_path
    
    def ensure_file(self) -> None:
        """Create the data file if it doesn't exist"""
        directory = os.path.dirname(self.file_path)
        if directory:  # Only create directory if there is one
            os.makedirs(directory, exist_ok=True)
        if not os.path.exists(self.file_path):
            # Write empty list directly without calling write_all to avoid recursion
            with open(self.file_path, 'wb') as f:
                pickle.dump([], f)
    
    def read_all(self) -> List[Student]:
        """Read all students from the data file"""
        self.ensure_file()
        try:
            with open(self.file_path, 'rb') as f:
                return pickle.load(f)
        except (EOFError, pickle.UnpicklingError):
            # File is corrupted or empty, return empty list
            return []
    
    def write_all(self, students: List[Student]) -> None:
        """Write all students to the data file"""
        self.ensure_file()
        with open(self.file_path, 'wb') as f:
            pickle.dump(students, f)
    
    def clear(self) -> None:
        """Clear all data from the database"""
        self.write_all([])
    
    def upsert(self, student: Student) -> None:
        """Insert or update a student in the database"""
        students = self.read_all()
        # Remove existing student with same ID if it exists
        students = [s for s in students if s.id != student.id]
        students.append(student)
        self.write_all(students)
    
    def remove_by_id(self, student_id: str) -> bool:
        """Remove a student by ID. Returns True if found and removed"""
        students = self.read_all()
        original_count = len(students)
        students = [s for s in students if s.id != student_id]
        removed = len(students) < original_count
        if removed:
            self.write_all(students)
        return removed
    
    def find_by_email(self, email: str) -> Optional[Student]:
        """Find a student by email address"""
        students = self.read_all()
        for student in students:
            if student.email == email:
                return student
        return None
    
    def find_by_id(self, student_id: str) -> Optional[Student]:
        """Find a student by ID"""
        students = self.read_all()
        for student in students:
            if student.id == student_id:
                return student
        return None
