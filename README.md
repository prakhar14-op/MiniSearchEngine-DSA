# Mini Search Engine - DSA Project

## 1. Project Overview
This project implements a **pure DSA-based information retrieval system** from scratch using Python. It includes a complete search engine pipeline featuring text preprocessing, inverted indexing, TF-IDF ranking, and a web interface. The system was built without relying on external machine learning libraries or search frameworks, focusing instead on manual implementation of core information retrieval algorithms.

Key capabilities include:
- **Core Engine**: Regex-based tokenization, stopword removal, and inverted indexing.
- **Ranking**: Log-normalized TF-IDF scoring with dot product for document ranking.
- **Autocomplete**: Trie-based prefix matching for real-time query suggestions.
- **Interface**: Both a CLI and a Flask-based web UI for interaction.

## 2. Dataset Description
The system uses the **20 Newsgroups** dataset, a standard collection of approximately 20,000 newsgroup documents partitioned across 20 different newsgroups. This dataset serves as a benchmark for text classification and text clustering.
- **Source**: 20_newsgroups.tar.gz
- **Total Documents**: ~20,000
- **Categories**: 20 (e.g., comp.graphics, sci.space, rec.autos)

## 3. Approach & Design
The design follows a standard Information Retrieval pipeline, constrained to use only Python standard libraries (plus Flask for UI).

### Architecture
```
mini_search_engine/
│
├── engine/ (Core Logic)
│   ├── preprocess.py      # Tokenization & Normalization
│   ├── inverted_index.py  # Index Construction
│   ├── tfidf.py           # Ranking Formulas
│   ├── search.py          # Query Processing
│   ├── autocomplete.py    # Trie Implementation
│
├── data/                  # Storage
├── ui/                    # User Interface
└── main.py                # Entry Point
```

### Design Decisions
- **Tokenization**: Implemented via Regex `[a-z]+` for simplicity and speed.
- **Stopwords**: A hardcoded set of top-50 English stopwords is used to reduce index noise without external dependencies.
- **Stemming**: Intentionally omitted to maintain determinism and explainability.
- **Ranking**: Dot product was chosen over cosine similarity for efficiency, as TF-IDF weights implicitly handle length normalization to a degree sufficient for this dataset.

## 4. Data Structures Used
- **Inverted Index**: A Hash Map (`Dictionary`) mapping terms to posting lists.
    - Type: `Dict[str, List[Tuple[int, int]]]`
    - Purpose: O(1) average lookup for query terms.
- **Trie (Prefix Tree)**: A tree data structure for storing vocabulary.
    - Purpose: O(P) lookup for autocomplete suggestions, where P is prefix length.
- **Sets**: Used for O(1) stopword lookups.

## 5. Algorithms Implemented
- **Indexing**: Single-pass tokenization and posting list construction.
- **TF-IDF Calculation**:
    - **TF**: `1 + log10(tf)` (if tf > 0)
    - **IDF**: `log10(N / df)`
- **Search & Ranking**:
    - Query terms are weighted using TF-IDF.
    - Documents are scored via the dot product of query and document vectors.
    - Top-K retrieval using sorting (Optimization: could use Heap for O(N log K)).
- **Autocomplete**:
    - Depth-First Search (DFS) on the Trie to collect completions for a given prefix.

## 6. Time & Space Complexity
### Inverted Index
- **Build Time**: O(D × L), where D is the number of documents and L is the average length.
- **Query Time**: O(Q × P), where Q is the number of query terms and P is the average posting list length.
- **Space Complexity**: O(Sum of all term frequencies), effectively proportional to collection size.

### Autocomplete (Trie)
- **Build Time**: O(V × W), where V is vocabulary size and W is average word length.
- **Query Time**: O(P + K), where P is prefix length and K is the number of suggestions.
- **Space**: O(total characters in vocabulary).

## 7. Performance Report
- **Documents Indexed**: 19,997
- **Vocabulary Size**: ~120,000 unique terms
- **Index Size**: ~24.6 MB (Serialized)
- **Indexing Time**: ~90-120 seconds
- **Query Latency**: < 0.1 seconds (Top-10 results)
- **Autocomplete Response**: < 50ms

## 8. How to Run the Project
### Prerequisites
Requires Python 3.x and Flask.
```bash
pip install flask
```

### Execution
**1. Build the Index**
```bash
python main.py --build
```
This extracts the dataset and compiles `data/index.pkl`.

**2. Run Interactive CLI**
```bash
python main.py --interactive
```

**3. Run Web Interface**
```bash
python ui/app.py
```

## 9. Sample Queries & Outputs
- **"computer graphics"**: Returns documents related to visualization and rendering (comp.graphics).
- **"neural network"**: Returns articles on AI/ML.
- **"encryption security"**: Matches documents in sci.crypt.
- **"space shuttle"**: Matches documents in sci.space.

*Edge Cases*: Common stopwords like "the" are filtered; terms not in the vocabulary return no matches.

## 10. Limitations
1. **Memory Usage**: The entire index is loaded into RAM, limiting scalability to datasets that fit in memory.
2. **Sequential Processing**: Indexing is single-threaded; parallelization could speed up build times.
3. **No Phrase Search**: Queries are treated as a "bag of words"; exact phrase matching is not supported.
4. **No Advanced Query Operators**: Boolean operators (AND, OR, NOT) are not implemented.
