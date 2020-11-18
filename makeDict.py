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


def mostIntersectionsSort(d, currentWords):
    interDict = {}
    for key in d:
        count = 0
        for word in currentWords:
            count += countIntersections(key, word)
        interDict[key] = count
    # makes keys = the list of d's keys, sorted in descending order
    keys = sorted(list(d.keys()), key=lambda x: interDict[x], reverse=True)
    array = []
    for i in range(len(keys)):
        key = keys[i]
        array.append((key, d.get(key)))
    return array


if __name__ == '__main__':
    # make the dictionary
    d = makeDictionary()

# sort the keys according to length
    print("SORTED KEYS BY LENGTH", shortestSort(d))

# count intersections between two words
    print("The number of intersections between hello and world is: ",
          countIntersections("hello", "world"))
    print("The number of intersections between hello and cello is:",
          countIntersections("hello", "cello"))

# sort keys by intersections
    currentWords = ["hello", "world", "cello"]
    print("SORTED KEYS BY INTERSECTIONS",
          mostIntersectionsSort(d, currentWords))
