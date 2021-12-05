from utils.conf import STARTING_SYMBOL, SLEEP_SECONDS
from getQuotes import getRealTimeQuote

# Get average of a list
def avg(lst):
    return sum(lst) / len(lst)

def constructURL(base,endpoint,key, query):
    return '{}{}/{}?apikey={}'.format(base,endpoint,query,key)

def areBotConfigurationsValids(symbol, seconds):
    if symbol is None or seconds is None:
        return False
    if symbol == '':
        return False
    if seconds < 60 or seconds > 10000:
        return False
    quote = getRealTimeQuote(symbol)
    if quote is None:
        return False
    return True

def loadContextConfigurations(context):
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
            return symbol, seconds
    context.user_data.update(
        {
        'starting_symbol': STARTING_SYMBOL,
        'sleep_seconds': SLEEP_SECONDS
        }
    )
    return STARTING_SYMBOL, SLEEP_SECONDS
    
def setContextFinishConfigurations(context):
    context.user_data.update(
        {
        'isRunning':False,
        'stopRun':False,
        'starting_symbol': STARTING_SYMBOL,
        'sleep_seconds': SLEEP_SECONDS
        }
    )  


