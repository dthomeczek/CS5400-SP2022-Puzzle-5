# Name: Devin Thomeczek
# Course: CS5400
# Professor: Dr. Morales
# Assignment: Puzzle Assignment #5
# Due Date: 3/28/2022
import sys
from queue import PriorityQueue

# A class to hold the values of a state of the game
class GameState:
    board: list # The actual game board
    on_snow: bool # Checks to see if Pengu was last on snow
    p_alive: bool # Checks to see if Pengu is alive in the given state
    score: int # Holds the score for the current state
    rows: int # The row size for the board
    cols: int # The col size for the board

    # Initializes the values of a game state
    def __init__(self, board, on_snow, p_alive, score, rows, cols):
        self.board = list(board)
        self.on_snow = on_snow
        self.p_alive = p_alive
        self.score = score
        self.rows = rows
        self.cols = cols

    # Used to create a copy of a game state
    def copy(self) -> 'GameState':
        return GameState(self.board, self.on_snow, self.p_alive, self.score, self.rows, self.cols)
    
    # Resets the values of the given state to the initial state
    def reset(self, state: 'GameState'):
        self.board = list(state.board)
        self.on_snow = state.on_snow
        self.p_alive = state.p_alive
        self.score = state.score
        self.rows = state.rows
        self.cols = state.cols
    
    # This function is used to move Pengu throughout the board
    def transitionfunction(self, path):
        p_row = 0 # Initial Pengu row value set to 0
        p_col = 0 # Initial Pengu col value set to 0
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                if self.board[i][j] == "P": # Assigns coordinates based on the location of P if found
                    p_row = i
                    p_col = j
                elif self.board[i][j] == 'X': # Ensures that the alive check is set to false if there's an X on the board
                    self.p_alive = False
        
        # Used to set the previous Pengu space back
        p_prev_row = 0 
        p_prev_col = 0

        # Used to increment/decrement the row based on the direction
        row = 0
        col = 0

        # Used to keep track of the position to move to next
        new_row = 0
        new_col = 0

        # Used to increment i throughout the while loop, initialized to 0
        i = 0
        while i < len(path): # Runs while there are still values to run in the path
            valid_move = True # Used to check for the end of a move

            # Changes row and col based on the given direction to check
            direction = path[i]
            if direction == 1:
                row += 1
                col += -1
            if direction == 2:
                row += 1
            if direction == 3:
                row += 1
                col += 1
            if direction == 4:
                col += -1
            if direction == 6:
                col += 1
            if direction == 7:
                row += -1
                col += -1
            if direction == 8:
                row += -1
            if direction == 9:
                row += -1
                col += 1
            
            # Sets the new values for row and col
            new_row = p_row + row
            new_col = p_col + col

            while valid_move:
                # Checks if Pengu is on snow followed by checking if valid move is still true
                if self.on_snow and valid_move: 
                    # Checks the next space for a star, increments if it is, and moves to that space, and increments/decrements movement values
                    if self.board[new_row][new_col] == '*': 
                        p_prev_row = p_row
                        p_prev_col = p_col
                        p_row = new_row
                        p_col = new_col
                        self.score += 1
                        self.board[p_prev_row] = self.board[p_prev_row][:p_prev_col] + '0' + self.board[p_prev_row][(1+p_prev_col):]
                        self.board[p_row] = self.board[p_row][:p_col] + 'P' + self.board[p_row][(1+p_col):]
                        new_row += row
                        new_col += col
                        self.on_snow = False

                    # Checks the next space for a U or S, kills Pengu if it is, and moves to that space marked with X
                    elif self.board[new_row][new_col] == 'U' or self.board[new_row][new_col] == 'S': 
                        p_prev_row = p_row
                        p_prev_col = p_col
                        p_row = new_row
                        p_col = new_col
                        self.board[p_prev_row] = self.board[p_prev_row][:p_prev_col] + '0' + self.board[p_prev_row][(1+p_prev_col):]
                        self.board[p_row] = self.board[p_row][:p_col] + 'X' + self.board[p_row][(1+p_col):]
                        self.on_snow = False
                        self.alive = False
                        valid_move = False

                    # Checks the next space for an empty space, and moves to that space, and increments/decrements movement values, resetting the snow spot and on_snow to false
                    elif self.board[new_row][new_col] == ' ': 
                        p_prev_row = p_row
                        p_prev_col = p_col
                        p_row = new_row
                        p_col = new_col
                        self.board[p_prev_row] = self.board[p_prev_row][:p_prev_col] + '0' + self.board[p_prev_row][(1+p_prev_col):]
                        self.board[p_row] = self.board[p_row][:p_col] + 'P' + self.board[p_row][(1+p_col):]
                        self.on_snow = False
                        new_row += row
                        new_col += col
                    
                    # Checks the next space for a 0, and moves to that space, stops movement, and marks on_snow to true
                    elif self.board[new_row][new_col] == '0': 
                        p_prev_row = p_row
                        p_prev_col = p_col
                        p_row = new_row
                        p_col = new_col
                        self.board[p_prev_row] = self.board[p_prev_row][:p_prev_col] + '0' + self.board[p_prev_row][(1+p_prev_col):]
                        self.board[p_row] = self.board[p_row][:p_col] + 'P' + self.board[p_row][(1+p_col):]
                        self.on_snow = True
                        valid_move = False

                elif not self.on_snow and valid_move:
                    # Checks the next space for a star, increments if it is, and moves to that space while resetting the snow space and on_snow to false
                    if self.board[new_row][new_col] == '*': 
                        p_prev_row = p_row
                        p_prev_col = p_col
                        p_row = new_row
                        p_col = new_col
                        self.score += 1
                        self.board[p_prev_row] = self.board[p_prev_row][:p_prev_col] + ' ' + self.board[p_prev_row][(1+p_prev_col):]
                        self.board[p_row] = self.board[p_row][:p_col] + 'P' + self.board[p_row][(1+p_col):]
                        new_row += row
                        new_col += col

                    # Checks the next space for a U or S, kills Pengu if it is, and moves to that space marked with X
                    elif self.board[new_row][new_col] == 'U' or self.board[new_row][new_col] == 'S':
                        p_prev_row = p_row
                        p_prev_col = p_col
                        p_row = new_row
                        p_col = new_col
                        self.board[p_prev_row] = self.board[p_prev_row][:p_prev_col] + ' ' + self.board[p_prev_row][(1+p_prev_col):]
                        self.board[p_row] = self.board[p_row][:p_col] + 'X' + self.board[p_row][(1+p_col):]
                        self.alive = False
                        valid_move = False

                    # Checks the next space for an empty space, and moves to that space, and increments/decrements movement values
                    elif self.board[new_row][new_col] == ' ':
                        p_prev_row = p_row
                        p_prev_col = p_col
                        p_row = new_row
                        p_col = new_col
                        self.board[p_prev_row] = self.board[p_prev_row][:p_prev_col] + ' ' + self.board[p_prev_row][(1+p_prev_col):]
                        self.board[p_row] = self.board[p_row][:p_col] + 'P' + self.board[p_row][(1+p_col):]
                        new_row += row
                        new_col += col

                    # Checks the next space for a wall, and stops movement on the space before the wall
                    elif self.board[new_row][new_col] == '#':
                        p_prev_row = p_row
                        p_prev_col = p_col
                        p_row = new_row - row
                        p_col = new_col - col
                        self.board[p_prev_row] = self.board[p_prev_row][:p_prev_col] + ' ' + self.board[p_prev_row][(1+p_prev_col):]
                        self.board[p_row] = self.board[p_row][:p_col] + 'P' + self.board[p_row][(1+p_col):]
                        valid_move = False

                    # Checks the next space for a 0, and moves to that space, stops movement, and marks on_snow to true
                    elif self.board[new_row][new_col] == '0':
                        p_prev_row = p_row
                        p_prev_col = p_col
                        p_row = new_row
                        p_col = new_col
                        self.board[p_prev_row] = self.board[p_prev_row][:p_prev_col] + ' ' + self.board[p_prev_row][(1+p_prev_col):]
                        self.board[p_row] = self.board[p_row][:p_col] + 'P' + self.board[p_row][(1+p_col):]
                        self.on_snow = True
                        valid_move = False

            # Resets values to 0 and increments i
            new_row = 0
            new_col = 0
            row = 0
            col = 0
            i += 1

# Used to get the possible moves from a specified state
def get_moves(state):
    p_x = 0
    p_y = 0

    moves = []
    
    for x in range(0, state.rows):
        for y in range(0, state.cols):
            if state.board[x][y] == "P":
                p_x = x
                p_y = y
            elif state.board[x][y] == 'X':
                state.p_alive = False
    
    # Checks a given direction if it isn't a wall and Pengu isn't dead and adds that direction to the list of possible moves
    if (state.board[p_x + 1][p_y - 1]) != "#" and state.p_alive:
        moves.append(1)
    if (state.board[p_x + 1][p_y]) != "#" and state.p_alive:
        moves.append(2)
    if (state.board[p_x + 1][p_y + 1]) != "#" and state.p_alive:
        moves.append(3)
    if (state.board[p_x][p_y - 1]) != "#" and state.p_alive:
        moves.append(4)
    if (state.board[p_x][p_y + 1]) != "#" and state.p_alive:
        moves.append(6)
    if (state.board[p_x - 1][p_y - 1]) != "#" and state.p_alive:
        moves.append(7)
    if (state.board[p_x - 1][p_y]) != "#" and state.p_alive:
        moves.append(8)
    if (state.board[p_x - 1][p_y + 1]) != "#" and state.p_alive:
        moves.append(9)
    
    return moves

# Heuristic Function that checks if a given move increments score
# If the move doesn't, check other paths with no increment to score
# Best path will be determined based on lowest value
def h(state: GameState, target):
    value = target-state.score
    return value

# Increases the cost of longer paths to try to find a solution in shorter paths first
# by penalizing Pengu for moving too much
def cost(state: GameState, path):
    value = int(len(path))
    if state.p_alive == False:
        value += 10
    return value

# A* Search Algorithm
def a_star(state: GameState, target_score):
    path = []
    pq = PriorityQueue()
    copy = state.copy()
    pq.put((copy.score, path))
    while not pq.empty():
        # Get next path
        path = pq.get()[1]
        # Apply path to the initial state
        copy.reset(state)
        copy.transitionfunction(path)

        # Check for goal state, if so return
        if copy.score == target_score:
            return path

        # Get all valid moves
        valid_moves = get_moves(copy)
        # For each move, generate state
        for move in valid_moves:
            new_path = list(path)
            new_path.append(move)
            # For each state, evaluate heuristic
            copy2 = state.copy()
            copy2.transitionfunction(new_path)
            # Add heuristic with cost function and add path to queue
            # This is where my heuristic + cost function value is
            value = h(copy2, target_score) + cost(copy2, new_path)
            pq.put(((value), new_path))
    
    # Indicates that no solution was found
    return "we should not see this"

if __name__ == '__main__':
    path = "" # Initial value for path
    score = 0 # Initial value for the score
    max_fish = 0

    infile = "infile.txt" # Used for my testing purposes to make testing easier
    outfile = "outfile.txt" # Used for my testing purposes to make testing easier

    # Reads in a file name to override infile with the first argument
    if len(sys.argv) > 1:
        infile = sys.argv[1]

    # Reads in the values from the file into various variables and then builds the board
    with open(infile, 'r') as f:
        lines = f.read().splitlines()
        data = lines[0].split(' ')
        row = int(data[0])
        col = int(data[1])
        board = [""] * row
        for i in range(1, len(lines)):
            board[i - 1] = lines[i]
        
    # Creates an initial game state with starting values
    state = GameState(board, False, True, 0, row, col)

    for i in range(0, state.rows):
        for j in range(0, state.cols):
            if board[i][j] == "*":
                max_fish += 1

    # Gets the solution path from runner for output
    path = a_star(state, max_fish)

    # Runs the solution path on the initial state
    state.transitionfunction(path)

    # Reads in a file name to override outfile with the second argument
    if len(sys.argv) > 2:
        outfile = sys.argv[2]
    
    # Assigns a variable to output values to the output file
    with open(outfile, "w") as out:

        # Writes the path to the output file
        for i in range(0, len(path)):
            out.write(str(path[i]))

        # Writes spacer lines and the score of the path to the output file
        out.write("\n")
        out.write(str(state.score))
        out.write("\n")

        # Writes the solution board to the output file
        for i in range(0, state.rows):
            for j in range(0, state.cols):
                out.write(state.board[i][j])
            out.write("\n")