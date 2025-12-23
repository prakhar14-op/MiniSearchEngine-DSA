from collections import defaultdict
from engine.preprocess import preprocess_text
from engine.tfidf import compute_tf, compute_idf
from engine.inverted_index import InvertedIndex

def search(query: str, index: InvertedIndex, top_k: int = 10):
    """
    Executes a search query against the provided inverted index.
    
    Strategy:
    1. Preprocess query.
    2. Calculate query TF-IDF vector (query_weights).
    3. Iterate through query terms, find matching docs.
    4. Accumulate scores (Dot Product).
    5. Sort and return top K.
    
    Returns:
    List of tuples: (doc_path, score)
    """
    tokens = preprocess_text(query)
    if not tokens:
        return []
    
    # 1. Compute Query Weights (TF-IDF)
    # For query: TF is count in query. IDF is from index.
    query_counts = defaultdict(int)
    for t in tokens:
        query_counts[t] += 1
        
    query_weights = {}
    for term, count in query_counts.items():
        # Check if term exists in our index
        if term in index.index:
            df = len(index.index[term])
            idf = compute_idf(index.total_docs, df)
            tf = compute_tf(count)
            query_weights[term] = tf * idf
    
    # 2. Accumulate Scores (Dot Product: sigma(w_q * w_d))
    scores = defaultdict(float)
    
    for term, w_q in query_weights.items():
        if term not in index.index:
            continue
            
        postings = index.index[term]
        
        # We need to re-calculate IDF here for the document weight
        # Optimization: We computed IDF above already
        df = len(postings)
        idf = compute_idf(index.total_docs, df)
        
        for doc_id, raw_tf in postings:
            w_d = compute_tf(raw_tf) * idf
            scores[doc_id] += (w_q * w_d)
            
    # 3. Sort and Retrieve
    # Sort by score desc
    sorted_docs = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    
    results = []
    for doc_id, score in sorted_docs[:top_k]:
        path = index.doc_map.get(doc_id, "Unknown")
        results.append((path, score))
        
    return results