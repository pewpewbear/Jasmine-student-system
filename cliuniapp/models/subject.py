"""
Subject model with mark and grade
"""


class Subject:
    """Subject model with mark and computed grade"""
    
    def __init__(self, id: str, mark: int, grade: str):
        self.id = id
        self.mark = mark
        self.grade = grade
