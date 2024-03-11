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

**Example Usage 1**

This example demonstrates how to find a route between Topeka and Harper in Kansas using two search algorithms: Best-First Search and A* Search.

**Input**

* Starting City: Topeka
* Destination City: Harper

**Search Algorithms**

* Function 1: Best-First Search
* Function 2: A* Search

**Output**

The program outputs a table comparing the performance of both algorithms and the paths discovered by each:

**Results**

| Algorithm         | Visited Cities | Total Distance (miles) | Search Time (milliseconds) | Memory Used (MB) |
|-------------------|----------------|------------------------|----------------------------|-----------------|
| Best-First Search  | 37              | 348.76                  | 0.04675                    | 116.371          |
| A* Search          | 35              | 280.58                   | 0.00101                    | 116.383          |

**Paths**

* **Best-First Search Path:** Topeka -> Manhattan -> Marion -> McPherson -> Hutchinson -> Pratt -> Coldwater -> Kiowa -> Attica -> Harper
* **A star Search Path:** Topeka -> Manhattan -> Marion -> McPherson -> Newton -> Andover -> Mulvane -> Mayfield -> Bluff_City -> Anthony -> Harper

**Key Observations**

* A* Search found a shorter path (280.58 miles) compared to Best-First Search (348.76 miles).
* A* Search also completed the search significantly faster (0.00101 milliseconds) than Best-First Search (0.04675 milliseconds).
* The memory usage for both algorithms was comparable (around 116 MB).


**Example Usage 2**

This example demonstrates how to find a route between Wichita and Anthony in Kansas using two search algorithms: Breadth-First Search (BFS) and Depth-First Search (DFS).

**Input**

* Starting City: Wichita
* Destination City: Anthony

**Search Algorithms**

* Function 1: Breadth-First Search
* Function 2: Depth-First Search

**Output**

The program outputs a table comparing the performance of both algorithms and the paths discovered by each:

**Results**

| Algorithm         | Visited Cities | Total Distance (miles) | Search Time (milliseconds) | Memory Used (MB) |
|-------------------|----------------|------------------------|----------------------------|-----------------|
| Breadth-First Search | 35              | 135.32                  | 0.00000                    | 116.547          |
| Depth-First Search  | 34              | 538.26                   | 0.00000                    | 116.559          |

**Paths**

* **Breadth-First Search Path:** Wichita -> Leon -> Andover -> Mulvane -> Mayfield -> Bluff_City -> Anthony
* **Depth-First Search Path:** (Due to the nature of DFS, the path may vary. This is one possible path found.)  Wichita -> Derby -> Clearwater -> Cheney -> Pratt -> Hutchinson -> McPherson -> Salina -> Lyons -> Hillsboro -> El_Dorado -> Towanda -> Andover -> Mulvane -> Mayfield -> Wellington -> Caldwell -> South_Haven -> Bluff_City -> Kiowa -> Attica -> Harper -> Anthony

**Key Observations**

* Breadth-First Search found a shorter path (135.32 miles) compared to Depth-First Search (which can vary depending on the exploration order).
* Breadth-First Search also completed the search much faster (essentially instantaneous in this case) compared to Depth-First Search (also instantaneous here).
* The memory usage for both algorithms was comparable (around 116 MB).

**Explanation**

Breadth-First Search systematically explores all neighboring nodes at each level, guaranteeing to find the shortest path first. Depth-First Search explores a single path deeply until it reaches the destination or a dead end. This can lead to longer paths being discovered first, especially for graphs with many branches. In this case, both algorithms completed the search very quickly.


**Explanation**

A* Search leverages a heuristic cost estimate to guide its search towards the most promising paths, leading to a shorter and faster solution in this example. While Best-First Search explores the search space methodically, it might not always find the optimal path as quickly as A*. The memory usage remained similar for both algorithms in this case.


