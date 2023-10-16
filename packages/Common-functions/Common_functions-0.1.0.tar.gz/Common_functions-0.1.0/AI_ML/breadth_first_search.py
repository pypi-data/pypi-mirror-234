from collections import deque

def breadth_first_search(graph, start_node):
    visited = set()  # Set to track visited nodes
    queue = deque()  # Queue for BFS traversal

    visited.add(start_node)
    queue.append(start_node)

    while queue:
        node = queue.popleft()
        print(node)  # Process the node (print it in this example)

        # Explore neighbors of the current node
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

