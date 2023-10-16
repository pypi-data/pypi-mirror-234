from queue import PriorityQueue

graph = {
    'A': {'B': 1, 'C': 5},
    'B': {'D': 3, 'E': 2},
    'C': {'F': 4},
    'D': {'G': 3},
    'E': {},
    'F': {},
    'G': {}
}
heuristic = {
    'A': 8,
    'B': 6,
    'C': 4,
    'D': 4,
    'E': 2,
    'F': 2,
    'G': 0
}
def a_star_optimistic(start, goal):
    frontier = PriorityQueue()
    frontier.put((0, start))
    cost_so_far = {start: 0}
    
    while not frontier.empty():
        _, current = frontier.get()
        
        if current == goal:
            break
        
        for neighbor, distance in graph[current].items():
            new_cost = cost_so_far[current] + distance
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic[neighbor]  # Use optimistic heuristic
                frontier.put((priority, neighbor))
    
    return cost_so_far[goal]