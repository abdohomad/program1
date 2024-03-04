import networkx as nx
from geopy.distance import geodesic
import heapq
from geopy.exc import GeopyError


class GraphManager:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.heuristics = {}

    def add_city(self, city, coordinates):
        """Add a city with its coordinates to the graph."""
        self.graph.add_node(city, coordinates=coordinates)

    def add_connection(self, source, destination, distance, one_way=False):
        """Add a connection between two cities with an optional one-way flag."""
        self.graph.add_edge(source, destination, weight=distance)
        if not one_way:
            self.graph.add_edge(destination, source, weight=distance)

    def breadth_first_search(self, start, goal):
        """Perform breadth-first search to find a path from start to goal."""
        queue = [(start, [start])]
        while queue:
            current, path = queue.pop(0)
            for next_city in set(self.graph.neighbors(current)) - set(path):
                if next_city == goal:
                    return path + [next_city]
                else:
                    queue.append((next_city, path + [next_city]))
        return None

    def depth_first_search(self, start, goal):
        """Perform depth-first search to find a path from start to goal."""
        stack = [(start, [start])]
        while stack:
            current, path = stack.pop()
            for next_city in set(self.graph.neighbors(current)) - set(path):
                if next_city == goal:
                    return path + [next_city]
                else:
                    stack.append((next_city, path + [next_city]))
        return None

    def best_first_search(self, start, goal):
        """Perform best-first search to find a path from start to goal."""
        queue = [(0, start, [start])]
        while queue:
            cost, current, path = heapq.heappop(queue)
            for next_city in set(self.graph.neighbors(current)) - set(path):
                if next_city == goal:
                    return path + [next_city]
                else:
                    next_cost = self.graph[current][next_city]["weight"]
                    heapq.heappush(
                        queue, (next_cost, next_city, path + [next_city]))
        return None

    def a_star_search(self, start_city, goal_city):
        """Perform A* search to find a path from start to goal."""
        queue = [(0, start_city, [start_city])]
        while queue:
            cost, current, path = heapq.heappop(queue)
            for next_city in set(self.graph.neighbors(current)) - set(path):
                if next_city == goal_city:
                    return path + [next_city]
                else:
                    next_cost = self.graph[current][next_city]["weight"]
                    heuristic = self.heuristics[(current, next_city)]
                    total_cost = cost + next_cost + heuristic
                    heapq.heappush(
                        queue, (total_cost, next_city, path + [next_city]))

    def heuristic_cost_estimate(self, current_coords, goal_coords):
        """Estimate the cost (heuristic) between two city coordinates."""
        try:
            distance = geodesic(current_coords, goal_coords).miles
            return distance
        except GeopyError as e:
            print(f"Error calculating heuristic: {e}")
            return 0

    def compute_heuristics(self):
        """Calculate and store heuristic values for all city pairs in self.heuristics."""
        for city1 in self.graph.nodes:
            for city2 in self.graph.nodes:
                if city1 != city2:
                    distance = self.heuristic_cost_estimate(
                        self.graph.nodes[city1]["coordinates"],
                        self.graph.nodes[city2]["coordinates"]
                    )
                    self.heuristics[(city1, city2)] = distance

    def get_graph(self):
        """Return the underlying graph."""
        return self.graph
