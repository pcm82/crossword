import makeDict
import Crossword
import CreateCrossword
import time
import math

def compare_beams():
  """
  :type: none
  :input: none
  :rtype: returns a string and a vector of floats. 
  :return: returns a string table describing the data on how the beam size 
          affects speed to get a crossword. Also returns a vector of times. 
  """ 
  t= []
  beams= []
  meets_threshold= []
  result= "Beam Size:      Completed:        Time:     \n"
  dictionary = makeDict.makeRandomDictionary(100, 10)
  for exp in range(50):
    threshold = 0.5
    size= 10
    beam_size= math.ceil(10**(exp / 2))
    beams.append(beam_size)
    beamTime0 = time.perf_counter()
    beamCrossword = CreateCrossword.beamSearchCreator(dictionary, threshold, size, beam_size, 0)
    if not (beamCrossword == None):
        meets_threshold.append(True)
    else:
        meets_threshold.append(False)
    beamTime1 = time.perf_counter() - beamTime0
    t.append(round(beamTime1, 5))
    result += str(beam_size) + "               " + str(not (beamCrossword == None)) + "              " + str(round(beamTime1, 5)) + "\n"
  print(beams)
  print(t)
  return t, result

def compare_BB_num_words():
  """
  :type: none
  :input: none
  :rtype: returns a string 
  :return: returns a string table describing the data on brute force vs beam 
          search for exponentially increasing lengths of dictionaries.  
  """ 
  t_brute= []
  t_beam= []
  meets_threshold= []
  beam= 3
  num= []
  result= "Dictionary Size:    Completed:   Brute Force Time:   Beam Search Time: \n"
  for exp in range(20):
    n= math.ceil(10**((exp + 3) / 8))
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
    result += str(n) + "                  " + str(meets_threshold[exp]) + "              " + str(round(bruteTime1, 5)) + "              " + str(round(beamTime1, 5)) + "\n"
  print(num)
  print(t_brute)
  print(t_beam)
  return result

def compare_BB_cross_size():
  """
  :type: none
  :input: none
  :rtype: returns a string 
  :return: returns a string table describing the data on brute force vs beam 
          search for exponentially increasing lengths of dictionaries.  
  """ 
  t_brute= []
  t_beam= []
  d_vec= []
  beam= 3
  dict_size= 50
  result= "Crossword Size:   Brute Force Time:   Beam Search Time: \n"
  for d in range(5):
    dictionary = makeDict.makeRandomDictionary(dict_size, d + 1)
    threshold = 0.5
    d_vec.append(d + 1)
    size= d + 1
    beamTime0 = time.perf_counter()
    beamCrossword = CreateCrossword.beamSearchCreator(dictionary, threshold, size, beam, 0)
    print("finished beam")
    beamTime1 = time.perf_counter() - beamTime0
    t_beam.append(round(beamTime1, 5))
    bruteTime0 = time.perf_counter()
    bruteCrossword, meetsThreshold = CreateCrossword.bruteForceCreator(dictionary, threshold, size, False)
    bruteTime1 = time.perf_counter() - bruteTime0
    t_brute.append(round(bruteTime1, 5))
    result += str(size) + "                " + str(round(bruteTime1, 5)) + "            " + str(round(beamTime1, 5)) + "\n"
  return d_vec, t_brute, t_beam, result

def compareHeuristics():
  """
  :type: none
  :input: none
  :rtype: returns a string, 3 float matrices
  :return: returns a string table describing the data on how the beam size 
          affects speed to get a crossword.  Also returned 3 float matrices, 
          each with two rows. Row 0 is generated using heuristic 0 for all 
          matrices, row 1 is generated using heuristic 1 for all matrices. 
  """ 
  t = [[], []]
  perc_filled = [[], []]
  perc_inter = [[], []]
  beam_size = 3
  result= "Trial:  | Heur 0 time: | Heur 1 time: |  Heur 0 Percent Filled: | Heur 0 Percent Filled: | Heur 0 Percent Intersections: | Heur 1 Percent Intersections \n"
  for trial in range(20):
    print("performing trial " + str(trial))
    dictionary = makeDict.makeRandomDictionary(100, 8)
    threshold = 0.5
    size= 8
    for i in range(2):
      print("performing heuristic " + str(i))
      beamTime0 = time.perf_counter()
      beamCrossword = CreateCrossword.beamSearchCreator(dictionary, threshold, size, beam_size, i)
      if beamCrossword == None:
        perc_filled[i].append(None)
        perc_inter[i].append(None)
      else:
        perc_filled[i].append(beamCrossword.percentFilled())
        perc_inter[i].append(beamCrossword.percentIntersect())
      beamTime1 = time.perf_counter() - beamTime0
      t[i].append(round(beamTime1, 5))

    result += str(trial) + "   " + str(round(t[0][trial], 5)) + "     " + str(round(t[1][trial], 5)) + "     " + str(round(perc_filled[0][trial], 5)) + "     " + str(round(perc_filled[1][trial], 5)) + "     " + str(round(perc_inter[0][trial], 5)) + "     " + str(round(perc_inter[1][trial], 5)) + "\n"

  return t, perc_filled, perc_inter, result  
  

if __name__ == '__main__':
  """
  Compare beam sizes
  """
  # t, result = compare_beams()
  # print(result)

  """
  Compare brute force vs beam search with respect to dictionary size
  """
  # result = compare_BB_num_words() #takes a long time, be patient
  # print(result)

  """
  Compare brute force vs beam search with respect to crossword size
  """
  d_vec, t_brute, t_beam, result = compare_BB_cross_size()
  print("Dimension: \n" + str(d_vec) + "\n")
  print("Brute Force Time: \n" + str(t_brute) + "\n")
  print("Beam Search Time: \n" + str(t_beam) + "\n")
  print(result)

  """
  Compare Heuristics
  """
  # t, perc_filled, perc_inter, result= compareHeuristics()
  # print("Time: \n" + str(t) + "\n")
  # print("Percent Filled: \n" + str(perc_filled) + "\n")
  # print("Percent Intersections: \n" + str(perc_inter) + "\n")
  # print(result)



