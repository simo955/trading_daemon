# Basic version of the deamon which did not use telegram-bot functionalities
import logging
import sys
import time
import daemonocle

from getQuotes import manage_stack
from utils.conf import STARTING_SYMBOL, SLEEP_SECONDS,UPDATE_MSG
from utils.myUpdaterService import myUpdaterService

updaterService = myUpdaterService()

def shutdown(message, code):
    updaterService.log('Daemon is stopping')

def main():
    quotes_list=[]
    updaterService.log('Daemon is starting')
    while True:
        msg = manage_stack(updaterService, quotes_list, STARTING_SYMBOL)
        updaterService.log('Ending iteration. MSG={}', [msg])
        if msg==UPDATE_MSG:
            updaterService.log(msg)
        time.sleep(SLEEP_SECONDS)

if __name__ == '__main__':
    daemon = daemonocle.Daemon(
        worker=main,
        shutdown_callback=shutdown,
        detach=False
    )
    daemon.do_action(sys.argv[1])


# run with python3 indexDeamon.py start