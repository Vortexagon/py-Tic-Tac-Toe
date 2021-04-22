class Board:
    def __init__(self):
        self.board: dict = {"X": 0, "O": 0}
        self.history: list[tuple] = []

    def __str__(self) -> str:
        board_string: str = ""

        # Four "+" signs each separated by a 3-length "-" sequence.
        horizontal_border: str = ("-" * 3).join(["+"] * 4)

        # Convert the bitboard representation to a 2D List for easier string building.
        grid_board: list[list[int]] = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        # Add a symbol into grid_board where there is a corresponding symbol in the bitboard.
        for i in range(3):
            for j in range(3):
                for symbol in "XO":
                    if self.board[symbol] & (1 << (8 - (3 * i + j))):
                        grid_board[i][j] = symbol

        for i in range(3):
            board_string += horizontal_border + "\n"

            cell_separator: str = " | "
            row: list[str] = [str(elem) if elem != 0 else str(3 * i + index + 1) for (index, elem) in enumerate(grid_board[i])]
            board_string += f"| {cell_separator.join(row)} |" + "\n"

        board_string += horizontal_border + "\n"

        return board_string

    def get_free_cells(self) -> list[int]:
        """
        Gets the free cells in the board.
        :return: A list of free indexes
        """

        # The conversions and work below is an implementation of a NOR gate.
        # Where there are two zeros there will be an output of 1, and zero otherwise.

        # Squash the board to get a bitarray of occupied and empty indexes regardless of symbol.
        squashed_board: int = 0
        for symbol in self.board.keys():
            squashed_board |= self.board[symbol]

        # Flip the bitarray to have 1s where there is a free cell.
        free_cells: int = squashed_board ^ 0b111_111_111
        return [i for i in range(9) if (256 >> i) & free_cells]

    def set_cell(self, index: int, chosen_layer: str) -> None:
        """
        Sets the index of the board with a symbol
        :param index: The index of the cell to set
        :param chosen_layer: The symbol to be placed / the layer of the bitboard
        :return: None
        """

        if chosen_layer not in self.board.keys():
            raise KeyError(f"{chosen_layer} isn't an entry in the bitboard.")

        on_mask: int = 1 << (8 - index)
        off_mask: int = on_mask ^ 0b111_111_111

        # Add the current state of the cell to the history stack
        self.history.append((index, chosen_layer, self.board[chosen_layer] & on_mask))

        for layer in self.board.keys():
            if layer == chosen_layer:
                # Activate the index in the chosen_layer
                self.board[layer] |= on_mask
            else:
                # Deactivate the index on all other layers.
                self.board[layer] &= off_mask

    def clear_cell(self, index: int) -> None:
        """
        Clears the board at the given index
        :param index: the index to clear
        :return: None
        """
        bit_mask: int = 1 << (8 - index)
        not_bit_mask: int = bit_mask ^ 0b111_111_111

        entry_added = False

        for symbol in self.board:
            if self.board[symbol] & bit_mask:
                # There was a symbol at this index, so add that to the history stack.
                self.history.append((index, symbol, 1))
                entry_added = True
                break

        if not entry_added:
            self.history.append((index, "ANY", 1))

        # Clear that index for all bitboard layers and don't regard the other indexes.
        for symbol in self.board.keys():
            self.board[symbol] &= not_bit_mask

    def undo(self) -> None:
        """
        Undo the last set_cell or clear_cell. Does nothing if history stack is empty
        :return: None
        """
        if len(self.history) > 0:
            index, layer, val = self.history.pop()
            # If the value of that bit was a 1, set_cell
            if val:
                self.set_cell(index, layer)
            # Otherwise, the cell had been empty, so clear the cell.
            else:
                self.clear_cell(index)

            # Remove the entry that we will have created in the history stack.
            self.history.pop()

    def is_ended(self):
        """
        Checks whether there is a win for any symbol, a draw or if nothing significant has happened.
        :return: The symbol that won, or "D" for draw, or False if nothing significant has happened.
        """
        # A list of all bit masks needed to check for a win
        win_masks: list[int] = [
            *[0b111_000_000 >> index for index in range(0, 9, 3)],  # Check rows
            *[0b100_100_100 >> index for index in range(3)],  # Check columns
            *[0b100_010_001,  # Check the TL-BR diagonal
              0b001_010_100]  # Check the BL-TR diagonal
        ]

        for symbol in self.board.keys():
            for mask in win_masks:
                # If this is true, the board contains a winning combination.
                # If these numbers aren't equal, the board didn't match up with the mask perfectly.
                # Therefore, that combination isn't present in the board.
                if self.board[symbol] & mask == mask:
                    return symbol

        # Squash the board to check if every index is occupied regardless of symbol.
        squashed_board: int = 0
        for symbol in self.board.keys():
            squashed_board |= self.board[symbol]

        # Every cell is occupied amd no win was detected, therefore there must be a draw.
        if squashed_board == 0b111_111_111:
            return "D"

        # Nothing significant has happened.
        return False
