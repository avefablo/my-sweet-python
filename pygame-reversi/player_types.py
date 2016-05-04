from enum import Enum


class Difficulty(Enum):
    easy = 1
    med = 2
    hard = 3


class AI:
    def __init__(self, diff, game=None):
        """
        Init the AI in given game with given difficulty
        """
        self.difficulty = diff
        self.game, self.corners = None, None

    def connect_to_game(self, game):
        self.game = game
        self.corners = [(0, 0),
                        (game.logic.height-1, 0),
                        (0, game.logic.width-1),
                        (game.logic.height-1, game.logic.width-1)]

    def ask_for_move(self):
        """
        Return a move by AI (depends on difficulty)
        """
        hints = self.game.logic.hint(self.game.int_player())
        if self.difficulty == Difficulty.easy:
            return self.easy_move(hints)
        elif self.difficulty == Difficulty.med:
            return self.med_move(hints)
        else:
            return self.hard_move(hints)

    def easy_move(self, hints):
        """
        Easy bot move by shortest way
        """
        sorted_hints = sorted(hints.items(), key=lambda x: x[1])
        if len(sorted_hints) > 0:
            return sorted_hints[0][0]
        return None

    def med_move(self, hints):
        """
        Medium bot move by medium way
        """
        sorted_hints = sorted(hints.items(), key=lambda x: x[1])
        if len(sorted_hints) > 0:
            return sorted_hints[len(sorted_hints) // 2][0]
        return None

    def hard_move(self, hints):
        """
        Hard bot move by longest way and go to corners
        """
        sorted_hints = sorted(hints.items(), key=lambda x: x[1], reverse=True)
        if len(sorted_hints) > 0:
            for i in sorted_hints:
                if i[0] in self.corners:
                    return i[0]
            return sorted_hints[0][0]
        return None


class LocalPlayer:
    """
    Filler to some procedures, that check that player is local and not AI.
    """
    def __init__(self):
        pass


class NetPlayer:
    """
    Filler to some procedures, that check that player isn't local.
    """
    def __init__(self):
        pass
