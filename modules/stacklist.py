class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class StackLinked:
    def __init__(self):
        self.top = None
        self.size = 0

    def is_empty(self):
        return self.top is None

    def push(self, item):
        """Push an item onto the stack"""
        new_node = Node(item)
        new_node.next = self.top
        self.top = new_node
        self.size += 1
        return True

    def pop(self):
        if self.is_empty():
            raise Exception("Stack Underflow! Cannot pop from an empty stack")
        
        popped_data = self.top.data
        self.top = self.top.next
        self.size -= 1
        return popped_data

    def peek(self):
        if self.is_empty():
            raise Exception("Stack is empty. Nothing to peek.")
        return self.top.data

    def get_size(self):
        return self.size

    def display(self):
        result = []
        current = self.top
        while current:
            result.append(current.data)
            current = current.next
        return result

    def clear(self):
        """Optional: Clear the entire stack"""
        self.top = None
        self.size = 0