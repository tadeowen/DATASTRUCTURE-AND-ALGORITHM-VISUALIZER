import time

class TowerOfHanoi:
    def __init__(self):
        self.moves = []
        self.reset()

    def reset(self):
        self.moves = []
        self.start_time = None
        self.end_time = None

    def solve(self, n_disks, source=0, target=2, auxiliary=1):
        self.reset()
        self.start_time = time.time()
        
        self._solve_recursive(n_disks, source, target, auxiliary)
        
        self.end_time = time.time()
        return self.moves

    def _solve_recursive(self, n, source, target, auxiliary):
        if n == 1:
            self.moves.append((source, target))
            return
        
        self._solve_recursive(n-1, source, auxiliary, target)
        self.moves.append((source, target))
        self._solve_recursive(n-1, auxiliary, target, source)

    def get_execution_time(self):
        if self.end_time and self.start_time:
            return round((self.end_time - self.start_time) * 1000, 3)
        return 0

    def get_total_moves(self):
        return len(self.moves)

    def get_moves(self):
        return self.moves

    @staticmethod
    def tower_labels():
        return ['A', 'B', 'C']