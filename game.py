import numpy as np
import pygame
import sys
import math
import time
from classes import GameBoard,Pieces,MiniMax,AlphaBetaMiniMax,ExpectiMiniMax
from PrettyPrint import PrettyPrintTree
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
class GameEnv(object):
    BLUE = (0,0,255)
    BLACK = (0,0,0)
    RED = (255,0,0)
    YELLOW = (255,255,0)
    SQUARESIZE = 100
    width = GameBoard.COLUMN_COUNT * SQUARESIZE
    height = (GameBoard.ROW_COUNT+1) * SQUARESIZE
    size = (width*2, height)
    RADIUS = int(SQUARESIZE/2 - 5)
    screen = pygame.display.set_mode(size)
    pygame.font.init()
    myfont = pygame.font.SysFont("monospace", 75)
    game_over = False
    turn = 0
    AiAgent = MiniMax(3)
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
        text_surface = cls.myfont.render('Score: %d'%board.get_score(), False, (255, 255, 255))
        pygame.draw.rect(cls.screen, cls.BLACK, (cls.width,0, cls.width, cls.SQUARESIZE))
        cls.screen.blit(text_surface, (cls.width,0))
        pygame.display.update()
    @classmethod
    def render_preview(cls,event):
        pygame.draw.rect(cls.screen, cls.BLACK, (0,0, cls.width, cls.SQUARESIZE))
        posx = min(int(event.pos[0]/cls.SQUARESIZE),GameBoard.COLUMN_COUNT-1)*cls.SQUARESIZE+int(cls.SQUARESIZE/2)
        if cls.turn == 0:
            pygame.draw.circle(cls.screen, cls.RED, (posx, int(cls.SQUARESIZE/2)), cls.RADIUS)
        pygame.display.update()
    @classmethod
    def play_move(cls,event,board):
        pygame.draw.rect(cls.screen, cls.BLACK, (0,0, cls.width, cls.SQUARESIZE))
        if cls.turn == 0:
            posx = event.pos[0]
            if posx<=cls.width:
                col = int(math.floor(posx/cls.SQUARESIZE))
                newBoard = board.drop_piece(cls.turn,col)
        if(newBoard is not None):
            cls.turn = 1
            cls.render_board(newBoard)
            newBoard = cls.ai_handover(newBoard)
            return newBoard
        else:
            return board
    @classmethod
    def ai_handover(cls,board):
        start = time.process_time()    
        newBoard = cls.AiAgent.getNextMove(board)
        print("Time Taken:")
        print(time.process_time() - start)
        print("Total Expanded Nodes:")
        print(len(board.GameBoardsDict))
        cls.turn = 0
        cls.render_board(newBoard)
        #print_tree(board)
        #draw_tree(board)
        return newBoard
def print_tree(tree):
    pt = PrettyPrintTree(lambda x: x.children, lambda x: {"min":x.min,"max":x.max},orientation=PrettyPrintTree.Horizontal)
    pt(tree)
def get_all_nodes(board):
        all_nodes = []
        stack = [board]
        while stack:
            node = stack.pop()
            all_nodes.append(node)
            stack.extend(node.children)
        return all_nodes
def draw_tree(tree):
    all_nodes = get_all_nodes(tree)

    G = nx.DiGraph()

    # Add edges to the graph
    for node in all_nodes:
        for child in node.children:
            G.add_edge(node, child)

    # Define labels for nodes
    labels = {node: f'min: {node.min}, max: {node.max}' for node in all_nodes}

    # Draw the graph
    pos = graphviz_layout(G, prog='dot')
    nx.draw(G, pos, with_labels=False, arrows=False)
    nx.draw_networkx_labels(G, pos, labels=labels)

    plt.show()	
if __name__ =="__main__":
    board = GameBoard()
    pygame.init()
    Game = GameEnv()
    Game.render_board(board)
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                Game.render_preview(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                board = Game.play_move(event,board)
            if event.type == pygame.QUIT:
                run =False

    pygame.quit()