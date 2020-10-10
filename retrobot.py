from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from season import Season
import logging

# Logger Settings
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Current Season Variables
season = Season(9)


# /newseason command
def newseason(update, context):
    """Create a New Season."""
    logger.info(update)
    message = update['message'].__dict__
    month = message['text'].replace('/newseason', '')
    global season
    season = Season(int(month))
    update.message.reply_text('A new Season has been created!')


# /enroll command
def enroll(update, context):
    """Enroll a new Player."""
    logger.info(update)
    message = update['message'].__dict__
    player_id = message['from_user']['id']
    player_name = message['from_user']['username']
    global season
    update.message.reply_text(season.add_player(player_id, player_name))


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text('This command does not exist.')


def main():
    """Start the bot."""
    updater = Updater("1323151706:AAFh-IXy2SHJm7cJjb1fV_JYnrlYHs02pj0")
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("newseason", newseason))
    dp.add_handler(CommandHandler("enroll", enroll))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
