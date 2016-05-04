from multiprocessing import Process
from player_types import AI, Difficulty
from tkinter import Label, Tk, StringVar, Entry, Button, RAISED


class Highscore:
    def __init__(self, name, score, opponent, condition):
        """
        Represent highscore with 4 fields
        """
        self.name = name
        self.score = score
        self.opponent = opponent
        self.condition = condition


class HighscoreTable:
    def __init__(self):
        """
        Represent table of highscores
        """
        self.txt = self.read_txt()
        if self.txt:
            self.records = self.read_records(self.txt)
        else:
            self.records = []

    def read_txt(self):
        """
        Read highscores from txt
        """
        try:
            return open('records.txt', 'r', encoding='utf-8').readlines()
        except FileNotFoundError:
            print('File not found!')

    def write_txt(self):
        """
        Write highscores to txt
        """
        f = open('records.txt', 'w', encoding='utf-8')
        for i in self.records:
            f.write('{}\t{}\t{}\t{}\n'.format(i.name,
                                              i.score,
                                              i.opponent,
                                              i.condition))
        f.close()

    def read_records(self, lines):
        """
        Parse records from string to Highscore
        """
        records = []
        for i in lines:
            name, score, opponent, condition = i.strip('\t \n').split('\t')
            records.append(Highscore(name, int(score), opponent, condition))
        sorted_records = sorted(records, key=lambda x: x.score, reverse=True)
        return sorted_records

    def add_record(self, record):
        """
        Add record to Highscore table and cut table to 10 elements
        """
        new_score = Highscore(*record)
        position = 0
        if not self.records:
            self.records.append(new_score)
        else:
            for i in self.records:
                if i.score <= new_score.score:
                    self.records.insert(position, new_score)
                    break
                position += 1
            if position == len(self.records):
                self.records.append(new_score)
            self.records = self.records[:10]


class HighScoresWindow:
    def __init__(self):
        """
        Represent tk grid for highscores
        """
        root = Tk()
        scores = HighscoreTable().records
        column = 1
        for i in ['Name', 'Score', 'Opponent', 'Condition']:
            Label(text=i, relief=RAISED, width=15).grid(row=0, column=column)
            column += 1
        row = 1
        for i in scores:
            Label(text=row, relief=RAISED, width=5).grid(row=row, column=0)
            column = 1
            for j in [i.name, i.score, i.opponent, i.condition]:
                Label(text=j,
                      relief=RAISED,
                      width=15).grid(row=row, column=column)
                column += 1
            row += 1
        root.mainloop()


class Asker:
    def __init__(self, score):
        """
        Represent window that ask your name
        """
        self.root = Tk()
        self.score, self.opponent, self.state = score
        self.root.wm_title('AvReversi v2.0 Launcher')
        self.root.resizable(0, 0)
        self.name = StringVar(None)
        self.records = HighscoreTable()
        Entry(self.root, textvariable=self.name).pack()
        Button(self.root, text="Remember me",
               command=lambda: self.button_action()).pack()
        self.root.mainloop()

    def button_action(self):
        """
        Handle 'remember' button action
        """
        self.records.add_record((self.name.get(),
                                 self.score,
                                 self.get_opponent_str(),
                                 self.state))
        self.records.write_txt()
        self.root.destroy()

    def get_opponent_str(self):
        """
        Return string represent of opponent
        It will be AI+Difficulty or opponent class name.
        """
        if isinstance(self.opponent, AI):
            return 'AI({})'.format(self.get_difficulty())
        else:
            return self.opponent.__class__.__name__

    def get_difficulty(self):
        """
        Return string represent of AI difficulty
        """
        if self.opponent.difficulty == Difficulty.easy:
            return 'easy'
        elif self.opponent.difficulty == Difficulty.med:
            return 'med'
        else:
            return 'hard'


def launch(new_score):
    Process(target=Asker(new_score).__init__)
    Process(target=HighScoresWindow().__init__)


if __name__ == '__main__':
    Asker((50, 'AI', "Win"))
    HighScoresWindow()
