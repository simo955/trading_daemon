from urllib.request import urlopen
from pydash import get as lget
import json

BASE_URL='https://financialmodelingprep.com/api/v3/quote/'
API_KEY= '34a1467433844d42bcb7b83695ff210b'

def queryEndpoint(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    parsed_response = json.loads(data)
    return lget(parsed_response, [0], {})

def getQuote(symbol):
    url = BASE_URL+symbol+'?apikey={}'.format(API_KEY)
    response = queryEndpoint(url)
    if (response):
        return response
    return None


def main():
    symbol = 'CCL'
    quote = getQuote(symbol)
    print(quote)

if __name__ == "__main__":
    main()