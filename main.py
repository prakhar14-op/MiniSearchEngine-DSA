import argparse
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engine.inverted_index import InvertedIndex
from engine.search import search
from engine.metrics import Timer, get_approx_memory_mb

INDEX_FILE = "data/index.pkl"
DATA_DIR = "data/20_newsgroups/20_newsgroups"

def main():
    parser = argparse.ArgumentParser(description="Mini Search Engine CLI")
    parser.add_argument("--build", action="store_true", help="Build the inverted index")
    parser.add_argument("--query", type=str, help="Run a search query")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    
    args = parser.parse_args()
    
    index = InvertedIndex()
    
    if args.build:
        if not os.path.exists(DATA_DIR):
            print(f"Error: Data directory not found at {DATA_DIR}")
            return
            
        with Timer("Build Index"):
            index.build_index(DATA_DIR)
            
        with Timer("Save Index"):
            index.save(INDEX_FILE)
            
        print(f"Vocabulary Size: {len(index.index)} terms")
        print(f"Approx Index Memory: {get_approx_memory_mb(index.index):.2f} MB")
        return

    # Load Index
    if os.path.exists(INDEX_FILE):
        with Timer("Load Index"):
            index = InvertedIndex.load(INDEX_FILE)
            print(f"Index loaded. {index.total_docs} docs, {len(index.index)} terms.")
    else:
        print("Index not found. Please run with --build first.")
        return

    if args.query:
        run_search(args.query, index)
    
    if args.interactive:
        while True:
            q = input("\nEnter query (or 'exit'): ")
            if q.lower() == 'exit':
                break
            run_search(q, index)

def run_search(query, index):
    with Timer("Search Query"):
        results = search(query, index, top_k=10)
    
    print(f"\nResults for '{query}':")
    if not results:
        print("No matches found.")
    for i, (path, score) in enumerate(results):
        print(f"{i+1}. {score:.4f} - {path}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Default to interactive if no args
        sys.argv.append("--interactive")
    main()