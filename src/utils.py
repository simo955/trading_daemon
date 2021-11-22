def areBotConfigurationsValids(ticker, seconds):
    if ticker is None or seconds is None:
        return False
    if ticker == '':
        return False
    if seconds < 60 or seconds > 10000:
        return False
    return True

# Get average of a list
def avg(lst):
    return sum(lst) / len(lst)

def constructURL(base,endpoint,key, query):
    return '{}{}/{}?apikey={}'.format(base,endpoint,query,key)

def formatMessage(text, args):
    return text.format(args)