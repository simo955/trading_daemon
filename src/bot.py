import os
import logging

from telegram.ext import Updater, MessageHandler, Filters,CommandHandler

from conf import bot_configuration_cmd, bot_start_deamong_cmd
from handlers import startHandler, helpHandler, configure_botHandler, start_deamonHandler,stopHandler, echoWrongCmdHandler

def main() -> None:
    BOT_TOKEN = os.environ['BOT_TOKEN']
    PORT = int(os.environ.get('PORT', '8443'))

    """Run bot."""
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", startHandler))
    dispatcher.add_handler(CommandHandler("stop", stopHandler))
    dispatcher.add_handler(CommandHandler("help", helpHandler))
    dispatcher.add_handler(CommandHandler(bot_configuration_cmd, configure_botHandler))
    dispatcher.add_handler(CommandHandler(bot_start_deamong_cmd, start_deamonHandler, run_async=True))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echoWrongCmdHandler))

    # Start the Bot
    ## To start it locally: updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=BOT_TOKEN,
                        webhook_url="https://tradingdeamon.herokuapp.com/" + BOT_TOKEN)
    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    isConfigured = False
    main()