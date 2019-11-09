# Maggie Jennings and Serena Fan
# CS 111 Final Project
# foxAndHounds.py

import Tkinter as tk
import animation

#RUNNING ISSUES LIST:

#   Hound winning conditions 

#From Lab 11:
class PhotoSlide(animation.AnimatedObject):
    
    # Read in an image file
    def __init__(self,canvas,filename,x,y):
        self.canvas = canvas
        self.photo = tk.PhotoImage(file = filename) 
        self.phototag = self.canvas.create_image(x,y, image=self.photo)
        self.photo_width=self.photo.width()
        self.photo_height=self.photo.height()
        self.delta = 5
        self.deltaY = 7
        
    def move(self): 
        if self.delta > 0:
            x1, y1 = self.canvas.coords(self.phototag)
            if x1 >= self.canvas.winfo_width()-self.photo_width/2: # bounce back from R wall
                self.delta *= -1
            
        elif self.delta < 0:
            x1, y1 = self.canvas.coords(self.phototag)
            if x1 <= self.photo_width/2: # bounce back from L wall
                self.delta *= -1
                
        if self.deltaY > 0:
            x1, y1 = self.canvas.coords(self.phototag)
            if y1 >= self.canvas.winfo_height()-self.photo_height/2: # bounce back from bottom
                self.deltaY *= -1
            
        elif self.deltaY < 0:
            x1, y1 = self.canvas.coords(self.phototag)
            if y1 <= self.photo_height/2: # bounce back from top
                self.deltaY *= -1
           
        self.canvas.move(self.phototag,self.delta,self.deltaY) # move left and right

class GameApp():
    def __init__(self,root,*args):
        self.root = root
        myFrame = tk.Frame(root)
        myFrame.pack()
        root.title('Fox and Hounds')
        
        # create canvas
        self.canvas = animation.AnimationCanvas(myFrame, width=400, height=400)
        self.canvas.pack()
        #self.canvas = tk.Canvas(myFrame,width=400,height=400,bg='white') 
        #self.canvas.pack()
        self.canvas.grid(row=0,columnspan=6)
        self.canvas.bind('<Button-1>',self.onClick)
        self.firstClick = True
        self.playerIndex = 0
        self.boxList = [] 
        self.winningBoxes = []
        self.createWidgets()
        self.isPlayer0Turn = True
        self.isPlayer1Turn = False
        
    def createWidgets(self):  
        # create and alternate the colors of the squares on the board between white and black
        # alternate the starting color of each line of squares
        for i in range(8): 
            # for even lines, every odd number square is black and even number square is white
            if i %2!=0:
                for n in range(8):
                    if n%2 != 0:
                        box = self.canvas.create_rectangle(50*i,50*n,50+(50*i),50+(50*n),fill='black')
                        self.boxList.append(box)    
                    else:
                        self.canvas.create_rectangle(50*i,50*n,50 +(50*i),50+ (50*n),fill='white')
            else:
                 # for odd lines, every even number square is black and odd number square is white
                for n in range (8):
                    if n%2 ==0:
                        box = self.canvas.create_rectangle(50*i,50*n,50 +(50*i),50+ (50*n),fill='black')
                        self.boxList.append(box)
                        if n==0:
                            self.winningBoxes.append(box)
                    else:          
                        self.canvas.create_rectangle(50*i,50*n,50 +(50*i),50+ (50*n),fill='white')              
                           
        # create game pieces: 1 orange piece that represents the fox and 
        #4 brown pieces that represent the hounds
        self.fox = self.canvas.create_oval(250,350,300,400,fill='orange')
        self.hound1 = self.canvas.create_oval(0,0,50,50,fill='brown')
        self.hound2 = self.canvas.create_oval(100,0,150,50,fill='brown')
        self.hound3 = self.canvas.create_oval(200,0,250,50,fill='brown')
        self.hound4 = self.canvas.create_oval(300,0,350,50,fill='brown')
        # create a list that can later be used to check coordinates to make sure pieces don't overlap
        self.pieces = [self.fox,self.hound1,self.hound2,self.hound3,self.hound4]
        self.hounds = [self.hound1,self.hound2,self.hound3,self.hound4]
        # the first player to move is the fox
        self.selectedPiece = self.fox
        
        # create button panel
        buttonPanel = tk.Frame(root)
        buttonPanel.pack()
        
        # create quit button and instructions button
        quitButton = tk.Button(buttonPanel,text='Quit',command=self.onQuitButtonClick)
        quitButton.grid(row=3,column=2)
        instructionButton = tk.Button(buttonPanel,text='Instructions',command=self.onInstructionButtonClick)
        instructionButton.grid(row=3,column=1)
        
        # create text label for incorporating helpful messages
        self.results = tk.StringVar()
        self.resultsLabel = tk.Label(buttonPanel, fg='red', font='Times 15 italic', textvariable=self.results)
        self.resultsLabel.grid(row=2,columnspan=3)
        
        self.turnMessage = tk.StringVar()
        self.turnMessage.set('Fox moves first.')
        self.turnLabel = tk.Label(buttonPanel, fg='blue', font='Times 15 italic', textvariable=self.turnMessage)
        self.turnLabel.grid(row=1,columnspan=3)
        
    # turn off loop that moves the other piece so both players cannot move simultaneously    
    def newPlayer(self):
        if self.isPlayer0Turn:
            self.isPlayer1Turn = True
            self.isPlayer0Turn = False
            self.turnMessage.set("Now it is the Hounds' turn!")
            self.hasGameBeenWon()
            self.results.set('')
        else:
            self.isPlayer1Turn = False
            self.isPlayer0Turn = True
            self.turnMessage.set("Now it is the Fox's turn!")
            self.hasGameBeenWon()
            self.results.set('')

    # move selected piece
    def onClick(self,event):
        if self.firstClick:
            # first click designates which piece to move
            for piece in self.pieces:
                coords = self.canvas.coords(piece)
                if (coords[0] <= event.x <= coords[2]) and (coords[1] <= event.y <= coords[3]):
                    self.selectedPiece = piece
                    self.results.set('')
        # second click designates which square to move the piece too. The piece will only move if
        # another piece is not in that square and if the square is within the range of permitted movement
        else:
            # fox
            #loop checks if a piece is already in the clicked on box
            if self.isPlayer0Turn:
                isPieceThere = False
                for piece in self.pieces:
                    oldCoords = self.canvas.coords(piece)
                    if (oldCoords[0] <= event.x <= oldCoords[2]) and (oldCoords[1] <= event.y <= oldCoords[3]):
                        self.results.set('A piece is already there!')
                        isPieceThere = True
                
                if isPieceThere == False:
                    if self.selectedPiece == self.fox:
                        coords = self.canvas.coords(self.fox)
                        if ((coords[0]-50) <= event.x <= (coords[2]+50)) and ((coords[1]-50) <= event.y <= (coords[3]+50)):
                            for box in self.boxList:
                                boxCoords = self.canvas.coords(box)
                                if (boxCoords[0] <= event.x <= boxCoords[2]) and (boxCoords[1] <= event.y <= boxCoords[3]):
                                    self.canvas.coords(self.selectedPiece,(boxCoords[0],boxCoords[1],
                                    boxCoords[2],boxCoords[3]))
                                    self.newPlayer()                             
                        else: 
                            self.results.set('Not a legal move!')
            # hounds           
            elif self.isPlayer1Turn:
                isPieceThere = False
                for piece in self.pieces:
                    oldCoords = self.canvas.coords(piece)
                    if (oldCoords[0] <= event.x <= oldCoords[2]) and (oldCoords[1] <= event.y <= oldCoords[3]):
                        self.results.set('A piece is already there!')
                        isPieceThere = True
                        
                if isPieceThere == False:
                    coords = self.canvas.coords(self.selectedPiece)
                    if ((coords[0]-50) <= event.x <= (coords[2]+50)) and ((coords[1]) <= event.y <= (coords[3]+50)):
                        #removed '-50' to keep hound pieces from moving backwards
                        for box in self.boxList:
                            boxCoords = self.canvas.coords(box)
                            if (boxCoords[0] <= event.x <= boxCoords[2]) and (boxCoords[1] <= event.y <= boxCoords[3]):
                                self.canvas.coords(self.selectedPiece,(boxCoords[0],boxCoords[1],
                                boxCoords[2],boxCoords[3]))
                                self.newPlayer()
                                  
                    elif ((coords[0]-50) > event.x > (coords[2]+50)) or ((coords[1]) > event.y > (coords[3]+50)): 
                        self.results.set('Not a legal move!')
                    else:
                        self.results.set('Not a legal move!')
        
        #  changes click setting after every click (for example, if it is the first click, 
        # it changes to the second and vice versa)      
        self.firstClick = not self.firstClick

    def hasGameBeenWon(self):
        #FOX CRITERIA
        #for fox piece, checks if coordinates match those of the winning boxes (the four in the top row)
        foxCoords = self.canvas.coords(self.fox)
        for box in self.winningBoxes:
            boxCoords = self.canvas.coords(box)
            if ((boxCoords[0] == foxCoords[0]) and (boxCoords[1] == foxCoords[1]) 
            and  (boxCoords[2] == foxCoords[2]) and (boxCoords[3] == foxCoords[3])):
                #if fox is in one of the spaces, set the winning message
                #and show an animation
                self.turnMessage.set('Fox has won the game!')
                fox = PhotoSlide(self.canvas,'smallfox.gif',200,200)
                self.canvas.addItem(fox)
                self.canvas.start()
            
        
        # HOUND CRITERIA
        #lists to be cleared/updated each time function is called
        self.surrounding = []
        self.ifSurrounding = []
        for box in self.boxList:
            boxCoords = self.canvas.coords(box)
            newBoxCoords = []
            
            #criteria for surrounding boxes 
            upperX = foxCoords[0]+50
            lowerX = foxCoords[0]-50
            upperY = foxCoords[1]+50
            lowerY = foxCoords[1]-50
            
            #updated coordinates to reduce Python's rounding errors
            for coord in boxCoords:
                newBoxCoords.append(int(coord +.3))
                
            # top X and Y of the new box
            boxX = newBoxCoords[0]
            boxY = newBoxCoords[1]
            
            #check uuper left corner of each box to see if it matches the critera
            if ((boxX == upperX) and (boxY == upperY)) or ((boxX == lowerX) and (boxY == upperY)) or ((boxX == upperX) and (boxY == lowerY)) or ((boxX == lowerX) and (boxY == lowerY)):
                #if the box matches the criteria for a surrounding box, add it to the list
                self.surrounding.append(box)
        #print self.surrounding
      
      #if coordinates of one of the hounds match one of the legal surrounding boxes, add a value to a list
        for hound in self.hounds:
            houndCoords = self.canvas.coords(hound)
            for box in self.surrounding:
                boxCoords = self.canvas.coords(box)
                if (boxCoords[0] == houndCoords[0]) and (boxCoords[1] == houndCoords[1]) and  (boxCoords[2] == houndCoords[2]) and (boxCoords[3] == houndCoords[3]):
                    self.ifSurrounding.append(True)
        #print self.ifSurrounding
            
        
        #use list to check number of surrounding hounds 
        #if number of sourrounding hounds is equal to number of surrounding boxes, 
        #hounds win
        if (((len(self.ifSurrounding) == len(self.surrounding)) and (len(self.surrounding) > 0))
        # (plausible) EXTRA CONDITIONS FOR THE SIDES  
        or ((foxCoords[0] == 0) and (len(self.ifSurrounding) > 1)) 
        or ((foxCoords[0] == 350) and (len(self.ifSurrounding) > 1))):
            self.turnMessage.set('Hounds won the game!') 
            hounds = PhotoSlide(self.canvas,'hounds.gif',200,200)
            self.canvas.addItem(hounds)
            self.canvas.start() 
        
    def onInstructionButtonClick(self):
        instWind = InstructionWindow()
        instWind.mainloop()
    
    def onQuitButtonClick(self):
        root.destroy()
        
#new class to create instruction window for viewing 
class InstructionWindow(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self,width=400, height=500)
        self.title("How to Play")
        pic = tk.PhotoImage(file='instructions.gif')  
        self.iLabel = tk.Label(self,image=pic,borderwidth=3)
        self.iLabel.pic = pic
        self.iLabel.grid(column=0,row=0)

root = tk.Tk()
app = GameApp(root)
root.mainloop()