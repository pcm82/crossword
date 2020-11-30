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
        :rtype: bool
        :return: True if placed successfuly, False otherwise
        """
        new_letters = 0
        if direction == 1:
            for i, letter in enumerate(word):
                if ((self.crossword[row + i][col]) != None and (self.crossword[row + i][col] != letter)):
                    return False
                elif self.crossword[row + i][col] == None:
                    new_letters += 1
                    self.crossword[row + i][col] = letter
        else:
            for i, letter in enumerate(word):
                if (self.crossword[row][col + i] != None and self.crossword[row][col + i] != letter):
                    return False
                elif self.crossword[row][col + i] == None:
                    new_letters += 1
                    self.crossword[row][col + i] = letter
        self.emptyspaces = self.emptyspaces - new_letters
        self.numwords += 1
        return True

    def find_locs(self, word):
        #TODO: find locs is placing words next to each other, where they should be going, for instance, dog and cat could be placed
        #such that the board reads "dogcat", which we cannot allow. We need to only allow placements if the words have an explicit overlap, 
        #but otherwise we need to leave a space between all characters from different words
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

    def place_word_randomly(self, word):
        """
        :type: word: string
        :input: word to randomly place on the crossword
        :rtype: bool
        :return: True if placed successfuly, False otherwise
        """
        locs= self.find_locs(word)
        if len(locs) < 1:
            return False
        rand_location = locs[random.randint(0, len(locs) - 1)] 
        return self.place_word(word, rand_location[0], rand_location[1], rand_location[2])
        

def bruteForce(dictionary = makeDictionary(), threshold = .80, size = 5):
    """
    :type: dictionary: dictionary, threshhold: float 0 <= threshold <= 1, size: integer 0 < size
    :input: a dictionary, threshold for how filled we would like to make a board of size "size"
    :rtype: a crossword string, and a boolean for whether it satisfies its threshold
    :return: the most filled crossword we can generate by searching the entire sample space
    """ 
    #TODO: Currently, this function only checks for randomly trying to place each permutation once. 
    # We need to, for each permutation, try every possible configuration of placing words until we place them all down, or until we have exhausted all options
    #Also, need to figure out why the outputted crossword never uses the five letter words, and why it always outputs 0.48 with these results, which are related issues
    numWords = len(dictionary)
    smallestWordLength = len(shortestSort(dictionary)[0][0])
    numTiles = size*size
    maxWords = min(numWords, int(numTiles / smallestWordLength))
    bestCrossword = []
    bestFill = 0
    for wordList in itertools.permutations(dictionary.keys(), maxWords):
        crossword = Crossword(size)
        for word in wordList:
            crossword.place_word_randomly(word)
        if crossword.percentFilled() > bestFill:
            bestCrossword = crossword
            bestFill = crossword.percentFilled()
    threshold_met = False
    if bestFill >= threshold:
        threshold_met = True
    return bestCrossword, threshold_met

if __name__ == '__main__':
    #Testing basic crossword functionality
    c = Crossword(10) #initialize a 10 by 10 crossword
    c.place_word("hello", 1, 1, 0) #place hello into row 1, col 1, east-west
    c.place_word("world", 0, 5, 1) #place world into row 0, col 5, north-south
    print("\nCrossword with hello and world: \n\n", c.print_matrix())
    c.place_word_randomly("foobar")
    print("\nCrossword after adding foobar: \n\n", c.print_matrix(), "\n")
    print("Percent of tiles filled: ", c.percentFilled(), "\n")
    
    #Testing brute force crossword creation
    testDict = {"hello": "", "hi": "", "dog": "", "cat": "", "place": "", "hoax": ""}#create a small dictionary for testing purposes
    print("Executing brute force: ")
    bruteCrossword, meetsThreshold = bruteForce(testDict, .30, 5)
    print("\n\nBrute force crossword: \n\n", bruteCrossword.print_matrix())
    print("Meets threshold: ", meetsThreshold)
    print("Percent filled: ", bruteCrossword.percentFilled())
