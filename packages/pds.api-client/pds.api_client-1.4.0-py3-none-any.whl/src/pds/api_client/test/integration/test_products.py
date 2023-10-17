import unittest
from pds.api_client import Configuration
from pds.api_client import ApiClient

from pds.api_client.api.all_products_api import AllProductsApi


class ProductsCase(unittest.TestCase):

    def setUp(self):
        # create an instance of the API class
        configuration = Configuration()
        configuration.host = 'http://localhost:8080'
        api_client = ApiClient(configuration)
        self.products = AllProductsApi(api_client)

    def test_products_by_keywords(self):
        results = self.products.product_list(
            keywords=['kernel']
        )

        self.assertEqual(len(results.data), 3)  # add assertion here


if __name__ == '__main__':
    unittest.main()
