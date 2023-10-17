import unittest
from pds.api_client import Configuration
from pds.api_client import ApiClient
from pds.api_client.api.by_product_classes_api import ByProductClassesApi
from pds.api_client.api.all_products_api import AllProductsApi
from pds.api_client.models.pds4_products import Pds4Products


class CollectionsApiTestCase(unittest.TestCase):

    def setUp(self):
        # create an instance of the API class
        configuration = Configuration()
        configuration.host = 'http://localhost:8080'
        api_client = ApiClient(configuration)
        self.product_by_class = ByProductClassesApi(api_client)
        self.all_products = AllProductsApi(api_client)

    def test_all_collections(self):

        api_response = self.product_by_class.class_list(
            'collections',
            start=0,
            limit=10
        )

        assert len(api_response.data) == 4
        assert api_response.summary.hits == 4

        assert all([hasattr(c, 'id') for c in api_response.data])

        # select one collection with lidvid 'urn:nasa:pds:insight_rad:data_calibrated::7.0'
        collection = [c for c in api_response.data if c.id == 'urn:nasa:pds:mars2020.spice:spice_kernels::3.0'][0]
        assert hasattr(collection, 'type')
        assert collection.type == 'Product_Collection'

        assert hasattr(collection, 'title')
        assert collection.title == "Mars 2020 Perseverance Rover Mission SPICE Kernel Collection"

    def test_all_collections_one_property(self):
        api_response = self.product_by_class.class_list(
            'collections',
            start=0,
            limit=20,
            fields=['ops:Label_File_Info.ops:file_ref']
        )

        assert hasattr(api_response, "data")

        collections_expected_labels = iter([
            "http://localhost:81/archive/custom-datasets/naif3/spice_kernels/collection_spice_kernels_v003.xml",
            "http://localhost:81/archive/custom-datasets/urn-nasa-pds-insight_rad/data_calibrated/collection_data_rad_calibrated.xml",
            "http://localhost:81/archive/custom-datasets/urn-nasa-pds-insight_rad/data_derived/collection_data_rad_derived.xml",
            "http://localhost:81/archive/custom-datasets/urn-nasa-pds-insight_rad/data_raw/collection_data_rad_raw.xml"
        ])

        for collection in api_response.data:
            urls = collection.properties['ops:Label_File_Info.ops:file_ref']
            assert next(collections_expected_labels) in urls[0]

    def test_collection_by_lidvid_all(self):
        collections = self.all_products.select_by_lidvid_all('urn:nasa:pds:mars2020.spice:spice_kernels')
        assert hasattr(collections, 'data')
        assert len(collections.data) > 0
        assert hasattr(collections.data[-1], 'id')
        assert collections.data[-1].id == 'urn:nasa:pds:mars2020.spice:spice_kernels::3.0'

    @unittest.skip("Does not work with the latest version of the openapi generator")
    def test_collection_by_lidvid_all_content_type(self):
        collections: Pds4Products = self.product_identifier_all.get(
            path_params={'identifier': 'urn:nasa:pds:insight_rad:data_derived::7.0'},
            accept_content_types=('application/vnd.nasa.pds.pds4+json',)
        ).body
        assert 'data' in collections
        assert len(collections.data) > 0
        assert 'pds4' in collections['data'][0]
        

if __name__ == '__main__':
    unittest.main()
