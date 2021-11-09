from urllib.request import urlopen
from pydash import get as lget
from conf import BASE_URL, quote_endpoint
from keys import API_KEY
import time
import json

NO_UPDATE_MSG = 'No significant different in percentage'


def areBotConfigurationsValids(ticker, seconds):
    if ticker is None or seconds is None:
        return False
    if ticker == '':
        return False
    if seconds < 10 or seconds > 10000:
        return False
    return True
    
def constructURL(base,endpoint,key, query):
    return '{}{}/{}?apikey={}'.format(base,endpoint,query,key)

#Query financialmodelingprep API to get the quote of the symbol
def getQuote(symbol):
    print('Get info of symbol ' + symbol)
    url = constructURL(BASE_URL,quote_endpoint,API_KEY,symbol)
    response = urlopen(url)
    data = response.read().decode("utf-8")
    parsed_response = json.loads(data)
    return lget(parsed_response, [0], None)

#Compute the difference between the current_quote and quotes_list[index]
def computeDifference(quotes_list, current_quote, index=0):
    previous_quote = quotes_list[index]
    abs_diff = abs(current_quote - previous_quote)
    return round(( abs_diff * 100 )/previous_quote)

#Get the quote of the symbol and compute the difference of the last 5 quotes
def manage_stack(logger, quotes_list, symbol):
    numPastQuotes = len(quotes_list)
    currentQuote = getQuote(symbol)
    currentPrice = lget(currentQuote, ['price'], None)
    if numPastQuotes>=1 and currentPrice:
        # compute difference only on the last 5 elems
        for i in range(max(numPastQuotes-5, 0),numPastQuotes):
            percentage_diff=computeDifference(quotes_list, currentPrice, i)
            print('********Differance in percentage********', percentage_diff)
        quotes_list.append(currentPrice)
    logger.debug('Manage Stack, quote list:', quotes_list)
    return quotes_list



