"""
Autocomplete Module - Pure DSA Implementation
Uses Trie (Prefix Tree) for efficient prefix-based vocabulary lookup.

Time Complexity:
- Build: O(V * L) where V = vocabulary size, L = avg term length
- Query: O(P + K) where P = prefix length, K = number of suggestions

Space Complexity: O(V * L)
"""

class TrieNode:
    def __init__(self):
        self.children = {}  # char -> TrieNode
        self.is_end_of_word = False
        self.word = None  # Store complete word at terminal nodes

class Autocomplete:
    def __init__(self):
        self.root = TrieNode()
        
    def build_from_vocabulary(self, vocabulary):
        """
        Builds the Trie from a list of vocabulary terms.
        
        Args:
            vocabulary: List of strings (terms from inverted index)
        """
        for term in vocabulary:
            self._insert(term)
    
    def _insert(self, word):
        """Insert a word into the Trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.word = word
    
    def get_suggestions(self, prefix, max_suggestions=5):
        """
        Returns up to max_suggestions words that start with the given prefix.
        
        Args:
            prefix: String prefix to search for
            max_suggestions: Maximum number of suggestions to return
            
        Returns:
            List of suggested words (sorted alphabetically)
        """
        if not prefix:
            return []
        
        # Navigate to the prefix node
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []  # Prefix not found
            node = node.children[char]
        
        # Collect all words with this prefix using DFS
        suggestions = []
        self._collect_words(node, suggestions, max_suggestions)
        
        return sorted(suggestions)[:max_suggestions]
    
    def _collect_words(self, node, suggestions, max_count):
        """DFS to collect words from a given node."""
        if len(suggestions) >= max_count:
            return
        
        if node.is_end_of_word:
            suggestions.append(node.word)
        
        for char in sorted(node.children.keys()):
            self._collect_words(node.children[char], suggestions, max_count)