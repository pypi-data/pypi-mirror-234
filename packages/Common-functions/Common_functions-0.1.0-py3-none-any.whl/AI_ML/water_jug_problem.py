from collections import deque

def water_jug_problem(capacity1, capacity2, target):
    visited = set()  # Set to track visited states
    queue = deque()  # Queue for BFS traversal

    # Initial state: both jugs are empty
    initial_state = (0, 0)
    visited.add(initial_state)
    queue.append(initial_state)

    while queue:
        current_state = queue.popleft()
        jug1, jug2 = current_state

        # Check if the target amount is achieved
        if jug1 == target or jug2 == target:
            return current_state

        # Generate all possible next states
        next_states = []

        # Fill jug1 to its capacity
        next_states.append((capacity1, jug2))
        # Fill jug2 to its capacity
        next_states.append((jug1, capacity2))
        # Empty jug1
        next_states.append((0, jug2))
        # Empty jug2
        next_states.append((jug1, 0))
        # Pour jug1 into jug2 until jug2 is full or jug1 is empty
        amount_to_pour = min(jug1, capacity2 - jug2)
        next_states.append((jug1 - amount_to_pour, jug2 + amount_to_pour))
        # Pour jug2 into jug1 until jug1 is full or jug2 is empty
        amount_to_pour = min(jug2, capacity1 - jug1)
        next_states.append((jug1 + amount_to_pour, jug2 - amount_to_pour))

        # Add unvisited next states to the queue and mark them as visited
        for state in next_states:
            if state not in visited:
                visited.add(state)
                queue.append(state)

    return None  # Target amount cannot be achieved


