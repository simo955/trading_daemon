import logging
import sys
import time
import daemonocle

from getQuotes import manage_stack
from conf import STARTING_SYMBOL, SLEEP_SECONDS,UPDATE_MSG

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)



def shutdown(message, code):
    logger.info('Daemon is stopping')
    logger.info(message)

def main():
    quotes_list=[]
    logger.info('Daemon is starting')
    while True:
        logger.debug('Still running')
        msg = manage_stack(logger, quotes_list, STARTING_SYMBOL)
        logger.info('Ending iteration. MSG={}'.format(msg))
        if msg==UPDATE_MSG:
            logger.warning(msg)
        time.sleep(SLEEP_SECONDS)

if __name__ == '__main__':
    daemon = daemonocle.Daemon(
        worker=main,
        shutdown_callback=shutdown,
        detach=False
    )
    daemon.do_action(sys.argv[1])



# run with python3 indexDeamon.py start