from random import randrange


class RandomAI:
    @staticmethod
    def move(board, symbol):
        while True:
            comp_move = randrange(10)
            if comp_move in board.get_free_cells():
                board.set_cell(comp_move, symbol)
                break
        return board
