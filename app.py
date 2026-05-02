from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import time

# Import all Data Structures
from modules.stackarray import StackArray
from modules.stacklist import StackLinked
from modules.queuearray import QueueArray
from modules.queuelist import QueueLinked
from modules.singlylikedlist import SinglyLinkedList
from modules.Linkedlist import DoublyLinkedList

# Import Algorithms
from modules.sorting import SortingAlgorithms
from modules.searching import SearchingAlgorithms

# NEW: Binary Search Tree
from modules.bst import BinarySearchTree
from modules.Tower import TowerOfHanoi
from modules.memory import MemoryTracker
from modules.graph import Graph
from modules.hashtable import HashTable
from modules.heap_and_search import heap_bp
app = Flask(__name__)
CORS(app)

# ====================== INSTANCES ======================
instances = {
    'stack_array': StackArray(),
    'stack_linked': StackLinked(),
    'queue_array': QueueArray(),
    'queue_linked': QueueLinked(),
    'singly_linked_list': SinglyLinkedList(),
    'doubly_linked_list': DoublyLinkedList(),
    'bst': BinarySearchTree(),  
    'hanoi': TowerOfHanoi(),   
    'hash_table': HashTable(size=10, hash_method="division")     
}
current_graph = Graph(directed=False)


# Add this new route
@app.route('/api/ds/<structure>/memory', methods=['GET'])
def get_memory_usage(structure):
    try:
        ds = instances[structure]
        memory_info = MemoryTracker.get_ds_memory_usage(ds)
        return jsonify({'success': True, 'memory': memory_info})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ====================== HANOI ROUTES ======================
@app.route('/api/hanoi/solve', methods=['POST'])
def solve_hanoi():
    try:
        n = int(request.json.get('disks', 4))
        if n < 1 or n > 8:
            return jsonify({'success': False, 'error': 'Disks must be between 1 and 8'}), 400

        hanoi = instances['hanoi']
        moves = hanoi.solve(n)
        
        return jsonify({
            'success': True,
            'moves': moves,
            'total_moves': len(moves),
            'execution_time': hanoi.get_execution_time(),
            'disks': n
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ====================== DATA STRUCTURES ROUTES ======================
@app.route('/api/ds/<structure>/push', methods=['POST'])
def push(structure):
    try:
        value = request.json.get('value')
        ds = instances[structure]

        if 'stack' in structure:
            ds.push(value)
        elif 'queue' in structure:
            ds.enqueue(value)
        else:  # Linked Lists
            ds.insert_at_beginning(value)

        return jsonify({'success': True, 'data': ds.display()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/ds/<structure>/pop', methods=['POST'])
def pop(structure):
    try:
        ds = instances[structure]
        value = ds.pop()
        return jsonify({'success': True, 'data': ds.display()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
@app.route('/api/ds/<structure>/peek', methods=['POST'])
def peek(structure):
    try:
        ds = instances[structure]
        value = ds.peek()
        return jsonify({'success': True, 'data': ds.display()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/ds/<structure>/enqueue', methods=['POST'])
def enqueue(structure):
    try:
        value = request.json.get('value')
        ds = instances[structure]
        ds.enqueue(value)
        return jsonify({'success': True, 'data': ds.display()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/ds/<structure>/dequeue', methods=['POST'])
def dequeue(structure):
    try:
        ds = instances[structure]
        value = ds.dequeue()
        return jsonify({'success': True, 'data': ds.display()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/ds/<structure>/insert_end', methods=['POST'])
def insert_end(structure):
    try:
        value = request.json.get('value')
        ds = instances[structure]
        ds.insert_at_end(value)
        return jsonify({'success': True, 'data': ds.display()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/ds/<structure>/delete', methods=['POST'])
def delete_value(structure):
    try:
        value = request.json.get('value')
        ds = instances[structure]
        ds.delete_by_value(value)
        return jsonify({'success': True, 'data': ds.display()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/ds/<structure>/display', methods=['GET'])
def display_structure(structure):
    try:
        ds = instances[structure]
        return jsonify({'success': True, 'data': ds.display()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ====================== BST ROUTES ======================
@app.route('/api/bst/insert', methods=['POST'])
def bst_insert():
    try:
        value = request.json.get('value')
        bst = instances['bst']
        start = time.time()
        bst.insert(value)
        end = time.time()
        
        return jsonify({
            'success': True,
            'data': bst.inorder_traversal(),
            'time_taken': round((end - start) * 1000, 3)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/bst/reset', methods=['POST'])
def bst_reset():
    instances['bst'] = BinarySearchTree()
    return jsonify({'success': True, 'data': []})
# ====================== ADDITIONAL LINKED LIST ROUTES ======================

@app.route('/api/ds/<structure>/insert_position', methods=['POST'])
def insert_at_position(structure):
    try:
        data = request.json
        value = data.get('value')
        position = data.get('position')
        
        ds = instances[structure]
        ds.insert_at_position(value, position)
        
        return jsonify({
            'success': True,
            'message': f'Inserted {value} at position {position}',
            'data': ds.display()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/ds/<structure>/delete_at_position', methods=['POST'])
def delete_at_position(structure):
    try:
        position = request.json.get('position')
        ds = instances[structure]
        
        deleted = ds.delete_at_position(position)
        
        return jsonify({
            'success': True,
            'message': f'Deleted {deleted} from position {position}',
            'data': ds.display()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/ds/<structure>/search', methods=['POST'])
def search_in_ds(structure):
    try:
        value = request.json.get('value')
        ds = instances[structure]
        
        if hasattr(ds, 'search'):
            index = ds.search(value)
            return jsonify({
                'success': True,
                'found': index != -1,
                'index': index,
                'data': ds.display()
            })
        else:
            return jsonify({'success': False, 'error': 'Search not supported'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ====================== ALGORITHMS ======================
@app.route('/api/algorithms/sort_with_metrics', methods=['POST'])
def sort_with_metrics():
    try:
        data = request.json
        algorithm = data.get('algorithm')
        arr = data.get('data', [])
        
        sorting = SortingAlgorithms()
        result, metrics = sorting.sort_with_metrics(algorithm, arr)
        
        return jsonify({
            'success': True,
            'sorted': result,
            'metrics': metrics.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/algorithms/search', methods=['POST'])
def search():
    try:
        data = request.json
        algorithm = data.get('algorithm')
        arr = data.get('data', [])
        target = data.get('target')
        
        searching = SearchingAlgorithms()
        
        if algorithm == 'linear':
            index = searching.linear_search(arr, target)
        else:
            sorted_arr = sorted(arr)
            index = searching.binary_search(sorted_arr, target)
        
        return jsonify({
            'success': True,
            'found': index != -1,
            'index': index
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
# ====================== GRAPH ROUTES ======================
@app.route('/api/graph/create', methods=['POST'])
def create_graph():
    global current_graph
    directed = request.json.get('directed', False)
    current_graph = Graph(directed=directed)
    return jsonify({'success': True, 'message': f"New {'Directed' if directed else 'Undirected'} Graph Created"})

@app.route('/api/graph/add_edge', methods=['POST'])
def add_edge():
    data = request.json
    current_graph.add_edge(data['from'], data['to'], data.get('weight', 1))
    return jsonify({'success': True, 'graph': current_graph.to_dict()})

@app.route('/api/graph/bfs', methods=['POST'])
def graph_bfs():
    start = request.json.get('start')
    result = current_graph.bfs(start)
    return jsonify({'success': True, 'result': result})

@app.route('/api/graph/dfs', methods=['POST'])
def graph_dfs():
    start = request.json.get('start')
    result = current_graph.dfs(start)
    return jsonify({'success': True, 'result': result})

@app.route('/api/graph/shortest_path', methods=['POST'])
def shortest_path():
    start = request.json.get('start')
    end = request.json.get('end')
    path, weight = current_graph.shortest_weighted_path(start, end)
    return jsonify({'success': True, 'path': path, 'weight': weight})

@app.route('/api/graph/display', methods=['GET'])
def display_graph():
    return jsonify({
        'success': True,
        'graph': current_graph.to_dict(),
        'display': current_graph.display()
    })
# ====================== HASH TABLE ROUTES ======================
@app.route('/api/ds/hash_table/insert', methods=['POST'])
def hash_insert():
    try:
        key = request.json.get('key')
        value = request.json.get('value')
        method = request.json.get('hash_method', 'division')

        # Update hash method if changed
        ht = instances['hash_table']
        if ht.hash_method != method:
            instances['hash_table'] = HashTable(size=10, hash_method=method)
            ht = instances['hash_table']

        ht.insert(key, value)
        return jsonify({
            'success': True,
            'data': ht.display(),
            'hash_method': ht.hash_method,
            'load_factor': ht.load_factor()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/ds/hash_table/get', methods=['POST'])
def hash_get():
    try:
        key = request.json.get('key')
        ht = instances['hash_table']
        value = ht.get(key)
        return jsonify({
            'success': True,
            'value': value,
            'data': ht.display()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/ds/hash_table/delete', methods=['POST'])
def hash_delete():
    try:
        key = request.json.get('key')
        ht = instances['hash_table']
        success = ht.delete(key)
        return jsonify({
            'success': success,
            'data': ht.display(),
            'message': f"Key '{key}' deleted" if success else f"Key '{key}' not found"
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/ds/hash_table/display', methods=['GET'])
def hash_display():
    try:
        ht = instances['hash_table']
        return jsonify({
            'success': True,
            'data': ht.display(),
            'hash_method': ht.hash_method,
            'load_factor': ht.load_factor(),
            'size': ht.size,
            'count': ht.get_size()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ====================== MAIN ROUTE ======================
@app.route('/')
def index():
    return render_template('index.html')

# Register the heap & search blueprint
app.register_blueprint(heap_bp)
if __name__ == '__main__':
    app.run(debug=True)