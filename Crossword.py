import copy
import random
import itertools
from makeDict import *

class Crossword:
    def __init__(self, dim):
        self.dimension = dim
        self.emptyspaces = dim * dim
        self.numwords = 0
        self.crossword = [[None for i in range(dim)] for j in range(dim)]
        self.words = []

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

    def cw(self,row,col):
        """
        returns the element in this row and column of the crossword
        """
        return self.crossword[row][col]

    def place_word(self, word, row, col, vertical, editCrossword = True):
        """
        :type: word: string, row: int, col: int, vertical: bool
        :input: the word to place, the row to place it in, the column to place it in, whether to place it vertically or not
        :rtype: bool
        :return: True if placed successfuly, False otherwise
        """
        dim = self.dimension
        n = len(word)
        if vertical and row+n <= dim:
            if row-1 >= 0 and self.crossword[row-1][col] != None:
                return False
            if row+n < dim and self.crossword[row+n][col] != None:
                return False
            for i, char in enumerate(word):
                if self.crossword[row+i][col] != char:
                    if (col + 1 < dim and self.crossword[row+i][col+1] != None) or (col - 1 >= 0 and self.crossword[row+i][col-1] != None) or self.crossword[row+i][col] != None:
                        return False
            if editCrossword:
                for i, char in enumerate(word):
                    self.crossword[row+i][col] = char
                self.numwords += 1
            return True

        if vertical == False and col+n <= dim:
            if col-1 >= 0 and self.crossword[row][col-1] != None:
                return False
            if col+n < dim and self.crossword[row][col+n] != None:
                return False
            for i, char in enumerate(word):
                if self.crossword[row][col+i] != char:
                    if (row + 1 < dim and self.crossword[row+1][col+i] != None) or (row - 1 >= 0 and self.crossword[row-1][col+i] != None) or self.crossword[row][col+1] != None:
                        return False
            if editCrossword:
                for i, char in enumerate(word):
                    self.crossword[row][col+i] = char
                self.numwords += 1
            return True
        return False

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
            for j in range(self.dimension):
                if self.place_word(word, i, j, vertical = True, editCrossword = False):
                        locations.append((i, j, True))
        for k in range(self.dimension):
            for l in range(self.dimension):
                if self.place_word(word, k, l, vertical = False, editCrossword = False):
                    locations.append((k, l, False))
        return locations

    def place_word_randomly_unoptimal(self, word):
        """
        :type: word: string
        :input: word to randomly place on the crossword
        :rtype: bool
        :return: True if placed successfuly, False otherwise
        """

        locs= self.find_locs(word)
        # print(word, locs)
        if len(locs) < 1:
            return False
        rand_location = locs[random.randint(0, len(locs) - 1)] 
        return self.place_word(word, rand_location[0], rand_location[1], rand_location[2], True)
        
def recursive_arrange(crossword, wordlist):
    """
    :type: crossword: crossword, wordlist: string list
    :input: crossword to place words in, wordlist is a list of words yet to 
            place in the crossword
    :rtype: returns a crossword, a remaining word list, and an efficiency
    :return: the crossword with the first word in the word list placed
    """
    best_fill= 0
    best_cross= crossword
    if len(wordlist) < 1:
        return best_cross
    else: 
        word= wordlist.pop(0)
        locs= crossword.find_locs(word)
        for location in locs:
            y = copy.deepcopy(crossword)
            y.place_word(word, location[0], location[1], location[2], True)
            cross= recursive_arrange(y, copy.deepcopy(wordlist))
            # print("\n\nCrossword:\n\n", cross.print_matrix())
            filled= cross.percentFilled()
            if filled > best_fill: 
                best_fill = filled
                best_cross= cross
        return best_cross

def bruteForceCreator(dictionary = makeDictionary(), threshold = .80, size = 5):
    """
    :type: dictionary: dictionary, threshhold: float 0 <= threshold <= 1, size: integer 0 < size
    :input: a dictionary, threshold for how filled we would like to make a board of size "size"
    :rtype: a crossword string, and a boolean for whether it satisfies its threshold
    :return: the most filled crossword we can generate by searching the entire sample space
    """ 
    
    numWords = len(dictionary)
    crossword = Crossword(size)
    maxWords = numWords #min(numWords, int(numTiles / smallestWordLength))
    best_cross = crossword
    bestFill = 0
    for wordList in itertools.permutations(dictionary.keys(), maxWords):
        cross= recursive_arrange(crossword, list(wordList))
        filled= cross.percentFilled()
        if filled > bestFill:
            best_cross = cross
            bestFill = filled
    if bestFill >= threshold:
        threshold_met = True
    else:
        threshold_met = False
    return best_cross, threshold_met

def beamSearchCreator(dictionary = makeDictionary(), threshold = .80, size = 5):
    """
    :type: dictionary: dictionary, threshhold: float 0 <= threshold <= 1, size: integer 0 < size
    :input: a dictionary, threshold for how filled we would like to make a board of size "size"
    :rtype: a crossword string, and a boolean for whether it satisfies its threshold
    :return: the most filled crossword we can generate by searching with beam search and our heuristic
    """ 
    #TODO 11.30.52: Write this heuristic function, probably after we finish the brute force method above
    return 

if __name__ == '__main__':

    testDict = {"hello": "", "hi": "", "dog": "", "cat": "", "place": "", "hoax": ""} #create a small dictionary for testing purposes
    testDict2 = {"hemp": "", "hoax": "", "bo": "", "ba": ""} #crafted to output with overlaps

    """
    test: basic placement
    """
    # c= Crossword(3)
    # c.place_word("aba", 0,0,vertical = True, editCrossword = True)
    # c.place_word("aca", 0,2,vertical = True, editCrossword = True)
    # print("\nCrossword: \n", c.print_matrix())
    # c.place_word("axa", 0,0,vertical = False, editCrossword=True)
    # print("\nCrossword: \n", c.print_matrix())

    """
    test: find_locs and place_word_randomly
    """
    # d = Crossword(5)
    # print("locations of hello", d.find_locs("hello"))
    # d.place_word_randomly_unoptimal("hello")
    # print(d.print_matrix())
    # print("locations of hoard: ", d.find_locs("hoard"))
    # d.place_word_randomly_unoptimal("hoard")
    # print(d.print_matrix())
    
    """
    test: bruceForce crossword creation-- this test demonstrates how the brute force creation creates things with overlap to demonstrate our find_locs and place word functionality
    I recommend testing with 4 or 5 words and dimension of 4 for quick output. It would be good to know whether the runtime suffers more from dimension or word count
    """
    # print("Executing brute force: ")
    # bruteCrossword, meetsThreshold = bruteForceCreator(testDict2, .625, 4)
    # print("\n\nBrute force crossword: \n\n", bruteCrossword.print_matrix())
    # print("Meets threshold: ", meetsThreshold)
    # print("Percent filled: ", bruteCrossword.percentFilled())

    """
    test: recursive_arrange
    """
    # c = Crossword(3) #initialize a 5 by 5 crossword
    # testWords= ["aoa", "aba", "aca", "ama"]
    # cross= recursive_arrange(c, testWords)
    # print("\n\nRecursive crossword:\n\n", cross.print_matrix())
