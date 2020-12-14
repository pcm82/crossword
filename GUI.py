import PySimpleGUI as sg 
import numpy
import CreateCrossword
import ast
import Crossword

BOX_SIZE = 50 # pixel size of box

def makeGUI(dim, crossword, words): 
  text_ids = [None]*dim

  # prepare words 
  across = []
  down = []
  count = [(-1,-1)] # for proper labelling of the clues 
  for key in words:
    row, col, vert, clue = words[key]
    if vert: 
      if (row,col) not in count: 
        count.append((row,col))
      down.append(str(count.index((row,col))) + ". " +clue)
    else:
      if (row,col) not in count: 
        count.append((row,col))
      across.append(str(count.index((row,col))) + ". " +clue)

  # now sort so the list of clues shows in decreasing order
  across.sort(key=lambda x: int(x[0]))
  down.sort(key=lambda x: int(x[0]))

  across = "".join([str(clue) + "\n" for clue in across])
  down = "".join([str(clue) + "\n" for clue in down])
  #todo: make graph size dynamic, unsolved / solved button toggle 
  
  layout = [
    [sg.Text(text="Welcome to Any Person Any Crossword")],
    [sg.Graph((dim*BOX_SIZE+10,dim*BOX_SIZE+10), (0,dim*BOX_SIZE+10), (dim*BOX_SIZE+10,0), key='_GRAPH_')], 
    [sg.Text("Across \n" + across)],
    [sg.Text("Down \n" + down)],
    [sg.Button('Unsolved'), 
    sg.Button('Solved'), 
    sg.Button('Quit')] 
  ]

  window = sg.Window('Crossword Puzzle').Layout(layout).Finalize()
  
  g = window.FindElement('_GRAPH_')

  # todo: change fonts 
  for row in range(dim):
    text_ids[row] = [None]*dim
    for i in range(dim):
      if crossword[row][i] != None: # letter belongs here
        g.DrawRectangle((i*BOX_SIZE+5,row*BOX_SIZE+3), (i*BOX_SIZE+BOX_SIZE+5,row*BOX_SIZE+BOX_SIZE+3), line_color='black')
        text_ids[row][i] = g.DrawText(crossword[row][i],(i*BOX_SIZE+(BOX_SIZE/2),row*BOX_SIZE+(BOX_SIZE/2))) 
        if (row, i) in count: # label only when needed
          number = str(count.index((row,i)))
          g.DrawText(number.format(row*dim+i+1),(i*BOX_SIZE+10,row*BOX_SIZE+10))

      else: # letter does not belong here
        g.DrawRectangle((i*BOX_SIZE+5,row*BOX_SIZE+3), (i*BOX_SIZE+BOX_SIZE+5,row*BOX_SIZE+BOX_SIZE+3), line_color='black', fill_color='black')

      # corner number
      # g.DrawText('{}'.format(row*dim+i+1),(i*BOX_SIZE+10,row*BOX_SIZE+8))



  while True: 
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Quit':
      break
    elif event == 'Unsolved':
      for row in range(dim):
        for i in range(dim):
          g.DeleteFigure(text_ids[row][i])
      #window.FindElement('_UNSOLVED_').update(disabled=True)
      #window.FindElement('_SOLVED_').update(disabled=False)
    elif event == 'Solved':
      for row in range(dim):
        for i in range(dim):
          text_ids[row][i] = g.DrawText(crossword[row][i],(i*BOX_SIZE+(BOX_SIZE/2),row*BOX_SIZE+(BOX_SIZE/2))) 
      #window.FindElement('_SOLVED_').update(disabled=True)
      #window.FindElement('_UNSOLVED_').update(disabled=False)

  window.Close()

if __name__ == '__main__':
  print("Welcome to Any Person Any Crossword.")

  custom = input("Do you want to customize your dictionary? Y/N\n> ")
  approach = input("What approach would you like to use? 'Best' or 'Brute'\n> ")

  testDict = {"hello": "CS_greeting[0]", "world":"CS_greeting[1]", "foobar":"cs func", "hell": "not heaven", "like": "enjoy", "seen": "noticed", "hi": "hey", "sup": "casual hey", "bellow": "loud yell", "cupholder": "hold my drink", "uplifting": "raise me up"}
  thresh = 10/16
  dim = 4

  if custom == "Y":
    dim = input("How big of a crossword would you like to use?\n> ")
    dim = int(dim)
    thresh = input("What threshold would you like to use?\n> ")  
    thresh = float(thresh)
    testDict = input("What dictionary would you like to use?\n> ")
    testDict = ast.literal_eval(testDict)
  
  if approach == 'Brute': 
    flag = input("You have selected the Brute Force approach. Would you like to enable findBest? Y/N\n> ")
    print("Working on it! Hang tight for your crossword")
    if flag == 'Y':
      crossword = CreateCrossword.bruteForceCreator(dictionary=testDict, threshold=thresh, size=dim, findBest= True)[0]
    else:
      crossword = CreateCrossword.bruteForceCreator(dictionary=testDict, threshold=thresh, size=dim, findBest= False)[0]
  else: 
    print("Working on it! Hang tight for your crossword")
    crossword = CreateCrossword.bestFirstSearchCreator(dictionary = testDict, threshold = thresh, size = dim, heuristic= 0)
  

  if crossword == None: 
    print("Unfortunately this crossword cannot be displayed")
  else:
    dim = crossword.get_dim()
    fill = crossword.get_crossword()
    words = crossword.get_words()
    makeGUI(dim, fill, words)