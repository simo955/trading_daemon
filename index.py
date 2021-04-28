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

def getInfo(symbol):
    print('Get quote of symbol ' + symbol)
    url = BASE_URL+symbol+'?apikey={}'.format(API_KEY)
    response = queryEndpoint(url)
    return response if response else None

def computeDifference(quotes_list, current_quote, index=0):
    previous_quote = quotes_list[index]
    abs_diff = abs(current_quote - previous_quote)
    return round(( abs_diff * 100 )/previous_quote, 2)

def manage_stack(quotes_list, symbol):
    info = getInfo(symbol)
    quote = lget(info, ['price'], None)
    l = len(quotes_list)
    if(l>=1):
        # compute difference only on the last 5 elems
        for i in range(max(l-5, 0),l):
            percentage_diff=computeDifference(quotes_list, quote, i)
            print('********Differance in percentage********', percentage_diff)
    if(quote):
        quotes_list.append(quote)
    print(quotes_list)
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



