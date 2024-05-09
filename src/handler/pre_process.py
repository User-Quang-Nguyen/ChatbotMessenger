from textblob import TextBlob
import re

def check_obscene(text):
    blob = TextBlob(text)
    if blob.sentiment.polarity < 0:
        # chứa ngôn ngữ tục tĩu
        return True
    else:
        # không chứa ngôn ngữ tục tĩu
        return False
    
def check_syntax(text):
    if re.search(r"^\s*(ls|pwd|cat|rm|ping|netcat|ssh)\s*", text):
        # chứa câu lệnh Linux
        return True
    else:
        # không chứa câu lệnh Linux
        return False
    
def check_text(text):
    if check_obscene(text) or check_syntax(text):
        return False
    return True