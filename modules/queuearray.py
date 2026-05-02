
class QueueArray:
    
    def __init__(self, capacity=5):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = 0
        self.rear = -1
        self.size = 0
        
    def enqueue(self, item):

        if self.is_full():
            raise Exception("Queue Overflow! Cannot enqueue to full queue")
        
        # Circular increment
        self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = item
        self.size += 1
        
    def dequeue(self):

        if self.is_empty():
            raise Exception("Queue Underflow! Cannot dequeue from empty queue")
        
        item = self.queue[self.front]
        self.queue[self.front] = None  # Clear reference
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return item
        
    def get_front(self):

        if self.is_empty():
            raise Exception("Queue is empty")
        
        return self.queue[self.front]
        
    def is_empty(self):
        return self.size == 0
        
    def is_full(self):
        return self.size == self.capacity
        
    def get_size(self):
        return self.size
        
    def display(self):
        if self.is_empty():
            return []  
        result = []
        for i in range(self.size):
            index = (self.front + i) % self.capacity
            result.append(self.queue[index])
        return result