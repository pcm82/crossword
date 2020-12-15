import makeDict
import Crossword
import CreateCrossword
import time
import math

def best_first_runtime(dictionary, threshold, size, heuristic):
  bestTime0 = time.perf_counter()
  bestCrossword = CreateCrossword.best_first_search(dictionary, threshold, size, 0)
  bestTime1 = time.perf_counter() - bestTime0
  return round(bestTime1, 5), (not (bestCrossword == None) and bestCrossword.percentFilled() > threshold)

def beam_runtime(dictionary, threshold, size, beam_size, heuristic):
  beamTime0 = time.perf_counter()
  beamCrossword = CreateCrossword.beamSearchCreator(dictionary, threshold, size, beam_size, 0)
  beamTime1 = time.perf_counter() - beamTime0
  return round(beamTime1, 5), (not (beamCrossword == None) and beamCrossword.percentFilled() > threshold)

def brute_runtime(dictionary, threshold, size, heuristic):
  bruteTime0 = time.perf_counter()
  bruteCrossword, threshold_met = CreateCrossword.bruteForceCreator(dictionary, threshold, size, 0)
  bruteTime1 = time.perf_counter() - bruteTime0
  return round(bruteTime1, 5), threshold_met

def make_table_best():
  """
  :type: none
  :input: none
  :rtype: returns a string and a vector of floats. 
  :return: returns a string table describing the data on how the crossword size 
          affects speed to get a crossword. Also returns a vector of times. 
  """
  times = []
  d_vec= []
  dict_size= 100
  for trial in range(10): 
    print("trial " + str(trial))
    t = []
    for d in range(10):
      dictionary = makeDict.makeRandomDictionary(dict_size, d + 1)
      threshold = 0.5
      d_vec.append(d + 1)
      size= d + 1
      bestTime0 = time.perf_counter()
      bestCrossword = CreateCrossword.bestFirstSearchCreator(dictionary, threshold, size, 0)
      bestTime1 = time.perf_counter() - bestTime0
      t.append(round(bestTime1, 5))
    times.append(t)
  return d_vec, times

def make_table_best2():
  """
  :type: none
  :input: none
  :rtype: returns a string and a vector of floats. 
  :return: returns a string table describing the data on how the crossword size 
          affects speed to get a crossword. Also returns a vector of times. 
  """
  times = []
  d_vec= []
  dict_size= 50
  for trial in range(5): 
    print("trial " + str(trial))
    t = []
    for d in range(10):
      dictionary = makeDict.makeRandomDictionary(dict_size, d + 1)
      threshold = 0.5
      d_vec.append(d + 1)
      size= d + 1
      rt, threshold_met= best_first_runtime(dictionary, threshold, size, 0)
      t.append(rt)
    times.append(t)
  return d_vec, times

def make_table_beam():
  """
  :type: none
  :input: none
  :rtype: returns a string and a vector of floats. 
  :return: returns a string table describing the data on how the crossword size 
          affects speed to get a crossword. Also returns a vector of times. 
  """
  times = []
  d_vec= []
  success= []
  dict_size= 100
  for trial in range(5): 
    print("trial " + str(trial))
    t = []
    s= []
    for d in range(10):
      dictionary = makeDict.makeRandomDictionary(dict_size, d + 1)
      threshold = 0.5
      d_vec.append(d + 1)
      size= d + 1
      rt, threshold_met= beam_runtime(dictionary, threshold, size, 3, 0)
      t.append(rt)
      s.append(threshold_met)
    times.append(t)
    success.append(s)
  return d_vec, times, success

def make_table_beam_size():
  times= []
  b_vec= []
  success= []
  dict_size= 100
  threshold = 0.6
  size= 5
  for trial in range(5):
    t= []
    s= []
    dictionary = makeDict.makeRandomDictionary(dict_size, size)
    for b in range(10):
      beam_size= math.ceil(10 ** (b / 2))
      b_vec.append(beam_size)
      print(beam_size)
      rt, threshold_met = beam_runtime(dictionary, threshold, size, beam_size, 0)
      t.append(rt)
      s.append(threshold_met)
    times.append(t)
    success.append(s)
  return b_vec, times, success      
     

def compare_BB_num_words():
  """
  :type: none
  :input: none
  :rtype: returns a string 
  :return: returns a string table describing the data on brute force vs beam 
          search for exponentially increasing lengths of dictionaries.  
  """ 
  t_brute= []
  t_best= []
  meets_threshold= []
  num= []
  result= "Dictionary Size:    Completed:   Brute Force Time:   Best First Search Time: \n"
  for exp in range(20):
    n= math.ceil(10**((exp + 3) / 8))
    num.append(n)
    print(n)
    dictionary = makeDict.makeRandomDictionary(n, 4)
    threshold = 0.4
    size= 4
    bestTime0 = time.perf_counter()
    bestCrossword = CreateCrossword.bestFirstSearchCreator(dictionary, threshold, size, 0)
    if not (bestCrossword == None):
        meets_threshold.append(True)
    else:
        meets_threshold.append(False)
    bestTime1 = time.perf_counter() - bestTime0
    t_best.append(round(bestTime1, 5))
    bruteTime0 = time.perf_counter()
    bruteCrossword, meetsThreshold = CreateCrossword.bruteForceCreator(dictionary, threshold, size, False)
    bruteTime1 = time.perf_counter() - bruteTime0
    t_brute.append(round(bruteTime1, 5))
    result += str(n) + "                  " + str(meets_threshold[exp]) + "              " + str(round(bruteTime1, 5)) + "              " + str(round(bestTime1, 5)) + "\n"
  print(num)
  print(t_brute)
  print(t_best)
  return result

def compare_BB_cross_size():
  """
  :type: none
  :input: none
  :rtype: returns a string 
  :return: returns a string table describing the data on brute force vs best first 
          search for exponentially increasing lengths of dictionaries.  
  """ 
  t_brute= []
  t_best= []
  d_vec= []
  dict_size= 50
  result= "Crossword Size:   Brute Force Time:   Best First Search Time: \n"
  for d in range(5):
    dictionary = makeDict.makeRandomDictionary(dict_size, d + 1)
    threshold = 0.5
    d_vec.append(d + 1)
    size= d + 1
    bestTime0 = time.perf_counter()
    bestCrossword = CreateCrossword.bestFirstSearchCreator(dictionary, threshold, size, 0)
    bestTime1 = time.perf_counter() - bestTime0
    t_best.append(round(bestTime1, 5))
    bruteTime0 = time.perf_counter()
    bruteCrossword, meetsThreshold = CreateCrossword.bruteForceCreator(dictionary, threshold, size, False)
    bruteTime1 = time.perf_counter() - bruteTime0
    t_brute.append(round(bruteTime1, 5))
    result += str(size) + "                " + str(round(bruteTime1, 5)) + "            " + str(round(bestTime1, 5)) + "\n"
  return d_vec, t_brute, t_best, result

def compare_BBB_num_words():
  """
  :type: none
  :input: none
  :rtype: returns vectors
  :return: returns a time matrix, where t[0], t[1], t[2] are the times for each dictionary 
            length for brute force search, best first search, and beam search respectively.
  """ 
  t= [[], [], []]
  success= [[], [], []]
  num= []
  for exp in range(20):
    n= math.ceil(10**((exp + 3) / 8))
    num.append(n)
    print(n)
    dictionary = makeDict.makeRandomDictionary(n, 4)
    threshold = 0.4
    size= 4
    rt_brute, success_brute = brute_runtime(dictionary, threshold, size, 0)
    t[0].append(rt_brute)
    success[0].append(success_brute)
    rt_best, success_best = best_first_runtime(dictionary, threshold, size, 0)
    t[1].append(rt_best)
    success[1].append(success_best)
    rt_beam, success_beam = beam_runtime(dictionary, threshold, size, 3, 0)
    t[2].append(rt_beam)
    success[2].append(success_beam)
  return num, t, success

def compare_BBB_cross_size():
  """
  :type: none
  :input: none
  :rtype: returns vectors
  :return: returns a time matrix, where t[0], t[1], t[2] are the times for each dictionary 
            length for brute force search, best first search, and beam search respectively.
  """ 
  t= [[], [], []]
  success= [[], [], []]
  dict_size= 100
  d_vec= []
  numtrials= 5
  for trial in range(numtrials):
    for d in range(4):
      print(d)
      dictionary = makeDict.makeRandomDictionary(dict_size, d + 1)
      threshold = 0.5
      d_vec.append(d + 1)
      size= d + 1
      rt_brute, success_brute = brute_runtime(dictionary, threshold, size, 0)
      t[0].append(rt_brute)
      success[0].append(success_brute)
      rt_best, success_best = best_first_runtime(dictionary, threshold, size, 0)
      t[1].append(rt_best)
      success[1].append(success_best)
      rt_beam, success_beam = beam_runtime(dictionary, threshold, size, 3, 0)
      t[2].append(rt_beam)
      success[2].append(success_beam)
  return d_vec, t, success

def compare_worst_case():
  """
  :type: none
  :input: none
  :rtype: returns an int vector, and two float vectors. 
  :return: returns an int vector to numerate the number of random trials and 
            two float vectors to represent the run times of each algorithm for 
            each  trial
  """
  t_brute= []
  t_best= []
  dict_size= 3
  trials= range(50)
  for trial in trials:
    dictionary = makeDict.makeRandomDictionary(dict_size, 4)
    threshold = 0.5
    size= 5
    bestTime0 = time.perf_counter()
    bestCrossword = CreateCrossword.bestFirstSearchCreator(dictionary, threshold, size, 0)
    bestTime1 = time.perf_counter() - bestTime0
    t_best.append(round(bestTime1, 5))
    bruteTime0 = time.perf_counter()
    bruteCrossword, meetsThreshold = CreateCrossword.bruteForceCreator(dictionary, threshold, size, False)
    bruteTime1 = time.perf_counter() - bruteTime0
    t_brute.append(round(bruteTime1, 5))
  return trials, t_brute, t_best

def compare_worst_case2():
  """
  :type: none
  :input: none
  :rtype: returns an int vector, and two float vectors. 
  :return: returns an int vector to numerate the number of random trials and 
            two float vectors to represent the run times of each algorithm for 
            each  trial
  """
  t_brute= []
  t_best= []
  t_beam= []
  dict_size= 3
  trials= range(50)
  for trial in trials:
    print(trial)
    dictionary = makeDict.makeRandomDictionary(dict_size, 4)
    threshold = 0.5
    size= 5
    rt_brute, success_brute = brute_runtime(dictionary, threshold, size, 0)
    t_brute.append(rt_brute)
    rt_best, success_best= best_first_runtime(dictionary, threshold, size, 0)
    t_best.append(rt_best)
    rt_beam, success_beam = beam_runtime(dictionary, threshold, size, 5, 0)
    t_beam.append(rt_beam)
  return trials, t_brute, t_best, t_beam

def compareHeuristics():
  """
  :type: none
  :input: none
  :rtype: returns a string, 3 float matrices
  :return: returns a string table describing the data on how the best first size 
          affects speed to get a crossword.  Also returned 3 float matrices, 
          each with two rows. Row 0 is generated using heuristic 0 for all 
          matrices, row 1 is generated using heuristic 1 for all matrices. 
  """ 
  t = [[], []]
  perc_filled = [[], []]
  perc_inter = [[], []]
  result= "Trial:  | Heur 0 time: | Heur 1 time: |  Heur 0 Percent Filled: | Heur 0 Percent Filled: | Heur 0 Percent Intersections: | Heur 1 Percent Intersections \n"
  for trial in range(15):
    print("performing trial " + str(trial))
    dictionary = makeDict.makeRandomDictionary(100, 8)
    threshold = 0.5
    size= 8
    for i in range(2):
      print("performing heuristic " + str(i))
      bestTime0 = time.perf_counter()
      bestCrossword = CreateCrossword.best_first_search(dictionary, threshold, size, i)
      if bestCrossword == None:
        perc_filled[i].append(None)
        perc_inter[i].append(None)
      else:
        perc_filled[i].append(bestCrossword.percentFilled())
        perc_inter[i].append(bestCrossword.percentIntersect())
      bestTime1 = time.perf_counter() - bestTime0
      t[i].append(round(bestTime1, 5))

    result += str(trial) + "   " + str(round(t[0][trial], 5)) + "     " + str(round(t[1][trial], 5)) + "     " + str(round(perc_filled[0][trial], 5)) + "     " + str(round(perc_filled[1][trial], 5)) + "     " + str(round(perc_inter[0][trial], 5)) + "     " + str(round(perc_inter[1][trial], 5)) + "\n"

  return t, perc_filled, perc_inter, result  
  


if __name__ == '__main__':
  """
  Analyze time complexity of best first search
  """
  # d_vec, t = make_table_best()
  # print("Dimension: \n" + str(d_vec) + "\n")
  # print("Time: \n" + str(t) + "\n")

  """
  Analyze time complexity of actual best first search
  """
  # d_vec, t = make_table_best2()
  # print("Dimension: \n" + str(d_vec) + "\n")
  # print("Time: \n" + str(t) + "\n")

  """
  Analyze time complexity of beam search
  """
  # d_vec, t, s = make_table_beam()
  # print("Dimension: \n" + str(d_vec) + "\n")
  # print("Time: \n" + str(t) + "\n")
  # b= [[int(s) for s in row] for row in s]
  # print("Success: \n" + str(b) + "\n")

  # b_vec, t, s= make_table_beam_size()
  # print("Beam Size: \n" + str(b_vec) + "\n")
  # print("Time: \n" + str(t) + "\n")
  # b= [[int(s) for s in row] for row in s]
  # print("Success: \n" + str(b) + "\n")

  """
  Compare brute force vs best first search with respect to dictionary size
  """
  # result = compare_BB_num_words() #takes a long time, be patient
  # print(result)

  """
  Compare brute force vs best first vs beam search with respect to dictionary size
  """
  # num, t, success = compare_BBB_num_words() #takes a long time, be patient
  # print("Comparing brute vs best first vs beam searches with respect to dicitonary size: ")
  # print("Dictionary Sizes: \n")
  # print(num)
  # print("Runtimes: \n") 
  # print(t)
  # print("Threshold met?")
  # b= [[int(s) for s in row] for row in success]
  # print(b)

  """
  Compare brute force vs best first vs beam search with respect to crossword size
  """
  # d_vec, t, success = compare_BBB_cross_size() #takes a long time, be patient
  # b= [[int(s) for s in row] for row in success]
  # print("Comparing brute vs best first vs beam searches with respect to crossword size: ")
  # print("Crossword sizes: \n")
  # print(d_vec)
  # print("Runtimes: \n") 
  # print(t)
  # print("Threshold met?")
  # print(b)


  """
  Compare brute force vs best first search with respect to crossword size
  """
  # d_vec, t_brute, t_best, result = compare_BB_cross_size()
  # print("Dimension: \n" + str(d_vec) + "\n")
  # print("Brute Force Time: \n" + str(t_brute) + "\n")
  # print("Best First Search Time: \n" + str(t_best) + "\n")
  # print(result)

  """
  Compare brute force vs best first in worst case: 
  """
  # trials, t_brute, t_best= compare_worst_case()
  # print("Trials: \n" + str(trials) + "\n")
  # print("Brute Force Time: \n" + str(t_brute) + "\n")
  # print("Best First Search Time: \n" + str(t_best) + "\n")

  """
  Compare brute force vs actual best vs beam first in worst case: 
  """
  # trials, t_brute, t_best, t_beam= compare_worst_case2()
  # print("Trials: \n" + str(trials) + "\n")
  # print("Brute Force Time: \n" + str(t_brute) + "\n")
  # print("Best First Search Time: \n" + str(t_best) + "\n")
  # print("Beam Search Time: \n" + str(t_beam) + "\n")


  """
  Compare Heuristics
  """
  t, perc_filled, perc_inter, result= compareHeuristics()
  print("Time: \n" + str(t) + "\n")
  print("Percent Filled: \n" + str(perc_filled) + "\n")
  print("Percent Intersections: \n" + str(perc_inter) + "\n")
  print(result)



