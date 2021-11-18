import logging
import time
import os

from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters,CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown

from getQuotes import manage_stack
from utils import areBotConfigurationsValids
from conf import STARTING_SYMBOL, SLEEP_SECONDS, BOT_NAME,UPDATE_MSG,WIKI_URL, bot_configuration_cmd, bot_start_deamong_cmd
from keys import BOT_TOKEN
PORT = int(os.environ.get('PORT', '8443'))

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def startCmd(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(
        'Hi welcom to {}! First: configure your deamon using: {} <TICKER> <POLLING_SECONDS>'.format(BOT_NAME,bot_configuration_cmd),
         quote=True
         )

def helpCmd(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(
        'Want to know more about Trading-Deamon? Click <a href="{}">here</a>'.format(WIKI_URL),
        parse_mode='HTML'
        )

def start_deamonCmd(update: Update, _: CallbackContext) -> None:
    global isConfigured
    if not isConfigured:
        update.message.reply_text(
            'First: configure your deamon using: {} <TICKER> <POLLING_SECONDS>'.format(bot_configuration_cmd),
            quote=True
        )
        return 
    quotes_list=[]
    update.message.reply_text('Daemon is starting')
    for i in range(0,5):
        logger.debug('Still running')
        msg = manage_stack(logger, quotes_list, STARTING_SYMBOL)
        logger.info('Ending iteration. MSG={}'.format(msg))
        if msg==UPDATE_MSG:
            update.message.reply_text(msg)
        time.sleep(SLEEP_SECONDS)

#Function used to to set all the configurations required for running the deamon
def configure_botCmd(update: Update, context: CallbackContext) -> None:
    global isConfigured
    global STARTING_SYMBOL
    global SLEEP_SECONDS
    defaultMessage = 'Wrong parameters passed. The bot is now using default values'
    
    isConfigured=True
    if context and isinstance(context.args, list) and len(context.args)>=2:
        ticker = context.args[0]
        seconds = int(context.args[1])
        if areBotConfigurationsValids(ticker, seconds):
            STARTING_SYMBOL=ticker
            SLEEP_SECONDS=seconds
            update.message.reply_text('Bot new configurations were updated correctly',quote=True)
            return

    update.message.reply_text(defaultMessage,quote=True)

def echoWrongCommand(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text('Wrong command used')

def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", startCmd))
    dispatcher.add_handler(CommandHandler("help", helpCmd))
    dispatcher.add_handler(CommandHandler(bot_configuration_cmd, configure_botCmd))
    dispatcher.add_handler(CommandHandler(bot_start_deamong_cmd, start_deamonCmd))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echoWrongCommand))

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=BOT_TOKEN,
                        webhook_url="https://tradingdeamon.herokuapp.com/" + BOT_TOKEN)
    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    isConfigured = False
    main()