from player_types import AI, LocalPlayer
from logic import Logic
from game import Game


class LocalGame(Game):
    """
    Represent local game.
    """
    def __init__(self, players):
        super().__init__()
        self.logic = Logic()
        self.first_player, self.second_player = players
        self.connect_bots()
        self.current_player = self.first_player
        self.no_moves = 0
        self.check_player()

    def connect_bots(self):
        """
        Connects bots to the game (tell them that this game is needed)
        """
        for player in self.first_player, self.second_player:
            if isinstance(player, AI):
                player.connect_to_game(self)

    def man_move(self, x, y):
        """Validate man move by click"""
        if isinstance(self.current_player, LocalPlayer):
            if self.logic.move(x, y, self.int_player()) is not None:
                self.change_current_player()

    def check_player(self):
        """Validate turns queue"""
        scores = self.logic.scores()
        if (
            scores[0] + scores[1] == self.logic.height * self.logic.width or
            self.no_moves == 2 or scores[0] == 0
            or scores[1] == 0
        ):
            self.end_game()
            return
        if len(self.logic.hint(self.int_player())) == 0:
            self.no_moves += 1
            if self.no_moves == 2:
                self.end_game()
                return
            self.change_current_player()
            return
        else:
            self.no_moves = 0
        if type(self.current_player) is AI:
            x, y = self.current_player.ask_for_move()
            self.logic.move(x, y, self.int_player())
            self.change_current_player()
