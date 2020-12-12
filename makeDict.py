import pandas as pd
import string
import random


def makeDictionary():
    """
    :type: 
    :input: 
    :rtype: dict = {string: string}
    :return: dictionary of form {word: clue}
    """
    data = pd.read_excel("Words,clues.xlsx")
    words = data['Word']
    clues = data['Clue']
    array = []
    for i in range(len(words)):
        array.append((words[i], clues[i]))
    return dict(array)


def makeSmallDictionary():
    """
    :type: 
    :input: 
    :rtype: dict = {string: string}
    :return: dictionary of form {word: clue}
    """
    data = pd.read_excel("Words,clues_short.xlsx")
    words = data['Word']
    clues = data['Clue']
    array = []
    for i in range(len(words)):
        array.append((words[i], clues[i]))
    return dict(array)

def makeRandomDictionary(n, max_length):
    dic= []
    for i in range(n):
        l= random.randint(1,max_length)
        letters = string.ascii_uppercase
        word= ''.join(random.choice(letters) for i in range(l))
        dic.append((word, ""))
    return dict(dic)


def shortestSort(d):
    """
    :type: d: dictionary
    :input: the word and clue dictionary
    :rtype: list of tuples
    :return: sorted tuples (key, value) according to key length
    """
    keys = list(d.keys())
    keys.sort(key=len)
    array = []
    for i in range(len(keys)):
        key = keys[i]
        array.append((key, d.get(key)))
    return array


def countIntersections(word1, word2):
    """
    :type: word1: string, word2: string
    :input: two words for which we count the intersections
    :rtype: integer
    :return: the number of non-unique characters two words have in common
    """
    inter = set(word1.lower()).intersection(word2.lower())
    return len(inter)


def mostIntersectionsSort(d, currentWords):
    """
    :type: d: dictionary, currentWords: list of words
    :input: a dictionary and list of words for which sort the dictionary by most intersections with the currentWords
    :rtype: list of tuples, words and their clues
    :return: sorted list of words and their clues from the dictionary based on how many times they intersect with words from currentWords
    """
    interDict = {}
    for key in d:
        count = 0
        for word in currentWords:
            count += countIntersections(key, word)
        interDict[key] = count
    keys = sorted(list(d.keys()), key=lambda x: interDict[x], reverse=True)
    array = []
    for key in keys:
        array.append((key, d.get(key)))
    return array


if __name__ == '__main__':
    # d = makeDictionary()  # make the dictionary
    # # sort the keys according to length
    # print("SORTED KEYS BY LENGTH", shortestSort(d))

    # # count intersections between two words
    # print("The number of intersections between hello and world is: ",
    #       countIntersections("hello", "world"))
    # print("The number of intersections between hello and cello is:",
    #       countIntersections("hello", "cello"))

    # # sort keys by intersections
    # currentWords = ["hello", "world", "cello"]
    # print("SORTED KEYS BY INTERSECTIONS",
    #       mostIntersectionsSort(d, currentWords))

    # # test random dictionary maker
    d= makeRandomDictionary(20)
    print(d.keys())
