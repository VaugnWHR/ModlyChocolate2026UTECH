def _is_int(x):
    """True only for real integers; rejects bool (True/False), which Python treats as int."""
    return isinstance(x, int) and not isinstance(x, bool)


class MoldyChocolateGame:
    def __init__(self, m, n, spoiled_r, spoiled_c):
        """
        Initializes the game model with robust input validation.
        :param m: Total rows of the initial chocolate bar
        :param n: Total columns of the initial chocolate bar
        :param spoiled_r: 0-indexed row of the spoiled square
        :param spoiled_c: 0-indexed column of the spoiled square
        """
        # Validate dimensions (prevents m = 0, negatives, non-integers and booleans)
        if not _is_int(m) or not _is_int(n) or m <= 0 or n <= 0:
            raise ValueError("Chocolate bar dimensions (m and n) must be positive integers greater than 0.")

        # Validate spoiled square coordinates
        if not _is_int(spoiled_r) or not _is_int(spoiled_c) or not (0 <= spoiled_r < m and 0 <= spoiled_c < n):
            raise ValueError("Spoiled square coordinates must be valid 0-indexed integers within the grid bounds.")

        self.m = m
        self.n = n
        self.spoiled_r = spoiled_r
        self.spoiled_c = spoiled_c

        # Active rectangular boundaries (inclusive 0-indexed coordinates)
        self.r1, self.r2 = 0, m - 1
        self.c1, self.c2 = 0, n - 1

    def copy(self):
        """
        Returns an independent copy of the current game state.
        Lets the solver try hypothetical moves without changing the real game.
        """
        g = MoldyChocolateGame(self.m, self.n, self.spoiled_r, self.spoiled_c)
        g.r1, g.r2, g.c1, g.c2 = self.r1, self.r2, self.c1, self.c2
        return g

    def get_state(self):
        """Returns the current state representation for the UI or solver."""
        return {
            "bounds": (self.r1, self.r2, self.c1, self.c2),
            "spoiled": (self.spoiled_r, self.spoiled_c),
            "current_dimensions": (self.r2 - self.r1 + 1, self.c2 - self.c1 + 1)
        }

    def is_terminal(self):
        """
        Terminal check (termchk): Returns True if the active bar
        has been reduced to a single 1x1 square (the spoiled piece).
        """
        return self.r1 == self.r2 and self.c1 == self.c2

    def get_legal_moves(self):
        """
        Generates all legal cuts along grid lines.
        Returns a list of tuples: ('H', row_index) or ('V', col_index).
        ('H', r) cuts between row r and row r+1; ('V', c) cuts between column c and column c+1.
        """
        if self.is_terminal():
            return []

        moves = []
        # Horizontal cuts: can cut at any row line from r1 up to r2 - 1
        for r in range(self.r1, self.r2):
            moves.append(('H', r))

        # Vertical cuts: can cut at any col line from c1 up to c2 - 1
        for c in range(self.c1, self.c2):
            moves.append(('V', c))

        return moves

    def is_legal_move(self, cut_type, cut_index):
        """Validates if a specific cut obeys the rules. Never raises on bad input; returns False."""
        if self.is_terminal():
            return False

        # Non-integer (or boolean) indices are never legal
        if not _is_int(cut_index):
            return False

        if cut_type == 'H':
            return self.r1 <= cut_index < self.r2
        elif cut_type == 'V':
            return self.c1 <= cut_index < self.c2
        return False

    def apply_move(self, cut_type, cut_index):
        """
        Enforces rules and updates state by executing a cut.
        Eats the piece without the spoiled square, retaining only the sub-rectangle
        containing the spoiled square.
        """
        if not self.is_legal_move(cut_type, cut_index):
            raise ValueError(f"Invalid move: {cut_type} at index {cut_index}")

        if cut_type == 'H':
            if self.spoiled_r <= cut_index:
                self.r2 = cut_index  # Keep top portion
            else:
                self.r1 = cut_index + 1  # Keep bottom portion

        elif cut_type == 'V':
            if self.spoiled_c <= cut_index:
                self.c2 = cut_index  # Keep left portion
            else:
                self.c1 = cut_index + 1  # Keep right portion


# --- Test Script ---
if __name__ == "__main__":
    # Initialize a 4x4 chocolate bar with the spoiled square at row 1, column 2
    game = MoldyChocolateGame(m=4, n=4, spoiled_r=1, spoiled_c=2)

    print("Initial State:", game.get_state())
    print("Is Terminal?", game.is_terminal())
    print("Legal Cuts:", game.get_legal_moves())

    # Apply a horizontal cut at row index 1
    print("\nApplying cut: Horizontal at row 1...")
    game.apply_move('H', 1)

    print("New State:", game.get_state())
    print("Remaining Legal Cuts:", game.get_legal_moves())
