import PySimpleGUI as sg 
import numpy
import pandas as pd
import CreateCrossword
import Crossword

BOX_SIZE = 50 # pixel size of box

def makeGUI(dim, crossword, words): 
  text_ids = [None]*dim

  # prepare words 
  across = []
  down = []
  for key in words:
    row, col, vert, clue = words[key]
    if vert: 
      down.append(clue)
    else:
      across.append(clue)

  if len(across) < len(down):
    across = across + [None] * (len(down)-len(across))
  elif len(across) > len(down):
    down = down + [None] * (len(across)-len(down))
  
  # data = {'Across': across, 'Down': down}
  # df = pd.DataFrame(data, columns = ['Across', 'Down'])
  # word_proc = df.to_string()
  # print(word_proc)
  word_proc = [across,down]
  print("before", word_proc)
  word_proc = numpy.transpose(word_proc)
  print("after", word_proc)

  #todo: make graph size dynamic, unsolved / solved button toggle 
  #[sg.Table(values = word_proc, justification="left", headings=["Across","Down"], key='_CLUES_')],
  layout = [
    [sg.Text(text="Welcome to your Crossword Puzzle")],
    [sg.Graph((dim*BOX_SIZE+10,dim*BOX_SIZE+10), (0,dim*BOX_SIZE+10), (dim*BOX_SIZE+10,0), key='_GRAPH_')], 
    [sg.Text("Clues")],
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
  testDict = {"helloworld": "CS greeting", "foobarfoobarfoobar":"3rd times the charm", "hell": "not heaven", "like": "enjoy", "seen": "noticed", "hi": "hey", "sup": "casual hey", "bellows": "loud yell", "cupholder": "hold my drink", "uplifting": "raise me up"}
  # take user input on crossword size
  # heuristic to use 
  # dictionary to use... tenatively our own
  crossword = CreateCrossword.beamSearchCreator(dictionary = testDict, threshold = 10/16, size = 4,beam= 3, heuristic= 0)
  if crossword == None: 
    print("Unfortunately this crossword cannot be displayed")
  else:
    dim = crossword.get_dim()
    fill = crossword.get_crossword()
    words = crossword.get_words()
    makeGUI(dim, fill, words)