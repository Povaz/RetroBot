from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from season import Season
import jsonpickle
import logging
import csv
import os

# Logger Settings
# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('./logs/retrobot.log')
c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

# Current Season Variables
season = Season(0)
loadbackup_check = False
nextmonth_check = False
newseason_check = False


# /command command
def command(update, context):
    """Command Description."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        if is_admin(update.message['from_user']['id']):
            return True
        else:
            update.message.reply_text('Not even an admin! weirdChamp', parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /command command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /help command
def helpcommand(update, context):
    """Returns the list of commands."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        msg = '*General Commands*\n'
        msg += '/help: Shows all commands. But you already know, I guess. \n' \
               '/adminhelp: Shows all sudo commands. You most probably cant use them, pleb. \n' \
               '/enroll: Enroll the user in the current season. \n' \
               '/addshort _gametitle_: Propose a Short Game (1 month length). \n' \
               '/addmedium _gametitle_: Propose a Medium Game (2 month length). \n' \
               '/addlong _gametitle_: Propose a Long Game (4 month length). \n' \
               '/resetshort _gametitle_: Reset the Short Game you proposed. \n' \
               '/resetmedium _gametitle_: Reset the Medium Game you proposed. \n' \
               '/resetlong _gametitle_: Reset the Long Game you proposed. \n' \
               '/addeasy _gametitle-easymode_: Add an Easy Mode description for a game. \n' \
               '/addhard _gametitle-hardmode_: Add an Hard Mode description for a game. \n' \
               '/addchallenge _gametitle-challenge_: Add a Challenge description for a game. \n' \
               '/addcomment _gametitle-comment_: Add an additional Comment for a game. \n' \
               '/list: Return the list of all the games in the Season. \n' \
               '/vote _numberofvotes_: Register how many votes you have expressed (for Voter Badge). \n' \
               '/activelist: Return the list of the currently Active Games. \n' \
               '/proposelist: Return the list of the proposed (but not yet chosen) Games. \n' \
               '/pastlist: Return the list of the past Games. \n' \
               '/infogame _gametitle_: Return the complete info about the Game. \n' \
               '/infoplayer _playername_: Return the complete info about the Player. \n' \
               '/easy _gametitle_: Submit easy difficulty for a completed Game. \n' \
               '/hard _gametitle_: Submit hard difficulty for a completed Game. \n' \
               '/challenge _gametitle_ : Submit challenge completed for a Game. \n' \
               '/leaderboard: See who is rolling and who is sucking. \n'
        update.message.reply_text(msg, parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /help command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /adminhelp command
def adminhelpcommand(update, context):
    """Returns the list of Admin commands."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        if is_admin(update.message['from_user']['id']):
            msg = '*Admin Commands*\n'
            msg += '/newseason _month_: Starts a new Season overriding the current one. Needs confirmation.\n' \
                   '/revokeeasy _gametitle-playername_: Revoke an Easy difficulty registered. \n' \
                   '/revokehard _gametitle-playername_: Revoke an Hard difficulty registered. \n' \
                   '/revokechallenge _gametitle-playername_: Revoke a Challenge registered. \n' \
                   '/revokescreenshot _gametitle-playername_: Revoke a Screenshot Badge. \n' \
                   '/revokeshithead _gametitle-playername_: Revoke a Shithead Badge. \n' \
                   '/resetshort _playername_: Cancel a Short Game proposed by a Player. \n' \
                   '/resetmedium _playername_: Cancel a Medium Game proposed by a Player. \n' \
                   '/resetlong _playername_: Cancel a Long Game proposed by a Player. \n' \
                   '/winner _gametitle_: Elects a Winner for an external Poll. \n' \
                   '/nextmonth: Set the next month as current one, moving all the games. Needs confirmation. \n' \
                   '/bestscreenshot _gametitle-playername_: Assigns the Best screenshot badge. \n' \
                   '/backup: Create a new Backup. All Backups are saved separately. \n' \
                   '/backuplist: Return the list of all backups with their ID. \n' \
                   '/loadbackup _backupid_: Loads a Backup, overriding the current Season state. Needs confirmation. \n'
            update.message.reply_text(msg, parse_mode='Markdown')
        else:
            update.message.reply_text('Not even an admin! weirdChamp', parse_mode='Markdown')

    except Exception:
        logger.exception('An Exception occurred executing /help command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /newseason ADMIN-command
def newseason(update, context):
    """Create a New Season."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    nextmonth_check = False
    try:
        if is_admin(update.message['from_user']['id']):
            if newseason_check:
                month = update.message['text'].replace('/newseason', '')
                season = Season(int(month))
                update.message.reply_text('A new Season has been created!', parse_mode='Markdown')
                newseason_check = False
            else:
                update.message.reply_text("Are you sure? Creating a new season will create a Backup of the current one"
                                          "and create a new one from scratch. The operation is reversible only with "
                                          "more God's work. Be careful.", parse_mode="Markdown")
                newseason_check = True
        else:
            update.message.reply_text('Not even an admin! weirdChamp', parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /newseason command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /enroll command
def enroll(update, context):
    """Enroll a new Player."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        player_id = update.message['from_user']['id']
        player_name = update.message['from_user']['username']
        update.message.reply_text(season.add_player(int(player_id), player_name), parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /enroll command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /addshort 'game_title' command
def addshort(update, context):
    """Propose a Short Game"""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        player_id = update.message['from_user']['id']
        game_title = update.message['text'].replace('/addshort ', '')
        update.message.reply_text(season.add_shortgame(game_title, int(player_id)), parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /addshort command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /addmedium 'game_title' command
def addmedium(update, context):
    """Propose a Medium Game"""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        player_id = update.message['from_user']['id']
        game_title = update.message['text'].replace('/addmedium ', '')
        update.message.reply_text(season.add_mediumgame(game_title, int(player_id)), parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /addmedium command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /addlong 'game_title' command
def addlong(update, context):
    """Propose a Long Game"""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        player_id = update.message['from_user']['id']
        game_title = update.message['text'].replace('/addlong ', '')
        update.message.reply_text(season.add_longgame(game_title, int(player_id)), parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /addlong command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /revokeeasy 'game_title-player_name' ADMIN-command
def revokeeasy(update, context):
    """Revoke finished game at easy difficulty."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        if is_admin(update.message['from_user']['id']):
            message = update.message['text'].replace('/revokeeasy ', '').split('-')
            game_title = message[0]
            player_name = message[1]
            update.message.reply_text(season.easy_revoke(game_title, player_name), parse_mode='Markdown')
        else:
            update.message.reply_text('Not even an admin! weirdChamp', parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /revokeeasy command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /revokehard 'game_title-player_name' ADMIN-command
def revokehard(update, context):
    """Revoke finished game at hard difficulty."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        if is_admin(update.message['from_user']['id']):
            message = update.message['text'].replace('/revokehard ', '').split('-')
            game_title = message[0]
            player_name = message[1]
            update.message.reply_text(season.hard_revoke(game_title, player_name), parse_mode='Markdown')
        else:
            update.message.reply_text('Not even an admin! weirdChamp', parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /revokehard command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /revokechallenge 'game_title-player_name' ADMIN-command
def revokechallenge(update, context):
    """Revoke challenge of a game."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        if is_admin(update.message['from_user']['id']):
            message = update.message['text'].replace('/revokechallenge ', '').split('-')
            game_title = message[0]
            player_name = message[1]
            update.message.reply_text(season.challenge_revoke(game_title, player_name), parse_mode='Markdown')
        else:
            update.message.reply_text('Not even an admin! weirdChamp', parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /revokechallenge command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /forceeasy 'game_title-player_name' ADMIN-command
def forceeasy(update, context):
    """Force the easy mode completion of a game on a player."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        if is_admin(update.message['from_user']['id']):
            message = update.message['text'].replace('/forceeasy ', '').split('-')
            game_title = message[0]
            player_name = message[1]
            update.message.reply_text(season.forceeasy_finished(game_title, player_name), parse_mode='Markdown')
        else:
            update.message.reply_text('Not even an admin! weirdChamp', parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /forceeasy command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /forcehard 'game_title-player_name' ADMIN-command
def forcehard(update, context):
    """Force the hard mode completion of a game on a player."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        if is_admin(update.message['from_user']['id']):
            message = update.message['text'].replace('/forcehard ', '').split('-')
            game_title = message[0]
            player_name = message[1]
            update.message.reply_text(season.forcehard_finished(game_title, player_name), parse_mode='Markdown')
        else:
            update.message.reply_text('Not even an admin! weirdChamp', parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /forcehard command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /forcechallenge 'game_title-player_name' ADMIN-command
def forcechallenge(update, context):
    """Force the challenge completion for a game on a player."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        if is_admin(update.message['from_user']['id']):
            message = update.message['text'].replace('/forcechallenge ', '').split('-')
            game_title = message[0]
            player_name = message[1]
            update.message.reply_text(season.forcechallenge_completed(game_title, player_name), parse_mode='Markdown')
        else:
            update.message.reply_text('Not even an admin! weirdChamp', parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /forcehard command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /resetshort command
def resetshort(update, context):
    """Resets the Short game for the player who uses the command."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        player_id = update.message['from_user']['id']
        update.message.reply_text(season.reset_shortgame(int(player_id)), parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /resetshort command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /resetmedium command
def resetmedium(update, context):
    """Resets the Medium game for the player who uses the command."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        player_id = update.message['from_user']['id']
        update.message.reply_text(season.reset_mediumgame(int(player_id)), parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /resetmedium command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /resetlong command
def resetlong(update, context):
    """Resets the Long game for the player who uses the command."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        player_id = update.message['from_user']['id']
        update.message.reply_text(season.reset_longgame(int(player_id)), parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /resetlong command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /resetshort 'player_name' ADMIN-command
def resetshort_admin(update, context):
    """Resets the short game of a player. Admin command."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        if is_admin(update.message['from_user']['id']):
            player_id = update.message['from_user']['id']
            player_name = update.message['text'].replace('/resetshort ', '')
            update.message.reply_text(season.reset_shortgame(player_id, player_name=player_name), parse_mode='Markdown')
        else:
            update.message.reply_text('Not even an admin! weirdChamp', parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /resetshort ADMIN-command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /resetmedium 'player_name' ADMIN-command
def resetmedium_admin(update, context):
    """Resets the medium game of a player. Admin command."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        if is_admin(update.message['from_user']['id']):
            player_id = update.message['from_user']['id']
            player_name = update.message['text'].replace('/resetmedium ', '')
            update.message.reply_text(season.reset_mediumgame(player_id, player_name=player_name), parse_mode='Markdown')
        else:
            update.message.reply_text('Not even an admin! weirdChamp', parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /resetmedium ADMIN-command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /resetmedium 'player_name' ADMIN-command
def resetlong_admin(update, context):
    """Resets the long game of a player. Admin command."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        if is_admin(update.message['from_user']['id']):
            player_id = update.message['from_user']['id']
            player_name = update.message['text'].replace('/resetlong ', '')
            update.message.reply_text(season.reset_longgame(player_id, player_name=player_name), parse_mode='Markdown')
        else:
            update.message.reply_text('Not even an admin! weirdChamp', parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /resetlong ADMIN-command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /addeasy 'game_title-desc' command
def addeasy(update, context):
    """Add Easy Mode Description for a game."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        message = update.message['text'].replace('/addeasy ', '').split('-')
        game_title = message[0]
        desc = message[1]
        update.message.reply_text(season.add_easymode(game_title, desc), parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /addeasy command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /addhard 'game_title-desc' command
def addhard(update, context):
    """Add Hard Mode Description for a game."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        message = update.message['text'].replace('/addhard ', '').split('-')
        game_title = message[0]
        desc = message[1]
        update.message.reply_text(season.add_hardmode(game_title, desc), parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /addhard command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /addchallenge 'game_title-desc' command
def addchallenge(update, context):
    """Add Challenge Description for a game."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        message = update.message['text'].replace('/addchallenge ', '').split('-')
        game_title = message[0]
        desc = message[1]
        update.message.reply_text(season.add_challenge(game_title, desc), parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /addchallenge command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /addcomment 'game_title-desc' command
def addcomment(update, context):
    """Add Comment for a game."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        message = update.message['text'].replace('/addcomment ', '').split('-')
        game_title = message[0]
        desc = message[1]
        update.message.reply_text(season.add_gamecomment(game_title, desc), parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /addcomment command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /list command
def list(update, context):
    """Add Comment for a game."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        msg = ''
        shortlist = season.retrieve_short()
        mediumlist = season.retrieve_medium()
        longlist = season.retrieve_long()

        msg += '*Short Games List* \n'
        for game in shortlist:
            msg += '    ' + game.title
            if game.active:
                msg += ' (Active) \n'
            else:
                msg += ' (Inactive) \n'

        msg += '*Medium Games List* \n'
        for game in mediumlist:
            msg += '    ' + game.title
            if game.active:
                msg += ' (Active) \n'
            else:
                msg += ' (Inactive) \n'

        msg += '*Long Games List* \n'
        for game in longlist:
            msg += '    ' + game.title
            if game.active:
                msg += ' (Active) \n'
            else:
                msg += ' (Inactive) \n'
        update.message.reply_text(msg, parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /addcomment command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /vote command
def vote(update, context):
    """Adds number of votes to player in order to keep track of Voter Badge."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        votes = int(update.message['text'].replace('/vote ', ''))
        player_id = update.message['from_user']['id']
        update.message.reply_text(season.record_votes(player_id, votes), parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /vote command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /winner 'game_title' ADMIN-command
def winner(update, context):
    """Set the winner game active."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        if is_admin(update.message['from_user']['id']):
            game_title = update.message['text'].replace('/winner ', '')
            update.message.reply_text(season.winner(game_title), parse_mode='Markdown')
        else:
            update.message.reply_text('Not even an admin! weirdChamp', parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /winner command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /activelist command
def activelist(update, context):
    """Retrieve the list of Active Games."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        active = season.retrieve_active()
        if not len(active):
            update.message.reply_text('No game in this list yet!', parse_mode='Markdown')
        else:
            msg = gameliststring(active)
            update.message.reply_text(msg, parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /activelist command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /proposelist command
def proposelist(update, context):
    """Retrieve the list of Proposed Games."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        proposed = season.retrieve_proposed()
        if not len(proposed):
            update.message.reply_text('No game in this list yet!', parse_mode='Markdown')
        else:
            msg = gameliststring(proposed)
            update.message.reply_text(msg, parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /proposelist command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /pastlist command
def pastlist(update, context):
    """Retrieve the list of Past Games."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        passed = season.retrieve_passed()
        if not len(passed):
            update.message.reply_text('No game in this list yet!', parse_mode='Markdown')
        else:
            msg = gameliststring(passed)
            update.message.reply_text(msg, parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /pastlist command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /infogame 'game_title' command
def infogame(update, context):
    """Retrieve all game info."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        game_title = update.message['text'].replace('/infogame ', '')
        game = season.retrieve_game(game_title)
        msg = gamestring(game)
        addmsg = gameadditionalstring(game)
        update.message.reply_text(msg + addmsg, parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /infogame command:')
        update.message.reply_text('Unexpected Shit happened!''No game in this list yet!', parse_mode='Markdown')


# /infoplayer 'game_title' command
def infoplayer(update, context):
    """Retrieve all player info."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        player_name = update.message['text'].replace('/infoplayer ', '')
        msg = season.retrieve_player(player_name)
        update.message.reply_text(msg, parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /infoplayer command:')
        update.message.reply_text('Unexpected Shit happened!''No game in this list yet!', parse_mode='Markdown')


def gameliststring(gamelist):
    msg = ''
    for game in gamelist:
        msg += gamestring(game)
        msg += '\n'
    return msg


def gamestring(game):
    msg = '*' + game.title + '* \n'
    msg += '    Length: ' + str(game.type.name) + '\n'
    msg += '    Easy Mode: ' + game.easy + '\n'
    msg += '    Hard Mode: ' + game.hard + '\n'
    msg += '    Challenge Mode: ' + game.challenge + '\n'
    msg += '    Comment: ' + game.comment + '\n'
    return msg


def gameadditionalstring(game):
    msg = '    Easy Players: '
    for player in game.get_easyplayers():
        msg += player.name + ', '
    msg += '\n    Hard Players: '
    for player in game.get_hardplayers():
        msg += player.name + ', '
    msg += '\n    Challenge Players: '
    for player in game.get_challengeplayers():
        msg += player.name + ', '
    msg += '\n'
    return msg


# /easy 'game_title' command
def easy(update, context):
    """Register game finished at easy difficulty"""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        game_title = update.message['text'].replace('/easy ', '')
        player_id = update.message['from_user']['id']
        update.message.reply_text(season.easy_finished(game_title, player_id), parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /easy command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /hard 'game_title' command
def hard(update, context):
    """Register game finished at hard difficulty"""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        game_title = update.message['text'].replace('/hard ', '')
        player_id = update.message['from_user']['id']
        update.message.reply_text(season.hard_finished(game_title, player_id), parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /hard command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /challenge 'game_title' command
def challenge(update, context):
    """Register game challenge completed"""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        game_title = update.message['text'].replace('/challenge ', '')
        player_id = update.message['from_user']['id']
        update.message.reply_text(season.challenge_completed(game_title, player_id), parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /challenge command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /nextmonth ADMIN-command
def nextmonth(update, context):
    """Manages the end of a month and the beginning of the new one."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    try:
        if is_admin(int(update.message['from_user']['id'])):
            if nextmonth_check:
                season.next_month()
                update.message.reply_text('The month of ' + str(season.current_month.name) + ' has begun!', parse_mode='Markdown')
                nextmonth_check = False
            else:
                nextmonth_check = True
                update.message.reply_text('Are you sure? The Season will pass to the next month and shifting all games'
                                          'accordingly. Type again the command if you know dafuq you doin.', parse_mode='Markdown')
        else:
            update.message.reply_text('Not even an admin! weirdChamp', parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /nextmonth command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /bestscreenshot 'game_title-player_name' ADMIN-command
def bestscreenshot(update, context):
    """Elects the best screenshot for the game."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    nextmonth_check = False
    newseason_check = False
    try:
        if is_admin(int(update.message['from_user']['id'])):
            message = update.message['text'].replace('/bestscreenshot ', '').split('-')
            game_title = message[0]
            player_name = message[1]
            update.message.reply_text(season.screenshot_badge(game_title, player_name), parse_mode='Markdown')
        else:
            update.message.reply_text('Not even an admin! weirdChamp', parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /bestscreenshot command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /revokescreenshot 'game_title-player_name' ADMIN-command
def revokescreenshot(update, context):
    """Revoke the best screenshot for the game."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    nextmonth_check = False
    newseason_check = False
    try:
        if is_admin(int(update.message['from_user']['id'])):
            message = update.message['text'].replace('/revokescreenshot ', '').split('-')
            game_title = message[0]
            player_name = message[1]
            update.message.reply_text(season.revoke_screenshotbadge(game_title, player_name), parse_mode='Markdown')
        else:
            update.message.reply_text('Not even an admin! weirdChamp', parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /revokescreenshot command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /revokeshithead 'game_title-player_name' ADMIN-command
def revokeshithead(update, context):
    """Revoke Shithead badge."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    nextmonth_check = False
    newseason_check = False
    try:
        if is_admin(int(update.message['from_user']['id'])):
            message = update.message['text'].replace('/revokeshithead ', '').split('-')
            game_title = message[0]
            player_name = message[1]
            update.message.reply_text(season.revoke_shitheadbadge(game_title, player_name), parse_mode='Markdown')
        else:
            update.message.reply_text('Not even an admin! weirdChamp', parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /revokeshithead command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /leaderboard command
def leaderboard(update, context):
    """Returns the current Leaderboard."""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    nextmonth_check = False
    newseason_check = False
    try:
        player_list = season.get_leaderboard()
        msg = '*Leaderboard*\n'
        position = 0
        for player in player_list:
            position += 1
            msg += str(position) + '° ' + player.name + '(' + str(player.points) + ') \n'
        update.message.reply_text(msg, parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /bestscreenshot command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /backup ADMIN-command
def backup(update, context):
    """Save a complete Backup of the current Season"""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        if is_admin(update.message['from_user']['id']):
            update.message.reply_text(season.backup(), parse_mode='Markdown')
        else:
            update.message.reply_text('Not even an admin! weirdChamp', parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /backup command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /backuplist ADMIN-command
def backuplist(update, context):
    """Return the list of backups done, with their ids"""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    loadbackup_check = False
    newseason_check = False
    nextmonth_check = False
    try:
        if is_admin(update.message['from_user']['id']):
            backups = os.listdir('./backups')
            msg = ''
            for i, backup in enumerate(backups):
                msg += str(i) + '. ' + backup + '\n'
            update.message.reply_text(msg, parse_mode='Markdown')
        else:
            update.message.reply_text('Not even an admin! weirdChamp', parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /backuplist command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# /loadbackup 'backupid' ADMIN-command
def loadbackup(update, context):
    """Load backup and overwrite current season"""
    logger.info(update)
    global loadbackup_check, nextmonth_check, newseason_check, season
    newseason_check = False
    nextmonth_check = False
    try:
        if is_admin(int(update.message['from_user']['id'])):
            if loadbackup_check:
                backup_id = int(update.message['text'].replace('/loadbackup', ''))
                file = open('./backups/' + os.listdir('./backups')[backup_id], 'r')
                backup = file.read()
                season = jsonpickle.decode(backup)
                update.message.reply_text('Backup has been restored!', parse_mode='Markdown')
                loadbackup_check = False
            else:
                loadbackup_check = True
                update.message.reply_text('Are you sure? Loading the chosen backup will overwrite the current season '
                                          'state. Type again the command to confirm the operation.', parse_mode='Markdown')
        else:
            update.message.reply_text('Not even an admin! weirdChamp', parse_mode='Markdown')
    except Exception:
        logger.exception('An Exception occurred executing /loadbackup command:')
        update.message.reply_text('Unexpected Shit happened!', parse_mode='Markdown')


# Unrecognized command
def notfound(update, context):
    """Command not recognized"""
    update.message.reply_text('This command does not exist. COJO, neanche scrivere.', parse_mode='Markdown')


def is_admin(user_id):
    with open('./admins/admins.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if user_id == int(row[1]):
                return True
        return False


def main():
    # Create Updater (and thus the bot)
    updater = Updater("1323151706:AAFh-IXy2SHJm7cJjb1fV_JYnrlYHs02pj0")
    dp = updater.dispatcher

    # Add Handlers for the Commands
    dp.add_handler(CommandHandler("help", helpcommand))
    dp.add_handler(CommandHandler("adminhelp", adminhelpcommand))
    dp.add_handler(CommandHandler("newseason", newseason))
    dp.add_handler(CommandHandler("enroll", enroll))
    dp.add_handler(CommandHandler("addshort", addshort))
    dp.add_handler(CommandHandler("addmedium", addmedium))
    dp.add_handler(CommandHandler("addlong", addlong))
    dp.add_handler(CommandHandler("revokeeasy", revokeeasy))
    dp.add_handler(CommandHandler("revokehard", revokehard))
    dp.add_handler(CommandHandler("revokechallenge", revokechallenge))
    dp.add_handler(CommandHandler("forceeasy", forceeasy))
    dp.add_handler(CommandHandler("forcehard", forcehard))
    dp.add_handler(CommandHandler("forcechallenge", forcechallenge))
    dp.add_handler(CommandHandler("resetshort", resetshort))
    dp.add_handler(CommandHandler("resetmedium", resetmedium))
    dp.add_handler(CommandHandler("resetlong", resetlong))
    dp.add_handler(CommandHandler("resetshort", resetshort_admin))
    dp.add_handler(CommandHandler("resetmedium", resetmedium_admin))
    dp.add_handler(CommandHandler("resetlong", resetlong_admin))
    dp.add_handler(CommandHandler("addeasy", addeasy))
    dp.add_handler(CommandHandler("addhard", addhard))
    dp.add_handler(CommandHandler("addchallenge", addchallenge))
    dp.add_handler(CommandHandler("addcomment", addcomment))
    dp.add_handler(CommandHandler("list", list))
    dp.add_handler(CommandHandler("vote", vote))
    dp.add_handler(CommandHandler("winner", winner))
    dp.add_handler(CommandHandler("activelist", activelist))
    dp.add_handler(CommandHandler("proposelist", proposelist))
    dp.add_handler(CommandHandler("pastlist", pastlist))
    dp.add_handler(CommandHandler("infogame", infogame))
    dp.add_handler(CommandHandler("infoplayer", infoplayer))
    dp.add_handler(CommandHandler("easy", easy))
    dp.add_handler(CommandHandler("hard", hard))
    dp.add_handler(CommandHandler("challenge", challenge))
    dp.add_handler(CommandHandler("nextmonth", nextmonth))
    dp.add_handler(CommandHandler("bestscreenshot", bestscreenshot))
    dp.add_handler(CommandHandler("revokescreenshot", revokescreenshot))
    dp.add_handler(CommandHandler("revokeshithead", revokeshithead))
    dp.add_handler(CommandHandler("leaderboard", leaderboard))
    dp.add_handler(CommandHandler("backup", backup))
    dp.add_handler(CommandHandler("backuplist", backuplist))
    dp.add_handler(CommandHandler("loadbackup", loadbackup))

    # Add Handler for messages not recognized
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, notfound))

    # Start the Bot Polling
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
