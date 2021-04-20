from random import randrange
from math import inf


class RandomAI:
    @staticmethod
    def move(board, symbol):
        while True:
            comp_move = randrange(10)
            if comp_move in board.get_free_cells():
                board.set_cell(comp_move, symbol)
                break
        return board


class OptimalAI:
    @staticmethod
    def minimax(board, alpha, beta, depth, maximising, own_symbol):
        opponent_symbol = "X" if own_symbol == "O" else "O"

        # Check if we've reached a terminal state. If so, return the state's score.
        # The score is divided by depth. This rewards quick wins and long losses.
        result = board.is_ended()
        if result == "D":
            return 0
        elif result == own_symbol:
            return 1 / depth
        elif result == opponent_symbol:
            return -1 / depth

        final_score = inf * (-1) ** maximising

        for cell in board.get_free_cells():
            board.set_cell(cell, own_symbol if maximising else opponent_symbol)
            score = OptimalAI.minimax(board, alpha, beta, depth + 1, not maximising, own_symbol)
            board.undo()

            if maximising:
                final_score = max(final_score, score)
                alpha = max(alpha, score)
                # If the maximiser realises that the minimiser has a better choice than this subtree, break.
                if beta <= final_score:
                    break
            else:
                final_score = min(final_score, score)
                beta = min(beta, score)
                # If the minimiser realises that the maximiser has a better choice than this subtree, break.
                if alpha >= final_score:
                    break

        return final_score

    @staticmethod
    def move(board, symbol):
        best_score = -inf
        best_index = None

        for cell in board.get_free_cells():
            board.set_cell(cell, symbol)
            score = OptimalAI.minimax(board, -inf, inf, 1, False, symbol)
            board.undo()

            if score > best_score:
                best_score = score
                best_index = cell

        board.set_cell(best_index, symbol)
        return board
