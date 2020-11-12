# process the input data as a dictionary
CornellWords = {}

# ------------PROCESS TEXT FILE AS PYTHON DICTIONARY---------------
# see makeDict


# ------------CROSSWORD OBJECT--------------------------------------
class Crossword:
    def __init__(self, dim):
        self.dimension = dim
        self.emptyspaces = dim * dim
        self.numwords = 0
        self.crossword = [[None for i in range(dim)] for j in range(dim)]

    def print_matrix(self):  # prints the matrix for a corresponding crossword
        print("CROSSWORD: ")
        for row in self.crossword:
            print(row)
        return

    # input the word to place, and the row and column location of the first letter
    # input the direction, 0 for horizontal, 1 for vertical
    # also updates emptyspaces

    def place_word(self, word, row, col, direction):
        letters = list(word)
        new_letters = 0
        if direction == 1:
            for i in range(len(letters)):
                letter = letters[i]
                if ((self.crossword[row + i][col]) != None and (self.crossword[row + i][col] != letter)):
                    raise ValueError
                elif self.crossword[row + i][col] == None:
                    new_letters += 1
                    self.crossword[row + i][col] = letter
        else:
            for i in range(len(letters)):
                letter = letters[i]
                if (self.crossword[row][col + i] != None and self.crossword[row][col + i] != letter):
                    raise ValueError
                elif self.crossword[row + i][col] == None:
                    new_letters += 1
                    self.crossword[row][col + i] = letter
        self.emptyspaces = self.emptyspaces - new_letters
        self.numwords += 1
        return

    # TODO fix bugs
    # input a word, finds possible placements for that word
    def find_locs(self, word):
        locations = []
        n = len(word)
        # if you orient in horizontal direction
        print(self.dimension - n)
        for i in range(self.dimension - n):
            for j in range(self.dimension):
                y = self
                try:
                    y.place_word(word, i, j, 0)
                    locations.append((i, j, 0))
                except:
                    print("failed")
                    pass
        for k in range(self.dimension):
            for l in range(self.dimension - n):
                y = self
                try:
                    y.place_word(word, k, l, 1)
                    locations.append((k, l, 1))
                except:
                    pass
        return locations

# TODO


def heuristic_1(words, board):
    return "", (0, 0, 0)

# TODO


def heuristic_2(words, board):
    return "", (0, 0, 0)

# TODO


def heuristic_3(words, board):
    return "", (0, 0, 0)


# needs to return a matrix that contains the generated crossword
def Generate_Beam_Search_Crossword(dictionary, heuristic, dimension=15):
    # by default we use a 15 by 15 board
    # generate result board, currently empty matrix
    result = Crossword(dimension)
    possible_to_place = False
    while possible_to_place:
        if heuristic == 1:
            word_to_place, loc = heuristic_1(dictionary, result)
        elif heuristic == 2:
            word_to_place, loc = heuristic_2(dictionary, result)
        else:
            word_to_place, loc = heuristic_3(dictionary, result)
    # place the word in those tiles

    # update what we know about the current board (how many intersections, average word length, etc.)
    # need to delete word from dictionary or mark it used
    # if you iterate through all possible words and can't place:
    #Possible_To_Place = False

    return result


# create each variation of the crosswords
Beam_Search_Heuristic_1 = Generate_Beam_Search_Crossword(CornellWords, 1)
Beam_Search_Heuristic_2 = Generate_Beam_Search_Crossword(CornellWords, 2)
Beam_Search_Heuristic_3 = Generate_Beam_Search_Crossword(CornellWords, 3)

# output each of the generated crosswords
# Print_Matrix(Beam_Search_Heuristic_1)
# Print_Matrix(Beam_Search_Heuristic_2)
# Print_Matrix(Beam_Search_Heuristic_3)

# testing for crossword function
if __name__ == '__main__':
    c = Crossword(15)
    c.print_matrix()
    c.place_word("hello", 1, 1, 0)
    c.print_matrix()
    c.place_word("world", 0, 5, 1)
    c.print_matrix()
    lst = c.find_locs("greetings")
    print(lst)
