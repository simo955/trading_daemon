from urllib.request import urlopen
from pydash import get as lget
import json
    
from conf import BASE_URL, PERCENTAGE_DIFF_TRESHOLD, NO_UPDATE_MSG, quote_endpoint
from utils import constructURL,  avg
from keys import API_KEY

#Query financialmodelingprep API to get the quote of the symbol
def getQuote(symbol):
    print('Get info of symbol ' + symbol)
    url = constructURL(BASE_URL,quote_endpoint,API_KEY,symbol)
    response = urlopen(url)
    data = response.read().decode("utf-8")
    parsed_response = json.loads(data)
    return lget(parsed_response, [0], None)

#Compute the difference between the last 5 quotes and current quote
def computeDifference(quotes_list, current_quote):
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
    numberPastQuotes = len(quotes_list)
    currentQuote = getQuote(symbol)
    currentPrice = lget(currentQuote, ['price'], None)
    if currentPrice is None:
        return 'Error'
    result = computeDifference(quotes_list,currentPrice)
    quotes_list.append(currentPrice)
    return result

