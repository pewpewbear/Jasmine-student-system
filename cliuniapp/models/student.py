"""
Student model with validation and subject management
"""

from typing import List, Optional
from .subject import Subject


class Student:
    """Student model with subject enrollment management"""
    
    def __init__(self, id: str, name: str, email: str, password: str, subjects: Optional[List[Subject]] = None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.subjects = subjects if subjects is not None else []
    
    def add_subject(self, subject: Subject) -> None:
        """Add a subject to the student's enrollment"""
        if len(self.subjects) >= 4:
            raise ValueError("Cannot enrol more than four (4) subjects")
        self.subjects.append(subject)
    
    def remove_subject_by_id(self, subject_id: str) -> bool:
        """Remove a subject by ID. Returns True if found and removed, False otherwise"""
        for i, subject in enumerate(self.subjects):
            if subject.id == subject_id:
                del self.subjects[i]
                return True
        return False
    
    def avg_mark(self) -> int:
        """Calculate average mark across all enrolled subjects"""
        if not self.subjects:
            return 0
        total_marks = sum(subject.mark for subject in self.subjects)
        return total_marks // len(self.subjects)
    
    def is_pass(self) -> bool:
        """Determine if student passes based on average mark >= 50"""
        return self.avg_mark() >= 50
    
    def change_password(self, new_pw: str) -> None:
        """Change student password"""
        self.password = new_pw
