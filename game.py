from prompt_toolkit import prompt

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

def draw_board(game):
    """Return the bar as text. X = spoiled square, . = chocolate left, blank = eaten.
    Row/column labels are 1-indexed and always refer to the ORIGINAL bar."""
    r1, r2, c1, c2 = game.get_state()["bounds"]
    sr, sc = game.get_state()["spoiled"]
    lines = ["     " + " ".join(f"{c + 1:>2}" for c in range(game.n))]
    for r in range(game.m):
        cells = []
        for c in range(game.n):
            if (r, c) == (sr, sc):
                ch = "X"
            elif r1 <= r <= r2 and c1 <= c <= c2:
                ch = "."
            else:
                ch = " "
            cells.append(f"{ch:>2}")
        lines.append(f"{r + 1:>3}  " + " ".join(cells))
    return "\n".join(lines)


def _span(lo, hi):
    return str(lo) if lo == hi else f"{lo}-{hi}"


def describe_legal_cuts(game):
    """One-line summary of the legal cuts in the player's 1-indexed numbering."""
    r1, r2, c1, c2 = game.get_state()["bounds"]
    parts = []
    if r2 > r1:
        parts.append("H " + _span(r1 + 1, r2))
    if c2 > c1:
        parts.append("V " + _span(c1 + 1, c2))
    if not parts:
        return "Legal cuts: none (only the spoiled square is left)"
    return "Legal cuts: " + ", ".join(parts)


def show_board(game, output_fn=print):
    rows, cols = game.get_state()["current_dimensions"]
    output_fn(draw_board(game))
    output_fn(f"Bar size: {rows} x {cols}")
    output_fn(describe_legal_cuts(game))

def ask_move(game, prompt=" Your cut (e.g H 2, or q to quit): ", input_fn=input, output_fn=print):
    """Keep asking until the player types a legal cut. Return a model move, e.g. ('H', 1)."""
    while True:
        text = input_fn(prompt)
        if text.strip().lower() == "q":
            raise QuitGame
        move = get_valid_move(game,text)
        if move is not None:
            return move
        output_fn("Thats not a legal cut " + describe_legal_cuts(game))

def demo_cut_loop(game, input_fn=input, output_fn=print):
    """Keep asking for cuts until game ends(spoiled square left)"""
    show_board(game, output_fn)
    while not game.is_terminal():
        move = ask_move(game, input_fn=input_fn, output_fn=output_fn)
        game.apply_move(*move)
        show_board(game, output_fn)
    output_fn("Only the spoiled square is left!")


if __name__ == "__main__":
    try:
        demo_cut_loop(setup_game())
    except QuitGame:
        print("Thanks for playing!")
