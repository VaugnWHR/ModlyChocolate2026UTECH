from model import MoldyChocolateGame


MAX_SIZE = 20   # keeps the board drawable in a terminal


def parse_move(text):
    """ 'H 2' into ('H', 1). Returns None if the text isn't in the right shape. """
    parts = text.strip().upper().split()
    if len(parts) != 2 or parts[0] not in ("H", "V"):
        return None
    try:
        return (parts[0], int(parts[1]) - 1)   # human 1-indexed -- machine 0 indexed
    except ValueError:
        return None

def get_valid_move(game, text):
    """Returns a legal ('H'/'V', index) move for this game, or None if the text is bad or the cut is illegal"""
    move = parse_move(text)
    if move is None or not game.is_legal_move(*move):
        return None
    return move



class QuitGame(Exception):
    """Raised when the player types 'q' at any prompt."""

def parse_int_in_range(text, low, high):
    """Return the integer in text if low <= value <= high, otherwise None."""
    try:
        value = int(text.strip())
    except ValueError:
        return None
    return value if low <= value <= high else None


def ask_int(prompt, low, high, input_fn=input, output_fn=print):
    """Keep asking until the player enters a whole number in [low, high]."""
    while True:
        text = input_fn(prompt)
        if text.strip().lower() == "q":
            raise QuitGame
        value = parse_int_in_range(text, low, high)
        if value is not None:
            return value
        output_fn(f"Please enter a whole number from {low} to {high} (or q to quit).")


def setup_game(input_fn=input, output_fn=print):
    """Ask for bar size and spoiled square (1-indexed) and return a new game."""
    m = ask_int(f"Number of rows (1-{MAX_SIZE}): ", 1, MAX_SIZE, input_fn, output_fn)
    n = ask_int(f"Number of columns (1-{MAX_SIZE}): ", 1, MAX_SIZE, input_fn, output_fn)
    r = ask_int(f"Spoiled square's row (1-{m}): ", 1, m, input_fn, output_fn)
    c = ask_int(f"Spoiled square's column (1-{n}): ", 1, n, input_fn, output_fn)
    return MoldyChocolateGame(m, n, r - 1, c - 1)   # human 1-indexed -> model 0-indexed