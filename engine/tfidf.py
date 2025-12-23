import math

def compute_tf(term_freq_raw: int) -> float:
    """
    Computes Log-Normalized Term Frequency.
    Formula: 1 + log(tf) if tf > 0 else 0
    Using base 10 usually, or natural log. 
    Standard IR often uses natural log or base 10. We will use log10 matching standard textbook examples.
    """
    if term_freq_raw <= 0:
        return 0.0
    return 1 + math.log10(term_freq_raw)

def compute_idf(total_docs: int, doc_freq: int) -> float:
    """
    Computes Log Inverse Document Frequency.
    Formula: log(N / df)
    Using base 10.
    """
    if doc_freq <= 0:
        return 0.0
    return math.log10(total_docs / doc_freq)