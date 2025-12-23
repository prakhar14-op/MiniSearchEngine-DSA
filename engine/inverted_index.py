import os
import pickle
import math
from collections import defaultdict
from engine.preprocess import preprocess_text

class InvertedIndex:
    def __init__(self):
        # term -> list of (doc_id, tf_raw)
        self.index = defaultdict(list)
        # doc_id -> filepath (to retrieve original)
        self.doc_map = {}
        # Total number of documents indexed
        self.total_docs = 0
        
    def build_index(self, root_path: str):
        """
        Walks through the dataset directory and indexes all files.
        """
        doc_id = 0
        print(f"Indexing docs in {root_path}...")
        
        for root, dirs, files in os.walk(root_path):
            for file in files:
                filepath = os.path.join(root, file)
                self.index_document(filepath, doc_id)
                self.doc_map[doc_id] = filepath
                doc_id += 1
                
                if doc_id % 1000 == 0:
                    print(f"Processed {doc_id} documents...")
                    
        self.total_docs = doc_id
        print(f"Indexing complete. Total docs: {self.total_docs}")

    def index_document(self, filepath: str, doc_id: int):
        """
        Reads, preproccesses, and updates the index for a single file.
        """
        try:
            # Latin-1 is usually safe for the 20 newsgroups dataset to avoid encoding errors
            with open(filepath, 'r', encoding='latin1') as f:
                content = f.read()
        except Exception as e:
            # Skip files that can't be read
            return

        tokens = preprocess_text(content)
        
        # Calculate Term Frequency for this document
        # We store raw counts, and normalize during search
        term_counts = defaultdict(int) 
        for token in tokens:
            term_counts[token] += 1
            
        # Update the inverted index
        for term, count in term_counts.items():
            self.index[term].append((doc_id, count))

    def save(self, output_path: str):
        """Saves the index object to disk using pickle."""
        print(f"Saving index to {output_path}...")
        with open(output_path, 'wb') as f:
            pickle.dump(self, f)
        print("Index saved.")

    @staticmethod
    def load(input_path: str):
        """Loads the index object from disk."""
        print(f"Loading index from {input_path}...")
        with open(input_path, 'rb') as f:
            return pickle.load(f)