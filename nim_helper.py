import tkinter as tk
from nim_ai import NimAI
from tkinter import messagebox

class NimHelper(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Nim Strategy Helper")
        self.geometry("800x800")  # Increased width

        # Add move order variable
        self.move_order = tk.StringVar(value="first")  # "first" or "second"
        self.rows = [1, 3, 5, 7]
        self.game_mode = tk.StringVar(value="normal")
        self.ai = NimAI()
        # Player is always the player, just the order changes
        self.is_player_turn = self.move_order.get() == "first"  # True if player's turn
        self.moves_made = 0
        self.last_move_by = None
        self.move_history = []
        self.predicted_moves = []

        self.create_layout()

    def create_layout(self):
        # Top frame for mode and order selection
        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", padx=10, pady=5)

        # Game Mode Selection (Left side)
        mode_frame = tk.LabelFrame(top_frame, text="Game Mode", padx=10, pady=5)
        mode_frame.pack(side="left", fill="both", expand=True, padx=5)

        # Mode selection
        modes_frame = tk.Frame(mode_frame)
        modes_frame.pack(fill="x", pady=5)

        tk.Radiobutton(modes_frame, text="Normal Nim", variable=self.game_mode,
                       value="normal", command=self.update_analysis).pack(side="left", padx=10)
        tk.Radiobutton(modes_frame, text="Misère Nim", variable=self.game_mode,
                       value="misere", command=self.update_analysis).pack(side="left", padx=10)

        # Mode explanations
        explanation_text = """
Normal Nim: The player who takes the last object WINS
Strategy: Try to end your turn with nim-sum = 0

Misère Nim: The player who takes the last object LOSES
Strategy: Play like normal Nim until near the end,
then leave an odd number of piles of size 1
    """
        tk.Label(mode_frame, text=explanation_text, justify="left").pack(pady=5)

        # Move Order Selection (Right side)
        order_frame = tk.LabelFrame(top_frame, text="Move Order", padx=10, pady=5)
        order_frame.pack(side="left", fill="both", expand=True, padx=5)

        orders_frame = tk.Frame(order_frame)
        orders_frame.pack(fill="x", pady=5)

        tk.Radiobutton(orders_frame, text="Play First", variable=self.move_order,
                       value="first", command=self.update_turn_order).pack(side="left", padx=10)
        tk.Radiobutton(orders_frame, text="Play Second", variable=self.move_order,
                       value="second", command=self.update_turn_order).pack(side="left", padx=10)

        # Move order explanation
        order_explanation = """
Play First: You make the first move,
then enter AI's responses

Play Second: Enter AI's first move,
then make your moves
    """
        tk.Label(order_frame, text=order_explanation, justify="left").pack(pady=5)

        # Rest of layout remains same...
        self.state_frame = tk.LabelFrame(self, text="Current NIM State", padx=10, pady=5)
        self.state_frame.pack(fill="x", padx=10, pady=5)
        self.update_nim_display()

        # Turn Management
        moves_frame = tk.LabelFrame(self, text="Turn Management", padx=10, pady=5)
        moves_frame.pack(fill="x", padx=10, pady=5)

        # Turn indicator
        self.turn_label = tk.Label(moves_frame, text="Player's Turn", font=("Arial", 12, "bold"))
        self.turn_label.pack(pady=5)

        # Move input area
        input_frame = tk.Frame(moves_frame)
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Row (1-4):", width=10).grid(row=0, column=0, padx=5)
        self.row_entry = tk.Entry(input_frame, width=8)
        self.row_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Amount:", width=10).grid(row=0, column=2, padx=5)
        self.amount_entry = tk.Entry(input_frame, width=8)
        self.amount_entry.grid(row=0, column=3, padx=5)

        self.submit_button = tk.Button(moves_frame, text="Submit Move", command=self.process_move)
        self.submit_button.pack(pady=5)

        # Analysis Frame
        analysis_frame = tk.LabelFrame(self, text="Position Analysis", padx=10, pady=5)
        analysis_frame.pack(fill="x", padx=10, pady=5)

        # Best Move Display (initially hidden)
        self.best_move_label = tk.Label(analysis_frame, text="Make a move to see best response", fg="gray")
        self.best_move_label.pack(pady=5)

        # Add Move Prediction Frame
        prediction_frame = tk.LabelFrame(self, text="Move Predictions", padx=10, pady=5)
        prediction_frame.pack(fill="x", padx=10, pady=5)

        # Move sequence display
        self.sequence_text = tk.Text(prediction_frame, height=6, width=50)
        self.sequence_text.pack(pady=5)

        # Add navigation buttons
        nav_frame = tk.Frame(prediction_frame)
        nav_frame.pack(fill="x", pady=5)

        tk.Button(nav_frame, text="Calculate Sequences",
                  command=self.calculate_move_sequences).pack(side="left", padx=5)
        tk.Button(nav_frame, text="Reset Analysis",
                  command=self.reset_analysis).pack(side="left", padx=5)

    def update_turn_order(self):
        """Update turn order based on selected move order"""
        self.is_player_turn = self.move_order.get() == "first"  # First move goes to player if "first"
        self.moves_made = 0  # Reset game state
        self.move_history.clear()
        self.update_turn_display()
        self.update_analysis()

    def update_turn_display(self):
        """Update the turn display and input states"""
        if self.is_player_turn:
            self.turn_label.config(text="Your Turn")
            # Enable inputs for player's turn
            state = "normal"
        else:
            self.turn_label.config(text="Enter AI's Move")
            # Enable inputs for entering AI's move
            state = "normal"

        self.row_entry.config(state=state)
        self.amount_entry.config(state=state)
        self.submit_button.config(state=state)

    def process_move(self):
        try:
            row = int(self.row_entry.get()) - 1
            amount = int(self.amount_entry.get())

            if 0 <= row < len(self.rows) and 1 <= amount <= self.rows[row]:
                # Apply move
                self.rows[row] -= amount
                self.moves_made += 1
                self.last_move_by = "player" if self.is_player_turn else "ai"
                self.update_nim_display()

                # Check for game over
                if self.is_game_over():
                    self.show_game_result()
                    return

                # Switch turns
                self.is_player_turn = not self.is_player_turn
                self.update_turn_display()

                # Clear inputs
                self.row_entry.delete(0, tk.END)
                self.amount_entry.delete(0, tk.END)

                # Update analysis
                if self.is_player_turn:
                    self.update_analysis()
                else:
                    self.best_move_label.config(text="Enter AI's move...", fg="gray")

                self.move_history.append((row, amount))
                self.calculate_move_sequences()

            else:
                messagebox.showerror("Invalid Move", "Invalid row or amount")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers")

    def is_game_over(self):
        return all(r == 0 for r in self.rows)

    def show_game_result(self):
        """Determine winner based on game mode, move order and last move"""
        game_mode = self.game_mode.get()
        move_order = self.move_order.get()

        # In Normal Nim: whoever takes last object wins
        # In Misère Nim: whoever takes last object loses
        if game_mode == 'normal':
            if self.last_move_by == "player":
                # Player took last object
                winner = "You"  # Player wins in normal mode by taking last object
            else:
                # AI took last object
                winner = "AI"  # AI wins in normal mode by taking last object
        else:  # misere
            if self.last_move_by == "player":
                # Player took last object
                winner = "AI"  # Player loses in misere mode by taking last object
            else:
                # AI took last object
                winner = "You"  # AI loses in misere mode by taking last object

        messagebox.showinfo("Game Over", f"{winner} wins!")
        self.destroy()

    def update_analysis(self):
        if self.moves_made > 0 and self.is_player_turn:
            # Show best move only during player's turn
            best_move = self.ai.get_best_move(self.rows, self.game_mode.get(), self.move_order.get())  # Pass move_order
            if best_move:
                row, amount = best_move
                self.best_move_label.config(
                    text=f"Best move: Remove {amount} object(s) from Row {row + 1}",
                    fg="blue"
                )
            else:
                self.best_move_label.config(text="No moves available")

    def update_nim_display(self):
        for widget in self.state_frame.winfo_children():
            widget.destroy()

        for i, count in enumerate(self.rows):
            row_frame = tk.Frame(self.state_frame)
            row_frame.pack()
            tk.Label(row_frame, text=f"Row {i + 1}: ").pack(side="left")
            tk.Label(row_frame, text="O " * count).pack(side="left")

    def calculate_move_sequences(self):
        """
        Algorithm: Move Sequence Prediction
        Purpose: Lookahead for move sequences and counter-moves based on current state
        Complexity: O(n*m) where n is number of rows, m is max objects
        """
        self.sequence_text.delete(1.0, tk.END)
        game_type = self.game_mode.get()
        current_state = self.rows.copy()

        # Get AI's top 3 possible moves
        ai_moves = self.get_top_ai_moves(current_state, game_type)

        self.sequence_text.insert(tk.END, f"Analysis for {game_type.title()} Nim:\n\n")

        for i, (ai_move, score) in enumerate(ai_moves, 1):
            row, amount = ai_move
            # Show AI move
            self.sequence_text.insert(tk.END, f"AI Move #{i}:\n")
            self.sequence_text.insert(tk.END, f"Take {amount} from Row {row + 1}\n")

            # Calculate state after AI move
            next_state = current_state.copy()
            next_state[row] -= amount

            # Get best counter-move
            counter_move = self.ai.get_best_move(next_state, game_type)
            if counter_move:
                c_row, c_amount = counter_move
                self.sequence_text.insert(tk.END, f"Best Counter: Take {c_amount} from Row {c_row + 1}\n")
            self.sequence_text.insert(tk.END, "\n")

    def get_top_ai_moves(self, state, game_type):
        """Get AI's top 3 moves with scores"""
        moves = []
        for row, count in enumerate(state):
            for amount in range(1, count + 1):
                next_state = state.copy()
                next_state[row] -= amount
                # Pass move to AI for evaluation
                score = self.ai.evaluate_move(next_state, (row, amount), game_type, self.move_order.get())
                moves.append(((row, amount), score))

        # Sort by score and return top 3
        moves.sort(key=lambda x: x[1], reverse=True)
        return moves[:3]

    def evaluate_move(self, state, move, game_type):
        """Updated move evaluation for better endgame handling"""
        # Use AI's nim_sum method
        nim_sum = self.ai.nim_sum(state)
        total = sum(state)
        ones = sum(1 for r in state if r == 1)
        piles_gt1 = sum(1 for r in state if r > 1)
        move_order = self.move_order.get()

        # Reject invalid moves
        row, amount = move
        if amount <= 0 or amount > state[row]:
            return float('-inf')

        if game_type == 'normal':
            if total == 0:
                return 100  # Winning move
            if nim_sum == 0:
                return 90  # Strong position
            return 50  # Average position
        else:  # misere
            if total == 0:
                return 0  # Losing move

            # Endgame handling
            if piles_gt1 == 0:
                # Want odd singles when playing second
                odd_singles = (ones % 2 == 1)
                if move_order == "second":
                    return 95 if odd_singles else 5
                else:
                    return 95 if not odd_singles else 5

            if piles_gt1 == 1:
                # Try to force opponent into losing position
                target_singles = 1 if move_order == "second" else 0
                return 90 if ones % 2 == target_singles else 10

            return 70 if nim_sum > 0 else 30

    def reset_analysis(self):
        """Reset move prediction analysis"""
        self.sequence_text.delete(1.0, tk.END)
        self.move_history.clear()
        self.predicted_moves.clear()
        self.update_analysis()
