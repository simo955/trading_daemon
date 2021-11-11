import unittest
from unittest.mock import patch # for Python >= 3.3 use unittest.mock
from pydash import get as lget
from utils import getQuote, computeDifference
from conf import NO_UPDATE_MSG
class TestSum(unittest.TestCase):
    def test_getQuote(self):
        quote = 'CCL'
        result = getQuote(quote)
        result_name = lget(result,'name', None)
        self.assertEqual(result_name.lower(), 'Carnival Corporation & Plc'.lower(), "Should be equal")

        quote = 'XXXXXXXXXXXX'
        result = getQuote(quote)
        result_name = lget(result,'name', None)
        self.assertEqual(result_name, None, "Should be null")

    def test_computeDifference(self):
        result = computeDifference([1,1,1],1)
        self.assertEqual(0, result)

        result = computeDifference([10],9)
        self.assertEqual(10, result)

        result = computeDifference([13, 7, 10],2)
        self.assertEqual(80, result)

        result = computeDifference([0, 0, 0],1)
        self.assertEqual(0, result)


if __name__ == '__main__':
    unittest.main()