import pandas as pd

# Main parser for crossword
# Returns a dictionary with words and clues


def makeDictionary():
    data = pd.read_excel("Words,clues.xlsx")
    words = data['Words']
    clues = data['Clues']
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
    inter = set(word1).intersection(word2)
    return len(inter)

# Compare function for sorting


def compareInt(key1, interDict):
    return (interDict.get(key1), key1)

# Takes in a dictionary and sorts it according to which words have the most
# letters in common with the current Word list
# Returns a sorted tuple list [(key, value), ...] with the words that intersect
# with the most other words first


def mostIntersectionsSort(d, currentWords):
    keys = list(d.keys())
    interDict = []
    for i in range(len(keys)):
        count = 0
        key = keys[i]
        for word in currentWords:
            count = count + countIntersections(key, word)
            print(count)
        interDict.append((key, count))
    interDict = dict(interDict)
    print(len(keys))
    keys = keys.sort(key=lambda x: (compareInt(x, interDict), x))  # BUG HERE
    return keys


if __name__ == '__main__':
    d = makeDictionary()
    sorted = shortestSort(d)
    print(mostIntersectionsSort(d, ['CKB']))
