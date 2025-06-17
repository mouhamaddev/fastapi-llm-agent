from enum import Enum


ALLOWED_EXTENSIONS = {".pdf", ".docx", ".jpg", ".jpeg", ".png"}

class SummaryLength(str, Enum):
    short = "short"
    medium = "medium"
    long = "long"