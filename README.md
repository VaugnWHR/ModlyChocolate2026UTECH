# ModlyChocolate2026UTECH

## Installation and Execution Instructions

### Requirements
- Python 3
- Any Python-compatible IDE or text editor(optional)

### Instructions to run the Game
1. Download and extract the project ZIP file.
2. Open the project folder in your preferred IDE.
3. Open 'play.py'.
4. Run the file using your IDE's Run command.
5. Follow the on-screen instructions to play Moldy Chocolate.

**Alternative: Command Prompt**
1. After extracting the files, in the file's directory type "cmd".
2. The termianl should now be open where you then type "py play.py" and click enter.
3. Follow the on-screen instructions to play Moldy Chocolate.

### Running Automated Tests
1. After extracting the files, in the file's directory type "cmd".
2. The termianl should now be open where you then type "python -m unittest discover -s tests -v" and click enter.

### Project Files
- 'play.py' - Starts the application. 
- 'game.py' - Handles user interaction and gameplay.
- 'model.py' - Manages the chocolate board, game states, and legal moves.
- 'solver.py' - Implements the memoized minimax algorithm.
- 'tests/' - Contains automated tests.
- 'docs/' - Contains supporting project documentation.


---INTERFACE----------------------------------------------------------------
Move format. Internally, 0-indexed: ('H', r) cuts between row r and r+1; ('V', c) cuts between column c and c+1, using original bar coordinates. The CLI uses 1-indexed input (H 2, V 3); game.py converts (typed − 1).
