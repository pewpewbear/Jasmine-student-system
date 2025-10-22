"""
Authentication and validation service
"""

import re
from models.database import Database
from models.student import Student


def is_valid_email(email: str) -> bool:
    """Validate email format - must end with @anything.uts.edu.au"""
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.uts\.edu\.au$'
    return bool(re.match(pattern, email))


def is_valid_password(pw: str) -> bool:
    """
    Validate password format:
    - Starts with uppercase letter
    - Then at least 4 more letters
    - Then at least 3 digits
    """
    pattern = r'^[A-Z][A-Za-z]{4,}\d{3,}$'
    return bool(re.match(pattern, pw))


def authenticate(email: str, password: str, db: Database) -> Student | None:
    """Authenticate a student by email and password"""
    student = db.find_by_email(email)
    if student and student.password == password:
        return student
    return None
