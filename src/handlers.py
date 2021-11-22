import time
import logging

from telegram import Update
from telegram.ext import CallbackContext
from getQuotes import manage_stack
from utils import areBotConfigurationsValids

from conf import STARTING_SYMBOL, SLEEP_SECONDS,UPDATE_MSG,WIKI_URL
from conf import bot_configuration_cmd

def startHandler(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(
        'Hi welcom! First: configure your deamon using: /{} <TICKER> <POLLING_SECONDS>'.format(bot_configuration_cmd),
         quote=True
         )

def helpHandler(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(
        'Want to know more about Trading-Deamon? Click <a href="{}">here</a>'.format(WIKI_URL),
        parse_mode='HTML'
        )

def start_deamonHandler(update: Update, _: CallbackContext) -> None:
    global isConfigured

    # Enable logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    if not isConfigured:
        update.message.reply_text(
            'First: configure your deamon using: /{} <TICKER> <POLLING_SECONDS>'.format(bot_configuration_cmd),
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
    update.message.reply_text('Daemon is stopping. {} prices over the deamon alive period: {}'.format(STARTING_SYMBOL, quotes_list))


#Function used to to set all the configurations required for running the deamon
def configure_botHandler(update: Update, context: CallbackContext) -> None:
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

def echoWrongCmdHandler(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text('Wrong command used')
