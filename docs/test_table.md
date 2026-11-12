| ID | Category | What is tested | Input | Expected | Actual | Result |
|---|---|---|---|---|---|---|
| T01 | Normal | Setup: 4x4 bar, spoiled square row 2, column 3 | `4, 4, 2, 3` | `spoiled=(1, 2), size=(4, 4), re-prompts=0` | `spoiled=(1, 2), size=(4, 4), re-prompts=0` | PASS |
| T02 | Normal | Parse a typed cut | `'H 2'` | `('H', 1)` | `('H', 1)` | PASS |
| T03 | Normal | Parse is case-insensitive | `'v 3'` | `('V', 2)` | `('V', 2)` | PASS |
| T04 | Normal | Parse ignores extra spaces | `'  V   3  '` | `('V', 2)` | `('V', 2)` | PASS |
| T05 | Normal | Legal cut accepted on fresh 4x4 bar | `'H 3'` | `('H', 2)` | `('H', 2)` | PASS |
| T06 | Normal | Legal cuts listed for fresh 4x4 bar | `4x4, X at (2,3)` | `Legal cuts: H 1-3, V 1-3` | `Legal cuts: H 1-3, V 1-3` | PASS |
| T07 | Normal | Board shows exactly one spoiled square | `4x4, X at (2,3)` | `1` | `1` | PASS |
| T08 | Normal | Cut keeps the part with the spoiled square | `4x4, X at (2,3); cut H 2` | `(2, 4)` | `(2, 4)` | PASS |
| T09 | Normal | Human cuts last and wins | `1x2 bar, X at (1,1), human first, 'V 1'` | `human` | `human` | PASS |
| T10 | Normal | Human left with the spoiled square loses | `2x2 bar, X at (1,1), human first, 'H 1'` | `computer` | `computer` | PASS |
| T11 | Normal | Computer moving first, 1x2 bar | `1x2 bar, X at (1,1), computer first` | `computer` | `computer` | PASS |
| T12 | Normal | A copy is independent of the original | `copy, then cut the copy` | `original size=(4, 4), copy size=(2, 4)` | `original size=(4, 4), copy size=(2, 4)` | PASS |
| T13 | Boundary | Setup: smallest bar, 1x1 | `1, 1, 1, 1` | `spoiled=(0, 0), size=(1, 1), re-prompts=0` | `spoiled=(0, 0), size=(1, 1), re-prompts=0` | PASS |
| T14 | Boundary | Setup: largest bar, 20x20, X in far corner | `20, 20, 20, 20` | `spoiled=(19, 19), size=(20, 20), re-prompts=0` | `spoiled=(19, 19), size=(20, 20), re-prompts=0` | PASS |
| T15 | Boundary | Setup: single row | `1, 5, 1, 3` | `spoiled=(0, 2), size=(1, 5), re-prompts=0` | `spoiled=(0, 2), size=(1, 5), re-prompts=0` | PASS |
| T16 | Boundary | Setup: single column | `5, 1, 4, 1` | `spoiled=(3, 0), size=(5, 1), re-prompts=0` | `spoiled=(3, 0), size=(5, 1), re-prompts=0` | PASS |
| T17 | Boundary | Setup: spoiled square in last row and column | `4, 4, 4, 4` | `spoiled=(3, 3), size=(4, 4), re-prompts=0` | `spoiled=(3, 3), size=(4, 4), re-prompts=0` | PASS |
| T18 | Boundary | Setup: size just above the limit is refused | `rows 21, then 3, 3, 1, 1` | `spoiled=(0, 0), size=(3, 3), re-prompts=1` | `spoiled=(0, 0), size=(3, 3), re-prompts=1` | PASS |
| T19 | Boundary | Cut on the outer bottom edge is illegal | `'H 4' on 4-row bar` | `None` | `None` | PASS |
| T20 | Boundary | Cut on the outer right edge is illegal | `'V 4' on 4-column bar` | `None` | `None` | PASS |
| T21 | Boundary | First and last legal cuts are accepted | `'H 1' and 'H 3'` | `(('H', 0), ('H', 2))` | `(('H', 0), ('H', 2))` | PASS |
| T22 | Boundary | Cut number 0 parses but is not a legal cut | `'H 0'` | `None` | `None` | PASS |
| T23 | Boundary | Legality shrinks after a move (cut H 2 already made) | `'H 2' again` | `None` | `None` | PASS |
| T24 | Boundary | Cut that was legal before still is (after H 2) | `'H 1'` | `('H', 0)` | `('H', 0)` | PASS |
| T25 | Boundary | 1x1 bar has no legal cuts | `'H 1' on 1x1` | `None` | `None` | PASS |
| T26 | Boundary | 1x1 bar: legal-cuts line | `1x1 bar` | `Legal cuts: none (only the spoiled square is left)` | `Legal cuts: none (only the spoiled square is left)` | PASS |
| T27 | Boundary | 1x1 start: player to move loses (human first) | `1x1 bar, human first` | `computer` | `computer` | PASS |
| T28 | Boundary | 1x1 start: player to move loses (computer first) | `1x1 bar, computer first` | `human` | `human` | PASS |
| T29 | Boundary | Single-row bar lists only vertical cuts | `1x5 bar, X at (1,3)` | `Legal cuts: V 1-4` | `Legal cuts: V 1-4` | PASS |
| T30 | Invalid | Setup re-prompts: zero rows | `rows 0, then 4, 4, 1, 1` | `spoiled=(0, 0), size=(4, 4), re-prompts=1` | `spoiled=(0, 0), size=(4, 4), re-prompts=1` | PASS |
| T31 | Invalid | Setup re-prompts: text, decimal, blank, negative | `'abc', '2.5', '', '-3', then 2, 2, 1, 1` | `spoiled=(0, 0), size=(2, 2), re-prompts=4` | `spoiled=(0, 0), size=(2, 2), re-prompts=4` | PASS |
| T32 | Invalid | Setup re-prompts: spoiled row outside the bar | `4, 4, row 5, then 2, 3` | `spoiled=(1, 2), size=(4, 4), re-prompts=1` | `spoiled=(1, 2), size=(4, 4), re-prompts=1` | PASS |
| T33 | Invalid | Quit at a setup prompt | `'q'` | `QuitGame` | `QuitGame` | PASS |
| T34 | Invalid | Parse: missing number | `'H'` | `None` | `None` | PASS |
| T35 | Invalid | Parse: empty input | `''` | `None` | `None` | PASS |
| T36 | Invalid | Parse: unknown direction | `'X 2'` | `None` | `None` | PASS |
| T37 | Invalid | Parse: number as a word | `'H two'` | `None` | `None` | PASS |
| T38 | Invalid | Parse: too many parts | `'H 2 3'` | `None` | `None` | PASS |
| T39 | Invalid | Parse: decimal number | `'H 2.5'` | `None` | `None` | PASS |
| T40 | Invalid | Parse: no space between letter and number | `'H2'` | `None` | `None` | PASS |
| T41 | Invalid | Cut far outside the bar | `'H 99'` | `None` | `None` | PASS |
| T42 | Invalid | Model refuses 0 rows | `MoldyChocolateGame(0, 3, 0, 0)` | `ValueError` | `ValueError` | PASS |
| T43 | Invalid | Model refuses a negative size | `MoldyChocolateGame(-2, 3, 0, 0)` | `ValueError` | `ValueError` | PASS |
| T44 | Invalid | Model refuses True as a size | `MoldyChocolateGame(True, 3, 0, 0)` | `ValueError` | `ValueError` | PASS |
| T45 | Invalid | Model refuses a text size | `MoldyChocolateGame(3, '3', 0, 0)` | `ValueError` | `ValueError` | PASS |
| T46 | Invalid | Model refuses a spoiled square outside the grid | `MoldyChocolateGame(3, 3, 3, 0)` | `ValueError` | `ValueError` | PASS |
| T47 | Invalid | Model refuses a negative spoiled square | `MoldyChocolateGame(3, 3, -1, 0)` | `ValueError` | `ValueError` | PASS |
| T48 | Invalid | is_legal_move: text index returns False, no crash | `is_legal_move('H', '1')` | `False` | `False` | PASS |
| T49 | Invalid | is_legal_move: True as index returns False | `is_legal_move('H', True)` | `False` | `False` | PASS |
| T50 | Invalid | is_legal_move: unknown direction returns False | `is_legal_move('X', 1)` | `False` | `False` | PASS |
| T51 | Invalid | apply_move refuses an illegal cut | `apply_move('H', 99)` | `ValueError` | `ValueError` | PASS |
| T52 | Invalid | apply_move refuses any cut on a 1x1 bar | `apply_move('H', 0) on 1x1` | `ValueError` | `ValueError` | PASS |

**52 of 52 test cases passed.**
