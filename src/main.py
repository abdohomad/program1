from tabulate import tabulate
from Graph_manager import GraphManager
from Coordinates import Coordinates
from geopy.distance import geodesic
import pandas as pd


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


def execute_search_function(graph_manager, choice, start_city, goal_city):
    if choice == "1":
        return graph_manager.breadth_first_search(start_city, goal_city)
    elif choice == "2":
        return graph_manager.depth_first_search(start_city, goal_city)
    elif choice == "3":
        return graph_manager.i_d_dfs_search(start_city, goal_city)
    elif choice == "4":
        return graph_manager.best_first_search(start_city, goal_city)
    elif choice == "5":
        return graph_manager.a_star_search(start_city, goal_city)
    else:
        return None, None


def get_user_input(prompt, validation_func=None):
    while True:
        user_input = input(prompt)
        if validation_func and not validation_func(user_input):
            print("Invalid input. Please try again.")
        else:
            return user_input


def validate_city_choice(choice, available_cities):
    return choice in available_cities


def validate_algorithm_choice(choice):
    return choice in {"1", "2", "3", "4", "5"}


def display_results(results_table, solution_path1, solution_path2, visited1, visited2):
    print("\nResults Table:")
    print(tabulate(results_table, headers='keys', tablefmt='pretty'))
    print("\nPath for Function 1:")
    print(solution_path1)
    print("\nPath for Function 2:")
    print(solution_path2)


def main():
    while True:
        coordinates_file = "src/coordinates.csv"
        adjacency_file = "src/Adjacencies.txt"

        # Load coordinates from the CSV file
        city_coordinates = load_coordinates(coordinates_file)

        # Create an instance of the GraphManager
        graph_manager = GraphManager()

        add_cities(graph_manager, city_coordinates)
        # Add cities to the graph and establish connections
        add_connections(graph_manager, city_coordinates, adjacency_file)

        available_cities = list(city_coordinates.keys())

        # Get the starting city with input validation
        start_city = get_user_input(
            "Enter the starting city: ", lambda choice: validate_city_choice(choice, available_cities))

        # Get the destination city with input validation
        goal_city = get_user_input(
            "Enter the destination city: ", lambda choice: validate_city_choice(choice, available_cities))

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
            "3": "i_d_dfs_search",
            "4": "Best-First Search",
            "5": "A* Search"
        }

        print(search_algorithms)

        function1_choice = get_user_input(
            "Enter the first function choice (1-5): ", lambda choice: validate_algorithm_choice(choice))
        function2_choice = get_user_input(
            "Enter the second function choice (1-5): ", lambda choice: validate_algorithm_choice(choice))

        if function1_choice not in search_algorithms or function2_choice not in search_algorithms:
            print("Invalid function choices. Please enter numbers between 1 and 5.")
            return

        function1_algorithm = search_algorithms[function1_choice]
        function2_algorithm = search_algorithms[function2_choice]

        solution_path1, visited1, time1, memory_used1 = execute_search_function(
            graph_manager, function1_choice, start_city, goal_city)

        solution_path2, visited2, time2, memory_used2 = execute_search_function(
            graph_manager, function2_choice, start_city, goal_city)
        formatted_path1 = ' -> '.join(
            solution_path1) if solution_path1 else None
        formatted_path2 = ' -> '.join(
            solution_path2) if solution_path2 else None

        # Display results as a table
        results_table = pd.DataFrame({
            "Algorithm": [function1_algorithm, function2_algorithm],
            "Visited Cities": [len(visited1) if visited1 else None, len(visited2) if visited2 else None],
            "Total Distance": [calculate_distance(solution_path1, city_coordinates) if solution_path1 else None,
                               calculate_distance(solution_path2, city_coordinates) if solution_path2 else None],
            "Search Time": ["{:.5f} milliseconds".format(time1), "{:.5f} milliseconds".format(time2)],
            "Memory Used": [f"{memory_used1:.3f} MB", f"{memory_used2:.3f} MB"]
        })

        display_results(results_table, formatted_path1,
                        formatted_path2, visited1, visited2)

        # Ask the user if they want to perform another comparison
        another_comparison = input(
            "\nDo you want to perform another comparison? (yes/no): ").lower()
        if another_comparison != 'yes':
            break


if __name__ == "__main__":
    main()
