import time
import logging

from telegram import Update
from telegram.ext import CallbackContext
from getQuotes import manage_stack
from utils import areBotConfigurationsValids

from conf import STARTING_SYMBOL, SLEEP_SECONDS,UPDATE_MSG,WIKI_URL
from conf import bot_configuration_cmd

runningFlag= True
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def startHandler(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(
        'Hi welcom! First: configure your deamon using: <br> /{} <TICKER> <POLLING_SECONDS>'.format(bot_configuration_cmd),
         quote=True,
         parse_mode='HTML'
         )
def stopHandler(update: Update, _: CallbackContext) -> None:
    global runningFlag
    logger.info('aaaaaaaaa',runningFlag)
    runningFlag=False
    logger.info('bbbbbbbbbbb',runningFlag)


def helpHandler(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(
        'Want to know more about Trading-Deamon? Click <a href="{}">here</a>'.format(WIKI_URL),
        parse_mode='HTML'
        )

def start_deamonHandler(update: Update, _: CallbackContext) -> None:
    global isConfigured
    global runningFlag

    if not isConfigured:
        update.message.reply_text(
            'First: configure your deamon using: <br> /{} <TICKER> <POLLING_SECONDS>'.format(bot_configuration_cmd),
            parse_mode='HTML',
            quote=True
        )
        return 
    quotes_list=[]
    update.message.reply_text('Daemon is going background')
    while runningFlag:
        logger.debug('Still running')
        msg = manage_stack(logger, quotes_list, STARTING_SYMBOL)
        logger.info('Ending iteration. MSG={}'.format(msg))
        if msg==UPDATE_MSG:
            update.message.reply_text(msg)
        time.sleep(SLEEP_SECONDS)
    update.message.reply_text(
        'Daemon is stopping. <br> {} prices over the deamon alive period: {} <br> {} '.format(STARTING_SYMBOL, quotes_list),
        parse_mode='HTML',
)

#Function used to to set all the configurations required for running the deamon
def configure_botHandler(update: Update, context: CallbackContext) -> None:
    global isConfigured
    global STARTING_SYMBOL
    global SLEEP_SECONDS
    defaultMessage = 'Wrong parameters passed. The bot is now using default values. TICKER={}, SLEEP_SECONDS={}'.format(STARTING_SYMBOL,SLEEP_SECONDS)
    
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
