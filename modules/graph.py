from collections import defaultdict, deque
import heapq


class Graph:
    def __init__(self, directed=False):
        self.graph = defaultdict(list)   
        self.directed = directed

    def add_vertex(self, v):
        if v not in self.graph:
            self.graph[v] = []

    def remove_vertex(self, v):
        if v not in self.graph:
            return
        del self.graph[v]
        for node in self.graph:
            self.graph[node] = [(n, w) for n, w in self.graph[node] if n != v]

    def get_vertices(self):
        return list(self.graph.keys())

    def vertex_exists(self, v):
        return v in self.graph

    def add_edge(self, u, v, weight=1):
        self.add_vertex(u)
        self.add_vertex(v)
        if not any(n == v for n, _ in self.graph[u]):
            self.graph[u].append((v, weight))
        if not self.directed:
            if not any(n == u for n, _ in self.graph[v]):
                self.graph[v].append((u, weight))

    def remove_edge(self, u, v):
        self.graph[u] = [(n, w) for n, w in self.graph[u] if n != v]
        if not self.directed:
            self.graph[v] = [(n, w) for n, w in self.graph[v] if n != u]

    def get_edges(self):
        edges = []
        seen = set()
        for u in self.graph:
            for v, w in self.graph[u]:
                key = (min(u, v), max(u, v)) if not self.directed else (u, v)
                if key not in seen:
                    seen.add(key)
                    edges.append((u, v, w))
        return edges

    def edge_exists(self, u, v):
        """Return True if an edge from u to v exists."""
        return any(n == v for n, _ in self.graph.get(u, []))

    def get_edge_weight(self, u, v):
        """Return the weight of edge (u, v), or None if it does not exist."""
        for n, w in self.graph.get(u, []):
            if n == v:
                return w
        return None

    def get_neighbors(self, v):
        """Return neighbor vertices of v (without weights)."""
        return [n for n, _ in self.graph.get(v, [])]

    def get_neighbors_weighted(self, v):
        """Return (neighbor, weight) pairs for v."""
        return list(self.graph.get(v, []))

    def is_adjacent(self, u, v):
        """Return True if there is an edge from u to v."""
        return self.edge_exists(u, v)

    def degree(self, v):
        """
        Return the degree of v.
        For directed graphs returns (in_degree, out_degree).
        For undirected graphs returns the single degree value.
        """
        out_deg = len(self.graph.get(v, []))
        if not self.directed:
            return out_deg
        in_deg = sum(1 for u in self.graph for n, _ in self.graph[u] if n == v)
        return {"in": in_deg, "out": out_deg}
    def bfs(self, start):
        """Breadth-First Search from start. Returns visited order."""
        if start not in self.graph:
            return []
        visited, queue, result = set(), deque([start]), []
        visited.add(start)
        while queue:
            node = queue.popleft()
            result.append(node)
            for neighbor in self.get_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return result

    def dfs(self, start):
        if start not in self.graph:
            return []
        visited, stack, result = set(), [start], []
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                result.append(node)
                stack.extend(reversed(self.get_neighbors(node)))
        return result

    def find_path(self, start, end):
        if start not in self.graph or end not in self.graph:
            return None
        visited, queue = set(), deque([(start, [start])])
        while queue:
            node, path = queue.popleft()
            if node == end:
                return path
            if node not in visited:
                visited.add(node)
                for neighbor in self.get_neighbors(node):
                    queue.append((neighbor, path + [neighbor]))
        return None

    def find_all_paths(self, start, end, path=None):
        """Find ALL simple paths from start to end. Returns list of paths."""
        if path is None:
            path = []
        path = path + [start]
        if start == end:
            return [path]
        if start not in self.graph:
            return []
        paths = []
        for neighbor in self.get_neighbors(start):
            if neighbor not in path:
                new_paths = self.find_all_paths(neighbor, end, path)
                paths.extend(new_paths)
        return paths

    def shortest_path_unweighted(self, start, end):
        path = self.find_path(start, end)
        if path is None:
            return None, -1
        return path, len(path) - 1

    def dijkstra(self, start):
        if start not in self.graph:
            return {}
        dist = {v: float("inf") for v in self.graph}
        dist[start] = 0
        prev = {v: None for v in self.graph}
        heap = [(0, start)]

        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for v, w in self.graph[u]:
                alt = dist[u] + w
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    heapq.heappush(heap, (alt, v))

        # Reconstruct paths
        result = {}
        for v in self.graph:
            if dist[v] == float("inf"):
                result[v] = {"distance": None, "path": None}
            else:
                path, cur = [], v
                while cur is not None:
                    path.append(cur)
                    cur = prev[cur]
                result[v] = {"distance": dist[v], "path": list(reversed(path))}
        return result

    def shortest_weighted_path(self, start, end):
        info = self.dijkstra(start)
        if end not in info or info[end]["path"] is None:
            return None, None
        return info[end]["path"], info[end]["distance"]
    def has_cycle(self):
        return self._has_cycle_directed() if self.directed else self._has_cycle_undirected()

    def _has_cycle_undirected(self):
        visited = set()

        def dfs(v, parent):
            visited.add(v)
            for neighbor in self.get_neighbors(v):
                if neighbor not in visited:
                    if dfs(neighbor, v):
                        return True
                elif neighbor != parent:
                    return True
            return False

        for v in self.graph:
            if v not in visited:
                if dfs(v, None):
                    return True
        return False

    def _has_cycle_directed(self):
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {v: WHITE for v in self.graph}

        def dfs(v):
            color[v] = GRAY
            for neighbor in self.get_neighbors(v):
                if color[neighbor] == GRAY:
                    return True
                if color[neighbor] == WHITE and dfs(neighbor):
                    return True
            color[v] = BLACK
            return False

        return any(dfs(v) for v in self.graph if color[v] == 0)

    def topological_sort(self):
        if not self.directed:
            return None

        in_degree = {v: 0 for v in self.graph}
        for u in self.graph:
            for v, _ in self.graph[u]:
                in_degree[v] += 1

        queue = deque(v for v in in_degree if in_degree[v] == 0)
        order = []

        while queue:
            u = queue.popleft()
            order.append(u)
            for v, _ in self.graph[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        return order if len(order) == len(self.graph) else None  # None = cycle detected

    def connected_components(self):
        visited = set()
        components = []

        for v in self.graph:
            if v not in visited:
                component = set(self.bfs(v))
                visited |= component
                components.append(component)

        return components

    def is_connected(self):
        """Return True if the graph is (weakly) connected."""
        if not self.graph:
            return True
        return len(self.connected_components()) == 1


    def minimum_spanning_tree(self):
        """
        Kruskal's MST algorithm.
        Returns list of (u, v, weight) edges in the MST,
        or None if the graph is directed or not connected.
        """
        if self.directed:
            return None

        parent = {v: v for v in self.graph}
        rank = {v: 0 for v in self.graph}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(x, y):
            rx, ry = find(x), find(y)
            if rx == ry:
                return False
            if rank[rx] < rank[ry]:
                rx, ry = ry, rx
            parent[ry] = rx
            if rank[rx] == rank[ry]:
                rank[rx] += 1
            return True

        edges = sorted(self.get_edges(), key=lambda e: e[2])
        mst = []
        for u, v, w in edges:
            if union(u, v):
                mst.append((u, v, w))

        return mst

    def to_dict(self):
        """
        Serialize the graph to a plain dict suitable for json.dumps / Flask jsonify.
        """
        return {
            "directed": self.directed,
            "vertices": self.get_vertices(),
            "edges": [
                {"from": u, "to": v, "weight": w} for u, v, w in self.get_edges()
            ],
        }

    @classmethod
    def from_dict(cls, data):
        """
        Deserialize a graph from the dict produced by to_dict().
        Usage:  g = Graph.from_dict(request.get_json())
        """
        g = cls(directed=data.get("directed", False))
        for v in data.get("vertices", []):
            g.add_vertex(v)
        for edge in data.get("edges", []):
            g.add_edge(edge["from"], edge["to"], edge.get("weight", 1))
        return g
    def display(self):
        """Return the adjacency list as a formatted string (Flask-safe)."""
        lines = []
        for node in self.graph:
            neighbors = ", ".join(f"{n}(w={w})" for n, w in self.graph[node])
            lines.append(f"{node} -> [{neighbors}]")
        return "\n".join(lines)