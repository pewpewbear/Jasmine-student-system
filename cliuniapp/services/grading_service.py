"""
Grading service for computing grades from marks
"""


def grade_from_mark(mark: int) -> str:
    """
    Convert a mark to a grade based on the grading scale:
    85-100 → HD
    75-84  → D
    65-74  → C
    50-64  → P
    25-49  → F
    """
    if mark >= 85:
        return "HD"
    elif mark >= 75:
        return "D"
    elif mark >= 65:
        return "C"
    elif mark >= 50:
        return "P"
    else:
        return "F"
