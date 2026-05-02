
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        
    def insert_at_beginning(self, data):
        new_node = Node(data)
        
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
            
        self.size += 1
        
    def insert_at_end(self, data):
        new_node = Node(data)
        
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
            
        self.size += 1
        
    def insert_at_position(self, data, position):
        if position < 0 or position > self.size:
            raise Exception("Invalid position")
            
        if position == 0:
            self.insert_at_beginning(data)
        elif position == self.size:
            self.insert_at_end(data)
        else:
            new_node = Node(data)
            
            # Navigate to the position
            if position < self.size // 2:
                # Start from head
                current = self.head
                for i in range(position):
                    current = current.next
            else:
                # Start from tail
                current = self.tail
                for i in range(self.size - position - 1):
                    current = current.prev
                    
            new_node.prev = current.prev
            new_node.next = current
            current.prev.next = new_node
            current.prev = new_node
            
            self.size += 1
            
    def delete_by_value(self, data):
        if self.is_empty():
            raise Exception("List is currently empty")
            
        current = self.head
        
        # Find the node
        while current and current.data != data:
            current = current.next
            
        if current:
            # Node found
            if current.prev:
                current.prev.next = current.next
            else:
                self.head = current.next
                
            if current.next:
                current.next.prev = current.prev
            else:
                self.tail = current.prev
                
            self.size -= 1
            return True
            
        return False
        
    def delete_at_position(self, position):
        if position < 0 or position >= self.size:
            raise Exception("This is an Invalid position")
            
        if position == 0:
            deleted_data = self.head.data
            self.head = self.head.next
            if self.head:
                self.head.prev = None
            else:
                self.tail = None
        elif position == self.size - 1:
            deleted_data = self.tail.data
            self.tail = self.tail.prev
            if self.tail:
                self.tail.next = None
            else:
                self.head = None
        else:
            # Navigate to the node
            if position < self.size // 2:
                current = self.head
                for i in range(position):
                    current = current.next
            else:
                current = self.tail
                for i in range(self.size - position - 1):
                    current = current.prev
                    
            deleted_data = current.data
            current.prev.next = current.next
            current.next.prev = current.prev
            
        self.size -= 1
        return deleted_data
        
    def search(self, data):
        current = self.head
        position = 0
        
        while current:
            if current.data == data:
                return position
            current = current.next
            position += 1
            
        return -1
        
    def is_empty(self):
        return self.head is None
        
    def get_size(self):
        return self.size
        
    def display(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
        
    def display_reverse(self):
        result = []
        current = self.tail
        while current:
            result.append(current.data)
            current = current.prev
        return result