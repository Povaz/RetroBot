from game import Game
from player import Player
from month import Month

# DURATION CONSTANTS
SEASON_DURATION = 4
SHORT_DURATION = 1
MEDIUM_DURATION = 2
LONG_DURATION = 4

# POINTS CONSTANTS
EASY_POINTS = 1
HARD_POINTS = 2
CHALLENGE_POINTS = 1

# GAME BADGES
SPEED_POINTS = 1
SCREENSHOT_POINTS = 1
VOTEWINNER_POINTS = 1
SHITHEAD_POINTS = -2

# SEASON BADGES
VOTER_POINTS = 2
VOTES_NEEDED = 7
COMPLETIONIST_POINTS = 3
TOTAL_GAMES = 7
TRYHARD_POINTS = 4
HARDCORE_POINTS = 5


class Season:

    # /newseason ADMIN-Command
    def __init__(self, start_month):
        self.months = [Month.sum(start_month, i) for i in range(0, SEASON_DURATION)]
        self.current_month = Month(start_month)
        self.proposed_games = []
        self.active_games = []
        self.passed_games = []
        self.players = []

    # TODO Backup procedure
    # TODO Player ID needs to be Telegram ID since Player Username can change
    # TODO /resetshort, /resetmedium, /resetlong commands to let people re-insert the game
    # TODO /resetshort player_name, /resetmedium player_name, /resetlong player_name for letting the admin act

    # /enroll command
    def add_player(self, player_id, player_name):
        self.players.append(Player(player_id, player_name))
        return 'Player successfully enrolled!'

    # /addshort 'game_title' command
    def add_shortgame(self, game_title, player_id):
        return self.add_proposedgame(game_title, SHORT_DURATION, player_id)

    # /addmedium 'game_title' command
    def add_mediumgame(self, game_title, player_id):
        return self.add_proposedgame(game_title, MEDIUM_DURATION, player_id)

    # /addlong 'game_title' command
    def add_longgame(self, game_title, player_id):
        return self.add_proposedgame(game_title, LONG_DURATION, player_id)

    def add_proposedgame(self, game_title, game_length, player_id):
        for player in self.players:
            if player_id == player.id:
                game = Game(game_title, game_length, player)
                success, message = player.add_proposed(game)
                if success:
                    if game.title not in [proposed.title for proposed in self.proposed_games]:
                        self.proposed_games.append(game)
                    else:
                        return 'This Game has already been proposed.'
                return message
        return 'Player does not exists.'

    # /addeasy 'game_title-desc' command
    def add_easymode(self, game_title, desc):
        return self.__add_info(game_title, desc, 'easy')

    # /addhard 'game_title-desc' command
    def add_hardmode(self, game_title, desc):
        return self.__add_info(game_title, desc, 'hard')

    # /addchallenge 'game_title-desc' command
    def add_challenge(self, game_title, desc):
        return self.__add_info(game_title, desc, 'challenge')

    # /addcomment 'game_title-desc' command
    def add_gamecomment(self, game_title, desc):
        return self.__add_info(game_title, desc, 'comment')

    def __add_info(self, game_title, desc, info_type):
        for game in self.proposed_games:
            if game.title == game_title:
                if info_type == 'easy':
                    game.set_easy(desc)
                    return 'Easy mode for ' + game.title + ' successfully added!'
                elif info_type == 'hard':
                    game.set_hard(desc)
                    return 'Hard mode for ' + game.title + ' successfully added!'
                elif info_type == 'challenge':
                    game.set_challenge(desc)
                    return 'Challenge for ' + game.title + ' successfully added!'
                else:
                    game.set_comment(desc)
                    return 'Comment for ' + game.title + ' successfully added!'
        return 'Not even writing the name correctly. (Game not found).'

    # /easylist command
    def retrieve_short(self):
        return self.retrieve(SHORT_DURATION)

    # /mediumlist command
    def retrieve_medium(self):
        return self.retrieve(MEDIUM_DURATION)

    # /longlist command
    def retrieve_long(self):
        return self.retrieve(LONG_DURATION)

    def retrieve(self, length):
        return [game.title for game in self.proposed_games if (not game.active and game.length == length)]

    # /vote 'times'
    def record_votes(self, player_id, times):
        player = self.__player_by_id(player_id)
        if player:
            player.add_votes(times)
        else:
            return 'Player does not exists.'

    # /winner 'game_title' ADMIN-command
    def winner(self, game_title):
        for game in self.proposed_games:
            if game.title == game_title:
                if not game.get_active() and game.length not in [active.length for active in self.active_games]:
                    game.set_active(self.current_month)
                    game.player.add_points(VOTEWINNER_POINTS)
                    self.active_games.append(game)
                    self.proposed_games.remove(game)
                else:
                    return 'A game of this duration has already been activated!'
                return 'Game successfully added as active game! A point for ' + game.player.name + '!'
        return 'Not even writing the name correctly. (Game not found).'

    # /activelist command
    def retrieve_active(self):
        return [game.title for game in self.active_games]

    # /proposelist command
    def retrieve_proposed(self):
        return [game.title for game in self.proposed_games]

    # /pastlist command
    def retrieve_passed(self):
        return [game.title for game in self.passed_games]

    # /infogame 'game_title' command
    def retrieve_info(self, game_title):
        for game in self.proposed_games:
            if game.title == game_title:
                return [game.title, game.easy, game.hard, game.challenge, game.comment, game.active, game.months]
        return 'Not even writing the name correctly. (Game not found).'

    # /easy 'game_title' command
    def easy_finished(self, game_title, player_id):
        player = self.__player_by_id(player_id)
        if player:
            game = self.__activegame_by_title(game_title)
            if game:
                game.add_count()
                count = game.get_count()
                points = EASY_POINTS
                if count <= 3:
                    points += SPEED_POINTS
                return player.add_played(game, 'easy', points)
            else:
                return 'Game is not active or does not exists! You cheating scum!'
        else:
            return 'Player does not exists.'

    # /hard 'game_title' command
    def hard_finished(self, game_title, player_id):
        player = self.__player_by_id(player_id)
        if player:
            game = self.__activegame_by_title(game_title)
            if game:
                return player.add_played(game, 'hard', HARD_POINTS)
            else:
                return 'Game is not active or does not exists! You cheating scum!'
        else:
            return 'Player does not exists.'

    # /challenge 'game_title' command
    def challenge_completed(self, game_title, player_id):
        player = self.__player_by_id(player_id)
        if player:
            game = self.__activegame_by_title(game_title)
            if game:
                return player.set_challenge(game.title, CHALLENGE_POINTS)
            else:
                return 'Game is not active or does not exists! You cheating scum!'
        else:
            return 'Player does not exists.'

    def __player_by_id(self, player_id):
        for player in self.players:
            if player.id == player_id:
                return player
        return None

    def __activegame_by_title(self, title):
        for game in self.active_games:
            if game.title == title:
                return game
        return None

    # /nextmonth command
    def next_month(self):
        self.current_month = Month.sum(self.current_month.value, 1)
        if self.current_month not in self.months:
            msg = 'This was the last month for this Season!'
        else:
            msg = 'A new month has begun!'

        finished = []
        for active in self.active_games:
            if self.current_month not in active.months:
                self.passed_games.append(active)
                finished.append(active)

                if active.length == 1:
                    game_len = 'short'
                elif active.length == 2:
                    game_len = 'medium'
                else:
                    game_len = 'long'
                msg += ' Time for ' + active.title + ' has finished! A new ' + game_len + ' game must be elected!'

                if active.title not in [played['game'].title for played in active.player.played]:
                    active.player.add_points(SHITHEAD_POINTS)
                    msg += ' Not even playing what you propose. Shithead. ' + str(SHITHEAD_POINTS) \
                           + ' to ' + active.player.name

        for f in finished:
            self.active_games.remove(f)

        return msg

    # /endseason ADMIN-command
    def endseason(self):
        for player in self.players:
            # Voter Badge
            if player.votes == VOTES_NEEDED:
                player.add_points(VOTER_POINTS)

            # Completionist Badge
            if len(player.played) == TOTAL_GAMES:
                player.add_points(COMPLETIONIST_POINTS)

            # Tryhard Badge
            tryhard = 0
            for game in player.played:
                if game['mode'] == 'hard':
                    tryhard += 1
            if tryhard >= 5:
                player.add_points(TRYHARD_POINTS)

            # Hardcore Badge
            hardcore = 0
            for game in player.played:
                if game['challenge']:
                    hardcore += 1
            if hardcore >= 4:
                player.add_points(HARDCORE_POINTS)

        return 'Season Badges points have been added! Check the Leaderboard to discover who has won!'

    # /bestscreenshot 'player_name' ADMIN-command
    def screenshot_badge(self, player_id):
        player = self.__player_by_id(player_id)
        player.add_points(SCREENSHOT_POINTS)
        return 'Best Screenshot points added to ' + player.name + ' points!'

    # /leaderboard command
    def get_leaderboard(self):
        leaderboard = sorted(self.players, key=lambda x: x.points, reverse=True)
        return leaderboard

    # /activeinfo command
    def get_activegames(self):
        return self.active_games
