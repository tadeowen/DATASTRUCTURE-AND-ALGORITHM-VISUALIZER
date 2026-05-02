import time
import copy

class SortingMetrics:
    def __init__(self):
        self.swaps = 0
        self.comparisons = 0
        self.passes = 0
        self.time_taken = 0.0
        self.algorithm_name = ""

    def to_dict(self):
        return {
            'algorithm': self.algorithm_name,
            'swaps': self.swaps,
            'comparisons': self.comparisons,
            'passes': self.passes if self.passes > 0 else None,
            'time_taken': round(self.time_taken * 1000, 2),   
            'time_unit': 'ms'
        }


class SortingAlgorithms:

    @staticmethod
    def sort_with_metrics(algorithm: str, arr: list):
        algorithms = {
            'bubble': SortingAlgorithms.bubble_sort,
            'selection': SortingAlgorithms.selection_sort,
            'insertion': SortingAlgorithms.insertion_sort,
            'merge': SortingAlgorithms.merge_sort,
            'quick': SortingAlgorithms.quick_sort
        }

        if algorithm not in algorithms:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        return algorithms[algorithm](arr, track_metrics=True)

    # ====================== INDIVIDUAL ALGORITHMS ======================

    @staticmethod
    def bubble_sort(arr, track_metrics=False):
        metrics = SortingMetrics() if track_metrics else None
        if track_metrics:
            metrics.algorithm_name = "Bubble Sort"
            start = time.time()
            arr = copy.deepcopy(arr)

        n = len(arr)
        for i in range(n):
            swapped = False
            if track_metrics:
                metrics.passes += 1

            for j in range(n - i - 1):
                if track_metrics:
                    metrics.comparisons += 1
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
                    if track_metrics:
                        metrics.swaps += 1

            if not swapped:
                break

        if track_metrics:
            metrics.time_taken = time.time() - start
            return arr, metrics
        return arr

    @staticmethod
    def selection_sort(arr, track_metrics=False):
        metrics = SortingMetrics() if track_metrics else None
        if track_metrics:
            metrics.algorithm_name = "Selection Sort"
            start = time.time()
            arr = copy.deepcopy(arr)

        n = len(arr)
        for i in range(n):
            if track_metrics:
                metrics.passes += 1
            min_idx = i
            for j in range(i + 1, n):
                if track_metrics:
                    metrics.comparisons += 1
                if arr[j] < arr[min_idx]:
                    min_idx = j

            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                if track_metrics:
                    metrics.swaps += 1

        if track_metrics:
            metrics.time_taken = time.time() - start
            return arr, metrics
        return arr

    @staticmethod
    def insertion_sort(arr, track_metrics=False):
        metrics = SortingMetrics() if track_metrics else None
        if track_metrics:
            metrics.algorithm_name = "Insertion Sort"
            start = time.time()
            arr = copy.deepcopy(arr)

        n = len(arr)
        for i in range(1, n):
            if track_metrics:
                metrics.passes += 1
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                if track_metrics:
                    metrics.comparisons += 1
                    metrics.swaps += 1
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key

        if track_metrics:
            metrics.time_taken = time.time() - start
            return arr, metrics
        return arr

    @staticmethod
    def merge_sort(arr, track_metrics=False):
        metrics = SortingMetrics() if track_metrics else None
        if track_metrics:
            metrics.algorithm_name = "Merge Sort"
            start = time.time()
            arr = copy.deepcopy(arr)
            result, metrics = SortingAlgorithms._merge_sort_recursive(arr, metrics)
            metrics.time_taken = time.time() - start
            return result, metrics
        else:
            return SortingAlgorithms._merge_sort_simple(arr.copy())

    @staticmethod
    def _merge_sort_recursive(arr, metrics):
        if len(arr) <= 1:
            return arr, metrics

        mid = len(arr) // 2
        left, metrics = SortingAlgorithms._merge_sort_recursive(arr[:mid], metrics)
        right, metrics = SortingAlgorithms._merge_sort_recursive(arr[mid:], metrics)

        return SortingAlgorithms._merge(left, right, metrics)

    @staticmethod
    def _merge(left, right, metrics):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if metrics:
                metrics.comparisons += 1
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
                if metrics:
                    metrics.swaps += 1   # Count as movement

        result.extend(left[i:])
        result.extend(right[j:])
        return result, metrics

    @staticmethod
    def quick_sort(arr, track_metrics=False):
        metrics = SortingMetrics() if track_metrics else None
        if track_metrics:
            metrics.algorithm_name = "Quick Sort"
            start = time.time()
            arr = copy.deepcopy(arr)
            result, metrics = SortingAlgorithms._quick_sort_recursive(arr, 0, len(arr)-1, metrics)
            metrics.time_taken = time.time() - start
            return result, metrics
        else:
            arr = arr.copy()
            SortingAlgorithms._quick_sort_simple(arr, 0, len(arr)-1)
            return arr

    # Quick Sort Helpers during implementation
    @staticmethod
    def _quick_sort_recursive(arr, low, high, metrics):
        if low < high:
            if metrics:
                metrics.passes += 1
            pi, metrics = SortingAlgorithms._partition(arr, low, high, metrics)
            SortingAlgorithms._quick_sort_recursive(arr, low, pi - 1, metrics)
            SortingAlgorithms._quick_sort_recursive(arr, pi + 1, high, metrics)
        return arr, metrics

    @staticmethod
    def _partition(arr, low, high, metrics):
        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            if metrics:
                metrics.comparisons += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                if metrics:
                    metrics.swaps += 1

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        if metrics:
            metrics.swaps += 1
        return i + 1, metrics

    @staticmethod
    def compare_algorithms(arr):
        """Compare all algorithms"""
        results = {}
        algos = ['bubble', 'selection', 'insertion', 'merge', 'quick']

        for algo in algos:
            _, metrics = SortingAlgorithms.sort_with_metrics(algo, arr)
            results[algo] = metrics.to_dict()

        return results