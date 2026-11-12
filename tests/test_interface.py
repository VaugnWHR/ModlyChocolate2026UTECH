import unittest
from model import MoldyChocolateGame
from game import parse_move, get_valid_move, parse_int_in_range, setup_game, draw_board, describe_legal_cuts, show_board, QuitGame, MAX_SIZE, ask_move, demo_cut_loop


class TestParseMove(unittest.TestCase):
    def test_valid_moves(self):
        self.assertEqual(parse_move("H 2"), ("H", 1))
        self.assertEqual(parse_move("v 3"), ("V", 2))           #lowercase accepted
        self.assertEqual(parse_move("  V  3  "),("V", 2))       #extra spaces

    def test_wrong_shape(self):
        for text in [ "", "H", "H 2 3", "X 2", "HV 2"]:
            self.assertIsNone(parse_move(text), text)

    def test_non_numeric(self):
        for text in["H two", "H 2.5", "H -", "V abc"]:
            self.assertIsNone(parse_move(text), text)

    def test_out_of_range_num_still_parse(self):
        #parse_move only checks the SHAPE of teh text; the model decides legality
        self.assertEqual(parse_move("H 0"), ("H", -1))
        self.assertEqual(parse_move("H -1"), ("H", -2))

class TestParseThenValidate(unittest.TestCase):
    def setUp(self):
    # 4x4 bar, spoiled square at model (1, 2) = human row 2, column 3
        self.game = MoldyChocolateGame(4, 4, 1, 2)

        
    def test_legal_cuts_accepted(self):
        self.assertEqual(get_valid_move(self.game, "H 1"), ("H", 0))
        self.assertEqual(get_valid_move(self.game, "H 3"), ("H", 2))
        self.assertEqual(get_valid_move(self.game, "V 3"), ("V", 2))

    def test_cuts_on_outer_edge_rejected(self):
        self.assertIsNone(get_valid_move(self.game, "H 4"))   # model ('H', 3): bottom edge
        self.assertIsNone(get_valid_move(self.game, "H 0"))   # model ('H', -1)
        self.assertIsNone(get_valid_move(self.game, "V 4"))

    def test_bad_text_rejected(self):
        self.assertIsNone(get_valid_move(self.game, "banana"))
        self.assertIsNone(get_valid_move(self.game, ""))

    def test_legality_changes_after_a_move(self):
        # After H 2 the bar is rows 1-2 (human numbering), so H 2 is now the bottom edge.
        self.game.apply_move(*parse_move("H 2"))
        self.assertIsNotNone(get_valid_move(self.game, "H 1"))
        self.assertIsNone(get_valid_move(self.game, "H 2"))
        self.assertIsNotNone(get_valid_move(self.game, "V 2"))

    def test_nothing_legal_on_1x1(self):
        game = MoldyChocolateGame(1, 1, 0, 0)
        self.assertIsNone(get_valid_move(game, "H 1"))
        self.assertIsNone(get_valid_move(game, "V 1"))

    if __name__ == "__main__":
        unittest.main()


def make_input(answers):
    """Fake input(): returns the scripted answers one at a time."""
    it = iter(answers)
    return lambda prompt="": next(it)


class TestParseIntInRange(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(parse_int_in_range("3", 1, 4), 3)
        self.assertEqual(parse_int_in_range("  3 ", 1, 4), 3)
        self.assertEqual(parse_int_in_range("1", 1, 4), 1)   # lower boundary
        self.assertEqual(parse_int_in_range("4", 1, 4), 4)   # upper boundary

    def test_invalid(self):
        for text in ["0", "5", "-1", "2.5", "", "abc", "two"]:
            self.assertIsNone(parse_int_in_range(text, 1, 4), text)


class TestSetupGame(unittest.TestCase):
    def test_valid_setup(self):
        game = setup_game(make_input(["4", "4", "2", "3"]), lambda *_: None)
        self.assertEqual(game.get_state()["spoiled"], (1, 2))
        self.assertEqual(game.get_state()["current_dimensions"], (4, 4))

    def test_reprompts_on_bad_input(self):
        messages = []
        game = setup_game(make_input(["0", "abc", "4", "4", "2", "3"]), messages.append)
        self.assertEqual(len(messages), 2)                    # two error messages shown
        self.assertEqual(game.get_state()["spoiled"], (1, 2))

    def test_spoiled_square_must_fit_the_bar(self):
        # 3x3 bar: spoiled row 5 is rejected, then 2 is accepted
        game = setup_game(make_input(["3", "3", "5", "2", "1"]), lambda *_: None)
        self.assertEqual(game.get_state()["spoiled"], (1, 0))

    def test_size_limits(self):
        game = setup_game(make_input([str(MAX_SIZE + 1), str(MAX_SIZE), "1", "1", "1"]),
                          lambda *_: None)
        self.assertEqual(game.get_state()["current_dimensions"], (MAX_SIZE, 1))

    def test_one_by_one_bar(self):
        game = setup_game(make_input(["1", "1", "1", "1"]), lambda *_: None)
        self.assertTrue(game.is_terminal())

    def test_quit(self):
        with self.assertRaises(QuitGame):
            setup_game(make_input(["q"]), lambda *_: None)


class TestDrawBoard(unittest.TestCase):
    def setUp(self):
        self.game = MoldyChocolateGame(4, 4, 1, 2)   # X at human row 2, column 3

    def test_initial_board(self):
        lines = draw_board(self.game).splitlines()
        self.assertEqual(lines[0].split(), ["1", "2", "3", "4"])        # column labels
        self.assertEqual(lines[2].split(), ["2", ".", ".", "X", "."])   # row with the X
        self.assertEqual(draw_board(self.game).count("X"), 1)
        self.assertEqual(draw_board(self.game).count("."), 15)

    def test_eaten_rows_keep_their_labels(self):
        self.game.apply_move("H", 1)                                    # human "H 2"
        lines = draw_board(self.game).splitlines()
        self.assertEqual(lines[3].split(), ["3"])                       # row 3 eaten, label stays
        self.assertEqual(lines[4].split(), ["4"])
        self.assertEqual(draw_board(self.game).count("."), 7)           # 2x4 = 8 cells minus X

    def test_spoiled_square_never_disappears(self):
        while not self.game.is_terminal():
            self.assertEqual(draw_board(self.game).count("X"), 1)
            self.game.apply_move(*self.game.get_legal_moves()[0])
        self.assertEqual(draw_board(self.game).count("X"), 1)
        self.assertEqual(draw_board(self.game).count("."), 0)

    def test_one_by_one_and_single_row(self):
        self.assertEqual(draw_board(MoldyChocolateGame(1, 1, 0, 0)).count("X"), 1)
        row = draw_board(MoldyChocolateGame(1, 5, 0, 2)).splitlines()
        self.assertEqual(row[1].split(), ["1", ".", ".", "X", ".", "."])


class TestLegalCutsText(unittest.TestCase):
    def test_initial_and_after_moves(self):
        game = MoldyChocolateGame(4, 4, 1, 2)
        self.assertEqual(describe_legal_cuts(game), "Legal cuts: H 1-3, V 1-3")
        game.apply_move("H", 1)
        self.assertEqual(describe_legal_cuts(game), "Legal cuts: H 1, V 1-3")

    def test_single_row_and_terminal(self):
        self.assertEqual(describe_legal_cuts(MoldyChocolateGame(1, 5, 0, 2)), "Legal cuts: V 1-4")
        self.assertIn("none", describe_legal_cuts(MoldyChocolateGame(1, 1, 0, 0)))

    def test_every_listed_cut_is_legal_and_nothing_else_is(self):
        # Cross-check the text against the model's own rules on every position of a 3-step game
        game = MoldyChocolateGame(5, 4, 3, 1)
        while True:
            legal = {(t, i + 1) for t, i in game.get_legal_moves()}
            for t in "HV":
                for k in range(0, 8):
                    self.assertEqual((t, k) in legal, game.is_legal_move(t, k - 1))
            if game.is_terminal():
                break
            game.apply_move(*game.get_legal_moves()[-1])


class TestShowBoard(unittest.TestCase):
    def test_prints_board_size_and_cuts(self):
        out = []
        show_board(MoldyChocolateGame(4, 4, 1, 2), out.append)
        self.assertEqual(len(out), 3)
        self.assertEqual(out[1], "Bar size: 4 x 4")
        self.assertEqual(out[2], "Legal cuts: H 1-3, V 1-3")


class TestAskMove(unittest.TestCase):
    def setUp(self):
        self.game = MoldyChocolateGame(4, 4, 1, 2)

    def test_returns_model_move(self):
        move = ask_move(self.game, input_fn=make_input(["H 2"]), output_fn=lambda *_: None)
        self.assertEqual(move, ("H", 1))                      # typed 2 -> model index 1

    def test_reprompts_until_legal(self):
        msgs = []
        move = ask_move(self.game, input_fn=make_input(["banana", "H 9", "H2", "v 3"]),
                        output_fn=msgs.append)
        self.assertEqual(move, ("V", 2))
        self.assertEqual(len(msgs), 3)                        # three rejected attempts
        self.assertIn("Legal cuts: H 1-3, V 1-3", msgs[0])

    def test_quit(self):
        with self.assertRaises(QuitGame):
            ask_move(self.game, input_fn=make_input(["q"]), output_fn=lambda *_: None)

    def test_asking_does_not_change_the_game(self):
        before = self.game.get_state()
        ask_move(self.game, input_fn=make_input(["H 9", "H 2"]), output_fn=lambda *_: None)
        self.assertEqual(self.game.get_state(), before)


class TestDemoLoop(unittest.TestCase):
    def test_full_game_reaches_terminal(self):
        out = []
        game = MoldyChocolateGame(2, 2, 0, 0)
        demo_cut_loop(game, make_input(["H 5", "H 1", "V 1"]), out.append)
        self.assertTrue(game.is_terminal())
        self.assertEqual(out[-1], "Only the spoiled square is left!")
        self.assertEqual(sum("not a legal cut" in m for m in out), 1)

    def test_one_by_one_needs_no_input(self):
        out = []
        game = MoldyChocolateGame(1, 1, 0, 0)
        demo_cut_loop(game, make_input([]), out.append)       # any input request would raise
        self.assertEqual(out[-1], "Only the spoiled square is left!")