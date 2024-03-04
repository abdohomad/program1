# benchmark.py
from rich.console import Console
from rich.table import Table
import richbench
from Graph_manager import GraphManager
from Coordinates import Coordinates
from geopy.distance import geodesic

# Create an instance of GraphManager and add cities and connections
graph_manager = GraphManager()

coordinates_instance = Coordinates("src/coordinates.csv")
city_coordinates = coordinates_instance.extract_coordinates()

# Create an instance of the GraphManager
graph_manager = GraphManager()

# Add cities to the graph
for city_name in city_coordinates.keys():
    graph_manager.add_city(
        city_name,
        city_coordinates.get(city_name)
    )

# Add connections to the graph based on the adjacency information
with open("src/Adjacencies.txt", "r") as adj_file:
    for line in adj_file:
        cities = line.strip().split()
        for i in range(len(cities) - 1):
            source_city = cities[i]
            destination_city = cities[i + 1]

            # Fetch coordinates from the city_coordinates dictionary
            source_coords = city_coordinates.get(source_city)
            destination_coords = city_coordinates.get(destination_city)

            if source_coords and destination_coords:
                # Assuming the distance is the straight-line distance between the city coordinates
                distance = geodesic(source_coords, destination_coords).miles
                graph_manager.add_connection(
                    source_city, destination_city, distance)
            else:
                print(
                    f"Coordinates not found for {source_city} or {destination_city}")


# Define the benchmark functions
def breadth_first_search():
    graph_manager.breadth_first_search('StartCity', 'GoalCity')


def depth_first_search():
    graph_manager.depth_first_search('StartCity', 'GoalCity')


def best_first_search():
    graph_manager.best_first_search('StartCity', 'GoalCity')


def a_star_search():
    graph_manager.a_star_search('StartCity', 'GoalCity')


# Create a table for results
console = Console()
table = Table(title="Algorithm Benchmarks")
table.add_column("Algorithm")
table.add_column("Time (s)")

# Run benchmarks
benchmark = richbench()
table.add_row("Breadth-First Search", benchmark(breadth_first_search))
table.add_row("Depth-First Search", benchmark(depth_first_search))
table.add_row("Best-First Search", benchmark(best_first_search))
table.add_row("A* Search", benchmark(a_star_search))

# Print the results
console.print(table)
