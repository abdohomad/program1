from Graph_manager import GraphManager
from Coordinates import Coordinates
from geopy.distance import geodesic
import timeit


def load_coordinates(file_path):
    coordinates_instance = Coordinates(file_path)
    city_coordinates = coordinates_instance.extract_coordinates()
    return city_coordinates


def add_cities(graph_manager, city_coordinates):

    for city_name in city_coordinates.keys():
        graph_manager.add_city(
            city_name,
            city_coordinates.get(city_name)
        )


def add_connections(graph_manager, city_coordinates, file_path):
    with open(file_path, "r") as adj_file:
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
    # Define search algorithms
    search_algorithms = {
        "1": "Breadth-First Search",
        "2": "Depth-First Search",
        "3": "Best-First Search (A* with heuristic based on straight-line distance)",
        "4": "A* Search (custom heuristic can be implemented)",
        "5": "Exit"
    }

    while True:
        # Get user choice for search algorithm
        choice = get_user_choice(search_algorithms)

        if choice == "5":
            print("Exiting the program. Goodbye!")
            break

        start_city = input("Enter the starting city: ")
        goal_city = input("Enter the destination city: ")

        start_coords, goal_coords = city_coordinates.get(
            start_city), city_coordinates.get(goal_city)

        # Check if the coordinates are found before calling the search
        if start_coords and goal_coords:
            if choice == "1":
                benchmark_algorithm(
                    graph_manager.breadth_first_search, start_city, goal_city)
            elif choice == "2":
                benchmark_algorithm(
                    graph_manager.depth_first_search, start_city, goal_city)
            elif choice == "3":
                benchmark_algorithm(
                    graph_manager.best_first_search, start_city, goal_city)
            elif choice == "4":
                graph_manager.compute_heuristics()
                benchmark_algorithm(graph_manager.a_star_search,
                                    start_city, goal_city)
                graph_manager.compute_heuristics()
            else:
                print("Invalid search algorithm choice.")
        else:
            print(f"Coordinates not found for {start_city} or {goal_city}")


def benchmark_algorithm(algorithm_function, start_city, goal_city):
    start_time = timeit.default_timer()
    path = algorithm_function(start_city, goal_city)
    end_time = timeit.default_timer()
    elapsed_time = end_time - start_time

    if path:
        print(f"{algorithm_function.__name__}:")
        print(f"Path: {path}")
        print(f"Elapsed Time: {elapsed_time} seconds\n")
    else:
        print(f"{algorithm_function.__name__}: No path found.\n")


if __name__ == "__main__":
    main()
