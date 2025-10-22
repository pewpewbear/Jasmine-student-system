"""
ID generation service for students and subjects
"""

import random
from typing import List
from models.database import Database
from models.student import Student


def new_student_id(db: Database) -> str:
    """Generate a new unique 6-digit student ID"""
    students = db.read_all()
    used_ids = {student.id for student in students}
    
    while True:
        # Generate 6-digit ID with leading zeros
        student_id = f"{random.randint(1, 999999):06d}"
        if student_id not in used_ids:
            return student_id


def new_subject_id(student: Student) -> str:
    """Generate a new unique 3-digit subject ID for a student"""
    used_ids = {subject.id for subject in student.subjects}
    
    while True:
        # Generate 3-digit ID with leading zeros
        subject_id = f"{random.randint(1, 999):03d}"
        if subject_id not in used_ids:
            return subject_id
