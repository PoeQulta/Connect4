import numpy as np
from abc import ABC, abstractmethod

#absract class for minimax, minimax Alpha-Beta, ExpectiMinimax
class AiAgent(ABC):
    @abstractmethod
    def getNextMove(self,board):
        pass


class GameBoard():
    ROW_COUNT = 6
    COLUMN_COUNT = 7
    @classmethod
    def init_empty_board(cls):
        board = np.zeros((cls.ROW_COUNT,cls.COLUMN_COUNT))
        return board
    def __init__(self):
        self.board = self.init_empty_board()
    def __hash__(self) -> int:
        hash(self.board.tobytes())
    def __eq__(self, __value: object) -> bool:
        return np.all(self.board == __value.board)
    def __getitem__(self,index):
        return self.board[index]