# --- Test Script ---
from model import MoldyChocolateGame


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