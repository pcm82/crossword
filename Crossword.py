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
        # TODO there is a bug here, if you try to make this matrix: 
        # a    x      a
        # b    None   c
        # a    None   a
        # it fails to do so. I know that this causes an intersection issue 
        # (which we should talk about) and should fail, but it gives an out of 
        # bounds error before it gets there, so something is up
        dim = self.dimension
        new_letters = 0

        if direction == 0: # PLACES A WORD VERTICALLY
            # out of bounds, consec with prev word, consec with following word
            if row + len(word) > self.dimension: # out of bounds
                print("Out of bounds")
                return False 
            if self.cw(max(0,row-1),col) != None: # consecutive with previous word
                print("consecutive with previous word")
                return False 
            if self.cw(min(dim-1, row+len(word)),col) != None: # consecutive with following word
                print("consecutive with following word")
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

            if col + len(word) > dim: # out of bounds TODO Error here, run the example on lines 283 - 288
                print("Out of bounds")
                return False 
            if self.cw(row, max(0, col-1)) != None: # consecutive with previous word
                print("consecutive with previous word")
                return False 
            if self.cw(row, min(dim-1, col+len(word))) != None: # consecutive with following word
                print("consecutive with following word")
                return False 

            # currently only allows for one intersection 
            intersect = False
            intersect_ind_c = -1
            for i, letter in enumerate(word):
                if not (self.cw(row,col+i) == letter or self.cw(row, col+i) == None):
                    print("problem at point A")
                    return False 
                if self.cw(row,col+i) == letter:
                    if intersect: 
                        print("problem at point B")
                        return False 
                    intersect = True 
                    intersect_ind_c = i 
                if i != intersect_ind_c and (self.cw(max(0,row-1),col+i) != None or self.cw(min(dim-1,row+1),col+i) != None):
                    print("problem at point C")
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
                    success = y.place_word(word, i, j, 0)
                    if success:
                        locations.append((i, j, 0))
                except:
                    #print("failed vertically")
                    pass
        for k in range(self.dimension):
            for l in range(self.dimension):
                y = copy.deepcopy(self)
                try:
                    success = y.place_word(word, k, l, 1)
                    if success:
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
        for i in range(len(locs)):
            location = locs[i]
            y = copy.deepcopy(crossword)
            y.place_word(word, location[0], location[1], location[2])
            cross= recursive_arrange(y, copy.deepcopy(wordlist))
            print("\n\nCrossword:\n\n", cross.print_matrix())
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
    smallestWordLength = len(shortestSort(dictionary)[0][0])
    numTiles = size*size
    maxWords = numWords #min(numWords, int(numTiles / smallestWordLength))
    best_cross = crossword
    bestFill = 0
    for wordList in itertools.permutations(dictionary.keys(), maxWords):
        #print("*************************************************************************************")
        #print(wordList)
        # for word in wordList:
        #     before = crossword.numwords
        #     crossword.place_word_randomly(word)
        #     after = crossword.numwords
        #     if before != after: # tracks words in the order they were added
        #         crossword.words.append(word)
        # if crossword.percentFilled() > bestFill:
        #     print("new percent is", crossword.percentFilled())
        #     print("the words were checked in the order", wordList)
        #     print("the words were placed in the order", crossword.words)
        #     print(crossword.print_matrix())
        #     #print("The word list leading to the best order was", wordList)
        #     bestCrossword = crossword
        #     bestFill = crossword.percentFilled()
        cross= recursive_arrange(crossword, wordList)
        filled= cross.percentFilled()
        if filled > bestFill:
            best_cross = cross
            bestFill = filled
        # can also add a break point here if we only want to hit the threshold
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
    # #Testing basic crossword functionality
    # c = Crossword(10) #initialize a 10 by 10 crossword
    # c.print_matrix()
    # c.place_word("hello", 1, 1, 0) #place hello into row 1, col 1, east-west
    # c.place_word("world", 0, 5, 1) #place world into row 0, col 5, north-south
    # print("\nCrossword with hello and world: \n\n", c.print_matrix())

    
    ##test find_locs
    # c = Crossword(5) #initialize a 5 by 5 crossword
    #locations= c.find_locs("hello")
    #print("possible places to put hello are:")
    #print(locations)
    # c.place_word("hello",0,1,0)
    # locations= c.find_locs("world")
    # print("Possible places to put world are")
    # print(locations)
    # print("\nCrossword with hello: \n", c.print_matrix())
    # for loc in locations:
    #     y= copy.deepcopy(c)
    #     y.place_word("world", loc[0], loc[1], loc[2])
    #     print("\nCrossword with hello world: \n", y.print_matrix())
    c= Crossword(3)
    c.place_word("aba", 0,0,0)
    c.place_word("aca", 0,2,0)
    print("\nCrossword: \n", c.print_matrix())
    c.place_word("axa", 0,0,1)
    print("\nCrossword: \n", c.print_matrix())


    #print("\nCrossword with hello and world: \n\n", c.print_matrix())
    #c.place_word_randomly("foobar")
    #print("\nCrossword after adding foobar: \n\n", c.print_matrix(), "\n")

    # # test percentFilled function
    # c = Crossword(5)
    # c.place_word("hello", 0,1,0)
    # print("Percent of tiles filled: ", c.percentFilled(), "\n")
    # c.place_word("world", 4, 0, 1)
    # print("Percent of tiles filled: ", c.percentFilled(), "\n")
    # print("\nCrossword with hello and world: \n\n", c.print_matrix())

    #Testing brute force crossword creation
    testDict = {"hello": "", "hi": "", "dog": "", "cat": "", "place": "", "hoax": ""} #create a small dictionary for testing purposes
    #print("Executing brute force: ")
    #bruteCrossword, meetsThreshold = bruteForceCreator(testDict, .30, 5)
    #print("\n\nBrute force crossword: \n\n", bruteCrossword.print_matrix())
    #print("Meets threshold: ", meetsThreshold)
    #print("Percent filled: ", bruteCrossword.percentFilled())

    # # Test recursive_arrange 
    # c = Crossword(3) #initialize a 5 by 5 crossword
    # testWords= ["aoa", "aba", "aca", "ama"]
    # cross= recursive_arrange(c, testWords)
    # print("\n\nRecursive crossword:\n\n", cross.print_matrix())

    #Test BruteForceCreate
    