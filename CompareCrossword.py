import makeDict
import Crossword
import CreateCrossword
import time
import math

def compare_beams():
  t= []
  meets_threshold= []
  result= "Beam Size:      Completed:        Time:     \n"
  dictionary = makeDict.makeRandomDictionary(100, 10)
  for beam in range(50):
    threshold = 0.5
    size= 10
    beamTime0 = time.perf_counter()
    beamCrossword = CreateCrossword.beamSearchCreator(dictionary, threshold, size, beam + 1, 0)
    if not (beamCrossword == None):
        meets_threshold.append(True)
    else:
        meets_threshold.append(False)
    beamTime1 = time.perf_counter() - beamTime0
    t.append(round(beamTime1, 5))
    result += str(beam + 1) + "               " + str(not (beamCrossword == None)) + "              " + str(round(beamTime1, 5)) + "\n"
  print(t)
  return t, result

def compare_BB_num_words():
  t_brute= []
  t_beam= []
  meets_threshold= []
  beam= 3
  num= []
  result= "Dictionary Size:    Completed:   Brute Force Time:   Beam Search Time: \n"
  for exp in range(10):
    n= math.ceil(10**((exp + 3) / 4))
    num.append(n)
    print(n)
    dictionary = makeDict.makeRandomDictionary(n, 4)
    threshold = 0.4
    size= 4
    beamTime0 = time.perf_counter()
    beamCrossword = CreateCrossword.beamSearchCreator(dictionary, threshold, size, beam, 0)
    print("finished beam")
    if not (beamCrossword == None):
        meets_threshold.append(True)
    else:
        meets_threshold.append(False)
    beamTime1 = time.perf_counter() - beamTime0
    t_beam.append(round(beamTime1, 5))
    bruteTime0 = time.perf_counter()
    bruteCrossword, meetsThreshold = CreateCrossword.bruteForceCreator(dictionary, threshold, size, False)
    bruteTime1 = time.perf_counter() - bruteTime0
    t_brute.append(round(bruteTime1, 5))
    result += str(n) + "               " + str(meets_threshold[exp]) + "              " + str(round(bruteTime1, 5)) + "              " + str(round(beamTime1, 5)) + "\n"
  print(num)
  print(t_brute)
  print(t_beam)
  return result

  

if __name__ == '__main__':
  # result = compare_beams()
  # print(result)
  result = compare_BB_num_words()
  print(result)