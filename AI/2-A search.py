import heapq

def a_star_search(graph, start, goal, heuristics):
    # Priority queue stores tuples: (f_score, current_node, path, g_score)
    open_list = [(heuristics[start], start, [start], 0)]
    visited = {}

    while open_list:
        f, current, path, g = heapq.heappop(open_list)

        if current == goal:
            return path, g

        if current in visited and visited[current] <= g:
            continue

        visited[current] = g

        for neighbor, cost in graph.get(current, []):
            new_g = g + cost
            new_f = new_g + heuristics.get(neighbor, 0)
            heapq.heappush(
                open_list, (new_f, neighbor, path + [neighbor], new_g)
            )

    return None, float('inf')


# Sample Graph Data
graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('D', 5)],
    'C': [('D', 1)],
    'D': []
}

heuristics = {'A': 6, 'B': 5, 'C': 1, 'D': 0}

# Execution
path, cost = a_star_search(graph, 'A', 'D', heuristics)
print(f"A* Path: {path}, Total Cost: {cost}")