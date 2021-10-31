import logging
import sys
import time
import daemonocle

from utils import manage_stack


def shutdown(message, code):
    logging.info('Daemon is stopping')
    logging.debug(message)

def main():
    print('1')
    quotes_list=[]
    logging.basicConfig(
        filename='/log/daemonocle_example.log',
        level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s',
    )
    print('2')
    logging.info('Daemon is starting')
    while True:
        print('3')
        logging.debug('Still running')
        manage_stack(quotes_list,STARTING_SYMBOL)
        time.sleep(60)

if __name__ == '__main__':
    daemon = daemonocle.Daemon(
        worker=main,
        shutdown_callback=shutdown,
        pid_file='/run/daemonocle_example.pid',
        detach=False
    )
    daemon.do_action(sys.argv[1])
