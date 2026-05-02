"""
heap_and_search.py
==================
Flask API routes for:
  • Min Heap       – insert, extract_min, peek, heapify, delete, search, display, memory
  • Max Heap       – insert, extract_max, peek, heapify, delete, search, display, memory
  • Interpolation Search – search, with full step trace

Every endpoint returns:
  {
    "success": true,
    "data": ...,
    "time_taken_ms": <float>,       # wall-clock time of the pure algorithm (not HTTP overhead)
    "memory_bytes": <int>,          # sys.getsizeof of the internal structure
    "memory_kb": <float>,
    "complexity": {
        "time_avg":   "...",
        "time_best":  "...",
        "time_worst": "...",
        "space":      "...",
        "note":       "..."
    }
  }

Register this blueprint in your main app.py with:
    from heap_and_search import heap_bp
    app.register_blueprint(heap_bp)
"""

import sys
import time
import tracemalloc
from flask import Blueprint, request, jsonify

heap_bp = Blueprint('heap', __name__)


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _ms(start: float) -> float:
    """Return elapsed milliseconds since `start` (from time.perf_counter())."""
    return round((time.perf_counter() - start) * 1000, 4)


def _mem(obj) -> dict:
    """Return memory usage of obj in bytes and KB."""
    b = sys.getsizeof(obj)
    return {"memory_bytes": b, "memory_kb": round(b / 1024, 4)}


def _ok(data, ms, mem_obj, complexity: dict, extra: dict = None) -> dict:
    """Build a standard success response."""
    resp = {
        "success": True,
        "data": data,
        "time_taken_ms": ms,
        **_mem(mem_obj),
        "complexity": complexity,
    }
    if extra:
        resp.update(extra)
    return resp


def _err(msg: str) -> dict:
    return {"success": False, "error": msg}


# ─────────────────────────────────────────────────────────────────────────────
# MIN HEAP
# ─────────────────────────────────────────────────────────────────────────────

class MinHeap:
    """
    Binary Min-Heap backed by a Python list.

    Index arithmetic (0-based):
        parent(i)      = (i - 1) // 2
        left_child(i)  = 2*i + 1
        right_child(i) = 2*i + 2
    """

    def __init__(self):
        self._heap: list = []
        self.comparisons: int = 0
        self.swaps: int = 0

    # ── internal helpers ──────────────────────────────────────────────────────

    def _reset_counters(self):
        self.comparisons = 0
        self.swaps = 0

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left(self, i: int) -> int:
        return 2 * i + 1

    def _right(self, i: int) -> int:
        return 2 * i + 2

    def _swap(self, i: int, j: int):
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]
        self.swaps += 1

    def _bubble_up(self, i: int):
        """Restore heap property upward from index i."""
        while i > 0:
            p = self._parent(i)
            self.comparisons += 1
            if self._heap[i] < self._heap[p]:
                self._swap(i, p)
                i = p
            else:
                break

    def _bubble_down(self, i: int):
        """Restore heap property downward from index i."""
        n = len(self._heap)
        while True:
            smallest = i
            l, r = self._left(i), self._right(i)

            self.comparisons += 1
            if l < n and self._heap[l] < self._heap[smallest]:
                smallest = l

            self.comparisons += 1
            if r < n and self._heap[r] < self._heap[smallest]:
                smallest = r

            if smallest != i:
                self._swap(i, smallest)
                i = smallest
            else:
                break

    # ── public operations ─────────────────────────────────────────────────────

    def insert(self, value) -> dict:
        """
        Insert a value.
        Time:  O(log n) average & worst  |  O(1) best (empty heap)
        Space: O(1)
        """
        self._reset_counters()
        t0 = time.perf_counter()

        self._heap.append(value)
        self._bubble_up(len(self._heap) - 1)

        return {
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "time_ms": _ms(t0),
        }

    def extract_min(self) -> dict:
        """
        Remove and return the minimum element (root).
        Time:  O(log n) average & worst  |  O(1) best (single element)
        Space: O(1)
        """
        self._reset_counters()
        t0 = time.perf_counter()

        if not self._heap:
            return {"error": "Heap is empty", "time_ms": _ms(t0)}

        min_val = self._heap[0]

        # Move last element to root and bubble down
        last = self._heap.pop()
        if self._heap:
            self._heap[0] = last
            self._bubble_down(0)

        return {
            "extracted": min_val,
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "time_ms": _ms(t0),
        }

    def peek(self) -> dict:
        """
        Return minimum without removing.
        Time:  O(1)
        Space: O(1)
        """
        t0 = time.perf_counter()
        if not self._heap:
            return {"error": "Heap is empty", "time_ms": _ms(t0)}
        return {"min": self._heap[0], "time_ms": _ms(t0)}

    def delete(self, value) -> dict:
        """
        Delete first occurrence of value.
        Time:  O(n) search + O(log n) restructure = O(n)
        Space: O(1)
        """
        self._reset_counters()
        t0 = time.perf_counter()

        try:
            idx = self._heap.index(value)
        except ValueError:
            return {"error": f"{value} not found in heap", "time_ms": _ms(t0)}

        # Replace with last element and re-heapify
        self._heap[idx] = self._heap[-1]
        self._heap.pop()

        if idx < len(self._heap):
            self._bubble_up(idx)
            self._bubble_down(idx)

        return {
            "deleted": value,
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "time_ms": _ms(t0),
        }

    def search(self, value) -> dict:
        """
        Linear scan (heap offers no faster search guarantee).
        Time:  O(n)
        Space: O(1)
        """
        t0 = time.perf_counter()
        comparisons = 0
        for i, v in enumerate(self._heap):
            comparisons += 1
            if v == value:
                return {
                    "found": True,
                    "index": i,
                    "comparisons": comparisons,
                    "time_ms": _ms(t0),
                }
        return {
            "found": False,
            "index": -1,
            "comparisons": comparisons,
            "time_ms": _ms(t0),
        }

    def heapify(self, array: list) -> dict:
        """
        Build heap from an arbitrary list in O(n) (Floyd's algorithm).
        Time:  O(n)   |  naive insert-one-by-one is O(n log n)
        Space: O(1)   (in-place)
        """
        self._reset_counters()
        t0 = time.perf_counter()

        self._heap = list(array)
        n = len(self._heap)

        # Start from last non-leaf and bubble down each node
        for i in range(n // 2 - 1, -1, -1):
            self._bubble_down(i)

        return {
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "time_ms": _ms(t0),
        }

    def display(self) -> list:
        return list(self._heap)

    def size(self) -> int:
        return len(self._heap)


# ─────────────────────────────────────────────────────────────────────────────
# MAX HEAP
# ─────────────────────────────────────────────────────────────────────────────

class MaxHeap:
    """
    Binary Max-Heap backed by a Python list.
    Mirror of MinHeap with comparisons inverted (> instead of <).
    """

    def __init__(self):
        self._heap: list = []
        self.comparisons: int = 0
        self.swaps: int = 0

    def _reset_counters(self):
        self.comparisons = 0
        self.swaps = 0

    def _parent(self, i):  return (i - 1) // 2
    def _left(self, i):    return 2 * i + 1
    def _right(self, i):   return 2 * i + 2

    def _swap(self, i, j):
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]
        self.swaps += 1

    def _bubble_up(self, i: int):
        while i > 0:
            p = self._parent(i)
            self.comparisons += 1
            if self._heap[i] > self._heap[p]:   # MAX: child > parent → swap
                self._swap(i, p)
                i = p
            else:
                break

    def _bubble_down(self, i: int):
        n = len(self._heap)
        while True:
            largest = i
            l, r = self._left(i), self._right(i)

            self.comparisons += 1
            if l < n and self._heap[l] > self._heap[largest]:
                largest = l

            self.comparisons += 1
            if r < n and self._heap[r] > self._heap[largest]:
                largest = r

            if largest != i:
                self._swap(i, largest)
                i = largest
            else:
                break

    def insert(self, value) -> dict:
        """Time: O(log n) | Space: O(1)"""
        self._reset_counters()
        t0 = time.perf_counter()
        self._heap.append(value)
        self._bubble_up(len(self._heap) - 1)
        return {
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "time_ms": _ms(t0),
        }

    def extract_max(self) -> dict:
        """Time: O(log n) | Space: O(1)"""
        self._reset_counters()
        t0 = time.perf_counter()

        if not self._heap:
            return {"error": "Heap is empty", "time_ms": _ms(t0)}

        max_val = self._heap[0]
        last = self._heap.pop()
        if self._heap:
            self._heap[0] = last
            self._bubble_down(0)

        return {
            "extracted": max_val,
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "time_ms": _ms(t0),
        }

    def peek(self) -> dict:
        """Time: O(1) | Space: O(1)"""
        t0 = time.perf_counter()
        if not self._heap:
            return {"error": "Heap is empty", "time_ms": _ms(t0)}
        return {"max": self._heap[0], "time_ms": _ms(t0)}

    def delete(self, value) -> dict:
        """Time: O(n) | Space: O(1)"""
        self._reset_counters()
        t0 = time.perf_counter()

        try:
            idx = self._heap.index(value)
        except ValueError:
            return {"error": f"{value} not found in heap", "time_ms": _ms(t0)}

        self._heap[idx] = self._heap[-1]
        self._heap.pop()

        if idx < len(self._heap):
            self._bubble_up(idx)
            self._bubble_down(idx)

        return {
            "deleted": value,
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "time_ms": _ms(t0),
        }

    def search(self, value) -> dict:
        """Time: O(n) | Space: O(1)"""
        t0 = time.perf_counter()
        comparisons = 0
        for i, v in enumerate(self._heap):
            comparisons += 1
            if v == value:
                return {
                    "found": True,
                    "index": i,
                    "comparisons": comparisons,
                    "time_ms": _ms(t0),
                }
        return {
            "found": False,
            "index": -1,
            "comparisons": comparisons,
            "time_ms": _ms(t0),
        }

    def heapify(self, array: list) -> dict:
        """Time: O(n) Floyd's algorithm | Space: O(1)"""
        self._reset_counters()
        t0 = time.perf_counter()

        self._heap = list(array)
        n = len(self._heap)

        for i in range(n // 2 - 1, -1, -1):
            self._bubble_down(i)

        return {
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "time_ms": _ms(t0),
        }

    def display(self) -> list:
        return list(self._heap)

    def size(self) -> int:
        return len(self._heap)


# ─────────────────────────────────────────────────────────────────────────────
# INTERPOLATION SEARCH
# ─────────────────────────────────────────────────────────────────────────────

class InterpolationSearch:
    """
    Interpolation Search on a sorted array.

    Formula:
        pos = low + ((target - arr[low]) * (high - low)) // (arr[high] - arr[low])

    Complexity:
        Average: O(log log n)  — for uniformly distributed data
        Worst:   O(n)          — for non-uniform / heavily skewed data
        Best:    O(1)          — target is at the first probe position
        Space:   O(1)

    The class also offers:
        • sort_and_search  — sort input first, then search (pre-condition helper)
        • range_search     — find all values in [lo, hi]
        • count_occurrences — count how many times a value appears
    """

    @staticmethod
    def _interpolate(arr: list, low: int, high: int, target) -> int:
        """
        Compute the interpolated probe index.
        Returns -1 if the formula would divide by zero (all elements equal).
        """
        denom = arr[high] - arr[low]
        if denom == 0:
            return -1   # All elements in range are equal → fall back to linear
        return low + ((target - arr[low]) * (high - low)) // denom

    @staticmethod
    def search(arr: list, target) -> dict:
        """
        Standard interpolation search on a sorted list.
        Returns found, index, all probe positions, comparisons, and time.
        """
        t0 = time.perf_counter()
        comparisons = 0
        probes = []          # List of probe indices for step-by-step trace
        steps = []           # Human-readable step descriptions

        if not arr:
            return {
                "found": False, "index": -1,
                "comparisons": 0, "probes": [],
                "steps": ["Array is empty"],
                "time_ms": _ms(t0),
            }

        # Interpolation search requires a sorted array
        sorted_arr = sorted(arr)
        low, high = 0, len(sorted_arr) - 1
        step_num = 0

        while low <= high and target >= sorted_arr[low] and target <= sorted_arr[high]:
            step_num += 1

            pos = InterpolationSearch._interpolate(sorted_arr, low, high, target)

            # Fall back to midpoint if interpolation breaks (equal elements)
            if pos == -1:
                pos = (low + high) // 2

            # Clamp to valid range (floating point edge cases)
            pos = max(low, min(high, pos))
            probes.append(pos)

            comparisons += 1
            steps.append(
                f"Step {step_num}: low={low}, high={high}, "
                f"probe={pos}, arr[{pos}]={sorted_arr[pos]}, target={target}"
            )

            if sorted_arr[pos] == target:
                # Find original index in unsorted array for accurate reporting
                original_index = arr.index(target) if target in arr else pos
                return {
                    "found": True,
                    "index": original_index,
                    "sorted_index": pos,
                    "sorted_array": sorted_arr,
                    "comparisons": comparisons,
                    "probes": probes,
                    "steps": steps,
                    "time_ms": _ms(t0),
                }
            elif sorted_arr[pos] < target:
                steps[-1] += f" → too low, move right"
                low = pos + 1
            else:
                steps[-1] += f" → too high, move left"
                high = pos - 1

        return {
            "found": False,
            "index": -1,
            "sorted_index": -1,
            "sorted_array": sorted_arr,
            "comparisons": comparisons,
            "probes": probes,
            "steps": steps,
            "time_ms": _ms(t0),
        }

    @staticmethod
    def sort_and_search(arr: list, target) -> dict:
        """
        Sort the array first, then interpolation-search.
        Total time: O(n log n) sort + O(log log n) search.
        """
        t0 = time.perf_counter()
        sorted_arr = sorted(arr)
        sort_time = _ms(t0)

        result = InterpolationSearch.search(sorted_arr, target)
        result["sort_time_ms"] = sort_time
        result["total_time_ms"] = _ms(t0)
        result["note"] = "Array was sorted before search (O(n log n) sort + O(log log n) search)"
        return result

    @staticmethod
    def range_search(arr: list, lo, hi) -> dict:
        """
        Find all values in the closed range [lo, hi].
        Time: O(n)  |  Space: O(k) where k = number of results
        """
        t0 = time.perf_counter()
        sorted_arr = sorted(arr)
        results = []
        comparisons = 0

        for i, v in enumerate(sorted_arr):
            comparisons += 1
            if lo <= v <= hi:
                results.append({"value": v, "sorted_index": i})
            elif v > hi:
                break   # Sorted array — no need to continue

        return {
            "found": len(results) > 0,
            "results": results,
            "count": len(results),
            "range": [lo, hi],
            "sorted_array": sorted_arr,
            "comparisons": comparisons,
            "time_ms": _ms(t0),
        }

    @staticmethod
    def count_occurrences(arr: list, target) -> dict:
        """
        Count how many times target appears.
        Uses binary search to find left & right boundary → O(log n).
        """
        t0 = time.perf_counter()
        sorted_arr = sorted(arr)
        comparisons = 0

        def lower_bound(a, val):
            nonlocal comparisons
            lo, hi = 0, len(a)
            while lo < hi:
                mid = (lo + hi) // 2
                comparisons += 1
                if a[mid] < val:
                    lo = mid + 1
                else:
                    hi = mid
            return lo

        def upper_bound(a, val):
            nonlocal comparisons
            lo, hi = 0, len(a)
            while lo < hi:
                mid = (lo + hi) // 2
                comparisons += 1
                if a[mid] <= val:
                    lo = mid + 1
                else:
                    hi = mid
            return lo

        lb = lower_bound(sorted_arr, target)
        ub = upper_bound(sorted_arr, target)
        count = ub - lb

        return {
            "value": target,
            "count": count,
            "found": count > 0,
            "sorted_array": sorted_arr,
            "comparisons": comparisons,
            "time_ms": _ms(t0),
        }


# ─────────────────────────────────────────────────────────────────────────────
# SINGLETON INSTANCES  (persist across requests in Flask's single-process dev)
# ─────────────────────────────────────────────────────────────────────────────

_min_heap = MinHeap()
_max_heap = MaxHeap()

# ─────────────────────────────────────────────────────────────────────────────
# BIG-O COMPLEXITY METADATA
# ─────────────────────────────────────────────────────────────────────────────

COMPLEXITY = {
    "min_heap": {
        "insert":      {"time_avg": "O(log n)", "time_best": "O(1)",      "time_worst": "O(log n)", "space": "O(1)", "note": "Bubble-up restores heap property"},
        "extract_min": {"time_avg": "O(log n)", "time_best": "O(1)",      "time_worst": "O(log n)", "space": "O(1)", "note": "Extract root, place last element at root, bubble-down"},
        "peek":        {"time_avg": "O(1)",     "time_best": "O(1)",      "time_worst": "O(1)",     "space": "O(1)", "note": "Root is always the minimum"},
        "delete":      {"time_avg": "O(n)",     "time_best": "O(log n)",  "time_worst": "O(n)",     "space": "O(1)", "note": "O(n) linear scan to find value + O(log n) restructure"},
        "search":      {"time_avg": "O(n)",     "time_best": "O(1)",      "time_worst": "O(n)",     "space": "O(1)", "note": "Heap gives no search shortcut; full scan required"},
        "heapify":     {"time_avg": "O(n)",     "time_best": "O(n)",      "time_worst": "O(n)",     "space": "O(1)", "note": "Floyd's bottom-up algorithm; faster than n inserts O(n log n)"},
        "display":     {"time_avg": "O(n)",     "time_best": "O(n)",      "time_worst": "O(n)",     "space": "O(n)", "note": "Copy of internal list"},
    },
    "max_heap": {
        "insert":      {"time_avg": "O(log n)", "time_best": "O(1)",      "time_worst": "O(log n)", "space": "O(1)", "note": "Bubble-up restores heap property"},
        "extract_max": {"time_avg": "O(log n)", "time_best": "O(1)",      "time_worst": "O(log n)", "space": "O(1)", "note": "Extract root, place last element at root, bubble-down"},
        "peek":        {"time_avg": "O(1)",     "time_best": "O(1)",      "time_worst": "O(1)",     "space": "O(1)", "note": "Root is always the maximum"},
        "delete":      {"time_avg": "O(n)",     "time_best": "O(log n)",  "time_worst": "O(n)",     "space": "O(1)", "note": "O(n) linear scan to find value + O(log n) restructure"},
        "search":      {"time_avg": "O(n)",     "time_best": "O(1)",      "time_worst": "O(n)",     "space": "O(1)", "note": "Heap gives no search shortcut; full scan required"},
        "heapify":     {"time_avg": "O(n)",     "time_best": "O(n)",      "time_worst": "O(n)",     "space": "O(1)", "note": "Floyd's bottom-up algorithm"},
        "display":     {"time_avg": "O(n)",     "time_best": "O(n)",      "time_worst": "O(n)",     "space": "O(n)", "note": "Copy of internal list"},
    },
    "interpolation": {
        "search":            {"time_avg": "O(log log n)", "time_best": "O(1)",      "time_worst": "O(n)",        "space": "O(1)", "note": "Avg case assumes uniformly distributed data"},
        "sort_and_search":   {"time_avg": "O(n log n)",  "time_best": "O(n log n)","time_worst": "O(n log n)",  "space": "O(n)", "note": "Includes O(n log n) sort cost"},
        "range_search":      {"time_avg": "O(n)",        "time_best": "O(1)",      "time_worst": "O(n)",        "space": "O(k)", "note": "k = number of elements in range"},
        "count_occurrences": {"time_avg": "O(log n)",    "time_best": "O(1)",      "time_worst": "O(log n)",    "space": "O(1)", "note": "Binary lower/upper bound search"},
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# MIN HEAP  ROUTES   /api/ds/min_heap/...
# ─────────────────────────────────────────────────────────────────────────────

@heap_bp.route('/api/ds/min_heap/push', methods=['POST'])
def min_heap_insert():
    body = request.get_json(silent=True) or {}
    value = body.get('value')
    if value is None:
        return jsonify(_err("'value' is required")), 400
    try:
        value = float(value) if '.' in str(value) else int(value)
    except (ValueError, TypeError):
        return jsonify(_err("Value must be numeric")), 400

    tracemalloc.start()
    result = _min_heap.insert(value)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return jsonify(_ok(
        data=_min_heap.display(),
        ms=result["time_ms"],
        mem_obj=_min_heap._heap,
        complexity=COMPLEXITY["min_heap"]["insert"],
        extra={
            "inserted": value,
            "heap_size": _min_heap.size(),
            "comparisons": result["comparisons"],
            "swaps": result["swaps"],
            "peak_memory_bytes": peak,
        }
    ))


@heap_bp.route('/api/ds/min_heap/pop', methods=['POST'])
def min_heap_extract():
    tracemalloc.start()
    result = _min_heap.extract_min()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if "error" in result:
        return jsonify(_err(result["error"])), 400

    return jsonify(_ok(
        data=_min_heap.display(),
        ms=result["time_ms"],
        mem_obj=_min_heap._heap,
        complexity=COMPLEXITY["min_heap"]["extract_min"],
        extra={
            "extracted": result["extracted"],
            "heap_size": _min_heap.size(),
            "comparisons": result["comparisons"],
            "swaps": result["swaps"],
            "peak_memory_bytes": peak,
        }
    ))


@heap_bp.route('/api/ds/min_heap/peek', methods=['POST'])
def min_heap_peek():
    result = _min_heap.peek()
    if "error" in result:
        return jsonify(_err(result["error"])), 400

    return jsonify(_ok(
        data=_min_heap.display(),
        ms=result["time_ms"],
        mem_obj=_min_heap._heap,
        complexity=COMPLEXITY["min_heap"]["peek"],
        extra={"min": result["min"], "heap_size": _min_heap.size()}
    ))


@heap_bp.route('/api/ds/min_heap/delete', methods=['POST'])
def min_heap_delete():
    body = request.get_json(silent=True) or {}
    value = body.get('value')
    if value is None:
        return jsonify(_err("'value' is required")), 400
    try:
        value = float(value) if '.' in str(value) else int(value)
    except (ValueError, TypeError):
        return jsonify(_err("Value must be numeric")), 400

    result = _min_heap.delete(value)
    if "error" in result:
        return jsonify(_err(result["error"])), 404

    return jsonify(_ok(
        data=_min_heap.display(),
        ms=result["time_ms"],
        mem_obj=_min_heap._heap,
        complexity=COMPLEXITY["min_heap"]["delete"],
        extra={
            "deleted": result["deleted"],
            "heap_size": _min_heap.size(),
            "comparisons": result["comparisons"],
            "swaps": result["swaps"],
        }
    ))


@heap_bp.route('/api/ds/min_heap/search', methods=['POST'])
def min_heap_search():
    body = request.get_json(silent=True) or {}
    value = body.get('value')
    if value is None:
        return jsonify(_err("'value' is required")), 400
    try:
        value = float(value) if '.' in str(value) else int(value)
    except (ValueError, TypeError):
        return jsonify(_err("Value must be numeric")), 400

    result = _min_heap.search(value)
    return jsonify(_ok(
        data=_min_heap.display(),
        ms=result["time_ms"],
        mem_obj=_min_heap._heap,
        complexity=COMPLEXITY["min_heap"]["search"],
        extra={
            "found": result["found"],
            "index": result["index"],
            "comparisons": result["comparisons"],
        }
    ))


@heap_bp.route('/api/ds/min_heap/heapify', methods=['POST'])
def min_heap_heapify():
    body = request.get_json(silent=True) or {}
    array = body.get('array', [])
    if not isinstance(array, list):
        return jsonify(_err("'array' must be a list")), 400

    try:
        array = [float(v) if '.' in str(v) else int(v) for v in array]
    except (ValueError, TypeError):
        return jsonify(_err("All values must be numeric")), 400

    tracemalloc.start()
    result = _min_heap.heapify(array)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return jsonify(_ok(
        data=_min_heap.display(),
        ms=result["time_ms"],
        mem_obj=_min_heap._heap,
        complexity=COMPLEXITY["min_heap"]["heapify"],
        extra={
            "heap_size": _min_heap.size(),
            "comparisons": result["comparisons"],
            "swaps": result["swaps"],
            "peak_memory_bytes": peak,
        }
    ))


@heap_bp.route('/api/ds/min_heap/display', methods=['GET'])
def min_heap_display():
    return jsonify(_ok(
        data=_min_heap.display(),
        ms=0,
        mem_obj=_min_heap._heap,
        complexity=COMPLEXITY["min_heap"]["display"],
        extra={"heap_size": _min_heap.size()}
    ))


@heap_bp.route('/api/ds/min_heap/memory', methods=['GET'])
def min_heap_memory():
    mem = _mem(_min_heap._heap)
    return jsonify({
        "success": True,
        "memory": {
            "memory_bytes": mem["memory_bytes"],
            "memory_kb": mem["memory_kb"],
            "elements": _min_heap.size(),
        }
    })


@heap_bp.route('/api/ds/min_heap/reset', methods=['POST'])
def min_heap_reset():
    global _min_heap
    _min_heap = MinHeap()
    return jsonify({"success": True, "message": "Min Heap cleared", "data": []})


# ─────────────────────────────────────────────────────────────────────────────
# MAX HEAP  ROUTES   /api/ds/max_heap/...
# ─────────────────────────────────────────────────────────────────────────────

@heap_bp.route('/api/ds/max_heap/push', methods=['POST'])
def max_heap_insert():
    body = request.get_json(silent=True) or {}
    value = body.get('value')
    if value is None:
        return jsonify(_err("'value' is required")), 400
    try:
        value = float(value) if '.' in str(value) else int(value)
    except (ValueError, TypeError):
        return jsonify(_err("Value must be numeric")), 400

    tracemalloc.start()
    result = _max_heap.insert(value)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return jsonify(_ok(
        data=_max_heap.display(),
        ms=result["time_ms"],
        mem_obj=_max_heap._heap,
        complexity=COMPLEXITY["max_heap"]["insert"],
        extra={
            "inserted": value,
            "heap_size": _max_heap.size(),
            "comparisons": result["comparisons"],
            "swaps": result["swaps"],
            "peak_memory_bytes": peak,
        }
    ))


@heap_bp.route('/api/ds/max_heap/pop', methods=['POST'])
def max_heap_extract():
    tracemalloc.start()
    result = _max_heap.extract_max()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if "error" in result:
        return jsonify(_err(result["error"])), 400

    return jsonify(_ok(
        data=_max_heap.display(),
        ms=result["time_ms"],
        mem_obj=_max_heap._heap,
        complexity=COMPLEXITY["max_heap"]["extract_max"],
        extra={
            "extracted": result["extracted"],
            "heap_size": _max_heap.size(),
            "comparisons": result["comparisons"],
            "swaps": result["swaps"],
            "peak_memory_bytes": peak,
        }
    ))


@heap_bp.route('/api/ds/max_heap/peek', methods=['POST'])
def max_heap_peek():
    result = _max_heap.peek()
    if "error" in result:
        return jsonify(_err(result["error"])), 400

    return jsonify(_ok(
        data=_max_heap.display(),
        ms=result["time_ms"],
        mem_obj=_max_heap._heap,
        complexity=COMPLEXITY["max_heap"]["peek"],
        extra={"max": result["max"], "heap_size": _max_heap.size()}
    ))


@heap_bp.route('/api/ds/max_heap/delete', methods=['POST'])
def max_heap_delete():
    body = request.get_json(silent=True) or {}
    value = body.get('value')
    if value is None:
        return jsonify(_err("'value' is required")), 400
    try:
        value = float(value) if '.' in str(value) else int(value)
    except (ValueError, TypeError):
        return jsonify(_err("Value must be numeric")), 400

    result = _max_heap.delete(value)
    if "error" in result:
        return jsonify(_err(result["error"])), 404

    return jsonify(_ok(
        data=_max_heap.display(),
        ms=result["time_ms"],
        mem_obj=_max_heap._heap,
        complexity=COMPLEXITY["max_heap"]["delete"],
        extra={
            "deleted": result["deleted"],
            "heap_size": _max_heap.size(),
            "comparisons": result["comparisons"],
            "swaps": result["swaps"],
        }
    ))


@heap_bp.route('/api/ds/max_heap/search', methods=['POST'])
def max_heap_search():
    body = request.get_json(silent=True) or {}
    value = body.get('value')
    if value is None:
        return jsonify(_err("'value' is required")), 400
    try:
        value = float(value) if '.' in str(value) else int(value)
    except (ValueError, TypeError):
        return jsonify(_err("Value must be numeric")), 400

    result = _max_heap.search(value)
    return jsonify(_ok(
        data=_max_heap.display(),
        ms=result["time_ms"],
        mem_obj=_max_heap._heap,
        complexity=COMPLEXITY["max_heap"]["search"],
        extra={
            "found": result["found"],
            "index": result["index"],
            "comparisons": result["comparisons"],
        }
    ))


@heap_bp.route('/api/ds/max_heap/heapify', methods=['POST'])
def max_heap_heapify():
    body = request.get_json(silent=True) or {}
    array = body.get('array', [])
    if not isinstance(array, list):
        return jsonify(_err("'array' must be a list")), 400

    try:
        array = [float(v) if '.' in str(v) else int(v) for v in array]
    except (ValueError, TypeError):
        return jsonify(_err("All values must be numeric")), 400

    tracemalloc.start()
    result = _max_heap.heapify(array)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return jsonify(_ok(
        data=_max_heap.display(),
        ms=result["time_ms"],
        mem_obj=_max_heap._heap,
        complexity=COMPLEXITY["max_heap"]["heapify"],
        extra={
            "heap_size": _max_heap.size(),
            "comparisons": result["comparisons"],
            "swaps": result["swaps"],
            "peak_memory_bytes": peak,
        }
    ))


@heap_bp.route('/api/ds/max_heap/display', methods=['GET'])
def max_heap_display():
    return jsonify(_ok(
        data=_max_heap.display(),
        ms=0,
        mem_obj=_max_heap._heap,
        complexity=COMPLEXITY["max_heap"]["display"],
        extra={"heap_size": _max_heap.size()}
    ))


@heap_bp.route('/api/ds/max_heap/memory', methods=['GET'])
def max_heap_memory():
    mem = _mem(_max_heap._heap)
    return jsonify({
        "success": True,
        "memory": {
            "memory_bytes": mem["memory_bytes"],
            "memory_kb": mem["memory_kb"],
            "elements": _max_heap.size(),
        }
    })


@heap_bp.route('/api/ds/max_heap/reset', methods=['POST'])
def max_heap_reset():
    global _max_heap
    _max_heap = MaxHeap()
    return jsonify({"success": True, "message": "Max Heap cleared", "data": []})


# ─────────────────────────────────────────────────────────────────────────────
# INTERPOLATION SEARCH  ROUTES   /api/algorithms/interpolation/...
# ─────────────────────────────────────────────────────────────────────────────

@heap_bp.route('/api/algorithms/interpolation/search', methods=['POST'])
def interpolation_search():
    """
    Standard interpolation search.
    Body: { "data": [int, ...], "target": int }
    """
    body = request.get_json(silent=True) or {}
    data = body.get('data', [])
    target = body.get('target')

    if not isinstance(data, list) or not data:
        return jsonify(_err("'data' must be a non-empty list")), 400
    if target is None:
        return jsonify(_err("'target' is required")), 400

    try:
        data = [float(v) if '.' in str(v) else int(v) for v in data]
        target = float(target) if '.' in str(target) else int(target)
    except (ValueError, TypeError):
        return jsonify(_err("All values must be numeric")), 400

    tracemalloc.start()
    result = InterpolationSearch.search(data, target)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return jsonify({
        "success": True,
        "found": result["found"],
        "index": result["index"],
        "sorted_index": result.get("sorted_index", -1),
        "sorted_array": result.get("sorted_array", []),
        "comparisons": result["comparisons"],
        "probes": result["probes"],
        "steps": result["steps"],
        "time_taken_ms": result["time_ms"],
        "memory_bytes": sys.getsizeof(data),
        "memory_kb": round(sys.getsizeof(data) / 1024, 4),
        "peak_memory_bytes": peak,
        "complexity": COMPLEXITY["interpolation"]["search"],
    })


@heap_bp.route('/api/algorithms/interpolation/sort_and_search', methods=['POST'])
def interpolation_sort_and_search():
    """
    Sort then search. Useful when caller cannot guarantee sorted input.
    Body: { "data": [int, ...], "target": int }
    """
    body = request.get_json(silent=True) or {}
    data = body.get('data', [])
    target = body.get('target')

    if not isinstance(data, list) or not data:
        return jsonify(_err("'data' must be a non-empty list")), 400
    if target is None:
        return jsonify(_err("'target' is required")), 400

    try:
        data = [float(v) if '.' in str(v) else int(v) for v in data]
        target = float(target) if '.' in str(target) else int(target)
    except (ValueError, TypeError):
        return jsonify(_err("All values must be numeric")), 400

    tracemalloc.start()
    result = InterpolationSearch.sort_and_search(data, target)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return jsonify({
        "success": True,
        "found": result["found"],
        "index": result["index"],
        "sorted_array": result.get("sorted_array", []),
        "comparisons": result["comparisons"],
        "probes": result["probes"],
        "steps": result["steps"],
        "sort_time_ms": result.get("sort_time_ms", 0),
        "search_time_ms": result["time_ms"],
        "total_time_ms": result.get("total_time_ms", result["time_ms"]),
        "memory_bytes": sys.getsizeof(data),
        "memory_kb": round(sys.getsizeof(data) / 1024, 4),
        "peak_memory_bytes": peak,
        "complexity": COMPLEXITY["interpolation"]["sort_and_search"],
        "note": result.get("note", ""),
    })


@heap_bp.route('/api/algorithms/interpolation/range_search', methods=['POST'])
def interpolation_range_search():
    """
    Find all values in [lo, hi].
    Body: { "data": [int, ...], "lo": int, "hi": int }
    """
    body = request.get_json(silent=True) or {}
    data = body.get('data', [])
    lo = body.get('lo')
    hi = body.get('hi')

    if not isinstance(data, list) or not data:
        return jsonify(_err("'data' must be a non-empty list")), 400
    if lo is None or hi is None:
        return jsonify(_err("'lo' and 'hi' are required")), 400

    try:
        data = [float(v) if '.' in str(v) else int(v) for v in data]
        lo = float(lo) if '.' in str(lo) else int(lo)
        hi = float(hi) if '.' in str(hi) else int(hi)
    except (ValueError, TypeError):
        return jsonify(_err("All values must be numeric")), 400

    if lo > hi:
        return jsonify(_err("'lo' must be ≤ 'hi'")), 400

    result = InterpolationSearch.range_search(data, lo, hi)

    return jsonify({
        "success": True,
        "found": result["found"],
        "results": result["results"],
        "count": result["count"],
        "range": result["range"],
        "sorted_array": result["sorted_array"],
        "comparisons": result["comparisons"],
        "time_taken_ms": result["time_ms"],
        "memory_bytes": sys.getsizeof(data),
        "memory_kb": round(sys.getsizeof(data) / 1024, 4),
        "complexity": COMPLEXITY["interpolation"]["range_search"],
    })


@heap_bp.route('/api/algorithms/interpolation/count', methods=['POST'])
def interpolation_count():
    """
    Count occurrences of target using binary boundary search.
    Body: { "data": [int, ...], "target": int }
    """
    body = request.get_json(silent=True) or {}
    data = body.get('data', [])
    target = body.get('target')

    if not isinstance(data, list) or not data:
        return jsonify(_err("'data' must be a non-empty list")), 400
    if target is None:
        return jsonify(_err("'target' is required")), 400

    try:
        data = [float(v) if '.' in str(v) else int(v) for v in data]
        target = float(target) if '.' in str(target) else int(target)
    except (ValueError, TypeError):
        return jsonify(_err("All values must be numeric")), 400

    result = InterpolationSearch.count_occurrences(data, target)

    return jsonify({
        "success": True,
        "value": result["value"],
        "count": result["count"],
        "found": result["found"],
        "sorted_array": result["sorted_array"],
        "comparisons": result["comparisons"],
        "time_taken_ms": result["time_ms"],
        "memory_bytes": sys.getsizeof(data),
        "memory_kb": round(sys.getsizeof(data) / 1024, 4),
        "complexity": COMPLEXITY["interpolation"]["count_occurrences"],
    })


# ─────────────────────────────────────────────────────────────────────────────
# ALSO handle the generic /api/algorithms/search route so existing JS works
# ─────────────────────────────────────────────────────────────────────────────

@heap_bp.route('/api/algorithms/search/interpolation', methods=['POST'])
def generic_interpolation_search():
    """
    Compatibility route for the existing JS executeSearch() function.
    Body: { "data": [...], "target": int, "algorithm": "interpolation" }
    """
    return interpolation_search()