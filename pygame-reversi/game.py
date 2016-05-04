from player_types import LocalPlayer
from logic import Logic


class Game:
    """
    Represent abstract game without players. Just Logic(),
    procedures to change current player and end game.
    """
    def __init__(self):
        self.logic = Logic()
        self.first_player, self.second_player = None, None
        self.current_player = None
        self.no_moves = 0
        self.finished = False
        self.finish_state = None

    def change_current_player(self):
        """
        Change current player
        """
        if self.current_player == self.second_player:
            self.current_player = self.first_player
        else:
            self.current_player = self.second_player
        self.check_player()

    def end_game(self):
        """
        This procedure called at the end of game.
        It determine the winner and if winner is local, call score counter
        """
        self.finished = True
        scores = self.logic.scores()
        if scores[0] == scores[1]:
            return
        winner = self.first_player \
            if scores[0] > scores[1] \
            else self.second_player
        opponent = self.second_player \
            if winner == self.first_player \
            else self.first_player
        if isinstance(winner, LocalPlayer):
            fin_scores = self.count_finish_state()
            if fin_scores:
                self.finish_state = fin_scores[0], opponent, fin_scores[1]

    def count_finish_state(self):
        """
        Count scores at the end of a game, if player is local
        """
        scores = self.logic.scores()
        self.finished = True
        if self.no_moves == 2:
            return max(scores) * 100, 'No moves'
        elif scores[0] == 0 or scores[1] == 0:
            return max(scores) * 200, 'No opponent chips'
        elif scores[0] + scores[1] == self.logic.width * self.logic.height:
            return max(scores) * 50, 'Win'
        else:
            return 0, 'Connection lost'

    def int_player(self):
        """
        Return 0 if first player playing now, 1 if second
        (needed for some methods)
        """
        if self.current_player == self.first_player:
            return 0
        else:
            return 1
