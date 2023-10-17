from __future__ import print_function
from pds.api_client.rest import ApiException
from pds.api_client import Configuration
from pds.api_client import ApiClient
from pds.api_client.api.product_references_api import ProductReferencesApi
from pprint import pprint

# create an instance of the API class
configuration = Configuration()
configuration.host = 'https://pds.nasa.gov/api/search/1'
api_client = ApiClient(configuration)


product_references = ProductReferencesApi(api_client)

try:
    # search product of collection urn:nasa:pds:messenger_mdis_2001
    api_response = product_references.product_members(
        'urn:nasa:pds:messenger_mdis_2001',
        start=0,
        limit=10
    )
    pprint(api_response['summary'])

except ApiException as e:
    print("Exception when calling CollectionsApi->get_collection: %s\n" % e)