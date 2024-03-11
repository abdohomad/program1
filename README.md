**Introduction**

This code implements a pathfinding algorithm  for finding routes between cities. It utilizes a graph data structure to represent the connections between cities and supports various search algorithms like Breadth-First Search (BFS), Depth-First Search (DFS), Iterative-Deepening Depth-First Search (ID-DFS), Best-First Search, and A* Search. The code also calculates the heuristic cost estimate to guide the search process in A* Search.

**Installation**

* networkx
* geopy
* pandas
* tabulate (optional, for displaying results in a table)

You can install them using the `pip` command:

```bash
pip install networkx geopy pandas tabulate
```

**Usage**

1. **Data Files:**
    * Ensure you have two data files in the `src` directory:
        * `coordinates.csv`: This file should contain a comma-separated list of cities and their corresponding geographical coordinates (latitude, longitude).
        * `Adjacencies.txt`: This file should represent the connections between cities. Each line should contain two city names separated by a space.

2. **Running the Script:**

   ```bash
   python main.py
   ```

**Explanation of the Code**

The code is divided into two main parts:

1. **GraphManager Class:**
   * This class manages the graph data structure, representing cities as nodes and connections as edges.
   * It provides functions to add cities, establish connections, calculate heuristics, and perform various search algorithms.

2. **main Function:**
   * This function serves as the entry point of the program.
   * It loads city coordinates and connections from the data files.
   * It interacts with the user to get the starting and destination cities.
   * It allows the user to choose two search algorithms for comparison.
   * It executes the chosen search algorithms and displays the results in a table, including:
       * Visited cities
       * Total distance of the path
       * Search time
       * Memory used

**Features**

* Supports various graph search algorithms: BFS, DFS, ID-DFS, Best-First Search, A* Search.
* Calculates heuristic cost estimate for A* Search, Best-First Search.
* Provides user interaction for selecting search algorithms and cities.
* Displays search results in a clear and informative table.

