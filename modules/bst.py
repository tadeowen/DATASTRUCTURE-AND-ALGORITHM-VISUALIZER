class BSTNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, data):
        if not isinstance(data, (int, float)):
            raise ValueError("BST only supports numbers")
            
        self.root = self._insert_recursive(self.root, data)
        self.size += 1
        return True

    def _insert_recursive(self, node, data):
        if node is None:
            return BSTNode(data)

        if data < node.data:
            node.left = self._insert_recursive(node.left, data)
        elif data > node.data:
            node.right = self._insert_recursive(node.right, data)
        # Ignore duplicates
        return node

    def inorder_traversal(self):
        """Return sorted list (In-order traversal)"""
        result = []
        self._inorder_helper(self.root, result)
        return result

    def _inorder_helper(self, node, result):
        if node:
            self._inorder_helper(node.left, result)
            result.append(node.data)
            self._inorder_helper(node.right, result)

    def search(self, data):
        """Search for a value in BST"""
        return self._search_recursive(self.root, data)

    def _search_recursive(self, node, data):
        if node is None or node.data == data:
            return node is not None
        if data < node.data:
            return self._search_recursive(node.left, data)
        return self._search_recursive(node.right, data)

    def get_size(self):
        return self.size

    def is_empty(self):
        return self.root is None
    def get_tree_structure(self):
        def build_tree(node):
            if not node:
                return None
            return {
                "value": node.data,
                "left": build_tree(node.left),
                "right": build_tree(node.right)
            }
        
        return build_tree(self.root)

    def clear(self):
        self.root = None
        self.size = 0