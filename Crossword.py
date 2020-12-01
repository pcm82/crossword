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

    def place_word(self, word, row, col, direction):
        """
        :type: word: string, row: int, col: int, direction: int
        :input: the word to place, the row to place it in, the column to place it in, the direction to place it in (1 means north-south, 0 means east-west)
        :rtype: bool
        :return: True if placed successfuly, False otherwise
        """
        dim = self.dimension
        new_letters = 0

        if direction == 0: # PLACES A WORD VERTICALLY
            # out of bounds, consec with prev word, consec with following word
            if col + len(word) > self.dimension: # out of bounds
                return False 
            if self.cw(max(0,row-1),col) != None: # consecutive with previous word
                return False 
            if self.cw(min(dim-1, row+len(word)),col) != None: # consecutive with following word
                return False 
            
            # currently only allows for one intersection 
            intersect = False
            intersect_ind_r = -1
            for i, letter in enumerate(word):
                if not (self.cw(row+i,col) == letter or self.cw(row+i,col) == None):
                    return False 
                if self.cw(row+i,col) == letter:
                    if intersect: 
                        return False 
                    intersect = True
                    intersect_ind_r = i 
                if i != intersect_ind_r and (self.cw(row+i, max(0,col-1)) != None or self.cw(row+i,min(dim-1,col+1)) != None):
                    return False  
            
            # need two loops for safety or else it places half finished words
            for i,letter in enumerate(word): 
                new_letters += 1
                self.crossword[row + i][col] = letter

        else: # PLACES A WORD HORIZONTALLY

            if row + len(word) > dim: # out of bounds
                return False 
            if self.cw(row, max(0, col-1)) != None: # consecutive with previous word
                return False 
            if self.cw(row, min(dim-1, col+len(word))) != None: # consecutive with following word
                return False 

            # currently only allows for one intersection 
            intersect = False
            intersect_ind_c = -1
            for i, letter in enumerate(word):
                if not (self.cw(row,col+i) == letter or self.cw(row, col+i) == None):
                    return False 
                if self.cw(row,col+i) == letter:
                    if intersect: 
                        return False 
                    intersect = True 
                    intersect_ind_c = i 
                if i != intersect_ind_c and (self.cw(max(0,row-1),col+i) != None or self.cw(min(dim-1,row+1),col+i) != None):
                    return False 
            
            for i,letter in enumerate(word):
                new_letters += 1
                self.crossword[row][col+i] = letter 
        
        self.emptyspaces = self.emptyspaces - new_letters
        self.numwords += 1
        return True

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
                y = copy.deepcopy(self)
                appended = False 
                try:
                    y.place_word(word, i, j, 0)
                    locations.append((i, j, 0))
                except:
                    #print("failed vertically")
                    pass
        for k in range(self.dimension):
            for l in range(self.dimension):
                y = copy.deepcopy(self)
                try:
                    y.place_word(word, k, l, 1)
                    locations.append((k, l, 1))
                except:
                    #print("failed horizontally")
                    pass
        return locations

    def place_word_randomly(self, word):
        """
        :type: word: string
        :input: word to randomly place on the crossword
        :rtype: bool
        :return: True if placed successfuly, False otherwise
        """
        # NOTE: this is NOT optimal. consider the word PLACE. on an empty board it should be placed
        # at the first row or first column. but it can be randomly placed in the middle of the cword
        # which is clearly unideal. but that's a problem for another time. 

        locs= self.find_locs(word)
        # print(word, locs)
        if len(locs) < 1:
            return False
        rand_location = locs[random.randint(0, len(locs) - 1)] 
        return self.place_word(word, rand_location[0], rand_location[1], rand_location[2])
        

def bruteForceCreator(dictionary = makeDictionary(), threshold = .80, size = 5):
    """
    :type: dictionary: dictionary, threshhold: float 0 <= threshold <= 1, size: integer 0 < size
    :input: a dictionary, threshold for how filled we would like to make a board of size "size"
    :rtype: a crossword string, and a boolean for whether it satisfies its threshold
    :return: the most filled crossword we can generate by searching the entire sample space
    """ 
    # TODO 11.30.50: Currently, this function only checks for randomly trying to place each permutation once. 
    # We need to, for each permutation, try every possible configuration of placing words until we place them all down, or until we have exhausted all options
    
    numWords = len(dictionary)
    smallestWordLength = len(shortestSort(dictionary)[0][0])
    numTiles = size*size
    maxWords = min(numWords, int(numTiles / smallestWordLength))
    bestCrossword = []
    bestFill = 0
    
    for wordList in itertools.permutations(dictionary.keys(), maxWords):
        #print("*************************************************************************************")
        #print(wordList)
        crossword = Crossword(size)
        for word in wordList:
            before = crossword.numwords
            crossword.place_word_randomly(word)
            after = crossword.numwords
            if before != after: # tracks words in the order they were added
                crossword.words.append(word)
        if crossword.percentFilled() > bestFill:
            print("new percent is", crossword.percentFilled())
            print("the words were checked in the order", wordList)
            print("the words were placed in the order", crossword.words)
            print(crossword.print_matrix())
            #print("The word list leading to the best order was", wordList)
            bestCrossword = crossword
            bestFill = crossword.percentFilled()
    
    threshold_met = False
    if bestFill >= threshold:
        threshold_met = True

    return bestCrossword, threshold_met

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
    #Testing basic crossword functionality
    # c = Crossword(10) #initialize a 10 by 10 crossword
    # c.place_word("hello", 1, 1, 0) #place hello into row 1, col 1, east-west
    # c.place_word("world", 0, 5, 1) #place world into row 0, col 5, north-south
    # print("\nCrossword with hello and world: \n\n", c.print_matrix())
    # c.place_word_randomly("foobar")
    # print("\nCrossword after adding foobar: \n\n", c.print_matrix(), "\n")
    # print("Percent of tiles filled: ", c.percentFilled(), "\n")
    
    #Testing brute force crossword creation
    testDict = {"hello": "", "hi": "", "dog": "", "cat": "", "place": "", "hoax": ""} #create a small dictionary for testing purposes
    print("Executing brute force: ")
    bruteCrossword, meetsThreshold = bruteForceCreator(testDict, .30, 5)
    print("\n\nBrute force crossword: \n\n", bruteCrossword.print_matrix())
    print("Meets threshold: ", meetsThreshold)
    print("Percent filled: ", bruteCrossword.percentFilled())
