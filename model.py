class MoldyChocolateGame:
    def __init__(self, m, n, spoiled_r, spoiled_c):
        """
        Initializes the game model.
        :param m: Total rows of the initial chocolate bar
        :param n: Total columns of the initial chocolate bar
        :param spoiled_r: 0-indexed row of the spoiled square
        :param spoiled_c: 0-indexed column of the spoiled square
        """
        self.m = m
        self.n = n
        self.spoiled_r = spoiled_r
        self.spoiled_c = spoiled_c
        
        # Active rectangular boundaries (inclusive 0-indexed coordinates)
        self.r1, self.r2 = 0, m - 1
        self.c1, self.c2 = 0, n - 1
        
        if not (0 <= spoiled_r < m and 0 <= spoiled_c < n):
            raise ValueError("Spoiled square coordinates must be within the grid bounds.")

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
        """Validates if a specific cut obeys the rules."""
        if self.is_terminal():
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
            raise ValueError(f"Invalid move: {{cut_type}} at index {{cut_index}}")
            
        if cut_type == 'H':
            # Horizontal cut at row index splits top ([r1, cut_index]) and bottom ([cut_index+1, r2])
            if self.spoiled_r <= cut_index:
                self.r2 = cut_index  # Keep top portion
            else:
                self.r1 = cut_index + 1  # Keep bottom portion
                
        elif cut_type == 'V':
            # Vertical cut at col index splits left ([c1, cut_index]) and right ([cut_index+1, c2])
            if self.spoiled_c <= cut_index:
                self.c2 = cut_index  # Keep left portion
            else:
                self.c1 = cut_index + 1  # Keep right portion

