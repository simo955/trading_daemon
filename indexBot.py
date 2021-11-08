#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to send timed Telegram messages.
This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import time

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext


from conf import BOT_TOKEN,BOT_NAME
from utils import manage_stack
from conf import STARTING_SYMBOL, SLEEP_SECONDS

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: _) -> None:
    """Sends explanation on how to use the bot."""
    update.message.reply_text(
        'Hi welcom to {} {}! Now it ll start a polling for CCL news'.format(BOT_NAME,isConfigured),
         quote=True
         )

def start_deamon(update: Update, context: _) -> None:
    global isConfigured
    if not isConfigured:
        update.message.reply_text(
            'First: configure your deamon with the /configure_bot command',
            quote=True
        )
        return 
    quotes_list=[]
    update.message.reply_text('Daemon is starting')
    while True:
        logger.debug('Still running')
        res = manage_stack(quotes_list,STARTING_SYMBOL)
        update.message.reply_text(res)
        time.sleep(SLEEP_SECONDS)

#Function used to to set all the configurations required for the Deamon run
def configure_bot(update: Update, context: _) -> None:
    global isConfigured
    isConfigured=True

def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("configure_bot", configure_bot))
    dispatcher.add_handler(CommandHandler("start_deamon", start_deamon))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    isConfigured = False
    main()