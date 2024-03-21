import numpy as np
from abc import ABC, abstractmethod
from enum import IntEnum
from itertools import groupby

#absract class for minimax, minimax Alpha-Beta, ExpectiMinimax
class AiAgent(ABC):
    @abstractmethod
    def getNextMove(self,board) -> int:
        pass

class MiniMax(AiAgent):
    def __init__(self,depth) -> None:
        super().__init__()
        self.Targetdepth = depth
        self.tree = None
    def applyMinMax(self,board,currentDepth,turn):
        if(currentDepth == self.Targetdepth or board.is_full()):
            return board
        board.expand_children(turn)
        if(turn==1):
            return max([self.applyMinMax(b,currentDepth+1,0) for b in board.children],key= lambda x: x.score)
        else:
            return min([self.applyMinMax(b,currentDepth+1,1) for b in board.children],key= lambda x: x.score)
    def getNextMove(self,board) -> int:
        bestBoard = self.applyMinMax(board,0,1)
        chosenMove = bestBoard
        while(chosenMove not in board.children):
            chosenMove = board.BoardparentMap[chosenMove.board.tobytes()]
        return chosenMove
    
class AlphaBetaMiniMax(AiAgent):
    def __init__(self,depth) -> None:
        super().__init__()
        self.Targetdepth = depth
    def applyMinMax(self, board, currentDepth, turn, alpha, beta):
        if(currentDepth == self.Targetdepth or board.is_full()):
            return board
        board.expand_children(turn)
        if(turn==1):
            maxEval = float('-inf')
            bestBoard = None
            for b in board.children:
                eval = self.applyMinMax(b, currentDepth+1, 0, alpha, beta)
                if eval.score > maxEval:
                    maxEval = eval.score
                    bestBoard = b
                alpha = max(alpha, eval.score)
                if beta <= alpha:
                    break
            return bestBoard
        else:
            minEval = float('inf')
            bestBoard = None
            for b in board.children:
                eval = self.applyMinMax(b, currentDepth+1, 1, alpha, beta)
                if eval.score < minEval:
                    minEval = eval.score
                    bestBoard = b
                beta = min(beta, eval.score)
                if beta <= alpha:
                    break
            return bestBoard
    def getNextMove(self,board) -> int:
        bestBoard = self.applyMinMax(board, 0, 1, float('-inf'), float('inf'))
        chosenMove = bestBoard
        while(chosenMove not in board.children):
            chosenMove = board.BoardparentMap[chosenMove.board.tobytes()]
        return chosenMove

class ExpectiMiniMax(AiAgent):
    WEIGHTS = [0.2, 0.6, 0.2]
    def __init__(self,depth) -> None:
        super().__init__()
        self.Targetdepth = depth
    def applyMinMax(self,board,currentDepth,turn):
        if(currentDepth == self.Targetdepth or board.is_full()):
            return board
        board.expand_children(turn)
        if(turn==1):
            choices = [self.applyMinMax(b,currentDepth+1,0) for b in board.children]
            scores = [self.WEIGHTS[0]*choices[max(i-1,0)].score +self.WEIGHTS[1]*choices[i].score+self.WEIGHTS[2]*choices[min(i+1,len(choices)-1)].score for i in range(len(choices))]
            return choices[scores.index(max(scores))]
        else:
            choices = [self.applyMinMax(b,currentDepth+1,1) for b in board.children]
            scores = [self.WEIGHTS[0]*choices[max(i-1,0)].score +self.WEIGHTS[1]*choices[i].score+self.WEIGHTS[2]*choices[min(i+1,len(choices)-1)].score for i in range(len(choices))]
            return choices[scores.index(min(scores))]
    def getNextMove(self,board) -> int:
        bestBoard = self.applyMinMax(board,0,1)
        chosenMove = bestBoard
        while(chosenMove not in board.children):
            chosenMove = board.BoardparentMap[chosenMove.board.tobytes()]
        return chosenMove
class Pieces(IntEnum):
    RED = 1
    YELLOW = 2

class GameBoard():
    ROW_COUNT = 6
    COLUMN_COUNT = 7
    GameBoardsDict = {}
    BoardparentMap = {}
    @classmethod
    def init_empty_board(cls) -> np.array:
        board = np.zeros((cls.ROW_COUNT,cls.COLUMN_COUNT),dtype="int")
        return board
    def __init__(self,board=None):
        if(board is None):
            self.board = self.init_empty_board()
            self.score = -1*np.inf
            self.children = []
            self.min = None
            self.max = None
        else:
            self.board = board
            self.children = []
            self.score = 0
            self.min = None
            self.max = None
            self.update_heurestic_score()
    def __hash__(self) -> int:
        return hash(self.board.tobytes())
    def __eq__(self, __value: object) -> bool:
        return np.all(self.board == __value.board)
    def __getitem__(self,index) -> np.array:
        return self.board[index]
    def is_valid_move(self,col) -> bool:
        return self.board[self.ROW_COUNT-1][col] == 0
    def get_valid_moves(self) -> np.array:
        return np.argwhere(self.board[self.ROW_COUNT-1] == 0).flatten()
    def runs_list(list):
        return [sum(g) for b, g in groupby(list) if b]
    def update_heurestic_score(self):
        rows = [self.board[x] for x in range(self.ROW_COUNT)]
        cols = [self.board[:,x] for x in range(self.COLUMN_COUNT)]
        diags = [np.diag(self.board,x) for x in range(4-self.ROW_COUNT,self.COLUMN_COUNT-3)]
        antiDiags = [np.diag(np.fliplr(self.board),x) for x in range(4-self.ROW_COUNT,self.COLUMN_COUNT-3)]
        runs = {Pieces.RED:[],Pieces.YELLOW:[]}
        for l in rows+cols+diags+antiDiags:
            for b,g in groupby(l):
                if(b!=0):
                    count = sum(1 for x in g)
                    if(1<count):
                        if(count<4):
                            runs[b].append(count)
                        else:
                            runs[b].extend([40 for x in range(count-3)])
        self.score = np.sum(np.exp(runs[Pieces.YELLOW]))-np.sum(np.exp(runs[Pieces.RED]))
        return runs
    def get_score(self):
        runs = self.update_heurestic_score()
        return sum([1 for b in runs[Pieces.YELLOW] if b>=4]) - sum([1 for b in runs[Pieces.RED] if b>=4]) 

    def expand_children(self,turn):
        if(len(self.children)==0):
            moves = self.get_valid_moves()
            self.children = [self.drop_piece(turn,x) for x in moves]
        for child in self.children:
            self.GameBoardsDict[child.board.tobytes()] = child
            self.BoardparentMap[child.board.tobytes()] = self
        self.min = min(self.children,key=lambda x: x.score).score
        self.max = max(self.children,key=lambda x: x.score).score
    def is_full(self):
        return not 0 in self.board
    def drop_piece(self,turn,col):
        if self.is_valid_move(col):
            if turn == 0:
                piece = Pieces.RED
            else:
                piece = Pieces.YELLOW
            row = np.nonzero(self.board[:,col]==0)[0][0]
            newBoard = self.board.copy()
            newBoard[row][col] = piece
            child = self.GameBoardsDict.get(newBoard.tobytes(),None)
            if(child is None):
                Board = GameBoard(board=newBoard)
                self.GameBoardsDict[newBoard.tobytes()] = Board
                self.BoardparentMap[newBoard.tobytes()] = self
                self.update_heurestic_score()
                return Board
            else:
                return child
        self.update_heurestic_score()
        print(self.get_score())
        return None
    
