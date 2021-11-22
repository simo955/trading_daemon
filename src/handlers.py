import time
import logging

from telegram import Update
from telegram.ext import CallbackContext
from getQuotes import manage_stack
from utils import areBotConfigurationsValids, formatMessage

from conf import STARTING_SYMBOL, SLEEP_SECONDS,UPDATE_MSG,WIKI_URL
from conf import bot_configuration_cmd

from text import WELCOME_MSG, HELP_MSG, WRONG_COMMAND_MSG, KO_CONFIGURATION_MSG,OK_CONFIGURATION_MSG, FINISH_MSG

runningFlag= True
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def startHandler(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(formatMessage(WELCOME_MSG, bot_configuration_cmd),quote=True)

def stopHandler(update: Update, _: CallbackContext) -> None:
    global runningFlag
    runningFlag=False


def helpHandler(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(formatMessage(HELP_MSG, WIKI_URL),parse_mode='HTML')

def echoWrongCmdHandler(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(WRONG_COMMAND_MSG)

#Function used to to set all the configurations required for running the deamon
def configure_botHandler(update: Update, context: CallbackContext) -> None:
    global isConfigured
    global STARTING_SYMBOL
    global SLEEP_SECONDS
    defaultMessage = KO_CONFIGURATION_MSG.format(STARTING_SYMBOL,SLEEP_SECONDS)
    
    isConfigured=True
    if context and isinstance(context.args, list) and len(context.args)>=2:
        ticker = context.args[0]
        seconds = int(context.args[1])
        if areBotConfigurationsValids(ticker, seconds):
            STARTING_SYMBOL=ticker
            SLEEP_SECONDS=seconds
            update.message.reply_text(OK_CONFIGURATION_MSG,quote=True)
            return

    update.message.reply_text(defaultMessage,quote=True)

def start_deamonHandler(update: Update, _: CallbackContext) -> None:
    global isConfigured
    global runningFlag

    quotes_list=[]
    update.message.reply_text('Daemon is going background')
    while runningFlag:
        logger.debug('Still running')
        msg = manage_stack(logger, quotes_list, STARTING_SYMBOL)
        logger.info('Ending iteration. MSG={}'.format(msg))
        if msg==UPDATE_MSG:
            update.message.reply_text(msg)
        time.sleep(SLEEP_SECONDS)
    update.message.reply_text(formatMessage(FINISH_MSG, [STARTING_SYMBOL, quotes_list]),parse_mode='HTML')
