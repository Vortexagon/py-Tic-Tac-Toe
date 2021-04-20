class Board:
    def __init__(self):
        self.board = [0] * 9
        self.history = []

    def __str__(self):
        board_string = ""

        # Four "+" signs each separated by a 7-length "-" sequence.
        horizontal_border = ("-" * 7).join(["+"] * 4)

        # Four "|" signs each separated by a 7-length space sequence.
        inner_border = (" " * 7).join(["|"] * 4)

        for i in range(3):
            board_string += horizontal_border + "\n"

            # To print easier.
            board = [self.board[0:3], self.board[3:6], self.board[6:9]]

            for j in range(3):
                if j == 1:
                    cell_separator = "   |   "
                    row = [str(elem) if elem != 0 else str(3 * i + index + 1) for (index, elem) in enumerate(board[i])]
                    board_string += f"|   {cell_separator.join(row)}   |" + "\n"

                else:
                    board_string += inner_border + "\n"

        board_string += horizontal_border + "\n"

        return board_string

    def get_free_cells(self):
        return [i for i in range(9) if self.board[i] == 0]

    def set_cell(self, index, content, save_to_history=True):
        if save_to_history:
            self.history.append((index, self.board[index]))
        self.board[index] = content

    def undo(self):
        last_change = self.history.pop()

        # Set the last change, but don't save this change to the history stack.
        self.set_cell(last_change[0], last_change[1], False)

    def is_ended(self):
        # Convert to 2D list, to check state easier.
        board = [self.board[0:3], self.board[3:6], self.board[6:9]]

        for symbol in "XO":
            #  Check rows, columns, and diagonals.
            if any(board[i] == [symbol] * 3 for i in range(3)) or \
                    any(all(board[i][j] == symbol for i in range(3)) for j in range(3)) or \
                    all(board[i][i] == symbol for i in range(3)) or \
                    all(board[2 - i][i] == symbol for i in range(3)):
                return symbol

        #  Check if there's a draw.
        if not any(cell == 0 for cell in self.board):
            return "D"

        #  Nothing significant has happened.
        return False

