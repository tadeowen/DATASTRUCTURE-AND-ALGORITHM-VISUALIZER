class HashTable:
    """
    Hash Table with multiple hash function options for educational purposes.
    Supports collision resolution using Separate Chaining.
    """
    def __init__(self, size=10, hash_method="division"):
        self.size = size
        self.table = [[] for _ in range(size)]   # buckets
        self.count = 0
        self.hash_method = hash_method.lower()

    def _hash(self, key):
        """Select hash function based on chosen method"""
        if not isinstance(key, (int, str)):
            key = str(key)

        if isinstance(key, str):
            key = sum(ord(c) for c in key)   # simple string to int conversion

        if self.hash_method == "division":
            return key % self.size

        elif self.hash_method == "mid_square":
            sq = key * key
            s = str(sq)
            mid = len(s) // 2
            return int(s[max(0, mid-1):mid+2]) % self.size

        elif self.hash_method == "truncation":
            s = str(key)
            return int(s[-2:]) % self.size if len(s) >= 2 else int(s) % self.size

        elif self.hash_method == "folding":
            s = str(key)
            total = 0
            for i in range(0, len(s), 2):
                total += int(s[i:i+2])
            return total % self.size

        elif self.hash_method == "multiplication":
            A = 0.6180339887   # golden ratio conjugate
            return int(self.size * (key * A % 1))

        else:  # default division
            return key % self.size

    def insert(self, key, value):
        """Insert or update key-value pair"""
        index = self._hash(key)
        bucket = self.table[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)   # update
                return True

        bucket.append((key, value))
        self.count += 1
        return True

    def get(self, key):
        """Retrieve value by key"""
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def delete(self, key):
        """Delete key-value pair"""
        index = self._hash(key)
        bucket = self.table[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.count -= 1
                return True
        return False

    def display(self):
        """Return nice format for frontend visualization"""
        result = []
        for i, bucket in enumerate(self.table):
            if bucket:
                result.append({
                    "index": i,
                    "bucket": [f"{k} → {v}" for k, v in bucket]
                })
        return result

    def get_size(self):
        return self.count

    def is_empty(self):
        return self.count == 0

    def load_factor(self):
        return round(self.count / self.size, 3) if self.size > 0 else 0

    def clear(self):
        self.table = [[] for _ in range(self.size)]
        self.count = 0