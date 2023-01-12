import random, pygame, sys
from pygame.locals import *

FPS = 30 # frames per second, controls the overall speed of the game
WINDOWWIDTH = 640 # width of the game window in pixels
WINDOWHEIGHT = 480 # height of the game window in pixels
REVEALSPEED = 8 # speed at which boxes reveal and cover in pixels per frame
BOXSIZE = 40 # size of each box (height and width) in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 10 # number of columns of boxes on the game board
BOARDHEIGHT = 7 # number of rows of boxes on the game board
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board must have an even number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2) # calculate the x-coordinate of the top left corner of the game board
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2) # calculate the y-coordinate of the top left corner of the game board

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 102,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

BGCOLOR = GREEN
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Memory Game')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None # stores the (x, y) of the first box clicked.

    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    while True: # main game loop
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            # The mouse is currently over a box.
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True # set the box as "revealed"
                if firstSelection == None: # the current box was the first box clicked
                    firstSelection = (boxx, boxy)
                else: # the current box was the second box clicked
                    # Check if there is a match between the two icons.
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                    if icon1shape != icon2shape or icon1color != icon2color:
                        # Icons don't match. Re-cover up both selections.
                        pygame.time.wait(1000) # 1000 milliseconds = 1 sec
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes): # check if all pairs found
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)

                        # Reset the board
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        # Show the fully unrevealed board for a second.
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        # Replay the start game animation.
                        startGameAnimation(mainBoard)
                    firstSelection = None # reset firstSelection variable

        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateRevealedBoxesData(val):
    """
    This function creates a 2D list that keeps track of which boxes on the game board have been revealed.
    The "val" parameter is the initial value for each element in the list (typically False for not revealed, or True for revealed)
    """
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT) # creates a list with "val" repeated BOARDHEIGHT times, and appends it to the revealedBoxes list
    # returns the completed 2D list of revealed boxes
    return revealedBoxes


def getRandomizedBoard():
    """
    Creates a randomized game board with a set of icons.
    The board is a 2D list of tuples, where each tuple contains a shape and a color.
    """
    icons = [] # Get a list of every possible shape in every possible color.
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append( (shape, color) )

    random.shuffle(icons) # randomize the order of the icons list
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2) # calculate how many icons are needed
    icons = icons[:numIconsUsed] * 2 # make two of each
    random.shuffle(icons)

    # Create the board data structure, with randomly placed icons.
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0] # remove the icons as we assign them
        board.append(column)
    return board

def splitIntoGroupsOf(groupSize, theList):
    """
    This function takes in two parameters, groupSize and theList.
    It splits theList into a list of lists, where the inner lists have at most groupSize number of items.
    """
    result = [] #initialize an empty list to store the split lists
    for i in range(0, len(theList), groupSize):  #iterate over theList with a step of groupSize
        result.append(theList[i:i + groupSize]) #append a slice of theList from i to i+groupSize to the result list
    return result #return the final list of lists.


def leftTopCoordsOfBox(boxx, boxy):
    """
    Convert board coordinates to pixel coordinates
    boxx: x-coordinate of the box on the board (column)
    boxy: y-coordinate of the box on the board (row)
    returns: a tuple containing the left and top pixel coordinates of the box
    """
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


def getBoxAtPixel(x, y):
    """
    Given x and y coordinates, this function returns the box number (in terms of
    column and row) that the coordinates belong to. If the coordinates do not belong
    to any box, it returns (None, None).
    """
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25)  # this variable is used as syntactic sugar for referencing 1/4 of the box size
    half =    int(BOXSIZE * 0.5)   # get pixel coordinates from board coordinates

    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
    # Draw the shapes
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)  # draw the outer circle
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5) # draw the inner circle
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))  # draw the square
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))  # draw the diamond
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top)) # draw the diagonal line from top left to bottom right
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))  # draw the diagonal line from bottom left to top right
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half)) # draw the oval


def getShapeAndColor(board, boxx, boxy):
    """
    Given the game board, and x, y coordinates for a box,
    this function returns the shape and color of the icon in that box
    """
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    """
    Draws boxes being covered/revealed.
    board: the game board containing the icons
    boxes: a list of two-item lists, which have the x & y spot of the box.
    coverage: the amount of coverage for boxes, where 0 is fully revealed and BOXSIZE is fully covered
    """
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0: # only draw the cover if there is an coverage
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    # Do the "box reveal" animation.
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):      # For each iteration, coverage decreases by REVEALSPEED. This causes the boxes to appear to slide open
        drawBoxCovers(board, boxesToReveal, coverage)  # Draw the boxes with the updated coverage value. This causes the boxes to appear to slide open


def coverBoxesAnimation(board, boxesToCover):
    # Do the "box cover" animation.
    # Loop through a range of values, incrementing by the REVEALSPEED variable

    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage) #     # Draw the box covers with the current coverage level


def drawBoard(board, revealed):
    # Iterate through each column (boxx) and row (boxy) on the game board
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            # Get the left and top pixel coordinates of the current box
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # If the box is not revealed, draw a covered box using the BOXCOLOR
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # If the box is revealed, draw the icon at that position using the shape and color from the board
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    #Draws a highlighted border around the box at the given x and y coordinates on the board
    left, top = leftTopCoordsOfBox(boxx, boxy)
    # Draw a rectangle with a 4 pixel wide border, offset by 5 pixels from the box coordinates
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def startGameAnimation(board):
    # Randomly reveal the boxes 8 at a time.
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)
    #Draw the initial state of the game board with all boxes covered
    drawBoard(board, coveredBoxes) 
    #Iterate through each group of boxes and reveal them one group at a time with a slight delay between each group
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


def gameWonAnimation(board):
    # flash the background color when the player has won
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):  # 13 iterations of animation
        color1, color2 = color2, color1  # swap colors for each iteration
        DISPLAYSURF.fill(color1)  # fill the background with the current color
        drawBoard(board, coveredBoxes) # draw the board with all boxes covered
        pygame.display.update()  # update the display with the new background color and board
        pygame.time.wait(300)  # wait for 300 milliseconds before swapping colors again


def hasWon(revealedBoxes):
    """
    Returns True if all the boxes have been revealed, otherwise False
    Input: revealedBoxes (list) - a 2D list that keeps track of the state of each box (True if revealed, False if covered)
    Output: True if all boxes are revealed, False otherwise
    """
    for i in revealedBoxes:
        if False in i:
            return False # return False if any boxes are covered.
    return True


if __name__ == '__main__':
    main()
