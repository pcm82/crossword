import copy
import random
import itertools
from makeDict import *
import time
import Crossword
import PySimpleGUI as sg 

def recursive_arrange(crossword, wordlist, cluelist):
    """
    :type: crossword: crossword, wordlist: string list, cluelist: string list
    :input: crossword to place words in, wordlist is a list of words yet to 
            place in the crossword, cluelist is the corresponding clues
    :rtype: returns a crossword, a remaining word list, and an efficiency
    :return: the crossword with the first word in the word list placed
    """
    best_fill= 0
    best_cross= crossword
    if len(wordlist) < 1:
        return best_cross
    else: 
        word= wordlist[0]
        clue=cluelist[0]
        locs= crossword.find_locs(word)
        if len(locs) > 0:
            for location in locs:
                y = copy.deepcopy(crossword)
                y.place_word(word, clue, location[0], location[1], location[2], True)
                cross= recursive_arrange(y, wordlist[1:len(wordlist)], cluelist[1:len(cluelist)])
                filled= cross.percentFilled()
                if filled > best_fill: 
                    best_fill = filled
                    best_cross= cross
            return best_cross
        else: 
            cross= recursive_arrange(crossword, wordlist[1:len(wordlist)], cluelist[1:len(cluelist)])
            return cross

def bruteForceCreator(dictionary = makeDictionary(), threshold = .80, size = 5, findBest = True):
    """
    :type: dictionary: dictionary, threshhold: float 0 <= threshold <= 1, size: integer 0 < size
    :input: a dictionary, threshold for how filled we would like to make a board of size "size"
    :rtype: a crossword string, and a boolean for whether it satisfies its threshold
    :return: the most filled crossword we can generate by searching the entire sample space
    """ 
    numWords = len(dictionary)
    crossword = Crossword.Crossword(size)
    maxWords = numWords
    best_cross = crossword
    bestFill = 0
    for wordList,clueList in itertools.combinations(dictionary.items(), maxWords):
        # print("permutation started")
        # print("wordList", wordList)
        cross= recursive_arrange(crossword, list(wordList), list(clueList))
        filled= cross.percentFilled()
        if findBest:
            if filled > bestFill:
                # print(filled)
                best_cross = cross
                bestFill = filled
        elif filled >= threshold:
            return cross, True
    if bestFill >= threshold:
        threshold_met = True
    else:
        threshold_met = False
    return best_cross, threshold_met

def beamSearchCreator(dictionary = makeDictionary(), threshold = .80, size = 5, beam = 3, heuristic = 0):
    """
    :type: dictionary: dictionary, threshhold: float 0 <= threshold <= 1, size: integer 0 < size
    :input: a dictionary, threshold for how filled we would like to make a board of size "size"
    :rtype: a crossword string, and a boolean for whether it satisfies its threshold
    :return: the most filled crossword we can generate by searching with beam search and our heuristic
    """ 
    c= Crossword.Crossword(size)
    word_list= list(dictionary.keys())
    clue_list= list(dictionary.values())
    visited = []
    return recursive_beam_search(c, heuristic, visited, word_list, clue_list, threshold, beam)

def getHeuristicValue(crossword, heuristic):
    """
    :type: crossword: Crossword, heuristic: int (0 or 1)
    :input: a crossword and an integer representing the heuristic we wish to apply to it
    :rtype: 0 <= int <= 1
    :return: the percentage of the tiles filled or percentage of intersecting tiles based on heuristic
    """ 
    if heuristic == 0:
        return crossword.percentFilled()
    else: 
        return crossword.percentIntersect()


def recursive_beam_search(crossword, heuristic, visited, word_list, clue_list, threshold, beam_size):
    """
    :type: crossword: Crossword, heuristic: int (0 or 1), visited: list, word_list: list, threshold: 0 <= int <= 1, beam_size: int > 0 
    :input: a crossword, the heuristic to use, a list of visited words, a list of words, a threshold value for the crossword be be filled, beam size
    :rtype: Crossword or None 
    :return: the most filled crossword we can generate by searching with beam search and our heuristic, or None if we cannot surpass the threshold
    """ 
    # pick word (use heuristic here? will do it just by order in the dictionary for now)
    n= len(word_list)
    if n == 0:
        return crossword
    word= word_list[0]
    word_list= word_list[1:n]
    clue= clue_list[0]
    clue_list= clue_list[1:n]
    # print(word)
    crosswords= []
    filled = []
    queue = []
    locs = crossword.find_locs(word)
    # Generate all possible locations for this word in current crossword
    while len(locs) < 1 and len(word_list) > 0:
        word = word_list[0]
        word_list= word_list[1:n]
        clue = clue_list[0]
        clue_list= clue_list[1:n]
        locs = crossword.find_locs(word)
       # print("finding word")
        # print(word)
        # print(locs)
    if len(locs) > 0:
    # Create all possible crosswords with these locations
        for loc in locs:
            y= copy.deepcopy(crossword)
            # print("placed word")
            y.place_word(word, clue, loc[0], loc[1], loc[2])
            crosswords.append(y)
        # for each crossword
        for c in crosswords:
            # print("generated crossword:")
            # print(c.print_matrix())
            if c.words in visited:
                filled.append(0)
            else: 
                # add to visited
                # print("added to visited")
                visited.append(c)
                # calculate value according to heuristic
                filled.append(getHeuristicValue(c, heuristic))
                # if goal, return
                if c.percentFilled() > threshold:
                    # print("reached threshold")
                    return c
        # add to stack with highest priority first
        sort= [x for _, x in sorted(zip(filled, crosswords), key=lambda pair: -1 * pair[0])]

        for ele in sort:
            queue.append(ele)
            # print("adding to queue")
        # for top beam size
        for beam in range(min(beam_size, len(queue))):
            # print("beam search")
            # pop 
            x= queue.pop()
            # print(x.print_matrix())
            # recurse with reduced list of words
            best= recursive_beam_search(x, heuristic, visited, word_list, clue_list, threshold, beam_size)
            if not (best == None):
                if best.percentFilled() > threshold:
                    return best
    # when beam is exhausted, try the others
    while (len(queue) > 0):
        # print("stuck here")
        # pop 
        x= queue.pop()
        # print(x.print_matrix())
        # recurse with reduced list of words
        best= recursive_beam_search(x, heuristic, visited, word_list, clue_list, threshold, beam_size)
        if not (best == None):
            if best.percentFilled() >= threshold:
                return best
    # if all fails
    return None

def compareBeamBrute(dictionary = makeDictionary(), size = 5, threshold = 0.50, beam_size = 3, heuristic = 0):
    """
    :type: dictionary: dictionary, size: int, threshold: int, beam_size: int, heuristic: int
    :input: a dictionary, the dimensions of the crossword, the threshold percentage, the size of the beam, and the heuristic we wish to use
    :rtype: string
    :return: the comparison of performance between beam search and brute force based on the input parameters
    """ 
    result = "\nBeam Search Crossword: "
    beamTime0 = time.perf_counter()
    beamCrossword = beamSearchCreator(dictionary, threshold, size, beam_size, heuristic)
    if beamCrossword:
        result += "\n\n" + str(beamCrossword.print_matrix()) + '\n\nMeets threshold: True' + '\nPercent filled: ' + str(beamCrossword.percentFilled()) 
    else:
        result += "----------NO CROSSWORD FOUND---------- \nMeets threshold: False"
    beamTime1 = time.perf_counter() - beamTime0
    result += "\ntime for beam search: " + str(round(beamTime1, 5))
    bruteTime0 = time.perf_counter()
    bruteCrossword, meetsThreshold = bruteForceCreator(dictionary, threshold, size, False)
    result += ("\n\nBrute force crossword: \n\n" + str(bruteCrossword.print_matrix()) + "\n\nMeets threshold: " 
    + str(meetsThreshold) + "\nPercent filled: " + str(bruteCrossword.percentFilled()))
    bruteTime1 = time.perf_counter() - bruteTime0
    result += "\ntime for brute search: " + str(round(bruteTime1, 5))

    if beamCrossword:
       result += ("\n\nbeam search was " + str(round(bruteTime1/beamTime1, 2)) + " times faster, but produced an output only " 
       + str(beamCrossword.percentFilled()/bruteCrossword.percentFilled()) + " as filled as brute force\n")
    return result


if __name__ == '__main__':

    testDict = {"hello": "", "hi": "", "dog": "", "cat": "", "place": "", "hoax": ""} #create a small dictionary for testing purposes
    testDict2 = {"hemp": "", "hoax": "", "bo": "", "ba": ""} #crafted to output with overlaps
    testDict3 = makeDictionary()
    testDict4= makeSmallDictionary()
  
    """
    test: can_place, place_word, find_locs
    """
    # a= Crossword.Crossword(3)
    # locs= a.find_locs("hi")
    # print(locs)
    # for loc in locs:
    #   a2= copy.deepcopy(a)
    #   a2.place_word("hi", loc[0], loc[1], loc[2])
    #   print(a2.print_matrix())
    #   print("")

    """
    test: num_intersect
    """
    # e= Crossword.Crossword(5)
    # e.place_word("hello", 0,0,0)
    # e.place_word("hoard", 0,0,1)
    # e.place_word("llama", 0,2,1)
    # # e.place_word("i", 3, 4, 0)
    # e.place_word("man", 3, 2, 0)
    # print("\nCrossword: \n", e.print_matrix())
    # print("words: ", e.words)
    # print("Number of Intersections: \n", e.num_intersect())

    """ 
    test: recursive_beam_search
    """ 

    # f= Crossword.Crossword(3)
    # out1= recursive_beam_search(f, 0, [], [], 0.5, 2)
    # print("Empty beam search: \n", out1.print_matrix())
    # out2= recursive_beam_search(f, 0, [], ["hi"], 0.5, 2)
    # print("Beam Search- hi in 3x3: \n", out2) #should give none
    # out3= recursive_beam_search(f, 0, [], ["hi"], 1/3, 2)
    # if out3:
    #     print("Beam Search- hi in 3x3: \n", out3.print_matrix())    
    # out4= recursive_beam_search(f, 0, [], ["hen", "man", "zxj"], 1/3, 2)
    # if out4:
    #     print("Beam Search- hi in 3x3: \n", out4.print_matrix())    

    """
    test: recursive_arrange
    """ 
    # testDict = {"hell": "", "like": "", "seen": "", "hi": ""}
    # f= Crossword.Crossword(4)
    # out= recursive_arrange(f, list(testDict.keys())) 
    # print(out.print_matrix())
        
    """ 
    test: beamSearchCreator
    """ 
    # testDict = {"hell": "", "like": "", "seen": "", "hi": ""}
    # result= beamSearchCreator(dictionary = testDict, threshold = 10/16, size = 4, beam = 3, heuristic = 0)
    # print(result.print_matrix())

    # c= Crossword.Crossword(5)
    # c.place_word("hi", 4, 3, 0)
    # print("placed hi")
    # print(c.print_matrix())
    # result= c.place_word("seen", 4, 1, 0) 
    # print("placed seen") 
    # print(c.print_matrix()) #should not change from above
    
    """
    test: compare beam_search vs brute force on a 4 by 4
    """
    # 
    testDict = {"helloworld": "", "foobarfoobarfoobar":"", "hell": "", "like": "", "seen": "", "hi": "", "sup": "", "bellows": "", "cupholder": "", "uplifting": ""}
    result = compareBeamBrute(dictionary = testDict, size = 4, threshold = 10/16, beam_size = 3, heuristic= 0)
    print(result)

    testDict= {"AAP": "", "CALS": "","CKB": "","CTB": "","EZRA": "","ILR": "", "OLIN": "", "MEWS": "","RAND": "","ROSE": "","SAGE": "","PSB": "","URIS": "","WINES": "","TCAT": "","LIBE": "","MANN": "","EHUB": "","MACS": "","EDDY": "", "BUS": "","SNOW": "","BOBA": "","CMS": "","BRB": "","DUO": "","GET": ""}
    result = compareBeamBrute(dictionary = testDict, size = 4, threshold = 0.6, beam_size = 3, heuristic= 0)
    print(result) # should not find anything
    # #surprisingly, brute force produces an output on this input, but when you try a size any higher it takes too long to run. Can we trim the dictionary down to only 4 letter words?
    result = compareBeamBrute(dictionary = makeDictionary(), size = 5, threshold = 0.6, beam_size = 3, heuristic = 0)
    print(result)