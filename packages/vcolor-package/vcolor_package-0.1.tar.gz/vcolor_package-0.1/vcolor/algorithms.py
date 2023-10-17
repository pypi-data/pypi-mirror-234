import random
# Graph Colouring using Dsatur Algorithm
def dsatur(self):
    # Finding Distinct number of Neighbouring Colours  
    def node_saturation(v, colour):
        neighbor_colours = set(colour[i] for i in self.graph[v])
        return len(neighbor_colours)
    max_colors = self.V
    colour = [-1] * self.V
    degree = [len(self.graph[i]) for i in range(self.V)]

    # Starting by coloring the node with the max degree
    start_node = degree.index(max(degree))
    colour[start_node] = 1
    visited = [False] * self.V
    visited[start_node] = True

    # Coloring the vertex with higest saturation or max degree
    for _ in range(self.V - 1):
        max_saturation = -1
        next_node = -1

        for v in range(self.V):
            if not visited[v]:
                n_saturation = node_saturation(v, colour)
                if n_saturation > max_saturation or (n_saturation == max_saturation and (degree[v] > degree[next_node] or (degree[v] == degree[next_node] and v < next_node))):
                    max_saturation = n_saturation
                    next_node = v

        # If node can't be found 
        if next_node == -1:  
            break

        available_colors = set(range(1, max_colors + 1))
        for neighbor in self.graph[next_node]:
            if colour[neighbor] in available_colors:
                available_colors.remove(colour[neighbor])

        colour[next_node] = min(available_colors)
        visited[next_node] = True

    return colour

# Graph Colouring using Firstfit Algorithm
def firstfit(self):
    max_colors = self.V
    colour = [-1] * self.V

    for v in range(self.V):
        available_colors = set(range(1, max_colors + 1))
        for i in self.graph[v]:
            if colour[i] in available_colors:
                available_colors.remove(colour[i])
        colour[v] = min(available_colors)

    return colour

 # Graph Colouring using Largestfit Algorithm
def largefit(self):
    max_colors = self.V
    colour = [-1] * self.V
    degrees = [len(self.graph[v]) for v in range(self.V)]

    # Sorting the nodes in descending order of degrees
    nodes_by_degree = sorted(range(self.V), key=lambda x: degrees[x], reverse=True)

    for node in nodes_by_degree:
        available_colors = set(range(1, max_colors + 1))
        for neighbor in self.graph[node]:
            if colour[neighbor] in available_colors:
                available_colors.remove(colour[neighbor])
        colour[node] = min(available_colors)

    return colour

def iterative_greedy(self):
        # Counting conflicts after Colouring the graph
        def count_conflicts(colours):
            conflicts = 0
            for i in range(self.V):
                for j in self.graph[i]:
                    if colours[i] == colours[j]:
                        conflicts += 1
            return conflicts
        num_iterations = 500
        best_coloring = None
        min_conflicts = float('inf')
        available_colors_set = set(range(1, self.V + 1))

        for _ in range(num_iterations):
            vertices_order = list(range(self.V))
            random.shuffle(vertices_order)

            graph_col = [0] * self.V
            for v in vertices_order:
                available_colors = available_colors_set.copy()
                available_colors.difference_update(graph_col[i] for i in self.graph[v])
                graph_col[v] = min(available_colors)

            conflicts = count_conflicts(graph_col)
            if conflicts < min_conflicts:
                min_conflicts = conflicts
                best_coloring = graph_col.copy()
                if min_conflicts == 0:
                    break

        return best_coloring



# Graph colouring using Tabu Search 
def tabu_search(graph, max_iter, tabu_tenure):
    # Counting conflicts after Colouring the graph
    def count_conflicts(colours):  
        conflicts = 0
        for i in range(graph.V):  
            for j in graph.graph[i]:  
                if colours[i] == colours[j]:
                    conflicts += 1
        return conflicts
    
        # Counting conflicts using delta after Colouring the graph
    def compute_delta_conflicts(graph, solution, node, new_color):
        original_color = solution[node]
        delta = 0

        for neighbor in graph.graph[node]:
            if solution[neighbor] == original_color:
                delta -= 1
            if solution[neighbor] == new_color:
                delta += 1

        return delta

    current_solution = iterative_greedy(graph)
    best_solution = current_solution.copy()
    best_conflicts = count_conflicts(best_solution)
    tabu_list = set()

    for _ in range(max_iter):
        best_neighbour = None
        best_neighbour_conflicts = float("inf")

        for i in range(graph.V):
            for c in range(1, max(current_solution) + 1):
                if current_solution[i] != c:
                    delta_conflicts = compute_delta_conflicts(graph, current_solution, i, c)
                    total_conflicts = best_conflicts + delta_conflicts
                    if (i, c) not in tabu_list and total_conflicts < best_neighbour_conflicts:
                        best_neighbour = (i, c)
                        best_neighbour_conflicts = total_conflicts

         # Updating Tabu List
        if best_neighbour:
            i, c = best_neighbour
            current_solution[i] = c
            best_conflicts = best_neighbour_conflicts
            tabu_list.add(best_neighbour)
            if len(tabu_list) > tabu_tenure:
                tabu_list.pop()

        if best_conflicts == 0:
            return current_solution

        if best_neighbour_conflicts < count_conflicts(best_solution):
            best_solution = current_solution.copy()

    return best_solution