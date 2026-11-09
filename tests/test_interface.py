import unittest
from model import MoldyChocolateGame
from game import parse_move, get_valid_move


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
    