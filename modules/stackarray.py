class StackArray:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.stack = []      
        self.top = -1        

    def is_empty(self):
        return self.top == -1

    def is_full(self):
        return self.top == self.capacity - 1

    def push(self, item):
        if self.is_full():
            raise Exception("Stack Overflow! Cannot push to a full stack")
        
        self.stack.append(item)
        self.top += 1
        return True

    def pop(self):
        if self.is_empty():
            raise Exception("Stack Underflow! Cannot pop from an empty stack")
        
        item = self.stack.pop()
        self.top -= 1
        return item

    def peek(self):
        if self.is_empty():
            raise Exception("Stack is empty. Nothing to peek.")
        return self.stack[self.top]

    def get_size(self):
        return self.top + 1

    def display(self):
        return self.stack.copy()

    def clear(self):
        self.stack.clear()
        self.top = -1