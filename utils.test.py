import logging
import unittest
from pydash import get as lget
from getQuotes import getQuote, computeDifference

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

class TestSum(unittest.TestCase):
    def test_getQuote(self):
        quote = 'CCL'
        result = getQuote(logger, quote)
        result_name = lget(result,'name', None)
        self.assertEqual(result_name.lower(), 'Carnival Corporation & Plc'.lower(), "Should be equal")

        quote = 'XXXXXXXXXXXX'
        result = getQuote(logger, quote)
        result_name = lget(result,'name', None)
        self.assertEqual(result_name, None, "Should be null")

    def test_computeDifference(self):
        result = computeDifference(logger,[1,1,1],1)
        self.assertEqual(0, result)

        result = computeDifference(logger,[10],9)
        self.assertEqual(10, result)

        result = computeDifference(logger,[13, 7, 10],2)
        self.assertEqual(80, result)

        result = computeDifference(logger,[0, 0, 0],1)
        self.assertEqual(0, result)


if __name__ == '__main__':
    unittest.main()