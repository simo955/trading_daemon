import logging
import time

from telegram import Update
from telegram.ext import CallbackContext
from getQuotes import manage_stack
from utils import areBotConfigurationsValids, formatMessage

from conf import STARTING_SYMBOL, SLEEP_SECONDS,UPDATE_MSG,WIKI_URL, MAXIMUM_ITERATIONS
from conf import bot_configuration_cmd

from text import WELCOME_MSG, HELP_MSG, WRONG_COMMAND_MSG,OK_CONFIGURATION_MSG, START_MSG, FINISH_MSG, ALREADY_RUNNING_MSG,STOPPING_MSG,STOPPING_NONEEDED__MSG


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def startHandler(update: Update, context: CallbackContext) -> None:
    context.user_data.update(
        {
        'alreadyRunning':False,
        'stopRun':False,
        'starting_symbol': STARTING_SYMBOL,
        'sleep_seconds': SLEEP_SECONDS
        }
    )
    update.message.reply_text(formatMessage(WELCOME_MSG, bot_configuration_cmd),quote=True)

def stopHandler(update: Update, context: CallbackContext) -> None:
    alreadyRunning = context.user_data.get('alreadyRunning', False)
    stopRun = context.user_data.get('stopRun', False)
    if alreadyRunning and not stopRun:
        context.user_data.update({'stopRun':True})
        update.message.reply_text(formatMessage(STOPPING_MSG))
        return
    update.message.reply_text(formatMessage(STOPPING_NONEEDED__MSG))

def helpHandler(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(formatMessage(HELP_MSG, WIKI_URL),parse_mode='HTML')

def echoWrongCmdHandler(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(WRONG_COMMAND_MSG)

def start_deamonHandler(update: Update, context: CallbackContext) -> None:
    alreadyRunning = context.user_data.get('alreadyRunning', False)

    if alreadyRunning:
        update.message.reply_text(ALREADY_RUNNING_MSG)
        return
    
    # Load configuration
    if context and isinstance(context.args, list) and len(context.args)>=2:
        symbol = context.args[0]
        seconds = int(context.args[1])
        if areBotConfigurationsValids(symbol, seconds):
            context.user_data.update(
                {
                'starting_symbol': symbol,
                'sleep_seconds': seconds
                }
            )
            update.message.reply_text(OK_CONFIGURATION_MSG,quote=True)

    context.user_data.update({'alreadyRunning':True})
    starting_symbol = context.user_data.get('starting_symbol',STARTING_SYMBOL)
    sleep_seconds = context.user_data.get('sleep_seconds',SLEEP_SECONDS)
    quotes_list=[]
    iterationCounter = 0
    update.message.reply_text(formatMessage(START_MSG,starting_symbol, sleep_seconds))
    while context.user_data.get('stopRun', False) and iterationCounter<MAXIMUM_ITERATIONS:
        msg, quotes_list = manage_stack(logger, quotes_list, starting_symbol)
        logger.info('Ending iteration. MSG={}'.format(msg))
        if msg==UPDATE_MSG or msg=='Error':
            update.message.reply_text(msg)
            context.user_data.update({'alreadyRunning':False})  
            context.user_data.update({'stopRun':False})   
            return
        iterationCounter+=1
        time.sleep(sleep_seconds)
    context.user_data.update({'alreadyRunning':False})  
    context.user_data.update({'stopRun':False})   
    update.message.reply_text(formatMessage(FINISH_MSG, [starting_symbol, quotes_list]))

