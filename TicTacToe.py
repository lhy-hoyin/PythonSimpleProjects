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
    current_player = Player.NO_PLAYER

    def __init__(self, root: tk.Frame = None):
        super().__init__(root)

        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.minsize(300, 300)
        # FIXME: set window name (to appear at taskbar)

        # Ensure min board size of 3x3
        self.row_size = 3 if self.row_size < 3 else self.row_size
        self.col_size = 3 if self.col_size < 3 else self.col_size
        smaller_side = min(self.row_size, self.col_size)
        self.win_requirement = smaller_side if self.win_requirement > smaller_side else self.win_requirement

        self.start_game()

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
        # TODO: view score
        # TODO: settings

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

        print(arr)  # DEBUG
        return arr

    def check_for_winner(self) -> int:
        # TODO
        self.board_to_matrix()
        pass

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
        self.btn_widget.grid(row=self.row, column=self.col, padx=1, pady=1, sticky='NSWE')

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

        # DEBUG
        print("Cell: ", self.row, self.col)
        print("Player:", game_instance.current_player, game_instance.current_player.value)

        # TODO: Check for winning condition

        # Check if game has finished (i.e. all cells filled)
        if game_instance.board_is_full():
            game_instance.game_active = False
            start_new_game = tk.messagebox.askyesno(title="Game Finished", message="No empty space left.\nNew Game?")
            if start_new_game:
                game_instance.reset_game()

        # Change player
        game_instance.next_player_turn()  # for 2-player mode


if __name__ == "__main__":
    app = TicTacToe(tk.Tk())
    app.mainloop()
