import os

from telegram.ext import Updater, MessageHandler, Filters,CommandHandler

from utils.conf import bot_start_deamong_cmd
from handlers import startHandler, helpHandler, start_deamonHandler,stopHandler, echoWrongCmdHandler, debugHandler
from keys import BOT_TOKEN

def main() -> None:
    PORT = int(os.environ.get('PORT', '8443'))

    """Run bot."""
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", startHandler))
    dispatcher.add_handler(CommandHandler("stop", stopHandler))
    dispatcher.add_handler(CommandHandler("help", helpHandler))
    dispatcher.add_handler(CommandHandler("debug", debugHandler))
    dispatcher.add_handler(CommandHandler(bot_start_deamong_cmd, start_deamonHandler, run_async=True))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echoWrongCmdHandler))

    # Start the Bot
    ## To start it locally: 
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    isConfigured = False
    main()