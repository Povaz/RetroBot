from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from season import Season
import jsonpickle
import logging
import json
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


# /newseason ADMIN-command
def newseason(update, context):
    """Create a New Season."""
    logger.info(update)
    try:
        if is_admin(update.message['from_user']['id']):
            month = update.message['text'].replace('/newseason', '')
            global season
            season = Season(int(month))
            update.message.reply_text('A new Season has been created!')
        else:
            update.message.reply_text('Not even an admin! weirdChamp')
    except Exception:
        logger.exception('An Exception occurred executing /newseason command:')
        update.message.reply_text('Unexpected Shit happened!')


# /enroll command
def enroll(update, context):
    """Enroll a new Player."""
    logger.info(update)
    try:
        player_id = update.message['from_user']['id']
        player_name = update.message['from_user']['username']
        global season
        update.message.reply_text(season.add_player(int(player_id), player_name))
    except Exception:
        logger.exception('An Exception occurred executing /enroll command:')
        update.message.reply_text('Unexpected Shit happened!')

        update.message.reply_text('Unexpected Shit happened!')


# /addshort 'game_title' command
def addshort(update, context):
    """Propose a Short Game"""
    logger.info(update)
    try:
        player_id = update.message['from_user']['id']
        game_title = update.message['text'].replace('/addshort ', '')
        global season
        update.message.reply_text(season.add_shortgame(game_title, int(player_id)))
    except Exception:
        logger.exception('An Exception occurred executing /addshort command:')
        update.message.reply_text('Unexpected Shit happened!')


# /addmedium 'game_title' command
def addmedium(update, context):
    """Propose a Medium Game"""
    logger.info(update)
    try:
        player_id = update.message['from_user']['id']
        game_title = update.message['text'].replace('/addmedium ', '')
        global season
        update.message.reply_text(season.add_mediumgame(game_title, int(player_id)))
    except Exception:
        logger.exception('An Exception occurred executing /addmedium command:')
        update.message.reply_text('Unexpected Shit happened!')


# /addlong 'game_title' command
def addlong(update, context):
    """Propose a Long Game"""
    logger.info(update)
    try:
        player_id = update.message['from_user']['id']
        game_title = update.message['text'].replace('/addlong ', '')
        global season
        update.message.reply_text(season.add_longgame(game_title, int(player_id)))
    except Exception:
        logger.exception('An Exception occurred executing /addlong command:')
        update.message.reply_text('Unexpected Shit happened!')


# /backup ADMIN-command
def backup(update, context):
    """Save a complete Backup of the current Season"""
    logger.info(update)
    try:
        if is_admin(update.message['from_user']['id']):
            global season
            update.message.reply_text(season.backup())
        else:
            update.message.reply_text('Not even an admin! weirdChamp')
    except Exception:
        logger.exception('An Exception occurred executing /backup command:')
        update.message.reply_text('Unexpected Shit happened!')


# /backuplist ADMIN-command
def backuplist(update, context):
    """Return the list of backups done, with their ids"""
    logger.info(update)
    try:
        if is_admin(update.message['from_user']['id']):
            backups = os.listdir('./backups')
            msg = ''
            for i, backup in enumerate(backups):
                msg += str(i) + '. ' + backup + '\n'
            global season
            update.message.reply_text(msg)
        else:
            update.message.reply_text('Not even an admin! weirdChamp')
    except Exception:
        logger.exception('An Exception occurred executing /backuplist command:')
        update.message.reply_text('Unexpected Shit happened!')


# /loadbackup 'backupid' ADMIN-command
def loadbackup(update, context):
    """Load backup and overwrite current season"""
    logger.info(update)
    try:
        if is_admin(int(update.message['from_user']['id'])):
            backup_id = int(update.message['text'].replace('/loadbackup', ''))
            file = open('./backups/' + os.listdir('./backups')[backup_id], 'r')
            backup = file.read()
            global season
            season = jsonpickle.decode(backup)
            update.message.reply_text('Backup has been restored!')
        else:
            update.message.reply_text('Not even an admin! weirdChamp')
    except Exception:
        logger.exception('An Exception occurred executing /loadbackup command:')
        update.message.reply_text('Unexpected Shit happened!')


# Unrecognized command
def notfound(update, context):
    """Command not recognized"""
    update.message.reply_text('This command does not exist.')


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
    dp.add_handler(CommandHandler("newseason", newseason))
    dp.add_handler(CommandHandler("enroll", enroll))
    dp.add_handler(CommandHandler("backup", backup))
    dp.add_handler(CommandHandler("backuplist", backuplist))
    dp.add_handler(CommandHandler("loadbackup", loadbackup))
    dp.add_handler(CommandHandler("addshort", addshort))
    dp.add_handler(CommandHandler("addmedium", addmedium))
    dp.add_handler(CommandHandler("addlong", addlong))

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
