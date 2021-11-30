from avaiableSymbols import isSymbolInList

def areBotConfigurationsValids(symbol, seconds):
    if symbol is None or seconds is None:
        return False
    if symbol == '':
        return False
    if seconds < 60 or seconds > 10000:
        return False
    return isSymbolInList(symbol)


# Get average of a list
def avg(lst):
    return sum(lst) / len(lst)

def constructURL(base,endpoint,key, query):
    return '{}{}/{}?apikey={}'.format(base,endpoint,query,key)

def formatMessage(text, argsList=[]):
    return text.format(*argsList)

