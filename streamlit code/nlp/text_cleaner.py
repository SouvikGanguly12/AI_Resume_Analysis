import re
import string

STOPWORDS = {
    "and", "or", "the", "a", "an", "in", "on", "at",
    "to", "for", "with", "of", "by", "is", "are"
}

def clean_text(text):
    if not text:
        return ""
    
    text = str(text)
    
    text = text.lower()
    
    text = re.sub(r'\d+', '', text)
    
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    text = re.sub(r'\s+', ' ', text).strip()
    
    words = text.split()
    words = [word for word in words if word not in STOPWORDS]

    cleaned_text = " ".join(words)

    return cleaned_text