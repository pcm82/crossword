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
    def place_word(self, word, row, col, direction):
        letters = word.split
        if direction == 1:
            for i in range(len(letters)):
                letter = letters[i]
                if (self.crossword[row + i, col] != None & self.crossword[row + i, col] != letter):
                    raise ValueError
                else:
                    self.crossword[row + i, col] = letter
        else:
            for i in range(len(letters)):
                letter = letters[i]
                if (self.crossword[row, col + i] != None & self.crossword[row, col + i] != letter):
                    raise ValueError
                else:
                    self.crossword[row, col + i] = letter


def heuristic_1(words, board, state):
    return word, tile


def heuristic_2(words, board, state):
    pass


def heuristic_3(words, board, state):
    pass


# needs to return a matrix that contains the generated crossword
def Generate_Beam_Search_Crossword(dictionary, heuristic, dimension=15):
    # by default we use a 15 by 15 board

    # generate result board, currently empty matrix
    result = [[None for i in range(dimension)] for j in range(dimension)]

    # holds interesting information we keep updated
    Board_State = {"numWords": 0,
                   "numIntersections": 0, "averageWordLength": 0}

    Possible_To_Place = True
    while Possible_To_Place:
        if heuristic == 1:
            word_to_place, tiles_to_place = heuristic_1(
                dictionary, result, Board_State)
        elif heuristic == 2:
            word_to_place, tiles_to_place = heuristic_2(
                dictionary, result, Board_State)
        else:
            word_to_place, tiles_to_place = heuristic_3(
                dictionary, result, Board_State)

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
Print_Matrix(Beam_Search_Heuristic_1)
Print_Matrix(Beam_Search_Heuristic_2)
Print_Matrix(Beam_Search_Heuristic_3)
