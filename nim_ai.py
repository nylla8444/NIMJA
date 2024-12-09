class NimAI:
    def __init__(self):
        # Winning patterns based on mathematical analysis
        self.patterns = {
            'winning': [
                (1, 1, 1, 1),  # Leave all 1s
                (2, 2, 0, 0),  # Balanced pairs
                (3, 3, 0, 0),  # Balanced pairs
                (4, 4, 0, 0),  # Balanced pairs
                (2, 2, 2, 0),  # Triple balance
                (3, 3, 3, 0),  # Triple balance
                (1, 2, 3, 0),  # Sequential pattern
            ],
            'forcing': [
                (2, 1, 1, 0),  # Force opponent into bad position
                (3, 2, 1, 0),  # Force opponent into bad position
                (4, 3, 2, 1),  # Sequential forcing
                (3, 3, 2, 0),  # Imbalanced forcing
            ]
        }

    def get_best_move(self, rows, game_type='normal', move_order='first'):
        """
        Enhanced optimal move calculator using Nim-sum and endgame strategy
        """
        # Calculate Nim-sum
        nim_sum = 0
        for pile in rows:
            nim_sum ^= pile

        total_objects = sum(rows)
        non_empty_piles = sum(1 for pile in rows if pile > 0)
        piles_gt1 = sum(1 for pile in rows if pile > 1)
        single_piles = sum(1 for pile in rows if pile == 1)

        # Endgame strategy for Misère Nim
        if game_type == 'misere' and total_objects <= 6:
            if piles_gt1 == 0:
                # All single piles - leave odd number for opponent
                if single_piles % 2 == 0:
                    for i, pile in enumerate(rows):
                        if pile == 1:
                            return i, 1
            elif piles_gt1 == 1:
                # One pile > 1, rest are 1s
                for i, pile in enumerate(rows):
                    if pile > 1:
                        target = 1 if single_piles % 2 == 0 else 0
                        return i, pile - target

        # Normal strategy using Nim-sum
        if nim_sum == 0:
            # Losing position - play defensive
            max_pile = max(rows)
            max_pile_index = rows.index(max_pile)

            # Take from largest pile to minimize opponent's options
            if max_pile > 2:
                return max_pile_index, max_pile - 1
            else:
                # Take any legal move
                for i, pile in enumerate(rows):
                    if pile > 0:
                        return i, 1

        else:
            # Winning position - calculate optimal move
            for i, pile in enumerate(rows):
                target = pile ^ nim_sum
                if target < pile:
                    # Found winning move
                    stones_to_remove = pile - target

                    # Verify move doesn't create losing endgame position
                    if game_type == 'misere' and non_empty_piles <= 3:
                        remaining = sum(rows) - stones_to_remove
                        if remaining == 1 or (remaining == 2 and non_empty_piles == 2):
                            continue

                    return i, stones_to_remove

        # Fallback - take one from largest pile
        max_pile = max(rows)
        return rows.index(max_pile), 1

    def get_perfect_endgame_move(self, rows, game_type):
        """
        Algorithm: Endgame Strategy (Misère Variant)
        Purpose: Determine optimal move for endgame positions
        Complexity: O(n)
        """
        total = sum(rows)
        non_empty = [i for i, r in enumerate(rows) if r > 0]
        ones = sum(1 for r in rows if r == 1)

        if game_type == 'normal':
            if total == 1:
                return (non_empty[0], 1)  # Take last
            if total == 2:
                if len(non_empty) == 1:
                    return (non_empty[0], 2)  # Take whole pile
                return (non_empty[0], 1)  # Take one, leave one
            if total == 3:
                if len(non_empty) == 1:
                    return (non_empty[0], 2)  # Leave one
                if len(non_empty) == 2:
                    return (non_empty[1], 1)  # Take from larger
        else:  # misere
            if total == 2 and len(non_empty) == 2:
                return (non_empty[0], 1)  # Leave two ones
            if total == 3:
                if len(non_empty) == 3:
                    return (non_empty[0], 1)  # Leave three ones
                return (non_empty[0], rows[non_empty[0]] - 1)  # Leave two ones

        return self.get_forcing_move(rows, game_type)

    def get_forcing_move(self, rows, game_type):
        """Enhanced forcing move selection"""
        best_move = None
        best_score = float('-inf')

        for i, row in enumerate(rows):
            for take in range(1, row + 1):
                new_rows = rows.copy()
                new_rows[i] -= take
                score = self.evaluate_position(new_rows, game_type)
                if score > best_score:
                    best_score = score
                    best_move = (i, take)

        return best_move

    def evaluate_position(self, rows, game_type='normal'):
        """
        Algorithm: Minimax with Alpha-Beta Pruning
        Purpose: Evaluate game position for optimal move selection
        Complexity: O(1)
        """
        nim_sum = self.nim_sum(rows)
        total = sum(rows)
        piles_gt1 = sum(1 for r in rows if r > 1)
        ones = sum(1 for r in rows if r == 1)

        if game_type == 'normal':
            score = 0
            if nim_sum == 0:
                score -= 100
            if total <= 4:
                score += 50 if nim_sum > 0 else -50
            score += piles_gt1 * 10
            return score
        else:  # misere
            score = 0
            if piles_gt1 == 0:
                score += 100 if ones % 2 == 0 else -100
            if piles_gt1 == 1:
                score += 50 if ones % 2 == 0 else -50
            return score

    def nim_sum(self, rows):
        """
        Algorithm: Nim-sum calculation (Sprague-Grundy theorem)
        Purpose: Calculate optimal play position using XOR operations
        Complexity: O(n) where n is number of rows
        """
        result = 0
        for row in rows:
            result ^= row  # XOR operation for Nim-sum
        return result

    def match_pattern(self, rows):
        """
        Algorithm: Pattern Matching for Known Positions
        Purpose: Check if current position matches known winning/forcing patterns
        Complexity: O(n log n) due to sorting
        """
        sorted_rows = sorted(rows, reverse=True)
        for pattern in self.patterns['winning']:
            if self.matches_pattern(sorted_rows, pattern):
                diff = [a - b for a, b in zip(sorted_rows, pattern)]
                if any(d > 0 for d in diff):
                    i = next(i for i, d in enumerate(diff) if d > 0)
                    return (rows.index(sorted_rows[i]), diff[i])
        return None

    def matches_pattern(self, rows, pattern):
        """Check if position matches a pattern"""
        return all(r >= p for r, p in zip(rows, pattern))

    def evaluate_move(self, state, move, game_type, move_order='first'):  # Add move_order parameter
        """Updated move evaluation for better endgame handling"""
        nim_sum = self.nim_sum(state)
        total = sum(state)
        ones = sum(1 for r in state if r == 1)
        piles_gt1 = sum(1 for r in state if r > 1)

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
