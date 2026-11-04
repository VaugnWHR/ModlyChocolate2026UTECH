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
    
if __name__ == "__main__":
    unittest.main()
    