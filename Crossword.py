import copy
import random
from makeDict import *

class Crossword:
    def __init__(self, dim):
        self.dimension = dim
        self.emptyspaces = dim * dim
        self.numwords = 0
        self.crossword = [[None for i in range(dim)] for j in range(dim)]

    def print_matrix(self):
        """
        :type: 
        :input: 
        :rtype: string
        :return: string representation of a matrix
        """
        matrix = self.crossword
        s = [[str(e) for e in row] for row in matrix]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        return ('\n'.join(table))

    def percentFilled(self):
        """
        :type: 
        :input: 
        :rtype: float
        :return: percent of board tiles filled, between 0 and 1
        """
        denominator = self.dimension*self.dimension
        numerator = 0
        for row in self.crossword:
            for entry in row:
                if entry != None:
                    numerator += 1
        return float(numerator)/float(denominator)

    def place_word(self, word, row, col, direction):
        """
        :type: word: string, row: int, col: int, direction: int
        :input: the word to place, the row to place it in, the column to place it in, the direction to place it in (1 means north-south, 0 means east-west)
        :rtype: 
        :return: 
        """
        new_letters = 0
        if direction == 1:
            for i, letter in enumerate(word):
                if ((self.crossword[row + i][col]) != None and (self.crossword[row + i][col] != letter)):
                    raise ValueError
                elif self.crossword[row + i][col] == None:
                    new_letters += 1
                    self.crossword[row + i][col] = letter
        else:
            for i, letter in enumerate(word):
                if (self.crossword[row][col + i] != None and self.crossword[row][col + i] != letter):
                    raise ValueError
                elif self.crossword[row][col + i] == None:
                    new_letters += 1
                    self.crossword[row][col + i] = letter
        self.emptyspaces = self.emptyspaces - new_letters
        self.numwords += 1
        return

    def find_locs(self, word):
        """
        :type: string
        :input: a word for which we will determine all the places it could go on the board
        :rtype: list
        :return: a list of all the tiles which we could place the word in 
        """
        locations = []
        n = len(word)
        for i in range(self.dimension):
            for j in range(self.dimension - n):
                y = copy.deepcopy(self)
                try:
                    y.place_word(word, i, j, 0)
                    locations.append((i, j, 0))
                except:
                    # print("failed horizontally")
                    pass
        for k in range(self.dimension - n):
            for l in range(self.dimension):
                y = copy.deepcopy(self)
                try:
                    y.place_word(word, k, l, 1)
                    locations.append((k, l, 1))
                except:
                    # print("failed vertically")
                    pass
        return locations


def main(dictionary = makeDictionary(), threshold = .80, size = 10):
    """
    :type: string
    :input: a word for which we will determine all the places it could go on the board
    :rtype: list
    :return: a list of all the tiles which we could place the word in 
    """
    return

if __name__ == '__main__':
    #Testing basic crossword functionality
    c = Crossword(10) #initialize a 10 by 10 crossword
    c.place_word("hello", 1, 1, 0) #place hello into row 1, col 1, east-west
    c.place_word("world", 0, 5, 1) #place world into row 0, col 5, north-south
    print("\nCrossword with hello and world: \n\n", c.print_matrix())
    locs_foobar = c.find_locs("foobar") #the possible locations to place the word "foobar"
    rand_loc_foobar = locs_foobar[random.randint(0, len(locs_foobar) - 1)] #choose a random position to place "foobar"
    c.place_word("foobar", rand_loc_foobar[0], rand_loc_foobar[1], rand_loc_foobar[2])
    print("\nCrossword after adding foobar: \n\n", c.print_matrix(), "\n")
    print("Percent of tiles filled: ", c.percentFilled(), "\n")
    
    #Execute real code to see if we can solve the threshold problem
    print(main())
