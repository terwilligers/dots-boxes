'''
board.py
created by Sam Terwilliger
This class creates a board object containing a list of lists of dots, lines and boxes.
It takes as an imput the rows and columns of the board which must be even numbers. The third input
is the number of pixals between dots.
An input example is Board(rows, columns ,linelength, winHeight, winWidth)


Here is a layout of an example 6x6 input board (vline is vertical line and hline is
horizontal line):
[[dot, hline, dot, hline, dot, hline, dot]
[vline, square, vline, square, vline, square, vline]
[dot, hline, dot, hline, dot, hline, dot]
[vline, square, vline, square, vline, square, vline]
[dot, hline, dot, hline, dot, hline, dot]
[vline, square, vline, square, vline, square, vline]
[dot, hline, dot, hline, dot, hline, dot]]
'''


from graphics import *


class Board(GraphWin):

    def __init__(self, rows, columns, linelength, winHeight, winWidth):
        self.rows = rows
        self.columns = columns
        self.linelength = linelength
        self.winHeight = winHeight
        self.winWidth = winWidth
        self.board = []
        self.draw_values = []
        self.alt_values = []

        #for the dots the radius is always 4
        self.radius = 4
        self.pcolor = "black"

        #the number of squares each player has completed
        self.square_count1 = 0
        self.square_count2 = 0
        self.game_complete = False

        #These are arbitrary values to initial assign the click position to before the first click
        self.xclick = 250
        self.yclick = 250

        #For self.move, 0 corresponds to a human while 1 corresponds to the computer
        # self.move = 2 corresponds to the human getting another move because they clicked wrong
        self.move = 0
        self.square_found = False
        self.click_completed = False


    #draws the actual lines
    def draw(self, window, row_value, column_value):
        #This checks if the input is drawn yet and draws it if it is not
        if self.draw_values[row_value][column_value] == False:
            self.board[row_value][column_value].draw(window)
            self.draw_values[row_value][column_value] = True

    #invisible lines for the computer AI to use
    def alt_draw(self, window, row_value, column_value):
        #This checks if the input is drawn yet and draws it if it is not
        if self.draw_values[row_value][column_value] == False and self.alt_values[row_value][column_value] == False:
            self.alt_values[row_value][column_value] = True

    def clear_alts(self, window):
        for j in range(self.rows + 1):
            for i in range(self.columns + 1):
                if self.alt_values[j][i]:
                    self.alt_values[j][i] = False


    def build_board(self, window):
        '''This function creates a board list which contains lists of each of the elements in
            a row. It also creates a draw_values list that contains a boolean corresponding to
            each graphical element. False if it is not drawn yet and True if it has been drawn.
            All the dots are drawn immediately.
        '''
        for row in range(self.rows + 1):
            self.board.append([])
            self.draw_values.append([])
            self.alt_values.append([])

        self.win = window

        for y in range(self.rows + 1):
            py = (self.winHeight / 4.5) + (self.linelength / 2) * y
            for x in range(self.columns + 1):
                px = (self.winWidth / 4.5) + (self.linelength / 2) * x

                #Tests whether it is a dot
                if x % 2 == 0 and y % 2 == 0:
                    dot = Circle(Point(px, py), self.radius)
                    dot.draw(window)
                    dot.setFill(self.pcolor)
                    self.board[y].append(dot)
                    self.draw_values[y].append(True)
                    self.alt_values[y].append(True)

                #Tests whether it is a horizontal line
                elif  x % 2 != 0 and  y % 2 == 0:
                    self.hline = Line(Point(px - self.linelength/2, py), Point(px + self.linelength/2, py))
                    self.hline.setWidth(3)
                    self.board[y].append(self.hline)
                    self.draw_values[y].append(False)
                    self.alt_values[y].append(False)

               #Tests whether it is a vertical line
                elif  x % 2 == 0 and  y % 2 != 0:
                    self.vline = Line(Point(px, py - self.linelength/2), Point(px, py + self.linelength/2))
                    self.vline.setWidth(3)
                    self.board[y].append(self.vline)
                    self.draw_values[y].append(False)
                    self.alt_values[y].append(False)

                #It must be a square
                else:
                    self.square = Polygon(Point(px - round(self.linelength/2 - 2), py - round(self.linelength/2 -2)),
                                            Point(px + round(self.linelength/2 -2), py - round(self.linelength/2 -2)),
                                            Point(px + round(self.linelength/2 -2), py + round(self.linelength/2 -2)),
                                            Point(px - round(self.linelength/2 -2), py + round(self.linelength/2 -2)))
                    self.board[y].append(self.square)
                    self.draw_values[y].append(False)
                    self.alt_values[y].append(False)


    def click(self,window):
        '''This function registers a mouse click and loops through the board list. For every
            line it checks whether the clicks coordinants are within a rectangle drawn at the line.
            If they are then draw() is called on the line. If the click's coordinants do not coorespond
            to any line the player gets to go again.
        '''
        while True:
            clickPoint = window.getMouse()
            self.xclick = clickPoint.getX()
            self.yclick = clickPoint.getY()
            for j in range(len(self.board)):
                row = self.board[j]
                for i in range(len(row)):
                    if i % 2 != 0 and j % 2 == 0:
                        #it is a horizontal line
                        #It checks whether the click point is within a square drawn around the line
                        #board[j][i].getCenter().getX() returns the x coordinate of the center of the  dot
                        if (self.board[j][i].getCenter().getX() - self.linelength / 3
                        <= self.xclick <= self.board[j][i].getCenter().getX() + self.linelength / 3
                        and self.board[j][i].getCenter().getY() - self.linelength / 5
                        <= self.yclick <= self.board[j][i].getCenter().getY() + self.linelength / 5
                        and not self.draw_values[j][i]):
                            self.draw(window, j, i)
                            return
                    elif i % 2 == 0 and j % 2 != 0:
                        #it is a vertical line
                        #It checks whether the click point is within a square drawn around the line
                        if (self.board[j][i].getCenter().getX() - self.linelength / 5
                        <= self.xclick <= self.board[j][i].getCenter().getX() + self.linelength / 5
                        and self.board[j][i].getCenter().getY() - self.linelength / 3
                        <= self.yclick <= self.board[j][i].getCenter().getY() + self.linelength / 3
                        and not self.draw_values[j][i]):
                            self.draw(window, j, i)
                            return

    def check_square(self, window, color):
        '''This function loops through each of the elements in the board list and checks
            if it is a square. If it is it checks if all 4 of its neighbor lines have been
            drawn. If they have it fills in the square.
        '''
        for j in range(len(self.board)):
            row = self.board[j]
            for i in range(len(row)):
                #Checks if it is a square
                if (i % 2) != 0 and (j % 2) != 0:
                    #Checks if it already was drawn
                    if self.draw_values[j][i] == False:
                        #Checks if the surrounding lines have been drawn
                        if ((self.draw_values[j - 1][i] == True) and (self.draw_values[j][i-1] == True)
                            and (self.draw_values[j +1][i] == True) and (self.draw_values[j][i+1] == True)):
                            self.board[j][i].setFill(color)
                            self.board[j][i].setOutline(color)
                            self.draw(window, j, i)
                            self.square_found = True
                            #checks which player filled in the square(0 or 2 for human, 1 for computer)
                            if self.move == 0:
                                self.square_count1 += 1
                            else:
                                self.square_count2 += 1

        #This part tests if a square was completed and if it was the player gets another turn
        if self.square_found == False:
            if self.move == 0:
                self.move = 1
            else:
                self.move = 0
        else:
            self.square_found = False



    def find_neighbors(self, window, j, i):
        '''This function gives a list of the lines that are neigbors of another line, meaning
            that if they are drawn a square is completed. The middle lines have two sets of
            neighbors.
        '''
        neighbors = []
        if j == 0:
            #The line is a horizontal line in the first row
            neighbors.append([self.draw_values[j+2][i], self.draw_values[j+1][i-1], self.draw_values[j+1][i+1],
            self.alt_values[j+2][i], self.alt_values[j+1][i-1], self.alt_values[j+1][i+1]])
        elif j == self.rows:
            #The line is a horizontal line in the final row
            neighbors.append([self.draw_values[j-2][i], self.draw_values[j-1][i-1], self.draw_values[j-1][i+1],
            self.alt_values[j-2][i], self.alt_values[j-1][i-1], self.alt_values[j-1][i+1]])
        elif j % 2 == 0:
            #The line is a horizontal line in one of the middle rows
            neighbors.append([self.draw_values[j-2][i], self.draw_values[j-1][i-1], self.draw_values[j-1][i+1],
            self.alt_values[j-2][i], self.alt_values[j-1][i-1], self.alt_values[j-1][i+1]])
            neighbors.append([self.draw_values[j+2][i], self.draw_values[j+1][i-1], self.draw_values[j+1][i+1],
            self.alt_values[j+2][i], self.alt_values[j+1][i-1], self.alt_values[j+1][i+1]])
        elif i == 0:
            #The line is a vertical line in the first column
            neighbors.append([self.draw_values[j][i+2], self.draw_values[j+1][i+1], self.draw_values[j-1][i+1],
            self.alt_values[j][i+2], self.alt_values[j+1][i+1], self.alt_values[j-1][i+1]])
        elif i == self.columns:
            #The line is a vertical line in the final column
            neighbors.append([self.draw_values[j][i-2], self.draw_values[j+1][i-1], self.draw_values[j-1][i-1],
            self.alt_values[j][i-2], self.alt_values[j+1][i-1], self.alt_values[j-1][i-1]])
        elif i % 2 == 0:
            #The line is a vertical line in one of the middle columns
            neighbors.append([self.draw_values[j][i-2], self.draw_values[j-1][i-1], self.draw_values[j+1][i-1],
            self.alt_values[j][i-2], self.alt_values[j-1][i-1], self.alt_values[j+1][i-1]])
            neighbors.append([self.draw_values[j][i+2], self.draw_values[j-1][i+1], self.draw_values[j+1][i+1],
            self.alt_values[j][i+2], self.alt_values[j-1][i+1], self.alt_values[j+1][i+1]])
        return neighbors


    def game_finished(self):
        #checks if all squares have been filled in
        self.game_complete = True
        for j in range(len(self.board)):
            row = self.board[j]
            for i in range(len(row)):
                #Checks if it is a square
                if (i % 2) != 0 and (j % 2) != 0:
                    if self.draw_values[j][i] == False:
                        self.game_complete = False




def testModule(): #A test module to test one object of the board class

    winHeight = 500
    winWidth = 500
    win = GraphWin('Board Module Test', winWidth, winHeight)
    win.setBackground("white")

    # make a board and draw it in the window
    board = Board(6, 6, 50, winHeight, winWidth)
    board.build_board(win)


    print('Board test.')
    while win.winfo_exists():
        board.click(win)
        board.check_square(win, 'red')
        win.update()

if __name__ == '__main__':
   testModule()
