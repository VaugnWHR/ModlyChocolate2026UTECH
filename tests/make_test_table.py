"""Generates the expected-vs-actual test table for the report.

Run from the repository root:
    python -m tests.make_test_table

Each case runs against the real code. The 'Actual' column is what the program
really did, not what we hoped it did. Output goes to the screen and to
docs/test_table.md. Exit status is 1 if any case fails.
"""
import os
import sys

from game import (parse_move, get_valid_move, setup_game, play_game,
                  draw_board, describe_legal_cuts, QuitGame)
from model import MoldyChocolateGame


# ---------- helpers ----------
def scripted(answers):
    """Fake input(): hands back the scripted answers one at a time."""
    it = iter(answers)
    return lambda prompt="": next(it)


def first_cut(game):
    """Deterministic stand-in for the computer: always the first legal cut."""
    return game.get_legal_moves()[0]


def raises(exc, fn):
    """Name of the exception fn raised, or 'no error'."""
    try:
        fn()
    except exc as e:
        return type(e).__name__
    except Exception as e:
        return f"unexpected {type(e).__name__}"
    return "no error"


def setup_result(answers):
    msgs = []
    g = setup_game(scripted(answers), msgs.append)
    s = g.get_state()
    return f"spoiled={s['spoiled']}, size={s['current_dimensions']}, re-prompts={len(msgs)}"


def outcome(m, n, r, c, human_first, answers):
    game = MoldyChocolateGame(m, n, r, c)
    return play_game(game, first_cut, human_first, scripted(answers), lambda *_: None)


def after_moves(m, n, r, c, moves, text):
    g = MoldyChocolateGame(m, n, r, c)
    for mv in moves:
        g.apply_move(*mv)
    return get_valid_move(g, text)


def copy_is_independent():
    g = MoldyChocolateGame(4, 4, 1, 2)
    c = g.copy()
    c.apply_move("H", 1)
    return f"original size={g.get_state()['current_dimensions']}, copy size={c.get_state()['current_dimensions']}"


def one_game():
    return MoldyChocolateGame(4, 4, 1, 2)


def terminal_game():
    return MoldyChocolateGame(1, 1, 0, 0)


# ---------- the cases: (category, what is tested, input, expected, how to run it) ----------
CASES = [
    # ----- Normal -----
    ("Normal", "Setup: 4x4 bar, spoiled square row 2, column 3",
     "4, 4, 2, 3", "spoiled=(1, 2), size=(4, 4), re-prompts=0",
     lambda: setup_result(["4", "4", "2", "3"])),
    ("Normal", "Parse a typed cut", "'H 2'", "('H', 1)",
     lambda: parse_move("H 2")),
    ("Normal", "Parse is case-insensitive", "'v 3'", "('V', 2)",
     lambda: parse_move("v 3")),
    ("Normal", "Parse ignores extra spaces", "'  V   3  '", "('V', 2)",
     lambda: parse_move("  V   3  ")),
    ("Normal", "Legal cut accepted on fresh 4x4 bar", "'H 3'", "('H', 2)",
     lambda: get_valid_move(one_game(), "H 3")),
    ("Normal", "Legal cuts listed for fresh 4x4 bar", "4x4, X at (2,3)", "Legal cuts: H 1-3, V 1-3",
     lambda: describe_legal_cuts(one_game())),
    ("Normal", "Board shows exactly one spoiled square", "4x4, X at (2,3)", "1",
     lambda: draw_board(one_game()).count("X")),
    ("Normal", "Cut keeps the part with the spoiled square", "4x4, X at (2,3); cut H 2",
     "(2, 4)",
     lambda: (lambda g: (g.apply_move("H", 1), g.get_state()["current_dimensions"])[1])(one_game())),
    ("Normal", "Human cuts last and wins", "1x2 bar, X at (1,1), human first, 'V 1'", "human",
     lambda: outcome(1, 2, 0, 0, True, ["V 1"])),
    ("Normal", "Human left with the spoiled square loses", "2x2 bar, X at (1,1), human first, 'H 1'",
     "computer",
     lambda: outcome(2, 2, 0, 0, True, ["H 1"])),
    ("Normal", "Computer moving first, 1x2 bar", "1x2 bar, X at (1,1), computer first", "computer",
     lambda: outcome(1, 2, 0, 0, False, [])),
    ("Normal", "A copy is independent of the original", "copy, then cut the copy",
     "original size=(4, 4), copy size=(2, 4)",
     copy_is_independent),

    # ----- Boundary -----
    ("Boundary", "Setup: smallest bar, 1x1", "1, 1, 1, 1", "spoiled=(0, 0), size=(1, 1), re-prompts=0",
     lambda: setup_result(["1", "1", "1", "1"])),
    ("Boundary", "Setup: largest bar, 20x20, X in far corner", "20, 20, 20, 20",
     "spoiled=(19, 19), size=(20, 20), re-prompts=0",
     lambda: setup_result(["20", "20", "20", "20"])),
    ("Boundary", "Setup: single row", "1, 5, 1, 3", "spoiled=(0, 2), size=(1, 5), re-prompts=0",
     lambda: setup_result(["1", "5", "1", "3"])),
    ("Boundary", "Setup: single column", "5, 1, 4, 1", "spoiled=(3, 0), size=(5, 1), re-prompts=0",
     lambda: setup_result(["5", "1", "4", "1"])),
    ("Boundary", "Setup: spoiled square in last row and column", "4, 4, 4, 4",
     "spoiled=(3, 3), size=(4, 4), re-prompts=0",
     lambda: setup_result(["4", "4", "4", "4"])),
    ("Boundary", "Setup: size just above the limit is refused", "rows 21, then 3, 3, 1, 1",
     "spoiled=(0, 0), size=(3, 3), re-prompts=1",
     lambda: setup_result(["21", "3", "3", "1", "1"])),
    ("Boundary", "Cut on the outer bottom edge is illegal", "'H 4' on 4-row bar", "None",
     lambda: get_valid_move(one_game(), "H 4")),
    ("Boundary", "Cut on the outer right edge is illegal", "'V 4' on 4-column bar", "None",
     lambda: get_valid_move(one_game(), "V 4")),
    ("Boundary", "First and last legal cuts are accepted", "'H 1' and 'H 3'",
     "(('H', 0), ('H', 2))",
     lambda: (get_valid_move(one_game(), "H 1"), get_valid_move(one_game(), "H 3"))),
    ("Boundary", "Cut number 0 parses but is not a legal cut", "'H 0'", "None",
     lambda: get_valid_move(one_game(), "H 0")),
    ("Boundary", "Legality shrinks after a move (cut H 2 already made)", "'H 2' again", "None",
     lambda: after_moves(4, 4, 1, 2, [("H", 1)], "H 2")),
    ("Boundary", "Cut that was legal before still is (after H 2)", "'H 1'", "('H', 0)",
     lambda: after_moves(4, 4, 1, 2, [("H", 1)], "H 1")),
    ("Boundary", "1x1 bar has no legal cuts", "'H 1' on 1x1", "None",
     lambda: get_valid_move(terminal_game(), "H 1")),
    ("Boundary", "1x1 bar: legal-cuts line", "1x1 bar", "Legal cuts: none (only the spoiled square is left)",
     lambda: describe_legal_cuts(terminal_game())),
    ("Boundary", "1x1 start: player to move loses (human first)", "1x1 bar, human first", "computer",
     lambda: outcome(1, 1, 0, 0, True, [])),
    ("Boundary", "1x1 start: player to move loses (computer first)", "1x1 bar, computer first", "human",
     lambda: outcome(1, 1, 0, 0, False, [])),
    ("Boundary", "Single-row bar lists only vertical cuts", "1x5 bar, X at (1,3)", "Legal cuts: V 1-4",
     lambda: describe_legal_cuts(MoldyChocolateGame(1, 5, 0, 2))),

    # ----- Invalid input -----
    ("Invalid", "Setup re-prompts: zero rows", "rows 0, then 4, 4, 1, 1",
     "spoiled=(0, 0), size=(4, 4), re-prompts=1",
     lambda: setup_result(["0", "4", "4", "1", "1"])),
    ("Invalid", "Setup re-prompts: text, decimal, blank, negative", "'abc', '2.5', '', '-3', then 2, 2, 1, 1",
     "spoiled=(0, 0), size=(2, 2), re-prompts=4",
     lambda: setup_result(["abc", "2.5", "", "-3", "2", "2", "1", "1"])),
    ("Invalid", "Setup re-prompts: spoiled row outside the bar", "4, 4, row 5, then 2, 3",
     "spoiled=(1, 2), size=(4, 4), re-prompts=1",
     lambda: setup_result(["4", "4", "5", "2", "3"])),
    ("Invalid", "Quit at a setup prompt", "'q'", "QuitGame",
     lambda: raises(QuitGame, lambda: setup_game(scripted(["q"]), lambda *_: None))),
    ("Invalid", "Parse: missing number", "'H'", "None",
     lambda: parse_move("H")),
    ("Invalid", "Parse: empty input", "''", "None",
     lambda: parse_move("")),
    ("Invalid", "Parse: unknown direction", "'X 2'", "None",
     lambda: parse_move("X 2")),
    ("Invalid", "Parse: number as a word", "'H two'", "None",
     lambda: parse_move("H two")),
    ("Invalid", "Parse: too many parts", "'H 2 3'", "None",
     lambda: parse_move("H 2 3")),
    ("Invalid", "Parse: decimal number", "'H 2.5'", "None",
     lambda: parse_move("H 2.5")),
    ("Invalid", "Parse: no space between letter and number", "'H2'", "None",
     lambda: parse_move("H2")),
    ("Invalid", "Cut far outside the bar", "'H 99'", "None",
     lambda: get_valid_move(one_game(), "H 99")),
    ("Invalid", "Model refuses 0 rows", "MoldyChocolateGame(0, 3, 0, 0)", "ValueError",
     lambda: raises(ValueError, lambda: MoldyChocolateGame(0, 3, 0, 0))),
    ("Invalid", "Model refuses a negative size", "MoldyChocolateGame(-2, 3, 0, 0)", "ValueError",
     lambda: raises(ValueError, lambda: MoldyChocolateGame(-2, 3, 0, 0))),
    ("Invalid", "Model refuses True as a size", "MoldyChocolateGame(True, 3, 0, 0)", "ValueError",
     lambda: raises(ValueError, lambda: MoldyChocolateGame(True, 3, 0, 0))),
    ("Invalid", "Model refuses a text size", "MoldyChocolateGame(3, '3', 0, 0)", "ValueError",
     lambda: raises(ValueError, lambda: MoldyChocolateGame(3, "3", 0, 0))),
    ("Invalid", "Model refuses a spoiled square outside the grid", "MoldyChocolateGame(3, 3, 3, 0)", "ValueError",
     lambda: raises(ValueError, lambda: MoldyChocolateGame(3, 3, 3, 0))),
    ("Invalid", "Model refuses a negative spoiled square", "MoldyChocolateGame(3, 3, -1, 0)", "ValueError",
     lambda: raises(ValueError, lambda: MoldyChocolateGame(3, 3, -1, 0))),
    ("Invalid", "is_legal_move: text index returns False, no crash", "is_legal_move('H', '1')", "False",
     lambda: one_game().is_legal_move("H", "1")),
    ("Invalid", "is_legal_move: True as index returns False", "is_legal_move('H', True)", "False",
     lambda: one_game().is_legal_move("H", True)),
    ("Invalid", "is_legal_move: unknown direction returns False", "is_legal_move('X', 1)", "False",
     lambda: one_game().is_legal_move("X", 1)),
    ("Invalid", "apply_move refuses an illegal cut", "apply_move('H', 99)", "ValueError",
     lambda: raises(ValueError, lambda: one_game().apply_move("H", 99))),
    ("Invalid", "apply_move refuses any cut on a 1x1 bar", "apply_move('H', 0) on 1x1", "ValueError",
     lambda: raises(ValueError, lambda: terminal_game().apply_move("H", 0))),
]


def cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def main():
    rows, failures = [], 0
    for i, (category, what, given, expected, run) in enumerate(CASES, start=1):
        try:
            actual = str(run())
        except Exception as e:                       # a crash is a failed test, not a crashed script
            actual = f"CRASH: {type(e).__name__}: {e}"
        ok = actual == expected
        failures += (not ok)
        rows.append(f"| T{i:02d} | {category} | {cell(what)} | `{cell(given)}` | `{cell(expected)}` | `{cell(actual)}` | {'PASS' if ok else '**FAIL**'} |")

    header = ("| ID | Category | What is tested | Input | Expected | Actual | Result |\n"
              "|---|---|---|---|---|---|---|")
    summary = f"\n**{len(CASES) - failures} of {len(CASES)} test cases passed.**\n"
    table = header + "\n" + "\n".join(rows) + "\n" + summary
    print(table)

    docs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")
    os.makedirs(docs, exist_ok=True)
    with open(os.path.join(docs, "test_table.md"), "w", encoding="utf-8") as f:
        f.write(table)
    print("Saved to docs/test_table.md")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()