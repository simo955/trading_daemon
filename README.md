# traidingDeamon

![](/img/hero.jpg)

This code has been written as an exercise with bots and deamons in my free time.

The idea is to have a deamon running in background which keeps fetching the price of the wanted stock. When it registers a fast increasing (or decreasing) with respect of the avg of the past n prices, it notifies you. 
In order to work it need an API_KEY from https://site.financialmodelingprep.com and a BOT_TOKEN from https://core.telegram.org/bots.

## Features

- Use the code as a Deamon or a Telegram-Bot (it depends on index.py file)
- Get notified if there was a % difference beetween the current stock quote and the avg of the last n quotes
- BOT: choose the wanted stock and the sleeping time

## Tech

trading_deamon uses a number of open source projects to work properly:

- [Daemonocle](https://pypi.org/project/daemonocle/) -is a library for creating your own Unix-style daemons written in Python
- [Python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot#documentation) - Library that provides a pure Python interface for the Telegram Bot API.
[FMP](https://site.financialmodelingprep.com) - APIs to fetch the current stock price