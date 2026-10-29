def rbfs_search(graph, start, goal, heuristics):
    def rbfs(node, g, f_limit, path):
        if node == goal:
            return path, g, f_limit

        successors = []
        for neighbor, cost in graph.get(node, []):
            if neighbor not in path:
                new_g = g + cost
                new_f = max(new_g + heuristics.get(neighbor, 0), heuristics.get(node, 0))
                successors.append({'node': neighbor, 'g': new_g, 'f': new_f})

        if not successors:
            return None, float('inf'), float('inf')

        while True:
            successors.sort(key=lambda x: x['f'])
            best = successors[0]

            if best['f'] > f_limit:
                return None, float('inf'), best['f']

            alternative = successors[1]['f'] if len(successors) > 1 else float('inf')

            result_path, final_g, new_f = rbfs(
                best['node'],
                best['g'],
                min(f_limit, alternative),
                path + [best['node']]
            )

            if result_path is not None:
                return result_path, final_g, new_f

            best['f'] = new_f

    return rbfs(start, 0, float('inf'), [start])


# Sample Graph Data (Same as A*)
graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('D', 5)],
    'C': [('D', 1)],
    'D': []
}

heuristics = {'A': 6, 'B': 5, 'C': 1, 'D': 0}

# Execution
path, cost, _ = rbfs_search(graph, 'A', 'D', heuristics)
print(f"RBFS Path: {path}, Total Cost: {cost}")