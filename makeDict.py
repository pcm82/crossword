import pandas as pd

# Main parser for crossword
# Returns a dictionary with words and clues


def makeDictionary():
    data = pd.read_excel("Words,clues.xlsx")
    words = data['Word']
    clues = data['Clue']
    array = []
    for i in range(len(words)):
        array.append((words[i], clues[i]))
    return dict(array)

# Takes in a dictionary and sorts it according to length of the key
# Returns a sorted tuple list [(key, value), ...] with shortest strings first


def shortestSort(d):
    keys = list(d.keys())
    keys.sort(key=len)
    array = []
    for i in range(len(keys)):
        key = keys[i]
        array.append((key, d.get(key)))
    return array

# function that finds out how many characters these two words have in common
# for heuristics


def countIntersections(word1, word2):
    inter = set(word1.lower()).intersection(word2.lower())
    return len(inter)

# Compare function for sorting


def compareInt(key1, interDict):
    return (interDict.get(key1), key1)

# Takes in a dictionary and sorts it according to which words have the most
# letters in common with the current Word list
# Returns a sorted tuple list [(key, value), ...] with the words that intersect
# with the most other words first
# TODO

def mostIntersectionsSort(d, currentWords):
    interDict = {}
    print("CUR WORDS: ", currentWords)
    for key in d:
        count = 0
        for word in currentWords:
            count += countIntersections(key, word)
        interDict[key] = count
    print("\n INTERDICT \n \n", interDict)
    keys = sorted(list(d.keys()), key=lambda x: interDict[x], reverse = True)#(compareInt(x, interDict), x))  # BUG HERE
    return keys


if __name__ == '__main__':
    #make the dictionary
    d = makeDictionary()
    #sort the keys according to length
    sortedD = shortestSort(d)
    #print list
    # print(sorted)
    #count intersections between two words
    inter1= countIntersections("hello", "world")
    print("The number of intersections between hello and world is:")
    print(inter1)
    inter2= countIntersections("hello", "cello") 
    currentWords = ["hello", "world", "cello"]
    print("SORTED KEYS", mostIntersectionsSort(d, currentWords))
    # print("The number of intersections between hello and cello is:")
    # print(inter2)
    
