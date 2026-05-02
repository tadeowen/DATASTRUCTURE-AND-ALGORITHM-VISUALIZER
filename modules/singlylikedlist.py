class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def is_empty(self):
        return self.head is None

    def insert_at_beginning(self, data):
        """Insert element at the beginning of the list"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
        return True

    def insert_at_end(self, data):
        """Insert element at the end of the list"""
        new_node = Node(data)
        
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
            
        self.size += 1
        return True

    def insert_at_position(self, data, position):
        """Insert element at a specific position"""
        if position < 0 or position > self.size:
            raise Exception("Invalid position")

        if position == 0:
            return self.insert_at_beginning(data)
        elif position == self.size:
            return self.insert_at_end(data)

        new_node = Node(data)
        current = self.head
        for _ in range(position - 1):
            current = current.next

        new_node.next = current.next
        current.next = new_node
        self.size += 1
        return True

    def delete_by_value(self, data):
        """Delete first occurrence of a value"""
        if self.is_empty():
            raise Exception("List is currently empty")

        # Delete head node
        if self.head.data == data:
            self.head = self.head.next
            self.size -= 1
            return True

        current = self.head
        while current.next and current.next.data != data:
            current = current.next

        if current.next:
            current.next = current.next.next
            self.size -= 1
            return True

        return False  # Value not found

    def delete_at_position(self, position):
        """Delete node at given position and return deleted value"""
        if position < 0 or position >= self.size:
            raise Exception("Invalid position")

        if position == 0:
            deleted_data = self.head.data
            self.head = self.head.next
        else:
            current = self.head
            for _ in range(position - 1):
                current = current.next
            deleted_data = current.next.data
            current.next = current.next.next

        self.size -= 1
        return deleted_data

    def search(self, data):
        """Return index of first occurrence of data, or -1 if not found"""
        current = self.head
        position = 0
        while current:
            if current.data == data:
                return position
            current = current.next
            position += 1
        return -1

    def get_size(self):
        return self.size

    def display(self):
        """Return list of all elements for visualization"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def clear(self):
        """Clear the entire linked list"""
        self.head = None
        self.size = 0