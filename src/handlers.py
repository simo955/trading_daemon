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
        'run':True,
        'starting_symbol': STARTING_SYMBOL,
        'sleep_seconds': SLEEP_SECONDS
        }
    )
    update.message.reply_text(formatMessage(WELCOME_MSG, bot_configuration_cmd),quote=True)

def stopHandler(update: Update, context: CallbackContext) -> None:
    logger.info('Stopping Deamon iteration')
    alreadyRunning = context.user_data.get('alreadyRunning', False)
    run = context.user_data.get('run', True)
    if alreadyRunning and run:
        context.user_data.update({'run':False})
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
        ticker = context.args[0]
        seconds = int(context.args[1])
        if areBotConfigurationsValids(ticker, seconds):
            context.user_data.update(
                {
                'starting_symbol': ticker,
                'sleep_seconds': seconds
                }
            )
            update.message.reply_text(OK_CONFIGURATION_MSG,quote=True)

    update.message.reply_text(START_MSG)

    context.user_data.update({'alreadyRunning':True})
    starting_symbol = context.user_data.get('starting_symbol')
    sleep_seconds = context.user_data.get('sleep_seconds')
    quotes_list=[]
    iterationCounter = 0
    while context.user_data.get('run', True) and iterationCounter<MAXIMUM_ITERATIONS:
        logger.info('Still running')
        msg, quotes_list = manage_stack(logger, quotes_list, starting_symbol)
        logger.info('Ending iteration. MSG={}'.format(msg))
        if msg==UPDATE_MSG or msg=='Error':
            update.message.reply_text(msg)
            context.user_data.update({'alreadyRunning':False})  
            context.user_data.update({'run':True})   
            return
        iterationCounter+=1
        time.sleep(sleep_seconds)
    context.user_data.update({'alreadyRunning':False})  
    context.user_data.update({'run':True})   
    update.message.reply_text(formatMessage(FINISH_MSG, [starting_symbol, quotes_list]))

