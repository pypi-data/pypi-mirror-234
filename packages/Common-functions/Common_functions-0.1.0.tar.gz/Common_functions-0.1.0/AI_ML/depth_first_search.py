def depth_first_search(graph, start_node):
    visited = set()  # Set to track visited nodes

    def dfs_helper(node):
        visited.add(node)
        print(node)  # Process the node (print it in this example)

        # Explore neighbors of the current node
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs_helper(neighbor)

    dfs_helper(start_node)
