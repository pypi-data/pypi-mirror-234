Graph Colouring Algorithms Library
This library offers multiple approaches to the graph colouring problem. Our algorithms leverage distinct techniques, ranging from simple greedy approaches to advanced heuristic methods. Feel free to delve in and discover the best approach for your specific needs.

Algorithms Included:
DSATUR Algorithm: DSATUR is a well-known algorithm in the graph colouring domain. It dynamically selects the vertex with the maximum saturation degree. If there's a tie, it selects the vertex with the highest degree. This approach is dynamic and tends to yield good results in a range of scenarios.

First Fit Algorithm: This algorithm uses a simple heuristic. It traverses the graph node by node and assigns the first available colour. It's a quick approach that may not always result in the minimum number of colours but serves as a decent baseline.

Largest Fit Algorithm: An improvement over the First Fit. Instead of just moving node by node, we prioritize nodes based on their degrees. Nodes with a higher degree are coloured first.

Iterative Greedy: It's a repeated application of the greedy approach, with randomized orders. It's an attempt to achieve better results than a simple greedy approach by adding a stochastic element.

Tabu Search: A more advanced technique which leverages the concepts of local search and memory. The algorithm tries to find the best move at every iteration while keeping track of previously made moves to avoid cycling.

Usage:
You can directly call any of the methods provided in the library on a given graph object. Each method returns a colouring of the graph according to the respective algorithm.
for eg:
    result = vcolor.dsatur(g)
    
    result = vcolor.firstfit(g)
    
    result = vcolor.largefit(g)

    result = vcolor.iterative_greedy(g)
    
    result = vcolor.tabu_search(g, max_iter=1000, tabu_tenure=10)
    Note: For Tabu Search, max_iter is for maximum iterations and tabu_tenure is for Tabu Tenure.

Contributions:
We always welcome improvements and bug fixes. If you're interested in contributing to this library, please feel free to open a pull request.

License:
UCC License. Please refer to the LICENSE.txt file for more details.