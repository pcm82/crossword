#process the input data as a dictionary
CornellWords = {}

#------------PROCESS TEXT FILE AS PYTHON DICTIONARY---------------

def heuristic_1(words, board, state):
    return word, tile

def heuristic_2(words, board, state):
    pass

def heuristic_3(words, board, state): 
    pass


def Generate_Beam_Search_Crossword(dictionary, heuristic, dimension = 15): #needs to return a matrix that contains the generated crossword
    #by default we use a 15 by 15 board

    #generate result board, currently empty matrix
    result = [[None for i in range(dimension)] for j in range(dimension)] 

    #holds interesting information we keep updated
    Board_State = {"numWords": 0, "numIntersections": 0, "averageWordLength": 0}

    Possible_To_Place = True
    while Possible_To_Place:
        if heuristic == 1:
            word_to_place, tiles_to_place = heuristic_1(dictionary, result, Board_State)
        elif heuristic == 2:
            word_to_place, tiles_to_place = heuristic_2(dictionary, result, Board_State)
        else:
            word_to_place, tiles_to_place = heuristic_3(dictionary, result, Board_State)

        #place the word in those tiles
            #update what we know about the current board (how many intersections, average word length, etc.)
            #need to delete word from dictionary or mark it used
        #if you iterate through all possible words and can't place:
            #Possible_To_Place = False

    return result

def Print_Matrix(crossword): #prints the matrix for a corresponding crossword
    print("CROSSWORD: ")
    for row in crossword:
        print(row)
    return


#create each variation of the crosswords
Beam_Search_Heuristic_1 = Generate_Beam_Search_Crossword(CornellWords, 1)
Beam_Search_Heuristic_2 = Generate_Beam_Search_Crossword(CornellWords, 2)
Beam_Search_Heuristic_3 = Generate_Beam_Search_Crossword(CornellWords, 3)

#output each of the generated crosswords
Print_Matrix(Beam_Search_Heuristic_1)
Print_Matrix(Beam_Search_Heuristic_2)
Print_Matrix(Beam_Search_Heuristic_3)
