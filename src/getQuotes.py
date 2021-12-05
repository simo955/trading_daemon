import json
import os
from urllib.request import urlopen
from pydash import get as lget
   
from utils.conf import BASE_URL, PERCENTAGE_DIFF_TRESHOLD, NO_UPDATE_MSG,UPDATE_MSG, quote_endpoint

from keys import API_KEY

#Get the quote of the symbol and compute the difference of the last 5 quotes
def manage_stack(updaterService, quotes_list, symbol):
    updaterService.log('Managing stack, current quote_list {}',[quotes_list])
    currentQuote = getRealTimeQuote(symbol)
    currentPrice = lget(currentQuote, ['price'], None)
    if currentQuote is None or currentPrice is None:
        return 'Error', quotes_list
    diff = computeDifference(updaterService, quotes_list,currentPrice)
    updaterService.log('Result difference {}',diff)
    quotes_list.append(currentPrice)
    if diff >=PERCENTAGE_DIFF_TRESHOLD:
        return UPDATE_MSG, quotes_list
    return NO_UPDATE_MSG, quotes_list

#Compute the difference between the last 5 quotes and current quote
def computeDifference(updaterService, quotes_list, current_quote):
    updaterService.log('Computing the percentage difference of avg({}) and {}',[quotes_list, current_quote])
    numberPastQuotes = len(quotes_list)
    if numberPastQuotes==0:
        return 0
    subQuotesToWatch = quotes_list[max(0,numberPastQuotes-5):]
    pastAvg = avg(subQuotesToWatch)
    if pastAvg ==0:
        return 0
    return int(abs(current_quote-pastAvg)*100/pastAvg)

#Query financialmodelingprep APIs to get the quote of the symbol
def getRealTimeQuote(symbol):
    url = constructURL(BASE_URL,quote_endpoint,API_KEY,symbol)
    response = urlopen(url)
    data = response.read().decode("utf-8")
    parsed_response = json.loads(data)
    return lget(parsed_response, [0], None)

def avg(array):
    return sum(array) / len(array)

def constructURL(base,endpoint,key, query):
    return '{}{}/{}?apikey={}'.format(base,endpoint,query,key)
    


