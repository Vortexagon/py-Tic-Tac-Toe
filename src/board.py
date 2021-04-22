from copy import deepcopy


class Board:
    def __init__(self):
        self.board = {"X": 0, "O": 0}
        self.history = []

    def __str__(self):
        board_string = ""

        for symbol in self.board.keys():
            board_string += symbol + ": " + bin(self.board[symbol])[2:].zfill(9) + "\n"

        return board_string

    def get_free_cells(self):
        squashed_board = 0
        for symbol in self.board.keys():
            squashed_board |= self.board[symbol]

        free_cells = squashed_board ^ 0b111_111_111
        return [i for i in range(9) if (256 >> i) & free_cells]

    def set_cell(self, index, chosen_layer):
        if chosen_layer not in self.board.keys():
            raise KeyError(f"{chosen_layer} isn't an entry in the bitboard.")

        on_mask = 1 << (8 - index)
        off_mask = on_mask ^ 0b111_111_111

        self.history.append(deepcopy(self.board))

        for layer in self.board.keys():
            if layer == chosen_layer:
                self.board[layer] |= on_mask
            else:
                self.board[layer] &= off_mask

    def clear_cell(self, index):
        bit_mask = 1 << (8 - index)
        not_bit_mask = bit_mask ^ 0b111_111_111

        self.history.append(deepcopy(self.board))

        for symbol in self.board.keys():
            self.board[symbol] &= not_bit_mask

    def undo(self):
        if len(self.history) > 0:
            self.board = deepcopy(self.history.pop())

    def is_ended(self):
        win_masks = [
            *[0b111_000_000 >> index for index in range(0, 9, 3)],
            *[0b100_100_100 >> index for index in range(3)],
            *[0b100_010_001,
              0b001_010_100]
        ]

        for symbol in self.board.keys():
            for mask in win_masks:
                if self.board[symbol] & mask == mask:
                    return symbol

        squashed_board = 0
        for symbol in self.board.keys():
            squashed_board |= self.board[symbol]

        if squashed_board == 0b111_111_111:
            return "D"

        return False
