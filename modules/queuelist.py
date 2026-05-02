class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class QueueLinked:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def is_empty(self):
        return self.front is None

    def enqueue(self, item):
        """Add an item to the rear of the queue"""
        new_node = Node(item)
        
        if self.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
            
        self.size += 1
        return True

    def dequeue(self):
        if self.is_empty():
            raise Exception("Queue Underflow! Cannot dequeue from an empty queue")
        
        dequeued_data = self.front.data
        self.front = self.front.next
        
        # If queue becomes empty, reset rear pointer
        if self.front is None:
            self.rear = None
            
        self.size -= 1
        return dequeued_data

    def peek(self):
        """Return the front item without removing it"""
        if self.is_empty():
            raise Exception("Queue is empty. Nothing to peek.")
        return self.front.data

    def get_size(self):
        return self.size

    def display(self):
        """Return list of elements from front to rear"""
        result = []
        current = self.front
        while current:
            result.append(current.data)
            current = current.next
        return result

    def clear(self):
        """Clear the entire queue"""
        self.front = None
        self.rear = None
        self.size = 0