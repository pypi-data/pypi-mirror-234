def min_max(game_state, depth, maximizing_player):
    # Base case: return the evaluation of the game state if depth is 0 or the game is over
    if depth == 0 or game_over(game_state):
        return evaluate(game_state)

    if maximizing_player:
        max_eval = float('-inf')

        # Generate all possible moves
        possible_moves = generate_moves(game_state)

        for move in possible_moves:
            # Apply the move to the game state
            new_game_state = apply_move(game_state, move)

            # Recursive call to min_max with decreased depth and switched player
            eval = min_max(new_game_state, depth - 1, False)

            # Update the maximum evaluation
            max_eval = max(max_eval, eval)

        return max_eval
    else:
        min_eval = float('inf')

        # Generate all possible moves
        possible_moves = generate_moves(game_state)

        for move in possible_moves:
            # Apply the move to the game state
            new_game_state = apply_move(game_state, move)

            # Recursive call to min_max with decreased depth and switched player
            eval = min_max(new_game_state, depth - 1, True)

            # Update the minimum evaluation
            min_eval = min(min_eval, eval)

        return min_eval
