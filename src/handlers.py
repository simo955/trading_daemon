import time

from telegram.ext import CallbackContext
from telegram import Update

from getQuotes import manage_stack
from utils.generalUtils import formatMessage, loadContextConfigurations, setContextFinishConfigurations

from utils.conf import bot_configuration_cmd, STARTING_SYMBOL, SLEEP_SECONDS,UPDATE_MSG,WIKI_URL, MAXIMUM_ITERATIONS
from utils.text import WELCOME_MSG, HELP_MSG, WRONG_COMMAND_MSG, START_MSG, FINISH_MSG, ALREADY_RUNNING_MSG,STOPPING_MSG,STOPPING_NONEEDED__MSG

from utils.myUpdater import myUpdate

def startHandler(update: myUpdate, context: CallbackContext) -> None:
    context.user_data.update(
        {
        'isRunning':False,
        'stopRun':False,
        'starting_symbol': STARTING_SYMBOL,
        'sleep_seconds': SLEEP_SECONDS
        }
    )
    update.sendMessageAndLog(WELCOME_MSG, bot_configuration_cmd)

def stopHandler(update: Update, context: CallbackContext) -> None:
    isRunning = context.user_data.get('isRunning', False)
    stopRun = context.user_data.get('stopRun', False)
    if isRunning and not stopRun:
        context.user_data.update({'stopRun':True})
        update.message.reply_text(formatMessage(STOPPING_MSG))
        return
    update.message.reply_text(formatMessage(STOPPING_NONEEDED__MSG))

def helpHandler(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(formatMessage(HELP_MSG, WIKI_URL),parse_mode='HTML')

def echoWrongCmdHandler(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(WRONG_COMMAND_MSG)

def start_deamonHandler(update: Update, context: CallbackContext) -> None:
    isRunning = context.user_data.get('isRunning', False)

    if isRunning:
        update.message.reply_text(ALREADY_RUNNING_MSG)
        return
    
    # Load configuration
    starting_symbol,sleep_seconds = loadContextConfigurations(context)

    context.user_data.update({'isRunning':True})
    quotes_list=[]
    iterationCounter = 0
    update.message.reply_text(formatMessage(START_MSG,[starting_symbol, sleep_seconds]))
    while not context.user_data.get('stopRun', False) and iterationCounter<MAXIMUM_ITERATIONS:
        msg, quotes_list = manage_stack(logger, quotes_list, starting_symbol)
        logger.info('Ending iteration. MSG={}'.format(msg))
        if msg==UPDATE_MSG or msg=='Error':
            update.message.reply_text(msg)
            setContextFinishConfigurations(context) 
            return
        iterationCounter+=1
        time.sleep(sleep_seconds)

    setContextFinishConfigurations(context) 
    update.message.reply_text(formatMessage(FINISH_MSG, [starting_symbol, quotes_list]))
