import time
import sys

class Timer:
    """Simple timer context manager to measure execution time."""
    def __init__(self, name="Operation"):
        self.name = name
        self.start_time = None
        self.end_time = None
        self.duration = 0

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        print(f"[{self.name}] finished in {self.duration:.4f} seconds.")

def get_approx_memory_mb(obj):
    """
    Returns approximate memory usage of an object in MB.
    Note: sys.getsizeof is shallow. reliable deep size is hard without external libs.
    """
    # This is a very rough estimate suitable for "No external libraries" constraint
    # For a dictionary, we can sum size of keys and values deeply if needed, 
    # but that's complex to implement manually. 
    # We will return the size of the pickle representation which is a good proxy.
    import pickle
    try:
        size_bytes = len(pickle.dumps(obj))
        return size_bytes / (1024 * 1024)
    except:
        return 0.0