import logging
import sys
import time
import daemonocle

from utils import manage_stack
from conf import STARTING_SYMBOL, SLEEP_SECONDS


def shutdown(message, code):
    logging.info('Daemon is stopping')
    logging.debug(message)

def main():
    quotes_list=[]
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s',
    )
    logging.info('Daemon is starting')
    while True:
        logging.debug('Still running')
        manage_stack(logging, quotes_list,STARTING_SYMBOL)
        time.sleep(SLEEP_SECONDS)

if __name__ == '__main__':
    daemon = daemonocle.Daemon(
        worker=main,
        shutdown_callback=shutdown,
        detach=False
    )
    daemon.do_action(sys.argv[1])
