from ai import RandomAI
from board import Board


def enter_move(board, symbol):
    while True:
        users_move = int(input("Enter a move: ")) - 1
        if users_move in board.get_free_cells():
            board.set_cell(users_move, symbol)
            return board


user_symbol = "X"
comp_symbol = "O"

board = Board()

# A game against RandomAI.
while not board.is_ended():

    print(board)
    board = enter_move(board, user_symbol)
    if board.is_ended():
        break
    board = RandomAI.move(board, comp_symbol)

print(board)

game_result = board.is_ended()

if game_result == user_symbol:
    print("User Wins!")

elif game_result == comp_symbol:
    print("Computer Wins!")

elif game_result == "D":
    print("Draw!")
