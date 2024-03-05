import networkx as nx
from geopy.distance import geodesic
import heapq
from geopy.exc import GeopyError
import matplotlib.pyplot as plt


class GraphManager:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.heuristics = {}
        self.steps = []

    def add_city(self, city, coordinates):
        self.graph.add_node(city, coordinates=coordinates)

    def add_connection(self, source, destination, distance, one_way=False):
        self.graph.add_edge(source, destination, weight=distance)
        if not one_way:
            self.graph.add_edge(destination, source, weight=distance)

    def breadth_first_search(self, start, goal):

        # Open list (queue) to store nodes to be explored next
        # Initialize with starting node and empty path
        open_list = [(start, [])]

        # Closed list to store explored nodes
        closed_list = set()

        while open_list:
            # Pop the current node and its path from the front of the open list (queue)
            current, path = open_list.pop(0)

            # Add the current node to the closed list
            closed_list.add(current)

            # Check if the goal node is reached
            if current == goal:
                # Path found, return the complete path from start to goal
                return path + [current]

            # Explore unvisited neighbors
            for next_city in set(self.graph.neighbors(current)) - closed_list:
                # Add the neighbor and updated path to the end of the open list
                open_list.append((next_city, path + [current]))

        # No path found, return None
        return None

    def depth_first_search(self, start, goal):

        # Open list (stack) to store nodes to be explored next.
        # Initialize with starting node and empty path.
        open_list = [(start, [])]

        # Closed list to store explored nodes.
        closed_list = set()

        while open_list:
            # Pop the current node and its path from the open list (stack).
            current, path = open_list.pop()

            # Add the current node to the closed list.
            closed_list.add(current)

            # Check if the goal node is reached.
            if current == goal:
                # Path found, return the complete path from start to goal.
                return path + [current]

            # Explore unvisited neighbors
            for next_city in set(self.graph.neighbors(current)) - closed_list:
                # Add the neighbor and updated path to the open list.
                open_list.append((next_city, path + [current]))

        # No path found, return None
        return None

    def best_first_search(self, start, goal):

        open_list = []  # Priority queue for open nodes
        closed_list = set()  # Set to store explored nodes

        # Initial node with estimated cost and path
        heapq.heappush(open_list, (0, start, [start]))

        while open_list:
            # Get node with lowest estimated cost
            current_cost, current_node, path = heapq.heappop(open_list)
            closed_list.add(current_node)

            # Goal reached, return path
            if current_node == goal:
                return path + [goal]

            # Explore neighbors
            for next_city in set(self.graph.neighbors(current_node)) - closed_list:
                next_cost = self.graph[current_node][next_city]["weight"]
                heuristic = self.heuristic_cost_estimate(
                    self.graph.nodes[next_city]["coordinates"],
                    self.graph.nodes[goal]["coordinates"])
                total_cost = current_cost + next_cost + heuristic
                next_node = (total_cost,
                             next_city,
                             path + [next_city])

            # Check for existing node in open list with higher cost
            for i, (existing_cost, _, _) in enumerate(open_list):
                if next_city == _ and next_cost < existing_cost:
                    del open_list[i]  # Remove existing node
                break

            # Add neighbor to open list with updated cost and path
            heapq.heappush(open_list, (next_cost,
                           next_city, path + [next_city]))

        return None  # No path found

    def a_star_search(self, start_city, goal_city):

        open_list = []  # Initialize open list
        closed_list = set()  # Initialize closed list

        start_node = (0, start_city, [start_city])  # (f_score, city, path)
        heapq.heappush(open_list, start_node)  # Add start node to open list

        while open_list:
            current_cost, current_city, current_path = heapq.heappop(open_list)
            closed_list.add(current_city)  # Add current node to closed list

            if current_city == goal_city:
                return current_path  # Found the goal, return the path

            for next_city in set(self.graph.neighbors(current_city)) - closed_list:
                next_cost = self.graph[current_city][next_city]["weight"]
                heuristic = self.heuristic_cost_estimate(
                    self.graph.nodes[next_city]["coordinates"],
                    self.graph.nodes[goal_city]["coordinates"])
                total_cost = current_cost + next_cost + heuristic
                next_node = (total_cost, next_city, current_path + [next_city])
                # Check for duplicates and update if necessary
                if next_city not in closed_list:
                    heapq.heappush(open_list, next_node)

                # If next_city is in open_list with a higher g_score, update it
                for i, (f_score, _, _) in enumerate(open_list):
                    if next_city == _ and total_cost < f_score:
                        open_list[i] = next_node
                        break
        return None  # No path found

    def heuristic_cost_estimate(self, current_coords, goal_coords):
        try:
            distance = geodesic(current_coords, goal_coords).miles
            return distance
        except GeopyError as e:
            print(f"Error calculating heuristic: {e}")
            return 0

    def compute_heuristics(self):
        for city1 in self.graph.nodes:
            for city2 in self.graph.nodes:
                if city1 != city2:
                    distance = self.heuristic_cost_estimate(
                        self.graph.nodes[city1]["coordinates"],
                        self.graph.nodes[city2]["coordinates"]
                    )
                    self.heuristics[(city1, city2)] = distance

    def get_graph(self):
        return self.graph
