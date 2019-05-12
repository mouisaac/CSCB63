#################################################################
#                                                               #
#    Define any helper functions you need in this file only.    #
#    You will be handing in HyperSudoku.py, nothing else.       #
#                                                               #
#    A few test cases are provided in Test.py. You can test     #
#    Your code by running: (See the file for more details)      #
#               python3 Test.py                                  #
#    in the directory where the files are located.              #
#                                                               #
#    We're using Python 3.X this time.                          #
#                                                               #
#################################################################


class HyperSudoku:

    @staticmethod
    def solve(grid):
        """
        Input: An 9x9 hyper-sudoku grid with numbers [0-9].
                0 means the spot has no number assigned.
                grid is a 2-Dimensional array. Look at
                Test.py to see how it's initialized.

        Output: A solution to the game (if one exists),
                in the same format. None of the initial
                numbers in the grid can be changed.
                'None' otherwise.
        """
        # first attempt
        current = HyperSudoku.fill(grid)

        # if it is successful
        if current is not None:
            poss = current[0]
            change = current[1]
            # keep filling the grid until there are more than one possibility
            if poss is None:
                # no possibility
                return None

            # keep filling whenever we have previously filled at least one cell
            while change:
                current = HyperSudoku.fill(grid, poss)
                #  if it is again successful
                if current is not None:
                    # current is true meaning we happen to fill the whole grid
                    if current is True:
                        return grid
                    # update poss and change
                    poss = current[0]
                    change = current[1]

                # fail to solve
                else:
                    # exit the loop
                    change = False
                    return None

        # unsolvable
        else:
            return None

        # start DFS (from top left)
        if HyperSudoku.DFSolve(grid, (0, 0), poss):
            # solve is successful
            return grid

        # if solve attempt is unsuccessful
        return None

    @staticmethod
    def DFSolve(grid, pos=(0, 0), numDict=None):
        """
        Given a 9x9 sudoku grid, position, and an optional dictionary of
        possibilities, recursively solve the sudoku using DFS.
        """
        # first empty cell
        pos = HyperSudoku.findEmpty(grid, pos)
        # return true if no cell is empty
        if pos is None:
            return True
        else:
            row = pos[0]
            col = pos[1]
        # get the numbers from the given dict
        if numDict is not None:
            possibility = numDict[pos]
        # otherwise the possibilities are all the digits
        else:
            possibility = {}
            for digit in range(1, 10):
                possibility[digit] = digit
        # go through each possibility
        for num in possibility:
                # check if the number is a valid input to the cell
                if HyperSudoku.check(grid, pos, num):
                        # assign this number
                        grid[row][col] = num
                        # recursively solve the grid
                        if HyperSudoku.DFSolve(grid, pos, numDict):
                                return True
                        # restore the value to 0 (for backtracking)
                        grid[row][col] = 0

        # reach here means the sudoku is not solvable
        return False

    @staticmethod
    def printGrid(grid):
        """
        Prints out the grid in a nice format. Feel free
        to change this if you need to, it will NOT be
        used in marking. It is just to help you debug.

        Use as:     HyperSudoku.printGrid(grid)
        """
        print("-"*25)
        for i in range(9):
            print("|", end=" ")
            for j in range(9):
                print(grid[i][j], end=" ")
                if (j % 3 == 2):
                    print("|", end=" ")
            print()
            if (i % 3 == 2):
                print("-"*25)

    @staticmethod
    def check(grid, position, number):
        row = position[0]
        col = position[1]
        # ranges of indices for the hyper square
        firstHyperRange = {1: 1, 2: 2, 3: 3}
        secondHyperRange = {5: 5, 6: 6, 7: 7}
        # check row, col, and square (cannot have same value appear twice)
        for num in range(0, 9):
            # only check all row, col, and square numbers except the given one
            if (row != num or col != num):
                r = grid[row][num]
                c = grid[num][col]
                # top left position of the square
                topLeftRow, topLeftCol = (row//3)*3, (col//3)*3
                # get the number in square (from top left to bottom right)
                square = grid[topLeftRow+(num//3)][topLeftCol+(num % 3)]
                # false when there is a cell with same value as number
                if (r == number or c == number or square == number):
                    return False

            # check if it is inside a hyper square
            if (row in firstHyperRange or row in secondHyperRange):
                if (col in firstHyperRange or col in secondHyperRange):
                    # top left position of the hyper square (index 1 or 5)
                    topLeftHRow, topLeftHCol = 1+(row//4)*4, 1+(col//4)*4
                    # get the number in hyper square (from top left)
                    h = grid[topLeftHRow+(num//3)][topLeftHCol+(num % 3)]
                    if (h == number):
                        return False
        # checked
        return True

    @staticmethod
    def findEmpty(grid, position=None):
        """
        given a 9x9 sudoku grid, return the first empty (zero) position.
        Position is optional but if given, start checking from it (exclude it).
        None is returned if there is no zeros in the grid.
        """
        # start from the next cell of the given position
        if position:
            row = position[0]
            col = position[1]
            for r in range(row, 9):
                # start from the beginning of the row after the given row
                if r > row:
                    col = 0
                for c in range(col, 9):
                    if grid[r][c] == 0:
                        return (r, c)
        # start from the top left if position is not given or reach the end
        for r in range(0, 9):
            for c in range(0, 9):
                if grid[r][c] == 0:
                    return (r, c)
        # no empty cell
        return None

    @staticmethod
    def possibilities(grid, position, numDict=None):
        """
        given a 9x9 sudoku grid, a position (row and column), and an optional
        possibility dictionary, return the possible values for that position.
        None is returned if the set is empty (no number); false is returned
        if there is only one possibility and we filled the cell.
        """
        number = {}
        row = position[0]
        col = position[1]
        # if numDict is given
        if numDict:
            number = numDict
        else:
            # create a dict with all 10 digits
            for digit in range(1, 10):
                number[digit] = digit

        # ranges of indices for the hyper square
        firstHyperRange = {1: 1, 2: 2, 3: 3}
        secondHyperRange = {5: 5, 6: 6, 7: 7}

        # check row, col, and square (remove numbers that are presented)
        for num in range(0, 9):
            if (row != num or col != num):
                r = grid[row][num]
                c = grid[num][col]
                # top left position of the square
                topLeftRow, topLeftCol = (row//3)*3, (col//3)*3
                # get the number in square (from top left to bottom right)
                square = grid[topLeftRow+(num//3)][topLeftCol+(num % 3)]
                # check number in the same row
                if (r != 0):
                    if r in number:
                        number.pop(r)
                # check number in the same column
                if (c != 0):
                    if c in number:
                        number.pop(c)
                # check number in the same square
                if (square != 0):
                    if square in number:
                        number.pop(square)

            # check hyper square
            if (row in firstHyperRange or row in secondHyperRange):
                if (col in firstHyperRange or col in secondHyperRange):
                    # top left position of the hyper square (index 1 or 5)
                    topLeftHRow, topLeftHCol = 1+(row//4)*4, 1+(col//4)*4
                    # get the number in hyper square (from top left)
                    h = grid[topLeftHRow+(num//3)][topLeftHCol+(num % 3)]
                    if (h != 0):
                        if h in number:
                            number.pop(h)

        # check if there is any possibility
        if number:
            # fill the cell if there is exactly one possibility
            if len(number) == 1:
                # get the value
                num = list(number.values())[0]
                # check if it is valid
                if HyperSudoku.check(grid, (row, col), num):
                    # (assign the only value from the possibility dictionary)
                    grid[row][col] = num
                # if not valid, then there is no possibility for this cell
                else:
                    return None
                # false is returned meaning we have filled the cell
                return False
            # return the dictionary if there are more than one possibility
            else:
                return number
        # no possibilities
        else:
            return None

    @staticmethod
    def fill(grid, numDict=None):
        """
        given a 9x9 sudoku grid, attempt to fill the board by checking
        possibilities of each cell, if there is only one possibility then
        we fill it into the cell, otherwise we store the possibilities of
        each cell and return a dictionary of possibilities (dict of dict).
        A boolean will be returned indicating whether there is a change.
        True is returned if we happen to fill every cell on our attempt.
        None is returned if we found a cell is empty but with no possibility.
        """
        # initially no change has been made
        change = False
        # get the first empty cell
        cell = HyperSudoku.findEmpty(grid)
        # return true if no cell is empty
        if cell is None:
            return True

        # initialize an empty dict to store possibility dictionaries
        possDict = {}
        # create a dict to store visited cells
        visited = {}

        # loop through every empty cell
        while cell:
            visited[cell] = cell
            # if numDict is not given
            if numDict is None:
                poss = HyperSudoku.possibilities(grid, cell)
            # get possible numbers given position and original possibilities
            else:
                poss = HyperSudoku.possibilities(grid, cell, numDict[cell])
            if poss is None:
                return None
            # if there is more than one possibilities, put it in to the dict
            elif poss:
                possDict[cell] = poss
            # if poss is False, then we have filled at least one cell
            else:
                change = True

            # want to get the position of the next cell
            row = cell[0]
            col = cell[1]
            # go to next row when col was at the end of the grid
            row = (row + ((col + 1) // 9)) % 9
            # next column (back to 0 after 8)
            col = (col + 1) % 9

            # next empty cell
            cell = HyperSudoku.findEmpty(grid, (row, col))
            # return true if no cell is empty
            if cell is None:
                return True
            # stop the loop if we reach a visited cell
            elif cell in visited:
                cell = None

        return (possDict, change)


def solveSudoku(grid, pos=(0,0)):
        pos = HyperSudoku.findEmpty(grid, pos)
        if pos is None:
            return True
        for e in range(1,10):
                if HyperSudoku.check(grid,pos,e):
                        grid[pos[0]][pos[1]] = e
                        if solveSudoku(grid, pos):
                                return True
                        # Undo the current cell for backtracking
                        grid[pos[0]][pos[1]] = 0
        return False

if __name__ == "__main__":
    import json
    import time
    times = []
    times2 = []
    different = 0
    faster = 0
    with open('100K_puzzles.txt', 'r') as f:
        puzzles = json.loads(f.readlines()[0].rstrip())
    x = 0
    for grid, soln in puzzles:
        # duplicate the grid
        grid1 = [row[:] for row in grid]
        # new method
        t = time.time()
        my_soln = HyperSudoku.solve(grid)
        s = time.time() - t
        times.append(s)

        # original method
        t2 = time.time()
        my_soln2 = solveSudoku(grid1)
        my_soln2 = grid1
        s2 = time.time() - t2
        times2.append(s2)

        if s < s2:
            faster +=1
        else:
            print(s, s2)

        # assert soln == my_soln
        if soln != my_soln or soln != my_soln2:
            different += 1
            HyperSudoku.printGrid(soln)
            HyperSudoku.printGrid(my_soln)
        x += 1
    print(sum(times)/len(times))
    print(sum(times2)/len(times2))
    print(different)
    print(faster)
