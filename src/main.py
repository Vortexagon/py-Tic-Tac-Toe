from ai import OptimalAI
from board import Board


def enter_move(board: Board, symbol: str) -> Board:
    """
    Gets an index from the user and returns the updated board after applying their move
    :param board: The current state of the board
    :param symbol: The symbol of the player
    :return: The board updated with a mark at their choice
    """
    while True:
        users_move: int = int(input("Enter a move: ")) - 1
        if users_move in board.get_free_cells():
            board.set_cell(users_move, symbol)
            return board


user_symbol: str = "X"
comp_symbol: str = "O"

board: Board = Board()

# A game against OptimalAI.
while not board.is_ended():
    print(board)
    board = enter_move(board, user_symbol)
    if board.is_ended():
        break
    board = OptimalAI.move(board, comp_symbol)

print(board)

game_result = board.is_ended()

if game_result == user_symbol:
    print("User Wins!")
elif game_result == comp_symbol:
    print("Computer Wins!")
elif game_result == "D":
    print("Draw!")

exit()
