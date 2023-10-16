import heapq

def uniform_cost_search(graph, start, goal):
    visited = set()  # Set to track visited nodes
    queue = [(0, start)]  # Priority queue for UCS traversal

    while queue:
        cost, node = heapq.heappop(queue)

        if node == goal:
            return cost

        if node not in visited:
            visited.add(node)

            for neighbor, edge_cost in graph[node]:
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + edge_cost, neighbor))

    return float('inf')  # No path found

