def hill_climbing(problem):
    current_state = problem.initial_state()

    while True:
        neighbors = problem.generate_neighbors(current_state)
        best_neighbor = None

        for neighbor in neighbors:
            if best_neighbor is None or problem.heuristic(neighbor) > problem.heuristic(best_neighbor):
                best_neighbor = neighbor

        if problem.heuristic(best_neighbor) <= problem.heuristic(current_state):
            return current_state

        current_state = best_neighbor