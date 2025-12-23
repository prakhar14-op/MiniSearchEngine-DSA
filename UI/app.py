from flask import Flask, render_template, request, jsonify
import sys
import os

# Perform path magic to import from engine
# Current file: .../mini_search_engine/ui/app.py
# We want to import from .../mini_search_engine/engine
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir) # .../mini_search_engine
sys.path.append(project_root)

from engine.inverted_index import InvertedIndex
from engine.search import search
from engine.metrics import Timer
from engine.autocomplete import Autocomplete

app = Flask(__name__)

# Path to the index file
INDEX_FILE = os.path.join(project_root, "data", "index.pkl")
index = None
autocomplete_engine = None

def load_global_index():
    global index, autocomplete_engine
    if os.path.exists(INDEX_FILE):
        print("Loading index...")
        index = InvertedIndex.load(INDEX_FILE)
        print(f"Index loaded with {index.total_docs} documents.")
        
        # Build autocomplete from vocabulary
        print("Building autocomplete...")
        autocomplete_engine = Autocomplete()
        autocomplete_engine.build_from_vocabulary(index.index.keys())
        print("Autocomplete ready.")
    else:
        print(f"WARNING: Index file not found at {INDEX_FILE}. Please run 'main.py --build' first.")

@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    query = ""
    duration = 0
    message = ""
    vocab_size = len(index.index) if index else 0
    total_docs = index.total_docs if index else 0
    
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query and index:
            with Timer("search") as t:
                results = search(query, index, top_k=10)
            duration = t.duration
        elif not index:
            message = "Index not loaded. Server maintenance required."
            
    return render_template("index.html", 
                         results=results, 
                         query=query, 
                         duration=duration, 
                         message=message,
                         vocab_size=vocab_size,
                         total_docs=total_docs)

@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    """API endpoint for autocomplete suggestions."""
    prefix = request.args.get("q", "").strip().lower()
    if not prefix or not autocomplete_engine:
        return jsonify([])
    
    suggestions = autocomplete_engine.get_suggestions(prefix, max_suggestions=5)
    return jsonify(suggestions)

if __name__ == "__main__":
    load_global_index()
    print("Starting Flask server...")
    app.run(debug=True, port=5000)