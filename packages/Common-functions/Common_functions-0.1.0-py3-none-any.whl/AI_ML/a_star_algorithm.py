import heapq

def heuristic(node, goal):
    # Calculate the heuristic value between the current node and the goal node
    # Return the estimated cost from the current node to the goal node
    current_x, current_y = node
    goal_x, goal_y = goal
    return abs(current_x - goal_x) + abs(current_y - goal_y)

def a_star(graph, start, goal):
    open_list = [(0, start)]  # Priority queue for A* traversal
    came_from = {}  # Dictionary to store the parent node for each visited node
    g_score = {node: float('inf') for node in graph}  # Dictionary to store the cost from start to each node
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}  # Dictionary to store the total estimated cost from start to each node
    f_score[start] = heuristic(start, goal)

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            # Reconstruct the path from the goal node to the start node
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor, edge_cost in graph[current]:
            tentative_g_score = g_score[current] + edge_cost
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None  # No path found

