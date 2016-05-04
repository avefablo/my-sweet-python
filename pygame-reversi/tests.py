import unittest
from game import Game
from logic import Logic
from player_types import AI, LocalPlayer, Difficulty
from local_game import LocalGame
from board import Board, CellState


class Tests(unittest.TestCase):
    def board_generator(self, lines, width, height):
        """
        Generate board from list of symbols.
        'b' == CellState.black
        'w' == CellState.white
        '.' == empty
        """
        board = Board(width, height, init_std=False)
        for i in range(len(lines)):
            for j in range(len(lines[i])):
                if lines[i][j] == '.':
                    board[i][j] = CellState.empty
                elif lines[i][j] == 'b':
                    board[i][j] = CellState.black
                elif lines[i][j] == 'w':
                    board[i][j] = CellState.white
        return board

    def test_hint(self):
        """
        Test hint system
        """
        logic = Logic(width=8, height=1, std_board=False)
        logic.board = self.board_generator(['.bbbbbbw'], 8, 1)
        self.assertEqual(logic.hint(1), {(0, 0): 6})

    def test_hint_two_var(self):
        """
        Test hint system
        """
        logic = Logic(width=7, height=1, std_board=False)
        logic.board = self.board_generator(['.bbwbb.'], 7, 1)
        self.assertEqual(logic.hint(1), {(0, 0): 2, (0, 6): 2})

    def bot_test_map1(self, difficulty):
        """
        Create map to test bots.
        """
        game = LocalGame((AI(difficulty), LocalPlayer()))
        game.logic = Logic(width=12, height=1, std_board=False)
        game.logic.board = self.board_generator(['bwww.bw.bww.'], 12, 1)
        game.connect_bots()
        game.current_player = game.first_player
        return game

    def test_easy_bot_map1(self):
        """
        Test easy bot on map1
        """
        game = self.bot_test_map1(Difficulty.easy)
        self.assertEqual(game.first_player.ask_for_move(), (0, 7))

    def test_med_bot_map1(self):
        """
        Test medium bot on map1
        """
        game = self.bot_test_map1(Difficulty.med)
        self.assertEqual(game.first_player.ask_for_move(), (0, 11))

    def test_hard_bot_map1(self):
        """
        Test hard bot on map1
        """
        game = self.bot_test_map1(Difficulty.hard)
        self.assertEqual(game.first_player.ask_for_move(), (0, 11))

    def ending(self, board, width, height):
        """
        Create game to test semi-finished states of board.
        """
        game = LocalGame((LocalPlayer(), LocalPlayer()))
        game.logic = Logic(width=width, height=height, std_board=False)
        game.logic.board = self.board_generator(board, width, height)
        game.current_player = game.first_player
        return game

    def test_endofgame(self):
        """
        Test that game is finished after move
        """
        game = self.ending(['bwwwwww.'], 8, 1)
        game.man_move(0, 7)
        self.assertTrue(game.finished)

    def test_scores_eat_all(self):
        """
        Test score system when player 'eat' all opponent's chips
        """
        game = self.ending(['bwwwwww.'], 8, 1)
        game.man_move(0, 7)
        self.assertEqual(game.finish_state,
                         (1600, game.second_player, 'No opponent chips'))

    def test_win(self):
        """
        Test score system when player just win
        """
        game = self.ending(['bw.wwwww'], 8, 1)
        game.man_move(0, 2)
        self.assertEqual(game.finish_state, (250, game.first_player, 'Win'))

    def test_no_moves(self):
        """
        Test score system when there is no moves for both players
        """
        game = self.ending(['bw..wwww'], 8, 1)
        game.man_move(0, 2)
        self.assertEqual(game.finish_state,
                         (400, game.first_player, 'No moves'))

    def test_finish_draw(self):
        """
        Test score system when there is a draw
        """
        game = self.ending(['bbw.wwww'], 8, 1)
        game.man_move(0, 3)
        self.assertTrue(game.finished)

if __name__ == '__main__':
    unittest.main()
