import json
import os
from urllib.request import urlopen
from pydash import get as lget
   
from conf import BASE_URL, PERCENTAGE_DIFF_TRESHOLD, NO_UPDATE_MSG,UPDATE_MSG, quote_endpoint
from utils import constructURL,  avg
API_KEY = os.environ['API_KEY']

#Query financialmodelingprep API to get the quote of the symbol
def getRealTimeQuote(logger,symbol):
    logger.debug('Getting quote of symbol {}'.format(symbol))
    url = constructURL(BASE_URL,quote_endpoint,API_KEY,symbol)
    response = urlopen(url)
    data = response.read().decode("utf-8")
    parsed_response = json.loads(data)
    return lget(parsed_response, [0], None)

#Compute the difference between the last 5 quotes and current quote
def computeDifference(logger, quotes_list, current_quote):
    logger.debug('Computing the percentage difference of avg({}) and {}'.format(quotes_list, current_quote))
    numberPastQuotes = len(quotes_list)
    if numberPastQuotes==0:
        return 0
    subQuotesToWatch = quotes_list[max(0,numberPastQuotes-5):]
    pastAvg = avg(subQuotesToWatch)
    if pastAvg ==0:
        return 0
    return int(abs(current_quote-pastAvg)*100/pastAvg)
    
#Get the quote of the symbol and compute the difference of the last 5 quotes
def manage_stack(logger, quotes_list, symbol):
    logger.debug('Managing stack, current quote_list {}'.format(quotes_list))
    currentQuote = getRealTimeQuote(logger, symbol)
    currentPrice = lget(currentQuote, ['price'], None)
    if currentQuote is None or currentPrice is None:
        return 'Error'
    diff = computeDifference(logger, quotes_list,currentPrice)
    logger.debug('Result difference {}'.format(diff))
    quotes_list.append(currentPrice)
    if diff >=PERCENTAGE_DIFF_TRESHOLD:
        return UPDATE_MSG
    return NO_UPDATE_MSG


