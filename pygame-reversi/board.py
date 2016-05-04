from enum import Enum


class CellState(Enum):
    """
    State of board cell.
    It may be white or black chip or empty space.
    """
    black = 0
    white = 1
    empty = 2


class Board:
    """
    Represent reversi board.
    Board containts list of states.
    """

    def __init__(self, width=8, height=8, init_std=True):
        """
        :param width: change width of board. !!!Change init_std to False
        to create non-standard board.
        :param height: change height of board. !!!Change init_std to False
        to create non-standard board.
        :param init_std: if this parameter True,
        create standart board (8x8, starting points: [(3, 4), (4, 3),
                                                      (3, 3), (4, 4)]
        else create empty board with given width and height
        """
        self._data = [[CellState.empty for i in range(width)] for j in range(width)]
        if init_std:
            self._data[4][3] = CellState.white
            self._data[4][4] = CellState.black
            self._data[3][3] = CellState.black
            self._data[3][4] = CellState.white

    def __iter__(self):
        for elem in self._data:
            yield elem

    def __len__(self):
        return len(self._data)

    def __getitem__(self, i):
        return self._data[i]
