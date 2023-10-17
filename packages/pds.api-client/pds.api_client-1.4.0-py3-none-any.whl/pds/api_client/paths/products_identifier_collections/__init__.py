# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from pds.api_client.paths.products_identifier_collections import Api

from pds.api_client.paths import PathValues

path = PathValues.PRODUCTS_IDENTIFIER_COLLECTIONS