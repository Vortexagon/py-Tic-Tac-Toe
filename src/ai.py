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
    def minimax(board, depth, maximising, own_symbol):
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

        scores = []

        for cell in board.get_free_cells():
            board.set_cell(cell, own_symbol if maximising else opponent_symbol)
            score = OptimalAI.minimax(board, depth + 1, not maximising, own_symbol)
            scores.append(score)
            board.undo()

        return max(scores) if maximising else min(scores)

    @staticmethod
    def move(board, symbol):
        best_score = -inf
        best_index = None

        for cell in board.get_free_cells():
            board.set_cell(cell, symbol)
            score = OptimalAI.minimax(board, 1, False, symbol)
            board.undo()

            if score > best_score:
                best_score = score
                best_index = cell

        board.set_cell(best_index, symbol)
        return board
