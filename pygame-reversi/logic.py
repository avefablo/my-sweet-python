from board import Board, CellState


class Logic:
    """
    Represent game logic, such is moves, scores, finished state, hints
    """
    def __init__(self, height=8, width=8, std_board=True):
        self.board = Board(init_std=std_board)
        self.no_moves = 0
        self.width = width
        self.height = height
        self.finished = False

    def scores(self):
        """
        Count the score of each player
        """
        white_chips = 0
        black_chips = 0
        for i in self.board:
            for j in i:
                if j == CellState.white:
                    white_chips += 1
                if j == CellState.black:
                    black_chips += 1
        return black_chips, white_chips

    def in_bound(self, y, x):
        """
        Check, if coordinates is on game board
        """
        return 0 <= x <= self.width-1 and 0 <= y <= self.height-1

    def check_move(self, target_y, target_x, player):
        """
        Validate move and return chips that should be flipped by this move
        :param target_y: y coordinate of needed cell
        :param target_x: x coordinate of needed cell
        :param player: int represent of needed player
        :return:
        """

        if self.board[target_y][target_x] != CellState.empty:
            return None
        else:
            self.board[target_y][target_x] = CellState(player)
            opponent = CellState(abs(player - 1))
            flip = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    curx, cury = target_x, target_y
                    curx += dx
                    cury += dy
                    if (
                        self.in_bound(cury, curx) and
                        self.board[cury][curx] == CellState(opponent)
                    ):
                        curx += dx
                        cury += dy
                        if not self.in_bound(cury, curx):
                            continue
                        while self.board[cury][curx] == CellState(opponent):
                            curx += dx
                            cury += dy
                            if not self.in_bound(cury, curx):
                                break
                        if not self.in_bound(cury, curx):
                            continue
                        if self.board[cury][curx] == CellState(player):
                            while True:
                                curx -= dx
                                cury -= dy
                                if curx == target_x and cury == target_y:
                                    break
                                flip.append([cury, curx])
                self.board[target_y][target_x] = CellState.empty
        if len(flip) > 0:
            return flip
        return None

    def move(self, target_y, target_x, player):
        """
        If (x, y) is correct move, change the content of board
        and return flipped chips
        """
        checked = self.check_move(target_y, target_x, player)
        if checked is not None:
            for chip in checked:
                self.board[chip[0]][chip[1]] = CellState(player)
            self.board[target_y][target_x] = CellState(player)
        return checked

    def hint(self, player):
        """
        Return all possible moves with numbers of chips, that will be flipped
        """
        moves = {}
        for y in range(self.height):
            for x in range(self.width):
                move = self.check_move(y, x, player)
                if move is not None:
                    moves[(y, x)] = len(move)
        return moves
