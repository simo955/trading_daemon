import unittest
from pydash import get as lget
from index import getQuote, computeDifference

class TestSum(unittest.TestCase):

    def test_getQuote(self):
        quote = 'CCL'
        result = getQuote(quote)
        result_name = lget(result,'name', None)
        self.assertEqual(result_name, 'Carnival Corporation & Plc', "Should be equal")

        quote = 'XXXXXXXXXXXX'
        result = getQuote(quote)
        result_name = lget(result,'name', None)
        self.assertEqual(result_name, None, "Should be null")


    def test_computeDifference(self):
        result = computeDifference([1,2,1,100],85)
        self.assertEqual(result, 15.0, "Should be 15%")


if __name__ == '__main__':
    unittest.main()