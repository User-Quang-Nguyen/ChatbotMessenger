from textblob import TextBlob
import re

def contains_offensive_language(text):
    text_blob = TextBlob(text)
    return text_blob.sentiment.polarity < 0
    
def check_linux_command(text):
    """Check if the given text contains a Linux command."""
    linux_command_pattern = r"\s*(ls|pwd|rm|ping|netcat|ssh)\s*"
    return bool(re.search(linux_command_pattern, text))
    
def is_text_valid(text):
    """Check if the given text is valid by not containing offensive language and not containing a Linux command."""
    return not contains_offensive_language(text) and not check_linux_command(text)
