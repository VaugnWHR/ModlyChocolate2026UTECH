class MoldyChocolateSolver:
    def __init__(self):
        self.memo = {}  # Stores previously computed results for specific game states.

    @staticmethod 
    def _sides(game):
        """Calculates the distances from the spoiled square to the active boundaries."""
        return (
            game.spoiled_r - game.r1,
            game.r2 - game.spoiled_r,
            game.spoiled_c - game.c1,
            game.c2 - game.spoiled_c
        )
        
    @staticmethod
    def _successor_sides(game, move):
        """Computes the dimensions of the chocolate bar after a specific cut is made."""
        top = game.spoiled_r - game.r1
        bottom = game.r2 - game.spoiled_r
        left = game.spoiled_c - game.c1
        right = game.c2 - game.spoiled_c
        
        cut_type, cut_index = move
        if cut_type == 'H':
            if game.spoiled_r <= cut_index:
                bottom = cut_index - game.spoiled_r
            else:
                top = game.spoiled_r - (cut_index + 1)
        elif cut_type == 'V':
            if game.spoiled_c <= cut_index:
                right = cut_index - game.spoiled_c
            else:
                left = game.spoiled_c - (cut_index + 1)
        return (top, bottom, left, right)

    def _win(self, top, bottom, left, right):
        """Evaluates whether the current board is a winning position using memoized minimax."""
        key = (top, bottom, left, right)
        if key in self.memo:
            return self.memo[key]

        # Base case: 1x1 with spoiled square means the current player loses
        if top == 0 and bottom == 0 and left == 0 and right == 0:
            self.memo[key] = False
            return False

        # Check all possible top cuts
        for new_top in range(top):
            if not self._win(new_top, bottom, left, right):
                self.memo[key] = True
                return True
                
        # Check all possible bottom cuts
        for new_bottom in range(bottom):
            if not self._win(top, new_bottom, left, right):
                self.memo[key] = True
                return True
                
        # Check all possible left cuts
        for new_left in range(left):
            if not self._win(top, bottom, new_left, right):
                self.memo[key] = True
                return True
                
        # Check all possible right cuts (FIXED: moved above the terminal return False)
        for new_right in range(right):
            if not self._win(top, bottom, left, new_right):
                self.memo[key] = True
                return True

        self.memo[key] = False
        return False

    def best_move(self, game):
        """Determines the optimal next move based on game state and solver evaluation."""
        if game.is_terminal():
            return None
            
        legal = game.get_legal_moves()
        # Try to find a move that puts the opponent in a losing state
        for move in legal:
            succ = self._successor_sides(game, move)
            if not self._win(*succ):
                return move
                
        # If no winning move exists, return any legal move
        return legal[0]

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
    
    solver = MoldyChocolateSolver()
    best_move = solver.best_move(game)
    print("\nBest Move Suggested by Solver:", best_move)
    
