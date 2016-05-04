from board import CellState
from player_types import LocalPlayer
import scoreboard as sb
import pygame
import os
import sys
from multiprocessing import Process
from main import Launcher
from network_game import NetworkGame


class ImageWorker:
    """
    Class to open image
    """
    def get_image(self, name, transparent=False):
        """
        :param name: name of the file
        :param transparent: if True it makes convert_alpha
        :return: image and his rect for drawing
        """
        fullname = os.path.join('img', name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error:
            print("Cannot load image:", name)
            raise SystemExit
        # image = image.convert()
        if transparent:
            image = image.convert_alpha()
        return image, image.get_rect()


class NewGameButton:
    """
    Class for new button rect & label
    By click it open launcher
    """
    def __init__(self, sf):

        self.surface = pygame.display.get_surface()
        pygame.draw.rect(sf, (0, 98, 128), (560, 100, 160, 40))
        pygame.draw.rect(sf, (0, 117, 153), (564, 104, 152, 32))
        myfont = pygame.font.SysFont("monospace", 30)
        label = myfont.render("New game", 1, (0, 0, 0))
        sf.blit(label, (568, 102))


class Chip:
    """
    Chip image class
    """
    def __init__(self, color, x, y):
        self.image, self.rect = ImageWorker().get_image(color + '.png',
                                                        transparent=True)
        self.screen = pygame.display.get_surface()
        self.rect.center = (x, y)
        self.color = color


class GameWindow:
    """
    Main game window class
    """
    def __init__(self, game=None, hints=True):
        """
        :param game: Game() object, that contains logic
        :param hints: if True, there will be yellow points (hints) on the board
        :return:
        """
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('AvReversi v2.0')
        pygame.Surface((800, 600))
        bg_image = ImageWorker().get_image('bg.png')[0]
        self.board_image = ImageWorker().get_image('board.png')[0]
        screen.blit(bg_image, (0, 0))
        self.chips = []
        self.hints = hints
        self.screen = pygame.display.get_surface()
        self.game = game
        self.ngb = NewGameButton(screen)
        self.ask_score = False
        self.score_stored = False

    def mainloop(self):
        """
        Main game loop
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if isinstance(self.game, NetworkGame):
                        self.game.disconnect()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.click(pos)
            if self.game.finished:
                self.end_blit()
                self.ask_score = True
            else:
                self.update_board()
            self.print_scores_and_current(self.screen)
            pygame.display.flip()
            pygame.display.update()
            if (
                self.ask_score and not
                self.score_stored and
                self.game.finish_state
            ):
                sb.launch(self.game.finish_state)
                self.ask_score = False
                self.score_stored = True

    def end_blit(self):
        """
        Blit finish screen.
        It updates scores and print who is winner.
        """
        self.screen.blit(self.board_image, (60, 60))
        myfont = pygame.font.SysFont("monospace", 24)
        color = ''
        x = 160
        scores = self.game.logic.scores()
        if scores[0] > scores[1]:
            color = 'Black'
        elif scores[0] < scores[1]:
            color = 'White'
        else:
            color = 'Friendship'
            x = 140

        label = myfont.render('%s wins this time' % color, 1, (255, 255, 255))
        self.screen.blit(label, (x, 250))

    def click(self, pos):
        """
        React to click
        It handle press on board and press on new game button
        """
        if 560 <= pos[0] <= 560 + 160 and 100 <= pos[1] <= 100 + 40:
            if isinstance(self.game, NetworkGame):
                self.game.disconnect()
            Process(target=Launcher().__init__)
            pygame.quit()
        if (
            self.game is not None and
            type(self.game.current_player) is LocalPlayer
        ):
            x, y = [(i - 60) // 60 for i in pos]
            if 0 <= x <= 7 and 0 <= y <= 7:
                self.game.man_move(x, y)

    def update_chips(self):
        """
        Update list of chips objects, that in the game now
        """
        if self.game is None:
            return
        for i in range(len(self.game.logic.board)):
            for j in range(len(self.game.logic.board[i])):
                if self.game.logic.board[i][j] != CellState.empty:
                    color = self.get_color(self.game.logic.board[i][j])
                    self.chips.append(Chip(color,
                                           90 + i * 60,
                                           90 + j * 60))

    def get_color(self, cell):
        """
        :param cell: needed cellstate
        :return: string represent of cellstate
        """
        if cell == CellState.black:
            return 'black'
        else:
            return 'white'

    def print_scores_and_current(self, sf):
        """
        Draw current scores and current player.
        """
        pygame.draw.rect(sf, (130, 130, 130), (560, 150, 160, 320))
        pygame.draw.rect(sf, (191, 191, 191), (564, 154, 152, 312))
        black = (0, 0, 0)
        myfont = pygame.font.SysFont("monospace", 26)
        label = myfont.render("Scores", 1, black)
        sf.blit(label, (592, 166))
        label = myfont.render("Turn:", 1, black)
        sf.blit(label, (604, 266))
        scores = self.game.logic.scores()
        current = self.game.int_player()
        label = myfont.render("{} : {}".format(scores[0], scores[1]), 1, black)
        sf.blit(label, (594, 200))
        if current == 0:
            img = ImageWorker().get_image('black.png', transparent=True)
            sf.blit(img[0], (612, 300))
        else:
            img = ImageWorker().get_image('white.png', transparent=True)
            sf.blit(img[0], (612, 300))

    def update_board(self):
        """
        Redraw chips on the board and draw hints, if they enabled
        """
        self.update_chips()
        self.screen.blit(self.board_image, (60, 60))
        for i in self.chips:
            self.screen.blit(i.image, i.rect)
        if isinstance(self.game.current_player, LocalPlayer) and self.hints:
            self.draw_hints()

    def draw_hints(self):
        """
        Draw possible moves (if self.hints is True)
        """
        for i in self.game.logic.hint(self.game.int_player()):
            pygame.draw.circle(self.screen, (254, 204, 51),
                               (i[0] * 60 + 90, i[1] * 60 + 90), 3, 0)
