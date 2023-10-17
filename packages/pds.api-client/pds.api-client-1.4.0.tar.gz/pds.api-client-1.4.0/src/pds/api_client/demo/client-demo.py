from __future__ import print_function
from pds.api_client.rest import ApiException
from pds.api_client import Configuration
from pds.api_client import ApiClient
from pds.api_client.api.by_product_classes_api import ByProductClassesApi
from pprint import pprint

# create an instance of the API class
configuration = Configuration()
#configuration.host = 'https://pds.nasa.gov/api/search/1'
#configuration.host = 'https://pds.nasa.gov/api/search-en-gamma/1'
configuration.host = 'http://localhost:8080'
api_client = ApiClient(configuration)

classes = ByProductClassesApi(api_client)

try:
    # see ref doc on
    api_response = classes.class_list(
        'collections',
        start=0,
        limit=20,
        fields=['ops:Label_File_Info.ops:file_ref']
    )
    pprint(api_response.summary)

except ApiException as e:
    print("Exception when calling CollectionsApi->get_collection: %s\n" % e)