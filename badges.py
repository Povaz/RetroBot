
class SpeedBadge:

    def __init__(self, player, game):
        self.points = 1
        self.player = player
        self.game = game
        self.message = 'Speed Badge (+' + str(self.points) + ')!'
        self.string = 'Speed Badge (' + self.game.title + ')'

    def check_condition(self):
        if len(self.game.get_easyplayers()) <= 3:
            return True
        else:
            return False


class ScreenshotBadge:

    def __init__(self, player, game, image=None):
        self.points = 1
        self.player = player
        self.game = game
        if image:
            self.image = image
        self.message = player.name + ' won the Best Screenshot Badge (+' + str(self.points) + ') for ' + game.title + '!'
        self.string = 'Screenshot Badge (' + self.game.title + ')'


class VoteWinnerBadge:

    def __init__(self, player, game):
        self.points = 1
        self.player = player
        self.game = game
        self.message = self.game.title + ' was proposed by ' + player.name + '! VoteWinner Badge (+' + str(self.points) + ')!'
        self.string = 'VoteWinner Badge (' + self.game.title + ')'


class ShitheadBadge:

    def __init__(self, player, game):
        self.points = -2
        self.player = player
        self.game = game
        self.message = 'Not even playing what you propose. Shithead Badge (' + str(self.points) + ') for' + self.player.name
        self.string = 'Shithead Badge (' + self.game.title + ')'

    def check_condition(self):
        if self.game.title not in [played['game'].title for played in self.player.played]:
            return True
        else:
            return False


class VoterBadge:

    def __init__(self, player):
        self.points = 2
        self.player = player
        self.message = player.name + ' voted in each election! VoterBadge (+' + str(self.points) + ') for him!'
        self.string = 'Voter Badge'

    def check_condition(self):
        if self.player.votes == 7:
            return True
        else:
            return False


class CompletionistBadge:

    def __init__(self, player):
        self.points = 3
        self.player = player
        self.message = player.name + ' completed all the game for this Season! ' \
                                     'CompletionistBadge (+' + str(self.points) + ') for him!'
        self.string = 'Completionist Badge'

    def check_condition(self):
        if len(self.player.played) == 21:
            return True
        else:
            return False


class TryhardBadge:

    def __init__(self, player):
        self.points = 4
        self.player = player
        self.message = player.name + ' completed 5 games at Hard difficulty! ' \
                                     'TryhardBadge (+' + str(self.points) + ') for him!'
        self.string = 'Tryhard Badge'

    def check_condition(self):
        hardplayed = self.get_hardplayed_count()
        if hardplayed >= 5 and not self.check_badge_presence():
            return True
        else:
            return False

    def check_badge_presence(self):
        found = False
        for badge in self.player.badges:
            found = isinstance(badge, TryhardBadge)
        return found

    def get_hardplayed_count(self):
        hardplayed = 0
        for game in self.player.played:
            if game['mode'] == 'hard':
                hardplayed += 1
        return hardplayed


class HardcoreBadge:

    def __init__(self, player):
        self.points = 5
        self.player = player
        self.message = player.name + ' completed 4 challenges in this season! ' \
                                     'HardcoreBadge (+' + str(self.points) + ') for him!'
        self.string = 'Hardcore Badge'

    def check_condition(self):
        challenges = self.get_challenge_count()
        if challenges >= 4 and not self.check_badge_presence():
            return True
        else:
            return False

    def check_badge_presence(self):
        found = False
        for badge in self.player.badges:
            found = isinstance(badge, HardcoreBadge)
        return found

    def get_challenge_count(self):
        challenges = 0
        for game in self.player.played:
            if game['challenge']:
                challenges += 1
        return challenges
