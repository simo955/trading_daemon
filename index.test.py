import unittest
from pydash import get as lget
from index import getQuote

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


if __name__ == '__main__':
    unittest.main()