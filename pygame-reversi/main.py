from tkinter import Label, Button, Radiobutton, \
    Frame, Tk, LEFT, W, IntVar, \
    StringVar, Entry, Checkbutton
import tkinter.messagebox as mb
from ipgetter import Popup
import graphics
from local_game import LocalGame
from network_game import NetworkGame
from network import Server, Client
from player_types import AI, LocalPlayer, Difficulty, NetPlayer


class Launcher:
    """
    Represent game launcher. Here you can choose your opponent
    and edit settings
    """
    def __init__(self):
        """
        Create launcher (use tk)
        """
        self.root = Tk()
        x = int(self.root.winfo_screenwidth() / 2) - 225
        y = int(self.root.winfo_screenheight() / 2) - 88
        self.root.geometry("450x180+{}+{}".format(x, y))
        self.root.resizable(0, 0)
        self.root.wm_title('AvReversi v2.0 Launcher')
        self.hints = IntVar()
        self.hints.set(1)
        self.opponent = IntVar()
        self.opponent.set(1)
        self.color = IntVar()
        self.color.set(1)
        self.draw_local_selector()
        self.draw_network_selector()
        self.draw_settings_field()
        self.root.mainloop()

    def launch_local_game(self, opponent_int, color_int):
        """
        Parse ints from radiobuttons from tk launcher and
        launch local game with these parameters
        """
        opponent = None
        players = None, None
        if opponent_int == 1:
            opponent = LocalPlayer()
        elif opponent_int == 2:
            opponent = AI(Difficulty.easy)
        elif opponent_int == 3:
            opponent = AI(Difficulty.med)
        elif opponent_int == 4:
            opponent = AI(Difficulty.hard)
        if color_int == 1:
            players = LocalPlayer(), opponent
        elif color_int == 2:
            players = opponent, LocalPlayer()
        game = LocalGame(players)
        # connect bots to game
        for player in players:
            if isinstance(player, AI):
                player.game = game

        g = graphics.GameWindow(game=game,
                                hints=self.hints_bool())
        self.root.destroy()
        g.mainloop()

    def host(self):
        """
        Show IPs popup and host network game
        """
        network = Server()
        mb.showinfo('IPs', Popup().phrase +
                    '\nClose this window to lookup for opponent')
        color = network.wait()
        players = None
        if color == 1:
            players = NetPlayer(), LocalPlayer()
        elif color == 2:
            players = LocalPlayer(), NetPlayer()
        if players:
            g = graphics.GameWindow(game=NetworkGame(players, network),
                                    hints=self.hints_bool())
            self.root.destroy()
            g.mainloop()

    def join(self, ip, color_int):
        """
        Connect to the host, sent him color and create GameWindow
        """
        players = None
        if color_int == 1:
            players = LocalPlayer(), NetPlayer()
        elif color_int == 2:
            players = NetPlayer(), LocalPlayer()
        network = Client()
        if network.establish(ip, color_int):
            g = graphics.GameWindow(game=NetworkGame(players, network),
                                    hints=self.hints_bool())
            self.root.destroy()
            g.mainloop()

    def hints_bool(self):
        """
        Convert IntVar to bool
        """
        if self.hints.get() == 1:
            return True
        else:
            return False

    def draw_local_selector(self):
        """
        Draw radiobuttons to choose local opponent
        """
        Label(self.root, text="Local opponent:").pack()
        frame = Frame(self.root, width=320, height=160, bd=1)
        players = [
            ('Man', 1),
            ('AI (easy)', 2),
            ('AI (medium)', 3),
            ('AI (hard)', 4)
        ]
        for b in players:
            Radiobutton(frame, text=b[0], variable=self.opponent,
                        value=b[1]).pack(side=LEFT, anchor=W)
        b = Button(frame, text="Play Local",
                   command=lambda: self.launch_local_game(self.opponent.get(),
                                                          self.color.get()))
        b.pack(side='left', anchor='w')
        frame.pack()

    def draw_network_selector(self):
        """
        Draw boxes and buttons to choose online opponent
        """
        frame = Frame(self.root, width=320, height=160, bd=1)
        frame.pack()
        Label(frame, text="\nNetwork opponent:").pack()
        Label(frame, text="Opponent IP:").pack(side="left", anchor='w')
        ip = StringVar()
        ip.set('127.0.0.1')
        ip_entry = Entry(frame, textvariable=ip)
        b1 = Button(frame, text="Join",
                    command=lambda: self.join(ip.get(), self.color.get()))
        ip_entry.pack(side="left", anchor='w')
        b1.pack(side='left')
        b2 = Button(self.root, text='Host', command=self.host)
        b2.pack()
        frame.pack()

    def draw_settings_field(self):
        """
        Draw checkboxes to settings
        """
        frame = Frame(self.root, width=320, height=160, bd=1)
        c = Checkbutton(frame, text="Show hints", variable=self.hints)
        c.pack(side='left', anchor='w')
        for b in [('Black', 1), ('White', 2)]:
            Radiobutton(frame, text=b[0], variable=self.color,
                        value=b[1]).pack(side=LEFT, anchor=W)
        frame.pack()


if __name__ == '__main__':
    l = Launcher()
