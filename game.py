from month import Month
from enum import Enum


class Game:

    def __init__(self, title, length, player):
        self.title = title
        self.type = GameType(length)
        self.player = player

        self.easy = None
        self.hard = None
        self.challenge = None
        self.comment = None

        self.active = False
        self.months = []

        self.easy_players = []
        self.hard_players = []
        self.challenge_players = []

        self.bestscreenshot_player = []
        self.bestscreenshot = None

    def set_easy(self, desc):
        self.easy = desc

    def set_hard(self, desc):
        self.hard = desc

    def set_challenge(self, desc):
        self.challenge = desc

    def set_comment(self, desc):
        self.comment = desc

    def set_active(self, month):
        self.active = True
        self.months = [Month.sum(month.value, i) for i in range(0, self.type.value)]

    def get_active(self):
        return self.active

    def add_easyplayer(self, player):
        self.easy_players.append(player)

    def get_easyplayers(self):
        return self.easy_players

    def add_hardplayer(self, player):
        self.hard_players.append(player)

    def get_hardplayers(self):
        return self.hard_players

    def add_challengeplayer(self, player):
        self.challenge_players.append(player)

    def get_challengeplayers(self):
        return self.challenge_players


class GameType(Enum):
    Short = 1
    Medium = 2
    Long = 4
