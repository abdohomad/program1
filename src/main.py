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
            start_time = time.time()  # Start time measurement

            if choice == "1":
                solution_path = graph_manager.breadth_first_search(
                    start_city, goal_city)
            elif choice == "2":
                solution_path = graph_manager.depth_first_search(
                    start_city, goal_city)
            elif choice == "3":
                solution_path = graph_manager.best_first_search(
                    start_city, goal_city)
            elif choice == "4":
                solution_path = graph_manager.a_star_search(
                    start_city, goal_city)  # Implement custom heuristic here
            else:
                print("Invalid search algorithm choice.")

            # Stop time measurement and calculate elapsed time
            elapsed_time = time.time() - start_time

            if solution_path:
                print(f"Solution path: {solution_path}")

                # Calculate total distance
                total_distance = calculate_distance(
                    solution_path, city_coordinates)
                print(f"Total distance: {total_distance:.2f} miles")

                print(f"Search time: {elapsed_time:.4f} seconds")

                visualize_route_on_map(graph_manager, solution_path)
            else:
                print("Route not found between these cities.")
        else:
            print(f"Coordinates not found for {start_city} or {goal_city}")


def visualize_route_on_map(graph_manager, route):
    # Extract coordinates and city names for cities in the route
    route_coords = [graph_manager.graph.nodes[city]['coordinates']
                    for city in route]
    city_names = route

    # Extract latitude and longitude for plotting
    lats, lons = zip(*route_coords)

    # Plot the scatter plot for all cities first
    plt.figure(figsize=(8, 6))
    scatter_plot = plt.scatter(lons, lats, color='red', label='Cities')

    # Optionally, mark the starting and goal cities differently
    plt.scatter(lons[0], lats[0], color='green',
                marker='s', s=100, label='Start City')
    plt.scatter(lons[-1], lats[-1], color='orange',
                marker='^', s=100, label='Goal City')

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Route Visualization')
    plt.legend()

    # Plot the route on top of the scatter plot using a line
    line_plot, = plt.plot(lons, lats, color='blue',
                          label='Route', linestyle='-', linewidth=2)

    # Add city names as annotations
    for name, lat, lon in zip(city_names, lats, lons):
        plt.text(lon, lat, name, fontsize=8,
                 ha='right', va='bottom', alpha=0.5)

    plt.ion()  # Enable interactive mode
    plt.show()

    # Animate the route progression

    for i in range(1, len(route)):
        current_city = route[i]

        # Highlight the current city by changing its color
        scatter_plot.set_array(
            [0 if city == current_city else 1 for city in route])

        # Update the line plot to show the progression
        line_plot.set_data(lons[:i + 1], lats[:i + 1])

        plt.title(f'Current City: {current_city}')
        plt.pause(0.5)

    plt.ioff()  # Disable interactive mode to keep the plot open
    plt.show()


if __name__ == "__main__":
    main()
