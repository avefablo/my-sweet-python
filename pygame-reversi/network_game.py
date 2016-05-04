from player_types import LocalPlayer, NetPlayer
from logic import Logic
from threading import Thread
from game import Game
from datetime import datetime as dt


class NetworkGame(Game):
    """
    Represent network game
    """
    def __init__(self, players, network=None):
        super().__init__()
        self.logic = Logic()
        self.network = network
        self.first_player, self.second_player = players
        self.current_player = self.first_player
        self.no_moves = 0
        self.check_player()

    def man_move(self, x, y):
        """
        By click, validate man move locally and send this move to opponent
        """
        if isinstance(self.current_player, LocalPlayer):
            if self.logic.move(x, y, self.int_player()) is not None:
                self.network.send_move((x, y))
                self.change_current_player()

    def receive(self):
        """
        Receive move from socket and perform that move
        """
        move = self.network.wait_for_move()
        if move == 'en':
            self.end_game()
            return
        if move:
            x, y = [int(i) for i in move]
            self.logic.move(x, y, self.int_player())
            self.change_current_player()
        else:
            self.end_game()

    def check_player(self):
        """
        Validate turns queue and check that game isn't finished.
        """
        if (
            self.logic.scores()[0] + self.logic.scores()[1] == 64 or
            self.no_moves == 2 or self.logic.scores()[0] == 0 or
            self.logic.scores()[1] == 0
        ):
            self.disconnect()
            self.end_game()
            return
        if len(self.logic.hint(self.int_player())) == 0:
            self.no_moves += 1
            if self.no_moves == 2:
                self.disconnect()
                self.end_game()
                return
            self.change_current_player()
            self.check_player()
            return
        else:
            self.no_moves = 0
        if isinstance(self.current_player, NetPlayer) and not self.finished:
            t = Thread(target=self.receive, name=dt.now())
            t.start()

    def disconnect(self):
        """
        Send 'en' command (if it possible) and close connection.
        """
        self.network.closed = True
        try:
            self.network.send_end()
        except (BrokenPipeError, OSError):
            pass

        try:
            self.network.send_end()
        except (BrokenPipeError, OSError):
            pass
