class SearchingAlgorithms:

    @staticmethod
    def linear_search(arr, target):
        """
        Linear Search - Checks every element sequentially
        Time Complexity: O(n)
        """
        for i, element in enumerate(arr):
            if element == target:
                return i
        return -1

    @staticmethod
    def binary_search(arr, target):
        """
        Iterative Binary Search 
        Requires a sorted array
        Time Complexity: O(log n)
        """
        left = 0
        right = len(arr) - 1
        
        while left <= right:
            mid = left + (right - left) // 2
            
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
                
        return -1

    @staticmethod
    def binary_search_recursive(arr, target, left=None, right=None):
        if left is None:
            left = 0
        if right is None:
            right = len(arr) - 1
            
        if left > right:
            return -1
            
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            return SearchingAlgorithms.binary_search_recursive(arr, target, mid + 1, right)
        else:
            return SearchingAlgorithms.binary_search_recursive(arr, target, left, mid - 1)

    @staticmethod
    def linear_search_steps(arr, target):
        steps = []
        for i, element in enumerate(arr):
            steps.append({
                'index': i,
                'value': element,
                'found': element == target
            })
            if element == target:
                return i, steps
        return -1, steps

    @staticmethod
    def binary_search_steps(arr, target):
        """Returns steps for binary search visualization"""
        steps = []
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = left + (right - left) // 2
            steps.append({
                'left': left,
                'right': right,
                'mid': mid,
                'mid_value': arr[mid]
            })
            
            if arr[mid] == target:
                return mid, steps
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
                
        return -1, steps