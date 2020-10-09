class Player:

    def __init__(self, name):
        self.name = name
        self.points = 0

        self.proposed = []
        self.votes = 0
        self.played = []

    def add_points(self, points):
        self.points += points

    def add_proposed(self, game):
        for proposal in self.proposed:
            if proposal.length == game.length:
                return False, 'Already proposed a game of this length.'
        self.proposed.append(game)
        return True, 'Game successfully proposed!'

    def add_votes(self, votes):
        self.votes += votes

    def add_played(self, game, mode, points):
        finished = self.__is_in_played(game)
        if not finished:
            self.played.append({
                'game': game,
                'mode': mode,
                'challenge': False
            })

            self.add_points(points)
            return mode + ' mode has been successfully registered for ' + game.title + '!'
        return 'Points for this game has already been redeemed!'

    def set_challenge(self, game_title, points):
        for game in self.played:
            if game['game'].title == game_title:
                if game['challenge']:
                    return 'Points for this challenge has already been redeemed!'
                else:
                    game['challenge'] = True
                    self.add_points(points)
                    return 'Challenge successfully registered for ' + game_title + '!'
        return 'Game not finished yet.'

    def __is_in_played(self, game):
        for g in self.played:
            if g['game'].title == game.title:
                return True
        return False
