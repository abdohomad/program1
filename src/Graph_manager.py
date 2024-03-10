import networkx as nx
from geopy.distance import geodesic
import heapq
from geopy.exc import GeopyError
from itertools import combinations


class GraphManager:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.heuristics = {}

    def add_city(self, city, coordinates):
        self.graph.add_node(city, coordinates=coordinates)

    def add_connection(self, source, destination, distance, one_way=False):
        self.graph.add_edge(source, destination, weight=distance)
        if not one_way:
            self.graph.add_edge(destination, source, weight=distance)

    def generic_blind_search(self, start, goal, search_type="bfs"):
        """
        Performs a generic search (either BFS or DFS) to find a path from start to goal.
        """

        # Open list (queue) to store nodes to be explored next
        # Initialize with starting node and empty path
        open_list = [(start, [])]
        explored_list = set()    # Closed list to store explored nodes

        while open_list:
            # Pop the current node and its path from the front of the open list (queue) or
            # Pop the current node and its path from the open list (stack).
            current, path = open_list.pop(
                0) if search_type == "bfs" else open_list.pop()
            # Add the current node to the closed list
            explored_list.add(current)

            if current == goal:
                # Path found, return the complete path from start to goal
                return path + [current], explored_list
            # Explore unvisited neighbors
            for neighbor in set(self.graph.neighbors(current)) - explored_list:
                # Add the neighbor and updated path to the end of the open list
                open_list.append((neighbor, path + [current]))

        return None, explored_list

    def breadth_first_search(self, start, goal):

        return self.generic_blind_search(start, goal, search_type="bfs")

    def depth_first_search(self, start, goal):

        return self.generic_blind_search(start, goal, search_type="dfs")

    def best_first_search(self, start, goal):

        open_list = []  # Priority queue for open nodes
        explored_list = []  # Set to store explored nodes

        # Initial node with estimated cost and path
        if start != goal:
            heapq.heappush(
                open_list, (self.heuristics[start, goal], start, [start]))
        elif start == goal:
            heapq.heappush(
                open_list, (0, start, [start]))

        while open_list:
            # Get node with lowest estimated cost
            current_cost, current_city, path = heapq.heappop(open_list)
            explored_list.append(current_city)

            # Goal reached, return path
            if current_city == goal:
                return path + [goal], explored_list

            # Explore neighbors
            for neighbor in set(self.graph.neighbors(current_city)):
                if neighbor not in explored_list:
                    if neighbor == goal:
                        return path + [goal], explored_list
                    # next_cost = self.graph[current_city][neighbor]["weight"]
                    heuristic = self.heuristics[neighbor, goal]
                    total_cost = heuristic
                    next_node = (total_cost,
                                 neighbor,
                                 path + [neighbor])
                    heapq.heappush(open_list, next_node)

        return None, explored_list  # No path found

    def a_star_search(self, start_city, goal_city):

        open_list = []  # Initialize open list
        explored_list = set()  # Initialize explored list
        start_node = (0, start_city, [start_city])
        heapq.heappush(open_list, start_node)  # Add start node
        while open_list:

            current_cost, current_city, current_path = heapq.heappop(open_list)
            explored_list.add(current_city)
            if current_city == goal_city:
                return current_path + [goal_city], explored_list

            for neighbor in set(self.graph.neighbors(current_city)) - explored_list:
                if neighbor == goal_city:
                    return current_path + [goal_city], explored_list

                next_cost = self.graph[current_city][neighbor]["weight"]
                heuristic = self.heuristics[neighbor, goal_city]
                total_cost = current_cost + next_cost + heuristic
                next_node = (total_cost, neighbor,
                             current_path + [neighbor])
                # Check for duplicates and update if necessary
                if neighbor not in explored_list:
                    heapq.heappush(open_list, next_node)

                # If neighbor is in open_list with a higher g_score, update it
                for i, (f_score, _, _) in enumerate(open_list):
                    if neighbor == _ and total_cost < f_score:
                        open_list[i] = next_node
                        break

        return None, explored_list  # No path found

    def compute_heuristics(self):
        for city1, city2 in combinations(self.graph.nodes, 2):
            distance = self.heuristic_cost_estimate(
                self.graph.nodes[city1]["coordinates"],
                self.graph.nodes[city2]["coordinates"]
            )
            self.heuristics[(city1, city2)] = distance
            self.heuristics[(city2, city1)] = distance

    def heuristic_cost_estimate(self, current_coords, goal_coords):
        try:
            distance = geodesic(current_coords, goal_coords).miles
            return distance
        except GeopyError as e:
            print(f"Error calculating heuristic: {e}")
            return 0

    def get_graph(self):
        return self.graph
