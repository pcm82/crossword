import copy
import random
import itertools
from makeDict import *
import time

class Crossword:
    def __init__(self, dim):
        self.dimension = dim
        self.numwords = 0
        self.crossword = [[None for i in range(dim)] for j in range(dim)]
        self.words = {} #dictionary

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

    def num_filled(self):
        """
        :type: crossword
        :input: crossword of interest
        :rtype: int
        :return: number of board tiles filled
        """
        filled= 0
        for row in self.crossword:
            for entry in row:
                if entry != None:
                    filled += 1
        return filled

    def percentFilled(self):
        """
        :type: 
        :input: 
        :rtype: float
        :return: percent of board tiles filled, between 0 and 1
        """
        denominator = self.dimension*self.dimension
        numerator = self.num_filled()
        return float(numerator)/float(denominator)

    def num_intersect(self):
        """
        :type: crossword
        :input: input any crossword to find out how many intersections exist
        :rtype: int
        :return: the number of intersections between words in the crossword
        """
        filled= self.num_filled()
        word_len = 0
        words_only= self.words.keys()
        for word in words_only:
            word_len = word_len + len(word)
        return (word_len - filled)

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
            self.words[word]= (row, col, vertical)
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
            self.words[word]= (row, col, vertical)
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

def bruteForceCreator(dictionary = makeDictionary(), threshold = .80, size = 5, findBest = True):
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
        if findBest:
            if filled > bestFill:
                best_cross = cross
                bestFill = filled
        elif filled >= threshold:
            return cross, True
    if bestFill >= threshold:
        threshold_met = True
    else:
        threshold_met = False
    return best_cross, threshold_met

def beamSearchCreator(dictionary = makeDictionary(), threshold = .80, size = 5, beam = 3):
    """
    :type: dictionary: dictionary, threshhold: float 0 <= threshold <= 1, size: integer 0 < size
    :input: a dictionary, threshold for how filled we would like to make a board of size "size"
    :rtype: a crossword string, and a boolean for whether it satisfies its threshold
    :return: the most filled crossword we can generate by searching with beam search and our heuristic
    """ 
    #TODO 11.30.52: Write this heuristic function, probably after we finish the brute force method above
    #Create Crossword
    c= Crossword(size)
    #initialize visited as a list of dictionaries with words and locations

    # while threshold not met and while still crosswords left in the heap

        # pick word (use heuristic here? will do it just by order in the dictionary for now)

        # Generate all possible locations for this word in current crossword

        # Create all possible crosswords with these locations

        # for each crossword

            # add to visited

            # calculate value according to heuristic

            # if goal, return

            # add to stack with highest priority first

        # for top beam size

            # pop 
            
            # recurse with reduced list of words
    return None


def recursive_beam_search(crossword, visited, word_list, threshold, beam_size):
    # pick word (use heuristic here? will do it just by order in the dictionary for now)
    if len(word_list) == 0:
        return crossword
    word= word_list.pop()
    crosswords= []
    filled = []
    queue = []
    # Generate all possible locations for this word in current crossword
    locs = crossword.find_locs(word)
    # Create all possible crosswords with these locations
    for loc in locs:
        y= copy.deepcopy(crossword)
        # print("placed word")
        y.place_word(word, loc[0], loc[1], loc[2])
        crosswords.append(y)
    # for each crossword
    for c in crosswords:
        if c.words in visited:
            pass
            filled.append(0)
        else: 
            # add to visited
            # print("added to visited")
            visited.append(c)
            # calculate value according to heuristic
            filled.append(c.percentFilled())
            # if goal, return
            if c.percentFilled() > threshold:
                # print("reached threshold")
                return c
    # add to stack with highest priority first
    sort= [x for _, x in sorted(zip(filled, crosswords), key=lambda pair: -1 * pair[0])]
    for ele in sort:
        # print("added to queue")
        queue.append(ele)
    # for top beam size
    for beam in range(min(beam_size, len(queue))):
        # print("beam search")
        # pop 
        x= queue.pop()
        # recurse with reduced list of words
        best= recursive_beam_search(x, visited, word_list, threshold, beam_size)
        if not (best == None):
            if best.percentFilled() > threshold:
                return best
    # when beam is exhausted, try the others
    while not (len(queue) == 0):
        # print("exhausted beam")
        # pop 
        x= queue.pop()
        # recurse with reduced list of words
        best= recursive_beam_search(x, visited, word_list, threshold, beam_size)
        if not (best == None):
            if best.percentFilled() > threshold:
                return best
    #if all fails
    return None

def compareBeamBrute(dictionary = makeDictionary(), size = 5, threshhold = 0.50, beam_size = 3, visited = []):
    g = Crossword(size)
    testList = list(dictionary.keys())
    result = "\nBeam Search Crossword: "
    beamTime0 = time.perf_counter()
    beamCrossword = recursive_beam_search(g, visited, testList, threshhold, beam_size)
    if beamCrossword:
        result += "\n\n" + str(beamCrossword.print_matrix()) + '\n\nMeets threshold: True' + '\nPercent filled: ' + str(beamCrossword.percentFilled()) 
    else:
        result += "----------NO CROSSWORD FOUND---------- \nMeets threshold: False"
    beamTime1 = time.perf_counter() - beamTime0
    result += "\ntime for beam search: " + str(round(beamTime1, 5))

    bruteTime0 = time.perf_counter()
    bruteCrossword, meetsThreshold = bruteForceCreator(dictionary, threshhold, size, False)
    result += "\n\nBrute force crossword: \n\n" + str(bruteCrossword.print_matrix()) + "\n\nMeets threshold: " + str(meetsThreshold) + "\nPercent filled: " + str(bruteCrossword.percentFilled())
    bruteTime1 = time.perf_counter() - bruteTime0
    result += "\ntime for brute search: " + str(round(bruteTime1, 5))

    if beamCrossword:
        result += "\n\nbeam search was " + str(round(bruteTime1/beamTime1, 2)) + " times faster, but produced an output only " + str(beamCrossword.percentFilled()/bruteCrossword.percentFilled()) + " as filled as brute force\n"

    return result

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
    # c2= Crossword(5)
    # c2.place_word("hello", 0,0,0)
    # c2.place_word("hoard", 0,0,1)
    # c2.place_word("llama", 0,3,1)
    # c2.place_word("llama", 0,2,1) #should fail
    # print("\nCrossword: \n", c2.print_matrix())

    """
    test: find_locs and place_word_randomly
    """
    # d = Crossword(6)
    # print("locations of hello", d.find_locs("hello"))
    # for loc in d.find_locs("hello"):
    #     y= copy.deepcopy(d)
    #     y.place_word("hello", loc[0], loc[1], loc[2])
    #     print("\nCrossword with loc \n", loc)
    #     print("\n", y.print_matrix())
    
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

    """
    test: num_intersect
    """
    # e= Crossword(5)
    # e.place_word("hello", 0,0,0)
    # e.place_word("hoard", 0,0,1)
    # e.place_word("llama", 0,2,1)
    # # e.place_word("i", 3, 4, 0)
    # print("\nCrossword: \n", e.print_matrix())
    # print("words: ", e.words)
    # print("Number of Intersections: \n", e.num_intersect())

    """ 
    test: num_intersect
    """ 
    # f= Crossword(3)
    # out1= recursive_beam_search(f, [], [], 0.5, 2)
    # print("Empty beam search: \n", out1.print_matrix())
    # out2= recursive_beam_search(f, [], ["hi"], 0.5, 2)
    # print("Beam Search- hi in 3x3: \n", out2) #should give none
    # out3= recursive_beam_search(f, [], ["hi"], 1/3, 2)
    # if out3:
    #     print("Beam Search- hi in 3x3: \n", out3.print_matrix())    
    # out4= recursive_beam_search(f, [], ["hen", "man", "zxj"], 1/3, 2)
    # if out4:
    #     print("Beam Search- hi in 3x3: \n", out4.print_matrix())    
    
    """
    test: compare beam_search vs brute force on a 4 by 4
    """
    # testDict = {"hell": "", "like": "", "seen": "", "hi": "", "earth": "", "elves": ""}
    # result = compareBeamBrute(dictionary = testDict, size = 4, threshhold = 0.30, beam_size = 3, visited = [])
    # print(result)

    #surprisingly, brute force produces an output on this input, but when you try a size any higher it takes too long to run. Can we trim the dictionary down to only 4 letter words?
    result = compareBeamBrute(dictionary = makeDictionary(), size = 3, threshhold = 0.30, beam_size = 3, visited = [])
    print(result)