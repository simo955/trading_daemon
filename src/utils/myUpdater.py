import logging
from telegram import Update

from generalUtils import formatMessage

class myUpdate(Update):
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    def sendMessageAndLog(self, msg, args=[], options={}):
        self.message.reply_text(formatMessage(msg, args),quote=True)
        self.logger.info('Eaaa')
