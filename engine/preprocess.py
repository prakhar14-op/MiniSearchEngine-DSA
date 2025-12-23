import re

# Hardcoded list of top 50 common English stopwords
STOPWORDS = {
    "the", "of", "and", "a", "to", "in", "is", "you", "that", "it",
    "he", "was", "for", "on", "are", "as", "with", "his", "they", "at",
    "be", "this", "have", "from", "or", "one", "had", "by", "word", "but",
    "not", "what", "all", "were", "we", "when", "your", "can", "said",
    "there", "use", "an", "each", "which", "she", "do", "how", "their",
    "if", "will", "up", "other", "about", "out", "many", "then", "them",
    "these", "so", "some"
}

def preprocess_text(text: str) -> list[str]:
    """
    Preprocesses raw text:
    1. Lowercases the text.
    2. Tokenizes using regex [a-z]+.
    3. Removes stopwords.
    Returns a list of tokens.
    """
    if not text:
        return []
        
    # 1. Lowercase
    text = text.lower()
    
    # 2. Tokenize (Regex [a-z]+)
    # This automatically handles punctuation removal by ignoring non-alphabet characters
    tokens = re.findall(r'[a-z]+', text)
    
    # 3. Stopword removal
    filtered_tokens = [t for t in tokens if t not in STOPWORDS]
    
    return filtered_tokens