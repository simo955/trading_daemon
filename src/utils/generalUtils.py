# Get average of a list
def avg(lst):
    return sum(lst) / len(lst)

def constructURL(base,endpoint,key, query):
    return '{}{}/{}?apikey={}'.format(base,endpoint,query,key)

def formatMessage(text, argsList=[]):
    if isinstance(argsList, list):
        return text.format(*argsList)
    else:
        return text.format(argsList)
