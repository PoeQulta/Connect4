import numpy as np
import pygame
import sys
import math
from enum import IntEnum
from classes import GameBoard



class Pieces(IntEnum):
    RED = 1
    YELLOW = 2
    
class GameEnv():
    BLUE = (0,0,255)
    BLACK = (0,0,0)
    RED = (255,0,0)
    YELLOW = (255,255,0)
    SQUARESIZE = 100
    width = GameBoard.COLUMN_COUNT * SQUARESIZE
    height = (GameBoard.ROW_COUNT+1) * SQUARESIZE
    size = (width, height)
    RADIUS = int(SQUARESIZE/2 - 5)
    screen = pygame.display.set_mode(size)
    game_over = False
    turn = 0
    @classmethod
    def render_board(cls,board):
        for c in range(board.COLUMN_COUNT):
            for r in range(board.ROW_COUNT):
                pygame.draw.rect(cls.screen, cls.BLUE, (c*cls.SQUARESIZE, r*cls.SQUARESIZE+cls.SQUARESIZE, cls.SQUARESIZE, cls.SQUARESIZE))
                pygame.draw.circle(cls.screen, cls.BLACK, (int(c*cls.SQUARESIZE+cls.SQUARESIZE/2), int(r*cls.SQUARESIZE+cls.SQUARESIZE+cls.SQUARESIZE/2)), cls.RADIUS)
        
        for c in range(board.COLUMN_COUNT):
            for r in range(board.ROW_COUNT):		
                if board[r][c] == Pieces.RED:
                    pygame.draw.circle(cls.screen, cls.RED, (int(c*cls.SQUARESIZE+cls.SQUARESIZE/2), cls.height-int(r*cls.SQUARESIZE+cls.SQUARESIZE/2)), cls.RADIUS)
                elif board[r][c] == Pieces.YELLOW: 
                    pygame.draw.circle(cls.screen, cls.YELLOW, (int(c*cls.SQUARESIZE+cls.SQUARESIZE/2), cls.height-int(r*cls.SQUARESIZE+cls.SQUARESIZE/2)), cls.RADIUS)
        pygame.display.update()
	
if __name__ =="__main__":
    board = GameBoard()
    pygame.init()
    Game = GameEnv()
    Game.render_board(board)
    pygame.display.update()
    run = True
    myfont = pygame.font.SysFont("monospace", 75)
    while run:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run =False

    pygame.quit()