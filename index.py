from urllib.request import urlopen
from pydash import get as lget
from consts import API_KEY, BASE_URL, STARTING_SYMBOL, quote_endpoint
import time
import json

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
def manage_stack(quotes_list, symbol):
    info = getQuote(symbol)
    price = lget(info, ['price'], None)
    l = len(quotes_list)
    if(l>=1):
        # compute difference only on the last 5 elems
        for i in range(max(l-5, 0),l):
            percentage_diff=computeDifference(quotes_list, price, i)
            print('I',i, percentage_diff)
            print('********Differance in percentage********', percentage_diff)
    if(price):
        quotes_list.append(price)
    print(quotes_list)
    return


def main():
    quotes_list = []
    while True:
        manage_stack(quotes_list,STARTING_SYMBOL)
        time.sleep(60.0 - ((time.time()) % 60.0))

if __name__ == "__main__":
    main()



