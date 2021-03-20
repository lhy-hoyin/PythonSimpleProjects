"""
Author: BarryHY
Date Created: 20 Feb 2021
Date Updated: 20 Mar 2021
Project Name: TicTacToe
Description: Play a tic-tac-toe game. Board can be of various sizes (min 3x3).

External library required:
    numpy   (https://pypi.org/project/numpy/)
    aenum   (https://pypi.org/project/aenum/)
"""

import numpy as np
import tkinter as tk
from tkinter import messagebox
from aenum import Enum


class Player(Enum):
    _init_ = 'value string'

    NO_PLAYER = 0, ' '
    PLAYER_ONE = 1, 'X'
    PLAYER_TWO = 2, 'O'

    def __str__(self):
        return self.string


class TicTacToe(tk.Frame):
    row_size = 3
    col_size = 3
    win_requirement = 3

    board = None
    game_active = False
    winning_matrices = []
    current_player = Player.NO_PLAYER
    scores = {}

    def __init__(self, root: tk.Frame = None):
        super().__init__(root)

        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.minsize(300, 300)
        # FIXME: set window name (to appear at taskbar)

        # Initialised scores
        for p in Player:
            if p == Player.NO_PLAYER:
                self.scores["Draw"] = 0
            else:
                self.scores['Player ' + p.string] = 0

        self.compute_win_conditions()
        self.start_game()

    def compute_win_conditions(self):
        # Ensure min board size of 3x3
        self.row_size = 3 if self.row_size < 3 else self.row_size
        self.col_size = 3 if self.col_size < 3 else self.col_size
        smaller_side = min(self.row_size, self.col_size)
        self.win_requirement = smaller_side if self.win_requirement > smaller_side else self.win_requirement

        # Create win conditions matrices
        self.winning_matrices.clear()
        self.winning_matrices.append(np.full((1, self.win_requirement), True))  # Row
        self.winning_matrices.append(np.full((self.win_requirement, 1), True))  # Column
        self.winning_matrices.append(np.identity(self.win_requirement, bool))  # Diagonal (Downwards)
        self.winning_matrices.append(np.fliplr(np.identity(self.win_requirement, bool)))  # Diagonal (Upwards)

    def start_game(self):
        self.populate_menu()
        self.create_board()
        self.populate_game_elements()

        self.game_active = True

        # Start with player 'X'
        self.current_player = Player.PLAYER_ONE

    def populate_menu(self):
        # Create menu bar
        menu_bar = tk.Menu(self.root)

        # New Menu
        new_menu = tk.Menu(menu_bar, tearoff=0)
        new_menu.add_command(label="New Game", command=self.reset_game)

        # Options Menu
        options_menu = tk.Menu(menu_bar, tearoff=0)
        # TODO: view rules
        options_menu.add_command(label="Scores", command=self.view_scores)
        # TODO: settings (e.g. always start with PLAYER_ONE)

        # Add the menus to menu bar
        menu_bar.add_cascade(label="New", menu=new_menu)
        menu_bar.add_cascade(label="Options", menu=options_menu)
        self.root.config(menu=menu_bar)

    def create_board(self):
        # Use board sizes to create board
        self.board = [[None for c in range(self.col_size)] for r in range(self.row_size)]

    def populate_game_elements(self):
        if self.board is None:
            return

        # Populate the required UI widgets
        for r in range(self.row_size):
            for c in range(self.col_size):
                self.board[r][c] = Cell(self, row=r, col=c)

    def board_to_matrix(self) -> np.ndarray:
        # Create numpy array
        arr = np.arange(self.row_size * self.col_size).reshape(self.row_size, self.col_size)

        # Copy enum value from board's Cells into array
        for r in range(self.row_size):
            for c in range(self.col_size):
                arr[r][c] = self.board[r][c].occupied_by.value

        # print("Current Board:\n", arr)  # DEBUG
        return arr

    def check_for_winner(self) -> int:
        board_matrix = self.board_to_matrix()
        for p in Player:
            if p == Player.NO_PLAYER:
                continue

            # Mask current board with player enum value (False for non-player cells)
            player_matrix = np.isin(board_matrix, p.value)

            # Check for matches with any winning_matrices
            # Loop through every element in player_matrix
            for r in range(player_matrix.shape[0]):
                for c in range(player_matrix.shape[1]):

                    # Check for each possible winning matrix
                    for win_matrix in self.winning_matrices:

                        # Slice player_matrix according to shape of win_matrix
                        sliced_matrix = player_matrix[r:r + win_matrix.shape[0], c:c + win_matrix.shape[1]]
                        if sliced_matrix.shape != win_matrix.shape:  # Ignore sliced_matrix of incorrect shape
                            continue

                        result_matrix = np.logical_and(sliced_matrix, win_matrix)

                        # Player has won game if fully match with win_matrix
                        if result_matrix.all():
                            return p.value

        return Player.NO_PLAYER.value

    def board_is_full(self) -> bool:
        return np.all(self.board_to_matrix())

    def next_player_turn(self):
        if self.current_player == Player.PLAYER_ONE:
            self.current_player = Player.PLAYER_TWO
        elif self.current_player == Player.PLAYER_TWO:
            self.current_player = Player.PLAYER_ONE
        else:
            raise ValueError("self.current_player is invalid state")

    def reset_game(self):
        self.board = None
        self.game_active = False
        self.current_player = Player.NO_PLAYER
        self.start_game()

    def view_scores(self):
        scores_text = ""
        for score_key in self.scores.keys():
            scores_text += score_key + ": " + str(self.scores[score_key]) + "\n"

        tk.messagebox.showinfo(title="Scores", message=scores_text)


class Cell:
    col = int
    row = int
    occupied_by = Player.NO_PLAYER
    btn_widget = None
    string_text = None

    def __init__(self, game_instance: TicTacToe, row: int, col: int):
        self.row = row
        self.col = col
        self.string_text = tk.StringVar()
        self.string_text.set(" ")
        self.btn_widget = tk.Button(game_instance.root,
                                    textvariable=self.string_text,
                                    command=lambda: self.player_select_cell(game_instance),
                                    borderwidth=1)
        self.btn_widget.grid(row=self.row, column=self.col, padx=1, pady=1, sticky='NSEW')

        # Makes cells to resize according to window size
        game_instance.root.rowconfigure(self.row, weight=1)
        game_instance.root.columnconfigure(self.col, weight=1)

    def player_select_cell(self, game_instance: TicTacToe):

        # Do nothing if game is not active
        if not game_instance.game_active:
            return

        # Cell is already occupied
        if self.occupied_by != Player.NO_PLAYER:
            print("Cell Occupied!")
            tk.messagebox.showwarning(title="Invalid", message="Sorry, space already occupied")
            return

        # Current player chooses this cell
        self.occupied_by = game_instance.current_player
        self.string_text.set(self.occupied_by.string)

        # Change player
        game_instance.next_player_turn()  # for 2-player mode

        # Check for winner
        winner = game_instance.check_for_winner()
        if Player(winner) != Player.NO_PLAYER:
            game_instance.scores['Player ' + Player(winner).string] += 1  # Update score
            game_instance.game_active = False  # End game

            win_msg = "Player " + Player(winner).string + " won.\nNew Game?"
            start_new_game = tk.messagebox.askyesno(title="You Win", message=win_msg)
            if start_new_game:
                game_instance.reset_game()

        # Check if game has finished (i.e. all cells filled)
        if game_instance.board_is_full():
            game_instance.scores['Draw'] += 1  # Update score
            game_instance.game_active = False  # End game

            start_new_game = tk.messagebox.askyesno(title="Game Finished", message="No empty space left.\nNew Game?")
            if start_new_game:
                game_instance.reset_game()


if __name__ == "__main__":
    app = TicTacToe(tk.Tk())
    app.mainloop()
