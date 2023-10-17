# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from pds.api_client.paths.collections_identifier import Api

from pds.api_client.paths import PathValues

path = PathValues.COLLECTIONS_IDENTIFIER