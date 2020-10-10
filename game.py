from month import Month


class Game:

    def __init__(self, title, length, player):
        self.title = title
        self.length = length
        self.player = player

        self.easy = None
        self.hard = None
        self.challenge = None
        self.comment = None

        self.active = False
        self.months = []

        self.count = 0

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
        self.months = [Month.sum(month.value, i) for i in range(0, self.length)]

    def get_active(self):
        return self.active

    def add_count(self):
        self.count += 1

    def get_count(self):
        return self.count
