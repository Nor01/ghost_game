from turtle import position
import pygame
import sys

board = [['  ' for i in range(6)] for i in range(6)]

## Create ghost pieces class that shows what team a piece is on(white,black), what type(good,bad) of piece it is and whether or not it can be killed by another selected piece.

class Piece:
    def __init__(self, team, type, image, killable=False):
        self.team = team
        self.type = type
        self.killable = killable
        self.image = image

bp = Piece('b','p','b_pawn.png')
wp = Piece('w', 'p', 'w_pawn.png')

starting_order = {(0, 0): None, (1, 0): pygame.image.load(bp.image),                  
                  (2, 0): pygame.image.load(bp.image), (3, 0): pygame.image.load(bp.image),
                  (4, 0): pygame.image.load(bp.image), (5, 0): None,                                   
                  (0, 1): None, (1, 1): pygame.image.load(bp.image),                  
                  (2, 1): pygame.image.load(bp.image), (3, 1): pygame.image.load(bp.image),                 
                  (4, 1): pygame.image.load(bp.image), (5, 1): None,                  

                  (0, 2): None, (1, 2): None, (2, 2): None, (3, 2): None,                  
                  (4, 2): None, (5, 2): None,                 
                  (0, 3): None, (1, 3): None, (2, 3): None, (3, 3): None,                  
                  (4, 3): None, (5, 3): None,   


                  (0, 4): None, (1, 4): pygame.image.load(wp.image), 
                  (2, 4): pygame.image.load(wp.image), (3, 4): pygame.image.load(wp.image),                  
                  (4, 4): pygame.image.load(wp.image), (5, 4): None,                 
                  (0, 5): None, (1, 5): pygame.image.load(wp.image), 
                  (2, 5): pygame.image.load(wp.image), (3, 5): pygame.image.load(wp.image),                  
                  (4, 5): pygame.image.load(wp.image), (5, 5): None,}

def create_board(board):
        
    return board

## returns the input if the input is within the boundaries of the board
def on_board(position):
    if position[0] > -1 and position[1] > -1 and position[0] < 6 and position[1] < 6:
        return True

## returns a string that places the rows and columns of the board in a readable manner
def convert_to_readeable(board):
    output = ''

    for i in board:
        for j in i:
            try:
                output+= j.team + j.type + ', '
            except:
                output+= j + ', '
        output+= '\n'
    return output

## resets "x's" and killable pieces
def deselect():
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == 'x ':
                board[row][column] = '  '
            else:
                try:
                    board[row][column].killable = False
                except:
                    pass
    return convert_to_readeable(board)

## Takes in board as argument then returns 2d array containing positions of valid moves
def highlight(board):
    highlighted = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'x ':
                highlighted.append((i,j))
            else:
                try:
                    if board[i][j].killable:
                        highlighted.append((i,j))
                except:
                    pass 
    return highlighted

def check_team(moves, index):
    row, col = index
    if moves%2 == 0:
        if board[row][col].team == 'w':
            return True
    else:
        if board[row][col].team == 'b':
            return True

WIDTH = 600
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))

""" 
This is creating the WINDOW that we are playing on, it takes a tuple argument which is the dimensions of the WINDOW so in this case 600 x 600px
"""

pygame.display.set_caption("Ghost Nor01")
WHITE = (255, 255, 255)
GREEN = (26, 78, 86)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)

class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.colour = WHITE
        self.occupied = None

    def draw(self,WINDOW):
        pygame.draw.rect(WINDOW, self.colour, (self.x, self.y, WIDTH / 6, WIDTH / 6))

    def setup(self, WINDOW):
        if starting_order[(self.row, self.col)]:
            if starting_order[(self.row, self.col)] == None:
                pass
            else:
                WINDOW.blit(starting_order[(self.row, self.col)], (self.x, self.y))

"""
        For now it is drawing a rectangle but eventually we are going to need it
        to use blit to draw the ghost pieces instead
"""

def make_grid(rows, width):
    grid = []
    gap = WIDTH // rows
    print(gap)

    for i in range(rows):
        grid.append([])

        for j in range(rows):
            node = Node(j, i, gap)
            grid[i].append(node)
            if (i+j)%2 ==1:
                grid[i][j].colour = GREEN
    return grid

"""
This is creating the nodes thats are on the board(so the ghost tiles)
I've put them into a 2d array
"""

def draw_grid(window, rows, width):
    gap = width // 6
    for i in range(rows):
        pygame.draw.line(window, BLACK, (0, i * gap), (width, i * gap))

        for j in range(rows):
            pygame.draw.line(window, BLACK, (j * gap, 0), (j * gap, width))

"""
    The nodes are all white so this we need to draw the GREEN lines that separate all the ghost tiles
    from each other and that is what this function does
"""

def update_display(window, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(window)
            spot.setup(window)

        draw_grid(window, rows, width)
        pygame.display.update()

def Find_Node(pos, WIDTH):
    interval = WIDTH / 6
    y, x = pos
    rows = y // interval
    columns = x // interval
    return int(rows), int(columns)

def display_potential_moves(positions, grid):
    for i in positions:
        x, y = i
        grid[x][y].colour = BLUE

def Do_Move(OriginalPos, FinalPosition, window):
    starting_order[FinalPosition] = starting_order[OriginalPos]
    starting_order[OriginalPos] = None

def remove_highlight(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i+j)%2 == 0:
                grid[i][j].colour = WHITE
            else:
                grid[i][j].colour = GREEN

    return grid

"""
this takes in 2 co-ordinate parameters which you can get as the position of the piece and then the position of the node it is moving to
you can get those co-ordinates using my old function for swap
"""

create_board(board)

def main(WINDOW, WIDTH):
    moves = 0
    selected = False
    piece_to_move=[]
    grid = make_grid(6, WIDTH)

    while True:
        pygame.time.delay(50) ##stops cpu dying

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                y, x = Find_Node(pos, WIDTH)
                

            update_display(WINDOW, grid, 6, WIDTH)

main(WINDOW, WIDTH)