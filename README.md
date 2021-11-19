# Trading Deamon

![](/img/hero.jpg)

This code has been written as an exercise with bots and deamons in my free time.

The idea is to have a deamon running in background which keeps fetching the price of the wanted stock. When it registers a fast increasing (or decreasing) with respect of the avg of the past n prices, it notifies you. 
In order to work properly it needs:<br />
    - `API_KEY` from https://site.financialmodelingprep.com 
    - `BOT_TOKEN` from https://core.telegram.org/bots.

## Goal
![bubble](/img/gmeBubble.png)

Get notified at the right moment! 
Every `POLLING_SECONDS` seconds it will query for the price of the wanted stock. If that price is very different from the avg of the past n prices it means that the stock is currenty on a roller coaster. It is wise to know it!
## Usage
1- `/start` to start the deamon <br />
2- `/conf_bot <TICKER> <POLLING_SECONDS>` to configure the bot.
 - The `TICKER` is the symbol of the wanted stock (example GME for GameStop). Check it out [here](https://stockanalysis.com/stocks/) for more.
 - The `POLLING_SECONDS` is the number of seconds between each query for the new price. This number must be above 60 because 1 minute is the minimum amout of time between each query.
 - If no parameter is passed then the default parameters will be used (GME 60). <br />
Example: <br />
 ```
`/conf_bot GME 120` // The bot will query for Amazon stock price every 2 minutes
 ```
3- `/start_deamon` actually starts the background activity of the bot.
## Features

- Use the code as a Deamon or a Telegram-Bot (it depends on the file you start)
- Get notified if there was a % difference beetween the current stock quote and the avg of the last n quotes
- BOT: choose the wanted stock and the sleeping time

## Tech

`trading_deamon` uses a number of open source projects to work properly:

- [Daemonocle](https://pypi.org/project/daemonocle/) -is a library for creating your own Unix-style daemons written in Python
- [Python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot#documentation) - Library that provides a pure Python interface for the Telegram Bot API.
- [FMP](https://site.financialmodelingprep.com) - APIs to fetch the current stock price