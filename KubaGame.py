# Author: Kyle Marrero
# Date: 6/2/2021
# Description: KubaGame file with a KubaGame class that allows
# to players to fully play the game of Kuba!


class KubaGame:
    """
    KubaGame class which implements all of the required functionality
    and rule checking necessary to play a full game of Kuba with
    two players
    """

    def __init__(self, playerA, playerB):
        """
        takes two player tuples (name and color) and initializes
        the game board and all respective global variables

        :playerA - tuple consisting of the players name and marble color
        :playerB - tuple consisting of the players name and marble color
        """
        self._playerA = playerA
        self._playerB = playerB
        self._gameBoard = [['W', 'W', 'X', 'X', 'X', 'B', 'B'], #row 0
                           ['W', 'W', 'X', 'R', 'X', 'B', 'B'], #row 1
                           ['X', 'X', 'R', 'R', 'R', 'X', 'X'], #row 2
                           ['X', 'R', 'R', 'R', 'R', 'R', 'X'], #row 3
                           ['X', 'X', 'R', 'R', 'R', 'X', 'X'], #row 4
                           ['B', 'B', 'X', 'R', 'X', 'W', 'W'], #row 5
                           ['B', 'B', 'X', 'X', 'X', 'W', 'W']] #row 6
        # will be set based on first player to be called from
        # makeMove method
        self.currentTurn = ''
        # variable to help ensure Ko rule isn't being violated
        self._priorBoardState = []
        # dictionary to hold player names as keys and number of
        # red marbles captured as values
        self._marblesCaptured = {playerA[0]: 0, playerB[0]: 0}
        self._winner = None
        self._playerColor = {playerA[0]: playerA[1], playerB[0]: playerB[1]}

    def get_current_turn(self):
        """
        returns the player name whose turn it is to play

        :return - self.currentTurn
        """
        if self.currentTurn == '':
            return None
        else:
            return self.currentTurn

    def set_current_turn(self, playerName):
        """
        sets the player name whose turn it is to play

        :playerName - name of player whose turn it is to play
        """
        self.currentTurn = playerName

    def make_move(self, playerName, coordinates, direction):
        """
        performs multiple checks (as well as calls to other functions) to first determine
        the validity of the move being requested.  If a move is determined to be invalid
        anywhere in the function body then it will return false.  If all validity checks
        are passed then the function will make the move, update all of the necessary variables,
        and return True

        :playerName - name of player requesting to make move
        :coordinates - location of marble to be moved
        :direction - direction of marble to be moved
        :return - True if move is valid and made successfully, false for any other reason
        """

        # if game has a winner, return false bc it's over
        if self.get_winner() is not None:
            return False

        # if current turn is not None (meaning the first game move has already been made)
        # and the player name is != to the player whose turn it is, return False
        if self.get_current_turn() is not None and self.get_current_turn() != playerName:
            return False

        # if coords are out of gameBoard bounds, then return False
        if (coordinates[0] < 0 or coordinates[0] > 6) or (coordinates[1] < 0 or coordinates[1] > 6):
            return False

        # call isValidMove for further checks
        if self.is_valid_move(playerName, coordinates, direction) is False:
            return False

        # deep copy
        temp_board = [x[:] for x in self._gameBoard]

        # PROCESS REQUESTED MOVE
        # used to swap current index with prior
        prev = 'X'
        # used to hold val/marble at current index while swapping w/ prev
        temp = 'X'
        row = coordinates[0]
        col = coordinates[1]
        if direction == 'L':
            for i in range(col + 1):
                if col == 0 and temp_board[row][col] == 'R':
                    # encountered a red marble at edge, so it will be
                    # pushed off and captured
                    # Does there need to be logic regarding opposing player
                    # marble capture????
                    self.increment_captured(playerName)
                if i != 0 and prev == 'X':
                    break
                temp = temp_board[row][col]
                temp_board[row][col] = prev
                prev = temp
                col -= 1
        if direction == 'R':
            print("Moving RIGHT!")
            for i in range(7 - col):
                if col == 6 and temp_board[row][col] == 'R':
                    # encountered a red marble at edge, so it will be
                    # pushed off and captured
                    self.increment_captured(playerName)
                # if we aren't on first iter and prev==X, we can stop!
                if i != 0 and prev == 'X':
                    break
                temp = temp_board[row][col]
                temp_board[row][col] = prev
                prev = temp
                col += 1

        if direction == 'F':
            for i in range(row + 1):
                if row == 0 and temp_board[row][col] == 'R':
                    # encountered a red marble at edge, so it will be
                    # pushed off and captured
                    self.increment_captured(playerName)
                if i != 0 and prev == 'X':
                    break
                temp = temp_board[row][col]
                temp_board[row][col] = prev
                prev = temp
                row -= 1

        if direction == 'B':
            for i in range(7 - row):
                if row == 6 and temp_board[row][col] == 'R':
                    # encountered a red marble at edge, so it will be
                    # pushed off and captured
                    self.increment_captured(playerName)
                if i != 0 and prev == 'X':
                    break
                temp = temp_board[row][col]
                temp_board[row][col] = prev
                prev = temp
                row += 1

        # since temp board has processed the requested move, if it is the exact
        # same state as _priorBoardState, then we know the Ko Rule has been
        # violated and we should return False
        if temp_board == self._priorBoardState:
            return False

        # take deep copy of _gameBoard
        self._priorBoardState = [x[:] for x in self._gameBoard]

        # take deep copy of temp_board
        self._gameBoard = [x[:] for x in temp_board]

        # winner is set for the first player that captures 7 red balls
        if self.get_captured(playerName) >= 7:
            self.set_winner(playerName)

        # Set player turn
        if self._playerA[0] == playerName:
            self.set_current_turn(self._playerB[0])
        else:
            self.set_current_turn(self._playerA[0])

        return True

    def is_valid_move(self, playerName, coords, direction):
        """
        handles more intensive move calculations for make_move method like checking
        if a move is open, if the board is completely full, and that the Ko rule is
        being upheld

        :playerName - name of player requesting to make move
        :coordinates - location of marble to be moved
        :direction - direction of marble to be moved
        :return - True if all validity checks pass, False otherwise
        """
        # set local board variable to game board
        board = self.get_game_board()

        # if value to the opposite direction is out of bounds (i.e. 7 or -1)
        # then the move can be made

        # check if there is an opening space in the opposite direction of
        # the requested move
        if direction == 'L' and coords[1]+1 < 7 and board[coords[0]][coords[1]+1] != 'X':
            return False
        elif direction == 'R' and coords[1]-1 > 0 and board[coords[0]][coords[1]-1] != 'X':
            return False
        elif direction == 'F' and coords[0]+1 < 7 and board[coords[0]+1][coords[1]] != 'X':
            return False
        elif direction == 'B' and coords[0]-1 > 0 and board[coords[0]-1][coords[1]] != 'X':
            return False

        # if the given row or col is full, we can't make a move
        if self.row_col_full(coords, direction) is True:
            return False

        # check if a player pushing off their own marbles since
        # that is an invalid move
        playerColor = self._playerColor[playerName]
        # set spaceEncountered to true if a space is encountered in the direction
        # marbles are being pushed
        spaceEncountered = False
        row = coords[0]
        col = coords[1]

        if direction == 'L':
            for i in range(col + 1):
                if self._gameBoard[row][col] == 'X':
                    spaceEncountered = True
                # decrement col to move to next index leftward
                col -= 1
            if self._gameBoard[row][0] == playerColor and spaceEncountered is False:
                return False
        if direction == 'R':
            for i in range(7 - col):
                if self._gameBoard[row][col] == 'X':
                    spaceEncountered = True
                col += 1
            if self._gameBoard[row][6] == playerColor and spaceEncountered is False:
                return False
        if direction == 'F':
            for i in range(row + 1):
                if self._gameBoard[row][col] == 'X':
                    spaceEncountered = True
                row -= 1
            if self._gameBoard[0][col] == playerColor and spaceEncountered is False:
                return False
        if direction == 'B':
            for i in range(7 - row):
                if self._gameBoard[row][col] == 'X':
                    spaceEncountered = True
                row += 1
            if self._gameBoard[6][col] == playerColor and spaceEncountered is False:
                return False

    def get_winner(self):
        """
        Returns the winner value, this will return None until a winner
        is determined.  Mostly used for validity checks in make_move method

        :return - self._winner
        """
        return self._winner

    def set_winner(self, playerName):
        """
        sets the player who won to the winner variable

        :playerName - name of the player who has won the game
        """
        self._winner = playerName

    def get_captured(self, playerName):
        """
        returns the number of red marbles that a given player has captured

        :playerName - name of the player to be queried for the number of
        red marbles captured
        """
        return self._marblesCaptured[playerName]

    def get_marble(self, coords):
        """
        returns the value ('W', 'B', 'R', 'X') at the given
        location on the board

        :coords - the coordinates of a board location as a tuple
        :return - the value at the given location of the board
        """
        # takes coords of a cell as tuple, returns the marble that
        # is present at that location, if none present, return 'X'
        return self._gameBoard[coords[0]][coords[1]]

    def get_marble_count(self):
        """
        returns the count of white, black, and red marbles that are present
        on the board in that specific order i.e. (W, B, R)

        :return - the count of white, black, and red marbles on the board
        as a tuple
        """
        white = 0
        black = 0
        red = 0

        for row in range(7):
            for col in range(7):
                if self._gameBoard[row][col] == 'W':
                    white += 1
                if self._gameBoard[row][col] == 'B':
                    black += 1
                if self._gameBoard[row][col] == 'R':
                    red += 1

        #  return as tuple
        return white, black, red

    def get_game_board(self):
        """
        returns the current gameBoard object

        :return - self._gameBoard object
        """
        # possible helper method to return current board state
        return self._gameBoard

    def increment_captured(self, playerName):
        """
        helper method to increment number of red marbles
        captured for a given player

        :playerName - name of player whose _marblesCaptured value should
        be incremented
        """
        self._marblesCaptured[playerName] += 1

    def display_board(self):
        """
        helper function to print out the game board object
        """
        for row in range(7):
            print(self._gameBoard[row])

    def row_col_full(self, coords, direction):
        """
        function that calculates if a given row or column (based on arguments)
        is full or not (all spaces in provided row or column are occupies by marbles)
        , to be used in is_valid_move method

        :coords - tuple of coordinates to check
        :direction - direction of requested move to be made
        :return - True if full, False otherwise
        """
        board = self.get_game_board()
        row = coords[0]
        col = coords[1]
        count = 0

        if direction == 'L' or direction == 'R':
            for i in range(7):
                if board[row][i] != 'X':
                    count += 1

        if direction == 'F' or direction == 'B':
            for i in range(7):
                if board[i][col] != 'X':
                    count += 1

        # if count is 0 then there are no open spaces in the given
        # row/col, so return True, otherwise False
        if count == 0:
            return True
        else:
            return False


def main():
    # walks through game where playerA wins
    game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))
    game.display_board()
    print(game.make_move('PlayerA', (6,5), 'F'))
    game.display_board()
    print(game.make_move('PlayerB', (0,6), 'L'))
    game.display_board()
    print(game.make_move('PlayerA', (5,6), 'L'))
    game.display_board()
    print(game.make_move('PlayerB', (5,0), 'R'))
    game.display_board()
    print(game.make_move('PlayerA', (5,5), 'L'))
    game.display_board()
    print(game.make_move('PlayerB', (0,4), 'R'))
    game.display_board()
    print(game.make_move('PlayerA', (1,0), 'R'))
    game.display_board()
    print(game.make_move('PlayerB', (0,6), 'L'))
    game.display_board()
    print(game.make_move('PlayerA', (1,2), 'B'))
    game.display_board()
    print(game.make_move('PlayerB', (0,4), 'R'))
    game.display_board()
    print(game.make_move('PlayerA', (2,2), 'B'))
    game.display_board()
    print(game.make_move('PlayerB', (0,6), 'L'))
    game.display_board()
    print(game.make_move('PlayerA', (3,2), 'B'))
    game.display_board()
    print(game.make_move('PlayerB', (0,4), 'R'))
    game.display_board()
    print(game.make_move('PlayerA', (4,2), 'B'))
    game.display_board()
    print(game.make_move('PlayerB', (0,6), 'L'))
    game.display_board()
    print(game.make_move('PlayerA', (5,2), 'B'))
    game.display_board()
    print(game.make_move('PlayerB', (0,4), 'R'))
    game.display_board()
    print(game.make_move('PlayerA', (5,3), 'F'))
    game.display_board()
    print(game.make_move('PlayerB', (0,6), 'L'))
    game.display_board()
    print(game.make_move('PlayerA', (4,3), 'F'))
    game.display_board()
    print(game.make_move('PlayerB', (0,4), 'B'))
    game.display_board()
    print(game.make_move('PlayerA', (3,3), 'F'))
    game.display_board()
    print(game.make_move('PlayerB', (1,4), 'B'))
    game.display_board()
    print(game.make_move('PlayerA', (2,3), 'F'))
    game.display_board()
    # AFTER PREV MOVE PLAYERA WON
    print(game.make_move('PlayerB', (0,5), 'B'))
    game.display_board()
    print(game.get_captured('PlayerA'))
    print(game.get_captured('PlayerB'))
    print(game.get_marble_count())
    print(game.get_winner())



if __name__ == "__main__":
    main()