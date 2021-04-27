from urllib.request import urlopen
from pydash import get as lget
import time
import json

BASE_URL='https://financialmodelingprep.com/api/v3/quote/'
API_KEY= '34a1467433844d42bcb7b83695ff210b'

def queryEndpoint(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    parsed_response = json.loads(data)
    return lget(parsed_response, [0], {})

def getQuote(symbol):
    print('Get quote of symbol ' + symbol)
    url = BASE_URL+symbol+'?apikey={}'.format(API_KEY)
    response = queryEndpoint(url)
    if (response):
        return lget(response, ['price'], None)
    return None

def computeDifference(quotes_list, current_quote):
    previous_quote = quotes_list[-1]
    abs_diff = abs(current_quote - previous_quote)
    return ( abs_diff * 100 )/previous_quote

def manage_stack(quotes_list, symbol):
    quote = getQuote(symbol)
    quotes_list.append(quote)
    if (len(quotes_list)>1):
        percentage_diff=computeDifference(quotes_list, quote)
        print('Differance in percentage', percentage_diff)
    print('LIST',quotes_list)
    return


def main():
    starttime = time.time()    
    quotes_list = []
    symbol = 'CCL'
    while True:
        manage_stack(quotes_list,symbol)
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))

if __name__ == "__main__":
    main()



