from game import Game, GameType
from player import Player
from month import Month
from badges import *
from datetime import datetime as dt
import jsonpickle

# DURATION CONSTANTS
SEASON_DURATION = 4
SHORT_DURATION = 1
MEDIUM_DURATION = 2
LONG_DURATION = 4

# POINTS CONSTANTS
EASY_POINTS = 1
HARD_POINTS = 2
CHALLENGE_POINTS = 1


class Season:

    # /newseason ADMIN-Command
    def __init__(self, start_month):
        self.months = [Month.sum(start_month, i) for i in range(0, SEASON_DURATION)]
        self.current_month = Month(start_month)
        self.proposed_games = []
        self.active_games = []
        self.passed_games = []
        self.players = []

    # /enroll command
    def add_player(self, player_id, player_name):
        if not self.__player_by_id(player_id):
            self.players.append(Player(player_id, player_name))
            return 'Player successfully enrolled!'
        else:
            return 'Player already enrolled! Alzheimer dude?'

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

    # /resetshort command and /resetshort 'player_name' ADMIN-command
    def reset_shortgame(self, player_id, player_name=None):
        return self.reset_game(player_id, SHORT_DURATION, player_name=player_name)

    # /resetmedium command and /resetmedium 'player_name' ADMIN-command
    def reset_mediumgame(self, player_id, player_name=None):
        return self.reset_game(player_id, MEDIUM_DURATION, player_name=player_name)

    # /resetlong command and /resetlong 'player_name' ADMIN-command
    def reset_longgame(self, player_id, player_name=None):
        return self.reset_game(player_id, LONG_DURATION, player_name=player_name)

    def reset_game(self, player_id, game_length, player_name=None):
        if player_name:
            player = self.__player_by_name(player_name)
        else:
            player = self.__player_by_id(player_id)
        if not player:
            return 'Player does not exists.'
        deleted = None

        for game in self.proposed_games:
            if game.player.id == player.id and game.type == GameType(game_length):
                deleted = game

        if deleted:
            self.proposed_games.remove(deleted)
            player.proposed.remove(deleted)
            return 'Game successfully removed!'
        else:
            return 'Game not found!'

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
        return [game for game in self.proposed_games if (not game.active and game.type.value == length)]

    # /vote 'times'
    def record_votes(self, player_id, times):
        player = self.__player_by_id(player_id)
        if player:
            player.add_votes(times)
            msg = 'Votes added successfully! You voted ' + str(player.votes) + ' times!'
            # VoterBadge
            voter_badge = VoterBadge(player)
            if voter_badge.check_condition():
                player.add_badge(voter_badge)
                msg += voter_badge.message
            else:
                for badge in player.badges:
                    if isinstance(badge, VoterBadge):
                        player.badges.remove(badge)
                        player.add_points(badge.points)
                        msg += 'Voter Badge removed! Stop sends false votes with your fat fingers, please.'
            return msg
        else:
            return 'Player does not exists.'

    # /winner 'game_title' ADMIN-command
    def winner(self, game_title):
        for game in self.proposed_games:
            if game.title == game_title:
                if not game.get_active() and game.type not in [active.type for active in self.active_games]:
                    game.set_active(self.current_month)
                    self.active_games.append(game)
                    self.proposed_games.remove(game)

                    # VoteWinner Badge
                    votewinner_badge = VoteWinnerBadge(game.player, game)
                    game.player.add_badge(votewinner_badge)
                    return 'Game successfully added as active game! ' + votewinner_badge.message
                else:
                    return 'A game of this duration has already been activated!'

        return 'Not even writing the name correctly. (Game not found).'

    # /activelist command
    def retrieve_active(self):
        return [game for game in self.active_games]

    # /proposelist command
    def retrieve_proposed(self):
        return [game for game in self.proposed_games]

    # /pastlist command
    def retrieve_passed(self):
        return [game for game in self.passed_games]

    # /infogame 'game_title' command
    def retrieve_game(self, game_title):
        game = self.__game_by_title(game_title)
        if game:
            return game
        else:
            return 'Not even writing the name correctly. (Game not found).'

    # /infoplayer 'player_name' command
    def retrieve_player(self, player_name):
        player = self.__player_by_name(player_name)
        if player_name:
            return player.get_player_string()
        else:
            return 'Not even writing the name correctly. (Player not found).'

    # /easy 'game_title' command
    def easy_finished(self, game_title, player_id):
        player = self.__player_by_id(player_id)
        if player:
            game = self.__activegame_by_title(game_title)
            if game:
                if player.is_in_played(game):
                    return 'This player has already completed this game!'
                else:
                    game.add_easyplayer(player)
                    msg = player.add_played(game, 'easy', EASY_POINTS)

                    # Speed Badge
                    speed_badge = SpeedBadge(player, game)
                    if speed_badge.check_condition():
                        player.add_badge(speed_badge)
                        msg += ' ' + speed_badge.message

                    # Completionist Badge
                    completionist_badge = CompletionistBadge(player)
                    if completionist_badge.check_condition():
                        player.add_badge(completionist_badge)
                        msg += ' ' + completionist_badge.message

                    return msg
            else:
                return 'Game is not active or does not exists! You cheating scum!'
        else:
            return 'Player does not exists.'

    # /forceeasy 'game_title-player_name' ADMIN-command
    def forceeasy_finished(self, game_title, player_name):
        player = self.__player_by_name(player_name)
        if player:
            game = self.__game_by_title(game_title)
            if game:
                if player.is_in_played(game):
                    return 'This player has already completed this game!'
                else:
                    game.add_easyplayer(player)
                    msg = player.add_played(game, 'easy', EASY_POINTS)

                    # Speed Badge
                    speed_badge = SpeedBadge(player, game)
                    if speed_badge.check_condition():
                        player.add_badge(speed_badge)
                        msg += ' ' + speed_badge.message

                    # Completionist Badge
                    completionist_badge = CompletionistBadge(player)
                    if completionist_badge.check_condition():
                        player.add_badge(completionist_badge)
                        msg += ' ' + completionist_badge.message

                    return msg
            else:
                return 'Game is not active or does not exists! You cheating scum!'
        else:
            return 'Player does not exists.'

    # /revokeeasy 'game_title-player_name' ADMIN-command
    def easy_revoke(self, game_title, player_name):
        player = self.__player_by_name(player_name)
        if player:
            game = self.__game_by_title(game_title)
            if game:
                deleted = None
                for played_game in player.played:
                    if played_game['game'].title == game_title and played_game['mode'] == 'easy':
                        deleted = played_game
                if deleted:
                    player.played.remove(deleted)
                    player.add_points(-EASY_POINTS)
                    game.easy_players.remove(player)
                    msg = 'Easy mode successfully revoked from ' + player.name + ' !\n'

                    # Revoke Speedbadge Routine
                    for badge in player.badges:
                        if isinstance(badge, SpeedBadge):
                            if badge.game == game_title:
                                player.badges.remove(badge)
                                player.add_points(-badge.points)
                                msg += 'Speedbadge successfully revoked from ' + player.name + ' !\n'
                                if len(game.easy_players) >= 3:
                                    speedbadge = SpeedBadge(game.easy_players[2], game)
                                    game.easy_players[2].add_badge(speedbadge)
                                    msg += 'Speedbadge successfully reassigned to ' + game.easy_players[2].name + ' !\n'

                    return msg
                return 'This has not completed this game on this difficulty!'
            else:
                return 'Game not found!'
        else:
            return 'Player does not exists.'

    # /hard 'game_title' command
    def hard_finished(self, game_title, player_id):
        player = self.__player_by_id(player_id)
        if player:
            game = self.__activegame_by_title(game_title)
            if game:
                if player.is_in_played(game):
                    return 'This player has already completed this game!'
                else:
                    game.add_hardplayer(player)
                    msg = player.add_played(game, 'hard', HARD_POINTS)

                    # Completionist Badge
                    completionist_badge = CompletionistBadge(player)
                    if completionist_badge.check_condition():
                        player.add_badge(completionist_badge)
                        msg += ' ' + completionist_badge.message

                    # Tryhard Badge
                    tryhard_badge = TryhardBadge(player)
                    if tryhard_badge.check_condition():
                        player.add_badge(tryhard_badge)
                        msg += ' ' + tryhard_badge.message

                    return msg
            else:
                return 'Game is not active or does not exists! You cheating scum!'
        else:
            return 'Player does not exists.'

    # /forcehard 'game_title-player_name' ADMIN-command
    def forcehard_finished(self, game_title, player_name):
        player = self.__player_by_name(player_name)
        if player:
            game = self.__game_by_title(game_title)
            if game:
                if player.is_in_played(game):
                    return 'This player has already completed this game!'
                else:
                    game.add_hardplayer(player)
                    msg = player.add_played(game, 'hard', HARD_POINTS)

                    # Completionist Badge
                    completionist_badge = CompletionistBadge(player)
                    if completionist_badge.check_condition():
                        player.add_badge(completionist_badge)
                        msg += ' ' + completionist_badge.message

                    # Tryhard Badge
                    tryhard_badge = TryhardBadge(player)
                    if tryhard_badge.check_condition():
                        player.add_badge(tryhard_badge)
                        msg += ' ' + tryhard_badge.message

                    return msg
            else:
                return 'Game is not active or does not exists! You cheating scum!'
        else:
            return 'Player does not exists.'

    # /revokehard 'game_title-player_name' ADMIN-command
    def hard_revoke(self, game_title, player_name):
        player = self.__player_by_name(player_name)
        if player:
            game = self.__game_by_title(game_title)
            if game:
                deleted = None
                for played_game in player.played:
                    if played_game['game'].title == game_title and played_game['mode'] == 'hard':
                        deleted = played_game
                if deleted:
                    player.played.remove(deleted)
                    player.add_points(-HARD_POINTS)
                    game.hard_players.remove(player)

                    msg = 'Hard mode successfully revoked! \n'
                    for badge in player.badges:
                        if isinstance(badge, CompletionistBadge):
                            player.add_points(-badge.points)
                            player.badges.remove(badge)
                            msg += 'Completionist Badge successfully revoked from ' + player.name + ' !\n'

                    for badge in player.badges:
                        if isinstance(badge, TryhardBadge):
                            if not badge.check_condition():
                                player.add_points(-badge.points)
                                player.badges.remove(badge)
                                msg += 'Tryhard Badge successfully revoked from ' + player.name + ' !\n'
                    return msg
                return 'This has not completed this game on this difficulty!'
            else:
                return 'Game not found!'
        else:
            return 'Player does not exists.'

    # /challenge 'game_title' command
    def challenge_completed(self, game_title, player_id):
        player = self.__player_by_id(player_id)
        if player:
            game = self.__activegame_by_title(game_title)
            if game:
                if player.challenge_complete(game):
                    return 'This player has already completed the challenge on this game!'
                else:
                    game.add_challengeplayer(player)
                    msg = player.set_challenge(game.title, CHALLENGE_POINTS)

                    # Hardcore Badge
                    hardcore_badge = HardcoreBadge(player)
                    if hardcore_badge.check_condition():
                        player.add_badge(hardcore_badge)
                        msg += ' ' + hardcore_badge.message

                    return msg
            else:
                return 'Game is not active or does not exists! You cheating scum!'
        else:
            return 'Player does not exists.'

    # /forcechallenge 'game_title-player_name' ADMIN-command
    def forcechallenge_completed(self, game_title, player_name):
        player = self.__player_by_name(player_name)
        if player:
            game = self.__game_by_title(game_title)
            if game:
                if player.challenge_complete(game):
                    return 'This player has already completed the challenge on this game!'
                else:
                    game.add_challengeplayer(player)
                    msg = player.set_challenge(game.title, CHALLENGE_POINTS)

                    # Hardcore Badge
                    hardcore_badge = HardcoreBadge(player)
                    if hardcore_badge.check_condition():
                        player.add_badge(hardcore_badge)
                        msg += ' ' + hardcore_badge.message

                    return msg
            else:
                return 'Game is not active or does not exists! You cheating scum!'
        else:
            return 'Player does not exists.'

    # /revokechallenge 'game_title-player_name' ADMIN-command
    def challenge_revoke(self, game_title, player_name):
        player = self.__player_by_name(player_name)
        if player:
            game = self.__game_by_title(game_title)
            if game:
                for played_game in player.played:
                    if played_game['game'].title == game_title and played_game['challenge']:
                        played_game['challenge'] = False
                        player.add_points(-CHALLENGE_POINTS)
                        game.challenge_players.remove(player)
                        msg = 'Challenge successfully revoked!'

                        for badge in player.badges:
                            if isinstance(badge, HardcoreBadge):
                                if not badge.check_condition():
                                    player.add_points(-badge.points)
                                    player.badges.remove(badge)
                                    msg += 'Hardcore Badge successfully revoked from ' + player.name + ' !\n'
                        return msg
                return 'This has not completed the challenge on this game!'
            else:
                return 'Game not found!'
        else:
            return 'Player does not exists.'

    def __player_by_id(self, player_id):
        for player in self.players:
            if player.id == player_id:
                return player
        return None

    def __player_by_name(self, player_name):
        for player in self.players:
            if player.name == player_name:
                return player
        return None

    def __activegame_by_title(self, title):
        for game in self.active_games:
            if game.title == title:
                return game
        return None

    def __game_by_title(self, title):
        complete_gamelist = self.proposed_games + self.active_games + self.passed_games
        for game in complete_gamelist:
            if game.title == title:
                return game
        return None

    # /nextmonth command
    def next_month(self):
        self.current_month = Month.sum(self.current_month.value, 1)
        if self.current_month not in self.months:
            msg = 'This was the last month for this Season!'
        else:
            msg = 'A new month of the season has begun!'

        finished = []
        for active in self.active_games:
            if self.current_month not in active.months:
                self.passed_games.append(active)
                finished.append(active)

                msg += ' Time for ' + active.title + ' has finished! A new ' + active.type.name + ' game must be elected!'

                # Shithead Badge
                shithead_badge = ShitheadBadge(active.player, active)
                if shithead_badge.check_condition():
                    active.player.add_badge(shithead_badge)
                    msg += ' ' + shithead_badge.message

        for f in finished:
            self.active_games.remove(f)

        return msg

    # /revokeshithead 'game_title-player_name' ADMIN-command
    def revoke_shitheadbadge(self, player_name, game_title):
        player = self.__player_by_name(player_name)
        game = self.__game_by_title(game_title)

        for badge in player.badges:
            if isinstance(badge, ShitheadBadge):
                if badge.game.title == game_title:
                    player.add_points(-badge.points)
                    player.badges.remove(badge)
                    return ' Shithead Badge successfully revoked from ' + player.name + ' on ' + game_title + ' !'
        return 'No Shithead Badge for ' + player_name + ' on ' + game_title + '!'

    # /bestscreenshot 'game_title-player_name' ADMIN-command
    def screenshot_badge(self, player_name, game_title):
        player = self.__player_by_name(player_name)
        game = self.__game_by_title(game_title)

        # Screenshot Badge
        screenshot_badge = ScreenshotBadge(player, game)
        player.add_badge(screenshot_badge)
        game.best_screenshotplayer.append(player)
        return screenshot_badge.message

    # /revokescreenshot 'game_title-player_name' ADMIN-command
    def revoke_screenshotbadge(self, player_name, game_title):
        player = self.__player_by_name(player_name)
        game = self.__game_by_title(game_title)

        for badge in player.badges:
            if isinstance(badge, ScreenshotBadge):
                if badge.game.title == game_title:
                    player.add_points(-badge.points)
                    player.badges.remove(badge)
                    return ' Screenshot Badge successfully revoked from ' + player.name + ' on ' + game_title + ' !'
        return 'No Screenshot Badge for ' + player_name + ' on ' + game_title + '!'

    # /leaderboard command
    def get_leaderboard(self):
        leaderboard = sorted(self.players, key=lambda x: x.points, reverse=True)
        return leaderboard

    # /backups ADMIN-command
    def backup(self):
        jsonbackup = jsonpickle.encode(self, indent=4)
        date = dt.now().strftime("%Y_%m_%d_%H_%M_%S")
        file = open('./backups/backup_' + date + '.json', 'w+')
        file.write(jsonbackup)
        return 'Backup_' + date + ' completed!'
