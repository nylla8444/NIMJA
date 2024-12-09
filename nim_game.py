import tkinter as tk
from tkinter import messagebox
from nim_ai import NimAI
from nim_helper import NimHelper

class NimGame:
    """
    Implementation of the Nim game using multiple AI algorithms:

    Algorithms Used:
    1. Nim-sum calculation - XOR operation for optimal play
    2. Alpha-Beta Pruning - For game tree search optimization
    3. Position evaluation - Strategic scoring of game states
    4. Minimax - For adversarial search in game tree

    Game Modes:
    - PvP (Player vs Player)
    - PvAI (Player vs AI)

    Game Types:
    - Normal Nim (Last to move wins)
    - Misère Nim (Last to move loses)
    """

    def __init__(self, master):
        self.master = master
        self.master.title("Nim Game")
        self.rows = [1, 3, 5, 7]  # Standard Nim configuration
        self.current_player = 1
        self.mode = None
        self.game_type = None  # 'normal' or 'misere'
        self.ai = NimAI()
        self.helper_window = None  # Store helper window reference
        self.create_mode_selection_screen()

    def create_mode_selection_screen(self):
        # Clear existing widgets first
        self.clear_main_screen()

        # Mode selection screen
        self.mode_label = tk.Label(self.master, text="Select Game Mode:", font=("Arial", 14))
        self.mode_label.pack(pady=20)

        self.pvp_button = tk.Button(self.master, text="Player vs Player", command=self.set_pvp_mode)
        self.pvp_button.pack(pady=10)

        self.pvai_button = tk.Button(self.master, text="Player vs AI", command=self.set_pvai_mode)
        self.pvai_button.pack(pady=10)

        # Add helper button
        self.helper_button = tk.Button(self.master, text="Strategy Helper",
                                       command=self.show_helper)
        self.helper_button.pack(pady=10)

    def show_helper(self):
        """Opens the strategy helper window if not already open"""
        if not self.helper_window or not self.helper_window.winfo_exists():
            self.helper_window = NimHelper(self.master)

    def clear_main_screen(self):
        """Clear main screen widgets while preserving helper"""
        for widget in self.master.winfo_children():
            if not isinstance(widget, tk.Toplevel):  # Don't destroy helper window
                widget.destroy()

    def create_game_type_screen(self):
        self.clear_main_screen()

        # Create back button frame for top-left positioning
        back_frame = tk.Frame(self.master)
        back_frame.pack(anchor='nw', padx=10, pady=5)

        # Add back button
        back_button = tk.Button(back_frame, text="← Back",
                                command=self.create_mode_selection_screen)
        back_button.pack()

        # Game type selection screen
        self.type_label = tk.Label(self.master, text="Select Game Type:", font=("Arial", 14))
        self.type_label.pack(pady=20)

        self.normal_button = tk.Button(self.master, text="Normal Nim\n(Last to move wins)",
                                       command=lambda: self.set_game_type('normal'))
        self.normal_button.pack(pady=10)

        self.misere_button = tk.Button(self.master, text="Misère Nim\n(Last to move loses)",
                                       command=lambda: self.set_game_type('misere'))
        self.misere_button.pack(pady=10)

    def set_game_type(self, type_):
        self.game_type = type_
        self.create_game_screen()

    def create_game_screen(self):
        self.clear_main_screen()
        # Game Board
        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack(pady=20)
        self.update_board()

        # Player action frame
        self.action_frame = tk.Frame(self.master)
        self.action_frame.pack()

        self.row_label = tk.Label(self.action_frame, text="Select Row:")
        self.row_label.grid(row=0, column=0)

        self.row_entry = tk.Entry(self.action_frame, width=5)
        self.row_entry.grid(row=0, column=1)

        self.amount_label = tk.Label(self.action_frame, text="Amount to Remove:")
        self.amount_label.grid(row=1, column=0)

        self.amount_entry = tk.Entry(self.action_frame, width=5)
        self.amount_entry.grid(row=1, column=1)

        self.submit_button = tk.Button(self.action_frame, text="Submit Move", command=self.make_move)
        self.submit_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Status Label
        self.status_label = tk.Label(self.master, text=f"Player {self.current_player}'s turn", font=("Arial", 12))
        self.status_label.pack(pady=10)

        # Move Log
        self.log_label = tk.Label(self.master, text="", font=("Arial", 10), fg="blue")
        self.log_label.pack(pady=5)

    def update_board(self):
        """
        Updates the visual game board using Tkinter widgets.
        Displays rows in pyramid formation with row numbers and objects.
        """
        # Clear the current board
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        # Display rows as a pyramid with row numbers
        for i, row in enumerate(self.rows):
            # Create frame for each row's display elements
            row_frame = tk.Frame(self.board_frame)
            row_frame.pack()

            # Add row identifier label
            row_label = tk.Label(row_frame, text=f"Row {i + 1}: ", font=("Courier", 14))
            row_label.pack(side=tk.LEFT)

            # Display objects in row using 'O' characters
            objects = tk.Label(row_frame, text="O " * row, font=("Courier", 14))
            objects.pack(side=tk.LEFT)

    def set_pvp_mode(self):
        """Sets game mode to Player vs Player and creates game type selection screen."""
        self.mode = "PvP"
        self.create_game_type_screen()

    def set_pvai_mode(self):
        """Sets game mode to Player vs AI and creates game type selection screen."""
        self.mode = "PvAI"
        self.create_game_type_screen()

    def make_move(self):
        """
        Processes a player's move using the following algorithm:
        1. Input validation
        2. Move application
        3. Win condition check
        4. Player switching
        5. AI move triggering (if in PvAI mode)

        Uses exception handling for input validation.
        """
        try:
            # Convert input to zero-based row index
            row = int(self.row_entry.get()) - 1
            amount = int(self.amount_entry.get())

            # Validate row bounds
            if row < 0 or row >= len(self.rows):
                raise ValueError("Invalid row number.")

            # Validate amount bounds
            if amount <= 0 or amount > self.rows[row]:
                raise ValueError("Invalid amount to remove.")

            # Apply move to game state
            self.rows[row] -= amount  # Update row state
            self.update_board()

            # Log the move
            self.log_label.config(text=f"Player {self.current_player} removed {amount} objects from Row {row + 1}.")

            # Clear input fields
            self.row_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)

            # Check for game over with correct win conditions
            if all(r == 0 for r in self.rows):
                if self.mode == "PvP":
                    if self.game_type == 'normal':
                        # In normal mode, current player wins by taking last object
                        winner = f"Player {self.current_player}"
                    else:  # misere
                        # In misere mode, current player loses by taking last object
                        winner = f"Player {2 if self.current_player == 1 else 1}"
                else:  # PvAI mode
                    if self.current_player == 1:  # Human player made last move
                        if self.game_type == 'normal':
                            winner = "Player 1"  # Human wins in normal mode
                        else:  # misere
                            winner = "AI"  # Human loses in misere mode
                    else:  # AI made last move
                        if self.game_type == 'normal':
                            winner = "AI"  # AI wins in normal mode
                        else:  # misere
                            winner = "Player 1"  # AI loses in misere mode

                messagebox.showinfo("Game Over", f"{winner} wins!")
                self.master.destroy()
                return

            # Switch players
            self.current_player = 2 if self.current_player == 1 else 1
            self.status_label.config(text=f"Player {self.current_player}'s turn")

            # AI move if in PvAI mode
            if self.mode == "PvAI" and self.current_player == 2:
                self.ai_move()

        except ValueError as e:
            messagebox.showerror("Invalid Move", str(e))

    def ai_move(self):
        try:
            best_move = self.ai.get_best_move(self.rows, self.game_type)
            if best_move:
                row, amount = best_move
                self.rows[row] -= amount
                self.log_label.config(text=f"AI removed {amount} objects from Row {row + 1}.")

            self.update_board()

            if all(r == 0 for r in self.rows):
                if self.game_type == 'normal':
                    winner = "AI"  # In normal mode, AI wins by taking last object
                else:  # misere
                    winner = "Player 1"  # In misere mode, AI loses by taking last object
                messagebox.showinfo("Game Over", f"{winner} wins!")
                self.master.destroy()
            else:
                self.current_player = 1
                self.status_label.config(text="Player 1's turn")

        except Exception as e:
            messagebox.showerror("AI Error", str(e))

    def get_possible_moves(self, rows):
        """
        Algorithm: State Space Search
        Purpose: Generate all valid moves for the current position.
        Used as part of Minimax and Alpha-Beta search space generation.
        Complexity: O(n*m) where n is number of rows, m is max objects in a row
        """
        moves = []
        for i, r in enumerate(rows):
            if r > 0:  # Only consider rows with objects
                for amount in range(1, r + 1):
                    moves.append((i, amount))
        return moves

    def apply_move(self, rows, move):
        """
        State transition function for game tree search algorithms.
        Used in both Minimax and Alpha-Beta pruning.
        """
        new_rows = rows.copy()
        row, amount = move
        new_rows[row] -= amount
        return new_rows
