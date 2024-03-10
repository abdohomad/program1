import pandas as pd
from Graph_manager import GraphManager
from Coordinates import Coordinates
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import time


def load_coordinates(file_path):
    coordinates_instance = Coordinates(file_path)
    city_coordinates = coordinates_instance.extract_coordinates()
    return city_coordinates


def add_cities(graph_manager, city_coordinates):

    for city_name in city_coordinates.keys():
        graph_manager.add_city(city_name, city_coordinates.get(city_name))


def add_connections(graph_manager, city_coordinates, file_path):
    with open(file_path, "r") as adj_file:
        for line in adj_file:
            cities = line.strip().split()
            for i in range(len(cities) - 1):
                source_city = cities[i]
                destination_city = cities[i + 1]

                source_coords = city_coordinates.get(source_city)
                destination_coords = city_coordinates.get(destination_city)

                if source_coords and destination_coords:
                    distance = geodesic(
                        source_coords, destination_coords).miles
                    graph_manager.add_connection(
                        source_city, destination_city, distance)
                else:
                    print(
                        f"Coordinates not found for {source_city} or {destination_city}")


def get_user_choice(search_algorithms):
    print("\nSelect a search algorithm:")
    for code, algorithm in search_algorithms.items():
        print(f"{code}. {algorithm}")

    while True:
        choice = input("Enter your choice (1-4): ")
        if choice in search_algorithms:
            return choice
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


def calculate_distance(path, city_coordinates):
    total_distance = 0
    for i in range(len(path) - 1):
        current_city = path[i]
        next_city = path[i + 1]
        current_coords = city_coordinates.get(current_city)
        next_coords = city_coordinates.get(next_city)
        if current_coords and next_coords:
            distance = geodesic(current_coords, next_coords).miles
            total_distance += distance
    return total_distance


def main():
    coordinates_file = "src/coordinates.csv"
    adjacency_file = "src/Adjacencies.txt"

    # Load coordinates from the CSV file
    city_coordinates = load_coordinates(coordinates_file)

    # Create an instance of the GraphManager
    graph_manager = GraphManager()

    add_cities(graph_manager, city_coordinates)
    # Add cities to the graph and establish connections
    add_connections(graph_manager, city_coordinates, adjacency_file)

    start_city = input("Enter the starting city: ")
    goal_city = input("Enter the destination city: ")

    start_coords, goal_coords = city_coordinates.get(
        start_city), city_coordinates.get(goal_city)

    if not start_coords or not goal_coords:
        print(f"Coordinates not found for {start_city} or {goal_city}")
        return

    graph_manager.compute_heuristics()

    # Define search algorithms
    search_algorithms = {
        "1": "Breadth-First Search",
        "2": "Depth-First Search",
        "3": "Best-First Search",
        "4": "A* Search"
    }

    function1_choice = input("Enter the first function choice (1-4): ")
    function2_choice = input("Enter the second function choice (1-4): ")

    if function1_choice not in search_algorithms or function2_choice not in search_algorithms:
        print("Invalid function choices. Please enter numbers between 1 and 4.")
        return

    function1_algorithm = search_algorithms[function1_choice]
    function2_algorithm = search_algorithms[function2_choice]

    start_time = time.time()  # Start time measurement

    solution_path1, visited1 = execute_search_function(
        graph_manager, function1_choice, start_city, goal_city)

    elapsed_time1 = time.time() - start_time

    start_time = time.time()  # Reset start time for the second function

    solution_path2, visited2 = execute_search_function(
        graph_manager, function2_choice, start_city, goal_city)

    elapsed_time2 = time.time() - start_time

    # Display results as a table
    results_table = pd.DataFrame({
        "Algorithm": [function1_algorithm, function2_algorithm],
        "Visited Cities": [len(visited1) if visited1 else None, len(visited2) if visited2 else None],
        "Total Distance": [calculate_distance(solution_path1, city_coordinates) if solution_path1 else None,
                           calculate_distance(solution_path2, city_coordinates) if solution_path2 else None],
        "Search Time": ["{:.9f}".format(elapsed_time1), "{:.9f}".format(elapsed_time2)]
    })

    print("\nSearch Results:")
    print(results_table)
    print('////////////////')
    print(visited1)
    print("/////")
    print(visited2)


def execute_search_function(graph_manager, choice, start_city, goal_city):
    if choice == "1":
        return graph_manager.breadth_first_search(start_city, goal_city)
    elif choice == "2":
        return graph_manager.depth_first_search(start_city, goal_city)
    elif choice == "3":
        return graph_manager.best_first_search(start_city, goal_city)
    elif choice == "4":
        return graph_manager.a_star_search(start_city, goal_city)
    else:
        return None, None


if __name__ == "__main__":
    main()
