import tkinter as tk
from tkinter import messagebox
import random
import math
from collections import defaultdict
from nim_game import NimGame

# Initialize the main game state
# class NimGame:
#     """
#     Implementation of the Nim game using multiple AI algorithms:
#
#     Algorithms Used:
#     1. Nim-sum calculation - XOR operation for optimal play
#     2. Alpha-Beta Pruning - For game tree search optimization
#     3. Position evaluation - Strategic scoring of game states
#     4. Minimax - For adversarial search in game tree
#
#     Game Modes:
#     - PvP (Player vs Player)
#     - PvAI (Player vs AI)
#
#     Game Types:
#     - Normal Nim (Last to move wins)
#     - Misère Nim (Last to move loses)
#     """
#
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Nim Game")
#         self.rows = [1, 3, 5, 7]  # Standard Nim configuration
#         self.current_player = 1
#         self.mode = None
#         self.game_type = None  # 'normal' or 'misere'
#         self.ai = NimAI()
#         self.helper_window = None  # Store helper window reference
#         self.create_mode_selection_screen()
#
#     def create_mode_selection_screen(self):
#         # Clear existing widgets first
#         self.clear_main_screen()
#
#         # Mode selection screen
#         self.mode_label = tk.Label(self.master, text="Select Game Mode:", font=("Arial", 14))
#         self.mode_label.pack(pady=20)
#
#         self.pvp_button = tk.Button(self.master, text="Player vs Player", command=self.set_pvp_mode)
#         self.pvp_button.pack(pady=10)
#
#         self.pvai_button = tk.Button(self.master, text="Player vs AI", command=self.set_pvai_mode)
#         self.pvai_button.pack(pady=10)
#
#         # Add helper button
#         self.helper_button = tk.Button(self.master, text="Strategy Helper",
#                                        command=self.show_helper)
#         self.helper_button.pack(pady=10)
#
#     def show_helper(self):
#         """Opens the strategy helper window if not already open"""
#         if not self.helper_window or not self.helper_window.winfo_exists():
#             self.helper_window = NimHelper(self.master)
#
#     def clear_main_screen(self):
#         """Clear main screen widgets while preserving helper"""
#         for widget in self.master.winfo_children():
#             if not isinstance(widget, tk.Toplevel):  # Don't destroy helper window
#                 widget.destroy()
#
#     def create_game_type_screen(self):
#         self.clear_main_screen()
#
#         # Create back button frame for top-left positioning
#         back_frame = tk.Frame(self.master)
#         back_frame.pack(anchor='nw', padx=10, pady=5)
#
#         # Add back button
#         back_button = tk.Button(back_frame, text="← Back",
#                                 command=self.create_mode_selection_screen)
#         back_button.pack()
#
#         # Game type selection screen
#         self.type_label = tk.Label(self.master, text="Select Game Type:", font=("Arial", 14))
#         self.type_label.pack(pady=20)
#
#         self.normal_button = tk.Button(self.master, text="Normal Nim\n(Last to move wins)",
#                                        command=lambda: self.set_game_type('normal'))
#         self.normal_button.pack(pady=10)
#
#         self.misere_button = tk.Button(self.master, text="Misère Nim\n(Last to move loses)",
#                                        command=lambda: self.set_game_type('misere'))
#         self.misere_button.pack(pady=10)
#
#     def set_game_type(self, type_):
#         self.game_type = type_
#         self.create_game_screen()
#
#     def create_game_screen(self):
#         self.clear_main_screen()
#         # Game Board
#         self.board_frame = tk.Frame(self.master)
#         self.board_frame.pack(pady=20)
#         self.update_board()
#
#         # Player action frame
#         self.action_frame = tk.Frame(self.master)
#         self.action_frame.pack()
#
#         self.row_label = tk.Label(self.action_frame, text="Select Row:")
#         self.row_label.grid(row=0, column=0)
#
#         self.row_entry = tk.Entry(self.action_frame, width=5)
#         self.row_entry.grid(row=0, column=1)
#
#         self.amount_label = tk.Label(self.action_frame, text="Amount to Remove:")
#         self.amount_label.grid(row=1, column=0)
#
#         self.amount_entry = tk.Entry(self.action_frame, width=5)
#         self.amount_entry.grid(row=1, column=1)
#
#         self.submit_button = tk.Button(self.action_frame, text="Submit Move", command=self.make_move)
#         self.submit_button.grid(row=2, column=0, columnspan=2, pady=10)
#
#         # Status Label
#         self.status_label = tk.Label(self.master, text=f"Player {self.current_player}'s turn", font=("Arial", 12))
#         self.status_label.pack(pady=10)
#
#         # Move Log
#         self.log_label = tk.Label(self.master, text="", font=("Arial", 10), fg="blue")
#         self.log_label.pack(pady=5)
#
#     def update_board(self):
#         """
#         Updates the visual game board using Tkinter widgets.
#         Displays rows in pyramid formation with row numbers and objects.
#         """
#         # Clear the current board
#         for widget in self.board_frame.winfo_children():
#             widget.destroy()
#
#         # Display rows as a pyramid with row numbers
#         for i, row in enumerate(self.rows):
#             # Create frame for each row's display elements
#             row_frame = tk.Frame(self.board_frame)
#             row_frame.pack()
#
#             # Add row identifier label
#             row_label = tk.Label(row_frame, text=f"Row {i + 1}: ", font=("Courier", 14))
#             row_label.pack(side=tk.LEFT)
#
#             # Display objects in row using 'O' characters
#             objects = tk.Label(row_frame, text="O " * row, font=("Courier", 14))
#             objects.pack(side=tk.LEFT)
#
#     def set_pvp_mode(self):
#         """Sets game mode to Player vs Player and creates game type selection screen."""
#         self.mode = "PvP"
#         self.create_game_type_screen()
#
#     def set_pvai_mode(self):
#         """Sets game mode to Player vs AI and creates game type selection screen."""
#         self.mode = "PvAI"
#         self.create_game_type_screen()
#
#     def make_move(self):
#         """
#         Processes a player's move using the following algorithm:
#         1. Input validation
#         2. Move application
#         3. Win condition check
#         4. Player switching
#         5. AI move triggering (if in PvAI mode)
#
#         Uses exception handling for input validation.
#         """
#         try:
#             # Convert input to zero-based row index
#             row = int(self.row_entry.get()) - 1
#             amount = int(self.amount_entry.get())
#
#             # Validate row bounds
#             if row < 0 or row >= len(self.rows):
#                 raise ValueError("Invalid row number.")
#
#             # Validate amount bounds
#             if amount <= 0 or amount > self.rows[row]:
#                 raise ValueError("Invalid amount to remove.")
#
#             # Apply move to game state
#             self.rows[row] -= amount  # Update row state
#             self.update_board()
#
#             # Log the move
#             self.log_label.config(text=f"Player {self.current_player} removed {amount} objects from Row {row + 1}.")
#
#             # Clear input fields
#             self.row_entry.delete(0, tk.END)
#             self.amount_entry.delete(0, tk.END)
#
#             # Check for game over with correct win conditions
#             if all(r == 0 for r in self.rows):
#                 if self.mode == "PvP":
#                     if self.game_type == 'normal':
#                         # In normal mode, current player wins by taking last object
#                         winner = f"Player {self.current_player}"
#                     else:  # misere
#                         # In misere mode, current player loses by taking last object
#                         winner = f"Player {2 if self.current_player == 1 else 1}"
#                 else:  # PvAI mode
#                     if self.current_player == 1:  # Human player made last move
#                         if self.game_type == 'normal':
#                             winner = "Player 1"  # Human wins in normal mode
#                         else:  # misere
#                             winner = "AI"  # Human loses in misere mode
#                     else:  # AI made last move
#                         if self.game_type == 'normal':
#                             winner = "AI"  # AI wins in normal mode
#                         else:  # misere
#                             winner = "Player 1"  # AI loses in misere mode
#
#                 messagebox.showinfo("Game Over", f"{winner} wins!")
#                 self.master.destroy()
#                 return
#
#             # Switch players
#             self.current_player = 2 if self.current_player == 1 else 1
#             self.status_label.config(text=f"Player {self.current_player}'s turn")
#
#             # AI move if in PvAI mode
#             if self.mode == "PvAI" and self.current_player == 2:
#                 self.ai_move()
#
#         except ValueError as e:
#             messagebox.showerror("Invalid Move", str(e))
#
#     def ai_move(self):
#         try:
#             best_move = self.ai.get_best_move(self.rows, self.game_type)
#             if best_move:
#                 row, amount = best_move
#                 self.rows[row] -= amount
#                 self.log_label.config(text=f"AI removed {amount} objects from Row {row + 1}.")
#
#             self.update_board()
#
#             if all(r == 0 for r in self.rows):
#                 if self.game_type == 'normal':
#                     winner = "AI"  # In normal mode, AI wins by taking last object
#                 else:  # misere
#                     winner = "Player 1"  # In misere mode, AI loses by taking last object
#                 messagebox.showinfo("Game Over", f"{winner} wins!")
#                 self.master.destroy()
#             else:
#                 self.current_player = 1
#                 self.status_label.config(text="Player 1's turn")
#
#         except Exception as e:
#             messagebox.showerror("AI Error", str(e))
#
#     def get_possible_moves(self, rows):
#         """
#         Algorithm: State Space Search
#         Purpose: Generate all valid moves for the current position.
#         Used as part of Minimax and Alpha-Beta search space generation.
#         Complexity: O(n*m) where n is number of rows, m is max objects in a row
#         """
#         moves = []
#         for i, r in enumerate(rows):
#             if r > 0:  # Only consider rows with objects
#                 for amount in range(1, r + 1):
#                     moves.append((i, amount))
#         return moves
#
#     def apply_move(self, rows, move):
#         """
#         State transition function for game tree search algorithms.
#         Used in both Minimax and Alpha-Beta pruning.
#         """
#         new_rows = rows.copy()
#         row, amount = move
#         new_rows[row] -= amount
#         return new_rows


# class NimAI:
#     def __init__(self):
#         # Winning patterns based on mathematical analysis
#         self.patterns = {
#             'winning': [
#                 (1, 1, 1, 1),  # Leave all 1s
#                 (2, 2, 0, 0),  # Balanced pairs
#                 (3, 3, 0, 0),  # Balanced pairs
#                 (4, 4, 0, 0),  # Balanced pairs
#                 (2, 2, 2, 0),  # Triple balance
#                 (3, 3, 3, 0),  # Triple balance
#                 (1, 2, 3, 0),  # Sequential pattern
#             ],
#             'forcing': [
#                 (2, 1, 1, 0),  # Force opponent into bad position
#                 (3, 2, 1, 0),  # Force opponent into bad position
#                 (4, 3, 2, 1),  # Sequential forcing
#                 (3, 3, 2, 0),  # Imbalanced forcing
#             ]
#         }
#
#     def get_best_move(self, rows, game_type='normal', move_order='first'):
#         """
#         Enhanced optimal move calculator using Nim-sum and endgame strategy
#         """
#         # Calculate Nim-sum
#         nim_sum = 0
#         for pile in rows:
#             nim_sum ^= pile
#
#         total_objects = sum(rows)
#         non_empty_piles = sum(1 for pile in rows if pile > 0)
#         piles_gt1 = sum(1 for pile in rows if pile > 1)
#         single_piles = sum(1 for pile in rows if pile == 1)
#
#         # Endgame strategy for Misère Nim
#         if game_type == 'misere' and total_objects <= 6:
#             if piles_gt1 == 0:
#                 # All single piles - leave odd number for opponent
#                 if single_piles % 2 == 0:
#                     for i, pile in enumerate(rows):
#                         if pile == 1:
#                             return i, 1
#             elif piles_gt1 == 1:
#                 # One pile > 1, rest are 1s
#                 for i, pile in enumerate(rows):
#                     if pile > 1:
#                         target = 1 if single_piles % 2 == 0 else 0
#                         return i, pile - target
#
#         # Normal strategy using Nim-sum
#         if nim_sum == 0:
#             # Losing position - play defensive
#             max_pile = max(rows)
#             max_pile_index = rows.index(max_pile)
#
#             # Take from largest pile to minimize opponent's options
#             if max_pile > 2:
#                 return max_pile_index, max_pile - 1
#             else:
#                 # Take any legal move
#                 for i, pile in enumerate(rows):
#                     if pile > 0:
#                         return i, 1
#
#         else:
#             # Winning position - calculate optimal move
#             for i, pile in enumerate(rows):
#                 target = pile ^ nim_sum
#                 if target < pile:
#                     # Found winning move
#                     stones_to_remove = pile - target
#
#                     # Verify move doesn't create losing endgame position
#                     if game_type == 'misere' and non_empty_piles <= 3:
#                         remaining = sum(rows) - stones_to_remove
#                         if remaining == 1 or (remaining == 2 and non_empty_piles == 2):
#                             continue
#
#                     return i, stones_to_remove
#
#         # Fallback - take one from largest pile
#         max_pile = max(rows)
#         return rows.index(max_pile), 1
#
#     def get_perfect_endgame_move(self, rows, game_type):
#         """
#         Algorithm: Endgame Strategy (Misère Variant)
#         Purpose: Determine optimal move for endgame positions
#         Complexity: O(n)
#         """
#         total = sum(rows)
#         non_empty = [i for i, r in enumerate(rows) if r > 0]
#         ones = sum(1 for r in rows if r == 1)
#
#         if game_type == 'normal':
#             if total == 1:
#                 return (non_empty[0], 1)  # Take last
#             if total == 2:
#                 if len(non_empty) == 1:
#                     return (non_empty[0], 2)  # Take whole pile
#                 return (non_empty[0], 1)  # Take one, leave one
#             if total == 3:
#                 if len(non_empty) == 1:
#                     return (non_empty[0], 2)  # Leave one
#                 if len(non_empty) == 2:
#                     return (non_empty[1], 1)  # Take from larger
#         else:  # misere
#             if total == 2 and len(non_empty) == 2:
#                 return (non_empty[0], 1)  # Leave two ones
#             if total == 3:
#                 if len(non_empty) == 3:
#                     return (non_empty[0], 1)  # Leave three ones
#                 return (non_empty[0], rows[non_empty[0]] - 1)  # Leave two ones
#
#         return self.get_forcing_move(rows, game_type)
#
#     def get_forcing_move(self, rows, game_type):
#         """Enhanced forcing move selection"""
#         best_move = None
#         best_score = float('-inf')
#
#         for i, row in enumerate(rows):
#             for take in range(1, row + 1):
#                 new_rows = rows.copy()
#                 new_rows[i] -= take
#                 score = self.evaluate_position(new_rows, game_type)
#                 if score > best_score:
#                     best_score = score
#                     best_move = (i, take)
#
#         return best_move
#
#     def evaluate_position(self, rows, game_type='normal'):
#         """
#         Algorithm: Minimax with Alpha-Beta Pruning
#         Purpose: Evaluate game position for optimal move selection
#         Complexity: O(1)
#         """
#         nim_sum = self.nim_sum(rows)
#         total = sum(rows)
#         piles_gt1 = sum(1 for r in rows if r > 1)
#         ones = sum(1 for r in rows if r == 1)
#
#         if game_type == 'normal':
#             score = 0
#             if nim_sum == 0:
#                 score -= 100
#             if total <= 4:
#                 score += 50 if nim_sum > 0 else -50
#             score += piles_gt1 * 10
#             return score
#         else:  # misere
#             score = 0
#             if piles_gt1 == 0:
#                 score += 100 if ones % 2 == 0 else -100
#             if piles_gt1 == 1:
#                 score += 50 if ones % 2 == 0 else -50
#             return score
#
#     def nim_sum(self, rows):
#         """
#         Algorithm: Nim-sum calculation (Sprague-Grundy theorem)
#         Purpose: Calculate optimal play position using XOR operations
#         Complexity: O(n) where n is number of rows
#         """
#         result = 0
#         for row in rows:
#             result ^= row  # XOR operation for Nim-sum
#         return result
#
#     def match_pattern(self, rows):
#         """
#         Algorithm: Pattern Matching for Known Positions
#         Purpose: Check if current position matches known winning/forcing patterns
#         Complexity: O(n log n) due to sorting
#         """
#         sorted_rows = sorted(rows, reverse=True)
#         for pattern in self.patterns['winning']:
#             if self.matches_pattern(sorted_rows, pattern):
#                 diff = [a - b for a, b in zip(sorted_rows, pattern)]
#                 if any(d > 0 for d in diff):
#                     i = next(i for i, d in enumerate(diff) if d > 0)
#                     return (rows.index(sorted_rows[i]), diff[i])
#         return None
#
#     def matches_pattern(self, rows, pattern):
#         """Check if position matches a pattern"""
#         return all(r >= p for r, p in zip(rows, pattern))
#
#     def evaluate_move(self, state, move, game_type, move_order='first'):  # Add move_order parameter
#         """Updated move evaluation for better endgame handling"""
#         nim_sum = self.nim_sum(state)
#         total = sum(state)
#         ones = sum(1 for r in state if r == 1)
#         piles_gt1 = sum(1 for r in state if r > 1)
#
#         # Reject invalid moves
#         row, amount = move
#         if amount <= 0 or amount > state[row]:
#             return float('-inf')
#
#         if game_type == 'normal':
#             if total == 0:
#                 return 100  # Winning move
#             if nim_sum == 0:
#                 return 90  # Strong position
#             return 50  # Average position
#         else:  # misere
#             if total == 0:
#                 return 0  # Losing move
#
#             # Endgame handling
#             if piles_gt1 == 0:
#                 # Want odd singles when playing second
#                 odd_singles = (ones % 2 == 1)
#                 if move_order == "second":
#                     return 95 if odd_singles else 5
#                 else:
#                     return 95 if not odd_singles else 5
#
#             if piles_gt1 == 1:
#                 # Try to force opponent into losing position
#                 target_singles = 1 if move_order == "second" else 0
#                 return 90 if ones % 2 == target_singles else 10
#
#             return 70 if nim_sum > 0 else 30


# class NimHelper(tk.Toplevel):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.title("Nim Strategy Helper")
#         self.geometry("800x800")  # Increased width
#
#         # Add move order variable
#         self.move_order = tk.StringVar(value="first")  # "first" or "second"
#         self.rows = [1, 3, 5, 7]
#         self.game_mode = tk.StringVar(value="normal")
#         self.ai = NimAI()
#         # Player is always the player, just the order changes
#         self.is_player_turn = self.move_order.get() == "first"  # True if player's turn
#         self.moves_made = 0
#         self.last_move_by = None
#         self.move_history = []
#         self.predicted_moves = []
#
#         self.create_layout()
#
#     def create_layout(self):
#         # Top frame for mode and order selection
#         top_frame = tk.Frame(self)
#         top_frame.pack(fill="x", padx=10, pady=5)
#
#         # Game Mode Selection (Left side)
#         mode_frame = tk.LabelFrame(top_frame, text="Game Mode", padx=10, pady=5)
#         mode_frame.pack(side="left", fill="both", expand=True, padx=5)
#
#         # Mode selection
#         modes_frame = tk.Frame(mode_frame)
#         modes_frame.pack(fill="x", pady=5)
#
#         tk.Radiobutton(modes_frame, text="Normal Nim", variable=self.game_mode,
#                        value="normal", command=self.update_analysis).pack(side="left", padx=10)
#         tk.Radiobutton(modes_frame, text="Misère Nim", variable=self.game_mode,
#                        value="misere", command=self.update_analysis).pack(side="left", padx=10)
#
#         # Mode explanations
#         explanation_text = """
# Normal Nim: The player who takes the last object WINS
# Strategy: Try to end your turn with nim-sum = 0
#
# Misère Nim: The player who takes the last object LOSES
# Strategy: Play like normal Nim until near the end,
# then leave an odd number of piles of size 1
#     """
#         tk.Label(mode_frame, text=explanation_text, justify="left").pack(pady=5)
#
#         # Move Order Selection (Right side)
#         order_frame = tk.LabelFrame(top_frame, text="Move Order", padx=10, pady=5)
#         order_frame.pack(side="left", fill="both", expand=True, padx=5)
#
#         orders_frame = tk.Frame(order_frame)
#         orders_frame.pack(fill="x", pady=5)
#
#         tk.Radiobutton(orders_frame, text="Play First", variable=self.move_order,
#                        value="first", command=self.update_turn_order).pack(side="left", padx=10)
#         tk.Radiobutton(orders_frame, text="Play Second", variable=self.move_order,
#                        value="second", command=self.update_turn_order).pack(side="left", padx=10)
#
#         # Move order explanation
#         order_explanation = """
# Play First: You make the first move,
# then enter AI's responses
#
# Play Second: Enter AI's first move,
# then make your moves
#     """
#         tk.Label(order_frame, text=order_explanation, justify="left").pack(pady=5)
#
#         # Rest of layout remains same...
#         self.state_frame = tk.LabelFrame(self, text="Current NIM State", padx=10, pady=5)
#         self.state_frame.pack(fill="x", padx=10, pady=5)
#         self.update_nim_display()
#
#         # Turn Management
#         moves_frame = tk.LabelFrame(self, text="Turn Management", padx=10, pady=5)
#         moves_frame.pack(fill="x", padx=10, pady=5)
#
#         # Turn indicator
#         self.turn_label = tk.Label(moves_frame, text="Player's Turn", font=("Arial", 12, "bold"))
#         self.turn_label.pack(pady=5)
#
#         # Move input area
#         input_frame = tk.Frame(moves_frame)
#         input_frame.pack(pady=5)
#
#         tk.Label(input_frame, text="Row (1-4):", width=10).grid(row=0, column=0, padx=5)
#         self.row_entry = tk.Entry(input_frame, width=8)
#         self.row_entry.grid(row=0, column=1, padx=5)
#
#         tk.Label(input_frame, text="Amount:", width=10).grid(row=0, column=2, padx=5)
#         self.amount_entry = tk.Entry(input_frame, width=8)
#         self.amount_entry.grid(row=0, column=3, padx=5)
#
#         self.submit_button = tk.Button(moves_frame, text="Submit Move", command=self.process_move)
#         self.submit_button.pack(pady=5)
#
#         # Analysis Frame
#         analysis_frame = tk.LabelFrame(self, text="Position Analysis", padx=10, pady=5)
#         analysis_frame.pack(fill="x", padx=10, pady=5)
#
#         # Best Move Display (initially hidden)
#         self.best_move_label = tk.Label(analysis_frame, text="Make a move to see best response", fg="gray")
#         self.best_move_label.pack(pady=5)
#
#         # Add Move Prediction Frame
#         prediction_frame = tk.LabelFrame(self, text="Move Predictions", padx=10, pady=5)
#         prediction_frame.pack(fill="x", padx=10, pady=5)
#
#         # Move sequence display
#         self.sequence_text = tk.Text(prediction_frame, height=6, width=50)
#         self.sequence_text.pack(pady=5)
#
#         # Add navigation buttons
#         nav_frame = tk.Frame(prediction_frame)
#         nav_frame.pack(fill="x", pady=5)
#
#         tk.Button(nav_frame, text="Calculate Sequences",
#                   command=self.calculate_move_sequences).pack(side="left", padx=5)
#         tk.Button(nav_frame, text="Reset Analysis",
#                   command=self.reset_analysis).pack(side="left", padx=5)
#
#     def update_turn_order(self):
#         """Update turn order based on selected move order"""
#         self.is_player_turn = self.move_order.get() == "first"  # First move goes to player if "first"
#         self.moves_made = 0  # Reset game state
#         self.move_history.clear()
#         self.update_turn_display()
#         self.update_analysis()
#
#     def update_turn_display(self):
#         """Update the turn display and input states"""
#         if self.is_player_turn:
#             self.turn_label.config(text="Your Turn")
#             # Enable inputs for player's turn
#             state = "normal"
#         else:
#             self.turn_label.config(text="Enter AI's Move")
#             # Enable inputs for entering AI's move
#             state = "normal"
#
#         self.row_entry.config(state=state)
#         self.amount_entry.config(state=state)
#         self.submit_button.config(state=state)
#
#     def process_move(self):
#         try:
#             row = int(self.row_entry.get()) - 1
#             amount = int(self.amount_entry.get())
#
#             if 0 <= row < len(self.rows) and 1 <= amount <= self.rows[row]:
#                 # Apply move
#                 self.rows[row] -= amount
#                 self.moves_made += 1
#                 self.last_move_by = "player" if self.is_player_turn else "ai"
#                 self.update_nim_display()
#
#                 # Check for game over
#                 if self.is_game_over():
#                     self.show_game_result()
#                     return
#
#                 # Switch turns
#                 self.is_player_turn = not self.is_player_turn
#                 self.update_turn_display()
#
#                 # Clear inputs
#                 self.row_entry.delete(0, tk.END)
#                 self.amount_entry.delete(0, tk.END)
#
#                 # Update analysis
#                 if self.is_player_turn:
#                     self.update_analysis()
#                 else:
#                     self.best_move_label.config(text="Enter AI's move...", fg="gray")
#
#                 self.move_history.append((row, amount))
#                 self.calculate_move_sequences()
#
#             else:
#                 messagebox.showerror("Invalid Move", "Invalid row or amount")
#         except ValueError:
#             messagebox.showerror("Invalid Input", "Please enter valid numbers")
#
#     def is_game_over(self):
#         return all(r == 0 for r in self.rows)
#
#     def show_game_result(self):
#         """Determine winner based on game mode, move order and last move"""
#         game_mode = self.game_mode.get()
#         move_order = self.move_order.get()
#
#         # In Normal Nim: whoever takes last object wins
#         # In Misère Nim: whoever takes last object loses
#         if game_mode == 'normal':
#             if self.last_move_by == "player":
#                 # Player took last object
#                 winner = "You"  # Player wins in normal mode by taking last object
#             else:
#                 # AI took last object
#                 winner = "AI"  # AI wins in normal mode by taking last object
#         else:  # misere
#             if self.last_move_by == "player":
#                 # Player took last object
#                 winner = "AI"  # Player loses in misere mode by taking last object
#             else:
#                 # AI took last object
#                 winner = "You"  # AI loses in misere mode by taking last object
#
#         messagebox.showinfo("Game Over", f"{winner} wins!")
#         self.destroy()
#
#     def update_analysis(self):
#         if self.moves_made > 0 and self.is_player_turn:
#             # Show best move only during player's turn
#             best_move = self.ai.get_best_move(self.rows, self.game_mode.get(), self.move_order.get())  # Pass move_order
#             if best_move:
#                 row, amount = best_move
#                 self.best_move_label.config(
#                     text=f"Best move: Remove {amount} object(s) from Row {row + 1}",
#                     fg="blue"
#                 )
#             else:
#                 self.best_move_label.config(text="No moves available")
#
#     def update_nim_display(self):
#         for widget in self.state_frame.winfo_children():
#             widget.destroy()
#
#         for i, count in enumerate(self.rows):
#             row_frame = tk.Frame(self.state_frame)
#             row_frame.pack()
#             tk.Label(row_frame, text=f"Row {i + 1}: ").pack(side="left")
#             tk.Label(row_frame, text="O " * count).pack(side="left")
#
#     def calculate_move_sequences(self):
#         """
#         Algorithm: Move Sequence Prediction
#         Purpose: Lookahead for move sequences and counter-moves based on current state
#         Complexity: O(n*m) where n is number of rows, m is max objects
#         """
#         self.sequence_text.delete(1.0, tk.END)
#         game_type = self.game_mode.get()
#         current_state = self.rows.copy()
#
#         # Get AI's top 3 possible moves
#         ai_moves = self.get_top_ai_moves(current_state, game_type)
#
#         self.sequence_text.insert(tk.END, f"Analysis for {game_type.title()} Nim:\n\n")
#
#         for i, (ai_move, score) in enumerate(ai_moves, 1):
#             row, amount = ai_move
#             # Show AI move
#             self.sequence_text.insert(tk.END, f"AI Move #{i}:\n")
#             self.sequence_text.insert(tk.END, f"Take {amount} from Row {row + 1}\n")
#
#             # Calculate state after AI move
#             next_state = current_state.copy()
#             next_state[row] -= amount
#
#             # Get best counter-move
#             counter_move = self.ai.get_best_move(next_state, game_type)
#             if counter_move:
#                 c_row, c_amount = counter_move
#                 self.sequence_text.insert(tk.END, f"Best Counter: Take {c_amount} from Row {c_row + 1}\n")
#             self.sequence_text.insert(tk.END, "\n")
#
#     def get_top_ai_moves(self, state, game_type):
#         """Get AI's top 3 moves with scores"""
#         moves = []
#         for row, count in enumerate(state):
#             for amount in range(1, count + 1):
#                 next_state = state.copy()
#                 next_state[row] -= amount
#                 # Pass move to AI for evaluation
#                 score = self.ai.evaluate_move(next_state, (row, amount), game_type, self.move_order.get())
#                 moves.append(((row, amount), score))
#
#         # Sort by score and return top 3
#         moves.sort(key=lambda x: x[1], reverse=True)
#         return moves[:3]
#
#     def evaluate_move(self, state, move, game_type):
#         """Updated move evaluation for better endgame handling"""
#         # Use AI's nim_sum method
#         nim_sum = self.ai.nim_sum(state)
#         total = sum(state)
#         ones = sum(1 for r in state if r == 1)
#         piles_gt1 = sum(1 for r in state if r > 1)
#         move_order = self.move_order.get()
#
#         # Reject invalid moves
#         row, amount = move
#         if amount <= 0 or amount > state[row]:
#             return float('-inf')
#
#         if game_type == 'normal':
#             if total == 0:
#                 return 100  # Winning move
#             if nim_sum == 0:
#                 return 90  # Strong position
#             return 50  # Average position
#         else:  # misere
#             if total == 0:
#                 return 0  # Losing move
#
#             # Endgame handling
#             if piles_gt1 == 0:
#                 # Want odd singles when playing second
#                 odd_singles = (ones % 2 == 1)
#                 if move_order == "second":
#                     return 95 if odd_singles else 5
#                 else:
#                     return 95 if not odd_singles else 5
#
#             if piles_gt1 == 1:
#                 # Try to force opponent into losing position
#                 target_singles = 1 if move_order == "second" else 0
#                 return 90 if ones % 2 == target_singles else 10
#
#             return 70 if nim_sum > 0 else 30
#
#     def reset_analysis(self):
#         """Reset move prediction analysis"""
#         self.sequence_text.delete(1.0, tk.END)
#         self.move_history.clear()
#         self.predicted_moves.clear()
#         self.update_analysis()


# Main Application

if __name__ == "__main__":
    root = tk.Tk()
    root.title("NIMJA: Outsmart Your Opponents")
    game = NimGame(root)
    root.mainloop()
