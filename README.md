> Disclaimer: This code has been written as an exercise with bots and deamons in my free time.
# Trading Deamon

![](/img/hero.jpg)


The idea is to have a deamon running in background which keeps fetching the price of the wanted stock. When it registers a suddenly increasing (or decreasing) with respect of the avg of the past *n* prices, the deamon notifies you. 
In order to work properly it needs:<br />
    - `API_KEY` from https://site.financialmodelingprep.com <br />
    - `BOT_TOKEN` from https://core.telegram.org/bots.

## Goal
![bubble](/img/gmeBubble.png)

Get notified at the right moment! <br />
Every x=`POLLING_SECONDS` seconds the deamon will query for the price of the wanted stock. If that price is different from the avg of the past *n* prices it means that the stock is currenty on a roller coaster. It is wise to know it!
## Usage
1- `/start` to start the deamon <br />
2- `/start_deamon <SYMBOL> <POLLING_SECONDS>` starts the background activity of the bot.
 - `SYMBOL` is the symbol of the wanted stock (example GME for Game Stop). Check it out [here](https://stockanalysis.com/stocks/) for more.
 - `POLLING_SECONDS` is the number of seconds between each query for the new price. This number must be above 60 because 1 minute is the minimum amout of time between each query.
 - If no parameter is passed then the default parameters will be used (GME 60). <br />
Example of usage: <br />
 ```
/start_deamon GME 60 // The bot will query for Game Stop stock price every minute
 ```
## Features

- Use the code as a Telegram-Bot.
- Get notified if there was a % difference beetween the current stock price and the avg of the last *n* quotes
- Choose the wanted stock and the sleeping time

## Tech

`trading_deamon` uses a number of open source projects to work properly:

- [Daemonocle](https://pypi.org/project/daemonocle/) - is a python library for creating your own Unix-style daemons.
- [Python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot#documentation) - is a python library that provides a pure Python interface for the Telegram Bot APIs.
- [FMP](https://site.financialmodelingprep.com) - provides APIs to fetch the current stock price.

## Limits
- Trading-Deamon is exploiting [FMP](https://site.financialmodelingprep.com) free APIs. Due to that only 250 requests/day are possible.  

## Future Development
- ~~Bot performs a more accurate test to verify that the passed symbol is actually valid.~~
- Bot is able to accept more than 1 symbol. This is currently impratical due to the [FMP](https://site.financialmodelingprep.com) free APIs limit.
- Bot is able to accept crypto too. Right now this is not possible because [FMP](https://site.financialmodelingprep.com) APIs does not fetch quotes for crypto.

# Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/yourFeature`)
3. Commit your Changes (`git commit -m 'Add some yourFeature'`)
4. Push to the Branch (`git push origin feature/yourFeature`)
5. Open a Pull Request

# Authors

* **Simone Patuelli** - [@simo955](https://github.com/simo955)

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details