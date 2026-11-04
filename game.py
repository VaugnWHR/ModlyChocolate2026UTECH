

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