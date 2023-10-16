def iterative_deepening_search(graph, start, goal, max_depth):
    # Depth-limited DFS function
    def depth_limited_search(node, depth):
        if depth == 0 and node == goal:
            return True
        if depth > 0:
            for neighbor in graph[node]:
                if depth_limited_search(neighbor, depth - 1):
                    return True
        return False

    # Main IDS loop
    for depth in range(max_depth + 1):
        if depth_limited_search(start, depth):
            return depth

    return None  # No path found within the depth limit

