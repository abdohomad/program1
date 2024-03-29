import networkx as nx
from geopy.distance import geodesic
import heapq
from geopy.exc import GeopyError
from itertools import combinations
import time
import psutil
from memory_profiler import profile


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

    def calculate_memory_usage(self):
        return psutil.Process().memory_info().rss / (1024**2)  # In MB

    def generic_blind_search(self, start, goal, search_type="bfs"):
        """
        Performs a generic search (either BFS or DFS) to find a path from start to goal.
        """

        # Open list (queue) to store nodes to be explored next
        # Initialize with starting node and empty path
        start_time = time.time()
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
                end_time = time.time()
                total_time = end_time - start_time
                memory_used = self.calculate_memory_usage()
                return path + [current], explored_list, total_time, memory_used
            # Explore unvisited neighbors
            for neighbor in set(self.graph.neighbors(current)) - explored_list:
                # Add the neighbor and updated path to the end of the open list
                open_list.append((neighbor, path + [current]))

        end_time = time.time()
        total_time = end_time - start_time
        memory_used = self.calculate_memory_usage()
        return None, explored_list, total_time, memory_used

    # @profile
    def breadth_first_search(self, start, goal):

        return self.generic_blind_search(start, goal, search_type="bfs")

    # @profile
    def depth_first_search(self, start, goal):

        return self.generic_blind_search(start, goal, search_type="dfs")

    def i_d_dfs_search(self, start, goal):
        start_time = time.time()
        depth_limit = 0
        explored_set = set()
        while True:
            result, explored = self.depth_limited_search(
                start, goal, depth_limit, explored_set)
            if result is not None:
                end_time = time.time()
                total_time = end_time - start_time
                memory_used = self.calculate_memory_usage()
                return result, explored, total_time, memory_used
            depth_limit += 1
            explored_set = set()  # Reset explored set for each depth iteration

    def depth_limited_search(self, start, goal, depth_limit, explored_set):

        if start == goal:
            return [start], explored_set

        if depth_limit == 0:
            return None, explored_set

        path = [start]
        explored_set.add(start)
        for neighbor in set(self.graph.neighbors(start)) - explored_set:
            result, explored = self.depth_limited_search(
                neighbor, goal, depth_limit - 1, explored_set.copy())
            if result is not None:
                return path + result, explored
        return None, explored_set

    def best_first_search(self, start, goal):
        start_time = time.time()
        open_list = dict()  # Dictionary instead of a list for faster lookups
        explored_list = set()  # Set to store explored nodes

        # Initial node with estimated cost and path
        if start is None or goal is None:
            raise ValueError("Start and goal nodes cannot be None")

        if start != goal:
            open_list[start] = (self.heuristics[start, goal], [start])
        elif start == goal:
            open_list[start] = (0, [start])

        while open_list:
            # Get node with lowest estimated cost
            try:
                time.sleep(0.001)
                current_cost, current_path = open_list[min(
                    open_list, key=open_list.get)]
            except KeyError:
                raise KeyError(
                    "Encountered a key that doesn't exist in open_list")

            current_city = current_path[-1]
            del open_list[current_city]
            explored_list.add(current_city)

            # Goal reached, return path
            if current_city == goal:
                end_time = time.time()
                total_time = end_time - start_time
                memory_used = self.calculate_memory_usage()
                return current_path + [goal], explored_list, total_time, memory_used

            # Explore neighbors
            for neighbor in set(self.graph.neighbors(current_city)):
                if neighbor not in explored_list:
                    if neighbor == goal:
                        end_time = time.time()
                        total_time = end_time - start_time
                        memory_used = self.calculate_memory_usage()
                        return current_path + [goal], explored_list, total_time, memory_used
                    try:
                        next_cost = self.graph[current_city][neighbor]["weight"]
                        heuristic = self.heuristics[neighbor, goal]
                    except KeyError:
                        raise KeyError(
                            "Encountered a key that doesn't exist in the graph"
                        )
                    total_cost = current_cost + next_cost + heuristic
                    open_list[neighbor] = (
                        total_cost, current_path + [neighbor])
        total_time = end_time - start_time
        memory_used = self.calculate_memory_usage()
        return None, explored_list, total_time, memory_used  # No path found

    def a_star_search(self, start_city, goal_city):
        start_time = time.time()
        open_list = dict()  # Dictionary instead of a list for faster lookups
        explored_list = set()  # Initialize explored list
        start_node = (0, start_city, [start_city])
        open_list[start_city] = start_node  # Add start node

        while open_list:
            try:
                current_cost, current_city, current_path = open_list[min(
                    open_list, key=open_list.get)]
            except (KeyError, ValueError):
                break  # open_list empty
            del open_list[current_city]
            explored_list.add(current_city)
            if current_city == goal_city:
                end_time = time.time()
                total_time = end_time - start_time
                memory_used = self.calculate_memory_usage()
                return current_path + [goal_city], explored_list, total_time, memory_used

            for neighbor in (set(self.graph.neighbors(current_city)) -
                             explored_list):
                if neighbor == goal_city:
                    end_time = time.time()
                    total_time = end_time - start_time
                    memory_used = self.calculate_memory_usage()
                    return current_path + [goal_city], explored_list, total_time, memory_used

                try:
                    next_cost = self.graph[current_city][neighbor]["weight"]
                    heuristic = self.heuristics[neighbor, goal_city]
                    total_cost = current_cost + next_cost + heuristic
                except (KeyError, TypeError):
                    continue  # Neighbor or edge not found

                if (neighbor not in open_list or
                        total_cost < open_list[neighbor][0]):
                    open_list[neighbor] = (total_cost, neighbor,
                                           current_path + [neighbor])

        end_time = time.time()
        total_time = end_time - start_time
        memory_used = self.calculate_memory_usage()
        return None, explored_list, total_time, memory_used  # No path found

    def compute_heuristics(self):
        """
        Compute heuristics for all pairs of cities based on their coordinates.
        """
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
