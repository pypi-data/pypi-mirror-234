import typing_extensions

from pds.api_client.apis.tags import TagValues
from pds.api_client.apis.tags.classes_api import ClassesApi
from pds.api_client.apis.tags.deprecated_api import DeprecatedApi
from pds.api_client.apis.tags.products_api import ProductsApi
from pds.api_client.apis.tags.references_api import ReferencesApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.CLASSES: ClassesApi,
        TagValues.DEPRECATED: DeprecatedApi,
        TagValues.PRODUCTS: ProductsApi,
        TagValues.REFERENCES: ReferencesApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.CLASSES: ClassesApi,
        TagValues.DEPRECATED: DeprecatedApi,
        TagValues.PRODUCTS: ProductsApi,
        TagValues.REFERENCES: ReferencesApi,
    }
)
