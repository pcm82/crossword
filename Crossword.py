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
        self.words = {} 

    def get_dim(self):
        return self.dimension
    
    def get_crossword(self):
        return self.crossword 
    
    def get_words(self):
        return self.words 

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

    def percentIntersect(self):
        """
        :type: crossword
        :input: input any crossword to find out how many intersections exist
        :rtype: float
        :return: the fraction of intersections out of total crossword space
        """
        return (self.num_intersect() / ( self.dimension * self.dimension))

    def can_place(self, word, row, col, vertical, editCrossword = True):
        """
        :type: word: string, row: int, col: int, vertical: bool
        :input: the word to place, the row to place it in, the column to place it in, whether to place it vertically or not
        :rtype: bool
        :return: True if placed successfuly, False otherwise
        """
        dim = self.dimension
        n = len(word)
        # vertical word checking
        if vertical and row+n <= dim:
            if row >= 1 and self.crossword[row-1][col] != None:
                return False
            if row+n < dim and self.crossword[row+n][col] != None:
                return False
            for i, char in enumerate(word):
                if self.crossword[row+i][col] != char:
                    if (col + 1 < dim and self.crossword[row+i][col+1] != None):
                        return False
                    if (col >= 1 and self.crossword[row+i][col-1] != None):
                        return False
                    if self.crossword[row+i][col] != None:
                        return False
            return True
        # horizontal word checking
        if vertical == False and col+n <= dim:
            if col-1 >= 0 and self.crossword[row][col-1] != None:
                return False
            if col+n < dim and self.crossword[row][col+n] != None:
                return False
            for i, char in enumerate(word):
                if self.crossword[row][col+i] != char:
                    if (row + 1 < dim and self.crossword[row+1][col+i] != None): 
                        return False
                    if (row - 1 >= 0 and self.crossword[row-1][col+i] != None):                     
                        return False
                    if self.crossword[row][col+i] != None:
                        return False
            return True
        # if nothing returns true, return false. 
        return False

    def place_word(self, word, clue, row, col, vertical, editCrossword = True):
        """
        :type: word: string, clue: string, row: int, col: int, vertical: bool
        :input: the word to place, the corresponding clue, the row to place it in, the column to place it in, whether to place it vertically or not
        :rtype: bool
        :return: True if placed successfuly, False otherwise
        """
        #check if the word can be placed
        can_place= self.can_place(word, row, col, vertical)
        # if not, return true
        if not can_place:
            return False
        #place vertical word
        if vertical:
            for i, char in enumerate(word):
                self.crossword[row+i][col] = char
            self.numwords += 1
        # place horizontal word
        if (vertical == False):
            for i, char in enumerate(word):
                self.crossword[row][col+i] = char
            self.numwords += 1
        # add word to the words list
        self.words[word]= (row, col, vertical, clue)

    def find_locs(self, word): 
        """
        :type: string
        :input: a word for which we will determine all the places it could go on the board
        :rtype: list
        :return: a list of all the tiles which we could place the word in 
        """
        locations = []

        n = len(word)
        if n > self.dimension:
            return []
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.can_place(word, i, j, vertical = True):
                        locations.append((i, j, True))
        for k in range(self.dimension):
            for l in range(self.dimension):
                if self.can_place(word, k, l, vertical = False):
                    locations.append((k, l, False))
        return locations

    def place_word_randomly_unoptimal(self, word, clue):
        """
        :type: word: string, clue: string 
        :input: word to randomly place on the crossword, clue is corresponding clue
        :rtype: bool
        :return: True if placed successfuly, False otherwise
        """

        locs= self.find_locs(word)
        if len(locs) < 1:
            return False
        rand_location = locs[random.randint(0, len(locs) - 1)] 
        return self.place_word(word, clue, rand_location[0], rand_location[1], rand_location[2], True)
