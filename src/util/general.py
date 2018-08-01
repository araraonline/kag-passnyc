import re


def snakecase(s):
    """Simple snake_case transform"""
    s = s.lower()
    s = re.sub(r'\s+', '_', s)
    return s
