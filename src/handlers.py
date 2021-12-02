import time

from telegram.ext import CallbackContext
from telegram import Update

from getQuotes import manage_stack
from utils.botUtils import loadContextConfigurations, setContextFinishConfigurations

from utils.conf import bot_configuration_cmd, STARTING_SYMBOL, SLEEP_SECONDS,UPDATE_MSG,WIKI_URL, MAXIMUM_ITERATIONS
from utils.text import WELCOME_MSG, HELP_MSG, WRONG_COMMAND_MSG, START_MSG, FINISH_MSG, ALREADY_RUNNING_MSG,STOPPING_MSG,STOPPING_NONEEDED__MSG

from utils.myUpdaterService import myUpdaterService

updaterService = myUpdaterService()

def startHandler(update: Update, context: CallbackContext) -> None:
    context.user_data.update(
        {
        'isRunning':False,
        'stopRun':False,
        'starting_symbol': STARTING_SYMBOL,
        'sleep_seconds': SLEEP_SECONDS
        }
    )
    updaterService.sendMessage(update, WELCOME_MSG, bot_configuration_cmd)

def stopHandler(update: Update, context: CallbackContext) -> None:
    isRunning = context.user_data.get('isRunning', False)
    stopRun = context.user_data.get('stopRun', False)
    if isRunning and not stopRun:
        context.user_data.update({'stopRun':True})
        updaterService.sendMessage(update, STOPPING_MSG)
        return
    updaterService.sendMessage(update, STOPPING_NONEEDED__MSG)

def helpHandler(update: Update, _: CallbackContext) -> None:
    updaterService.sendMessage(update, HELP_MSG, WIKI_URL, {'parse_mode':'HTML'})

def echoWrongCmdHandler(update: Update, _: CallbackContext) -> None:
    updaterService.sendMessage(update, WRONG_COMMAND_MSG)

def debugHandler(update: Update, context: CallbackContext) -> None:
    updaterService.sendMessage(update, '{}', [context.user_data])

def start_deamonHandler(update: Update, context: CallbackContext) -> None:
    isRunning = context.user_data.get('isRunning', False)

    if isRunning:
        updaterService.sendMessage(update, ALREADY_RUNNING_MSG)
        return
    
    # Load configuration
    starting_symbol,sleep_seconds = loadContextConfigurations(context)

    context.user_data.update({'isRunning':True})
    quotes_list=[]
    iterationCounter = 0
    
    updaterService.sendMessage(update, START_MSG, [starting_symbol, sleep_seconds])
    while context.user_data.get('stopRun', False)==False and iterationCounter<MAXIMUM_ITERATIONS:
        msg, quotes_list = manage_stack(updaterService, quotes_list, starting_symbol)
        updaterService.log('Ending iteration. MSG={}', msg)
        if msg==UPDATE_MSG or msg=='Error':
            updaterService.sendMessage(update, msg)
            updaterService.sendMessage(update,FINISH_MSG,[starting_symbol, quotes_list])             
            setContextFinishConfigurations(context) 
            return
        iterationCounter+=1
        time.sleep(sleep_seconds)

    setContextFinishConfigurations(context) 
    updaterService.sendMessage(update, FINISH_MSG, [starting_symbol, quotes_list])