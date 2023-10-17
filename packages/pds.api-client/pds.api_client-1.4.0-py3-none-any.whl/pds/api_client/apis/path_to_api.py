import typing_extensions

from pds.api_client.paths import PathValues
from pds.api_client.apis.paths.classes import Classes
from pds.api_client.apis.paths.classes_class import ClassesClass
from pds.api_client.apis.paths.classes_class_identifier_members import ClassesClassIdentifierMembers
from pds.api_client.apis.paths.classes_class_identifier_members_versions import ClassesClassIdentifierMembersVersions
from pds.api_client.apis.paths.classes_class_identifier_members_members import ClassesClassIdentifierMembersMembers
from pds.api_client.apis.paths.classes_class_identifier_members_members_versions import ClassesClassIdentifierMembersMembersVersions
from pds.api_client.apis.paths.classes_class_identifier_member_of import ClassesClassIdentifierMemberOf
from pds.api_client.apis.paths.classes_class_identifier_member_of_versions import ClassesClassIdentifierMemberOfVersions
from pds.api_client.apis.paths.classes_class_identifier_member_of_member_of import ClassesClassIdentifierMemberOfMemberOf
from pds.api_client.apis.paths.classes_class_identifier_member_of_member_of_versions import ClassesClassIdentifierMemberOfMemberOfVersions
from pds.api_client.apis.paths.products import Products
from pds.api_client.apis.paths.products_identifier import ProductsIdentifier
from pds.api_client.apis.paths.products_identifier_latest import ProductsIdentifierLatest
from pds.api_client.apis.paths.products_identifier_all import ProductsIdentifierAll
from pds.api_client.apis.paths.products_identifier_members import ProductsIdentifierMembers
from pds.api_client.apis.paths.products_identifier_members_versions import ProductsIdentifierMembersVersions
from pds.api_client.apis.paths.products_identifier_members_members import ProductsIdentifierMembersMembers
from pds.api_client.apis.paths.products_identifier_members_members_versions import ProductsIdentifierMembersMembersVersions
from pds.api_client.apis.paths.products_identifier_member_of import ProductsIdentifierMemberOf
from pds.api_client.apis.paths.products_identifier_member_of_versions import ProductsIdentifierMemberOfVersions
from pds.api_client.apis.paths.products_identifier_member_of_member_of import ProductsIdentifierMemberOfMemberOf
from pds.api_client.apis.paths.products_identifier_member_of_member_of_versions import ProductsIdentifierMemberOfMemberOfVersions
from pds.api_client.apis.paths.bundles import Bundles
from pds.api_client.apis.paths.bundles_identifier import BundlesIdentifier
from pds.api_client.apis.paths.bundles_identifier_all import BundlesIdentifierAll
from pds.api_client.apis.paths.bundles_identifier_latest import BundlesIdentifierLatest
from pds.api_client.apis.paths.bundles_identifier_collections import BundlesIdentifierCollections
from pds.api_client.apis.paths.bundles_identifier_collections_all import BundlesIdentifierCollectionsAll
from pds.api_client.apis.paths.bundles_identifier_collections_latest import BundlesIdentifierCollectionsLatest
from pds.api_client.apis.paths.bundles_identifier_products import BundlesIdentifierProducts
from pds.api_client.apis.paths.collections import Collections
from pds.api_client.apis.paths.collections_identifier import CollectionsIdentifier
from pds.api_client.apis.paths.collections_identifier_all import CollectionsIdentifierAll
from pds.api_client.apis.paths.collections_identifier_latest import CollectionsIdentifierLatest
from pds.api_client.apis.paths.collections_identifier_bundles import CollectionsIdentifierBundles
from pds.api_client.apis.paths.collections_identifier_products import CollectionsIdentifierProducts
from pds.api_client.apis.paths.collections_identifier_products_all import CollectionsIdentifierProductsAll
from pds.api_client.apis.paths.collections_identifier_products_latest import CollectionsIdentifierProductsLatest
from pds.api_client.apis.paths.products_identifier_bundles import ProductsIdentifierBundles
from pds.api_client.apis.paths.products_identifier_bundles_all import ProductsIdentifierBundlesAll
from pds.api_client.apis.paths.products_identifier_bundles_latest import ProductsIdentifierBundlesLatest
from pds.api_client.apis.paths.products_identifier_collections import ProductsIdentifierCollections
from pds.api_client.apis.paths.products_identifier_collections_all import ProductsIdentifierCollectionsAll
from pds.api_client.apis.paths.products_identifier_collections_latest import ProductsIdentifierCollectionsLatest

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.CLASSES: Classes,
        PathValues.CLASSES_CLASS: ClassesClass,
        PathValues.CLASSES_CLASS_IDENTIFIER_MEMBERS: ClassesClassIdentifierMembers,
        PathValues.CLASSES_CLASS_IDENTIFIER_MEMBERS_VERSIONS: ClassesClassIdentifierMembersVersions,
        PathValues.CLASSES_CLASS_IDENTIFIER_MEMBERS_MEMBERS: ClassesClassIdentifierMembersMembers,
        PathValues.CLASSES_CLASS_IDENTIFIER_MEMBERS_MEMBERS_VERSIONS: ClassesClassIdentifierMembersMembersVersions,
        PathValues.CLASSES_CLASS_IDENTIFIER_MEMBEROF: ClassesClassIdentifierMemberOf,
        PathValues.CLASSES_CLASS_IDENTIFIER_MEMBEROF_VERSIONS: ClassesClassIdentifierMemberOfVersions,
        PathValues.CLASSES_CLASS_IDENTIFIER_MEMBEROF_MEMBEROF: ClassesClassIdentifierMemberOfMemberOf,
        PathValues.CLASSES_CLASS_IDENTIFIER_MEMBEROF_MEMBEROF_VERSIONS: ClassesClassIdentifierMemberOfMemberOfVersions,
        PathValues.PRODUCTS: Products,
        PathValues.PRODUCTS_IDENTIFIER: ProductsIdentifier,
        PathValues.PRODUCTS_IDENTIFIER_LATEST: ProductsIdentifierLatest,
        PathValues.PRODUCTS_IDENTIFIER_ALL: ProductsIdentifierAll,
        PathValues.PRODUCTS_IDENTIFIER_MEMBERS: ProductsIdentifierMembers,
        PathValues.PRODUCTS_IDENTIFIER_MEMBERS_VERSIONS: ProductsIdentifierMembersVersions,
        PathValues.PRODUCTS_IDENTIFIER_MEMBERS_MEMBERS: ProductsIdentifierMembersMembers,
        PathValues.PRODUCTS_IDENTIFIER_MEMBERS_MEMBERS_VERSIONS: ProductsIdentifierMembersMembersVersions,
        PathValues.PRODUCTS_IDENTIFIER_MEMBEROF: ProductsIdentifierMemberOf,
        PathValues.PRODUCTS_IDENTIFIER_MEMBEROF_VERSIONS: ProductsIdentifierMemberOfVersions,
        PathValues.PRODUCTS_IDENTIFIER_MEMBEROF_MEMBEROF: ProductsIdentifierMemberOfMemberOf,
        PathValues.PRODUCTS_IDENTIFIER_MEMBEROF_MEMBEROF_VERSIONS: ProductsIdentifierMemberOfMemberOfVersions,
        PathValues.BUNDLES: Bundles,
        PathValues.BUNDLES_IDENTIFIER: BundlesIdentifier,
        PathValues.BUNDLES_IDENTIFIER_ALL: BundlesIdentifierAll,
        PathValues.BUNDLES_IDENTIFIER_LATEST: BundlesIdentifierLatest,
        PathValues.BUNDLES_IDENTIFIER_COLLECTIONS: BundlesIdentifierCollections,
        PathValues.BUNDLES_IDENTIFIER_COLLECTIONS_ALL: BundlesIdentifierCollectionsAll,
        PathValues.BUNDLES_IDENTIFIER_COLLECTIONS_LATEST: BundlesIdentifierCollectionsLatest,
        PathValues.BUNDLES_IDENTIFIER_PRODUCTS: BundlesIdentifierProducts,
        PathValues.COLLECTIONS: Collections,
        PathValues.COLLECTIONS_IDENTIFIER: CollectionsIdentifier,
        PathValues.COLLECTIONS_IDENTIFIER_ALL: CollectionsIdentifierAll,
        PathValues.COLLECTIONS_IDENTIFIER_LATEST: CollectionsIdentifierLatest,
        PathValues.COLLECTIONS_IDENTIFIER_BUNDLES: CollectionsIdentifierBundles,
        PathValues.COLLECTIONS_IDENTIFIER_PRODUCTS: CollectionsIdentifierProducts,
        PathValues.COLLECTIONS_IDENTIFIER_PRODUCTS_ALL: CollectionsIdentifierProductsAll,
        PathValues.COLLECTIONS_IDENTIFIER_PRODUCTS_LATEST: CollectionsIdentifierProductsLatest,
        PathValues.PRODUCTS_IDENTIFIER_BUNDLES: ProductsIdentifierBundles,
        PathValues.PRODUCTS_IDENTIFIER_BUNDLES_ALL: ProductsIdentifierBundlesAll,
        PathValues.PRODUCTS_IDENTIFIER_BUNDLES_LATEST: ProductsIdentifierBundlesLatest,
        PathValues.PRODUCTS_IDENTIFIER_COLLECTIONS: ProductsIdentifierCollections,
        PathValues.PRODUCTS_IDENTIFIER_COLLECTIONS_ALL: ProductsIdentifierCollectionsAll,
        PathValues.PRODUCTS_IDENTIFIER_COLLECTIONS_LATEST: ProductsIdentifierCollectionsLatest,
    }
)

path_to_api = PathToApi(
    {
        PathValues.CLASSES: Classes,
        PathValues.CLASSES_CLASS: ClassesClass,
        PathValues.CLASSES_CLASS_IDENTIFIER_MEMBERS: ClassesClassIdentifierMembers,
        PathValues.CLASSES_CLASS_IDENTIFIER_MEMBERS_VERSIONS: ClassesClassIdentifierMembersVersions,
        PathValues.CLASSES_CLASS_IDENTIFIER_MEMBERS_MEMBERS: ClassesClassIdentifierMembersMembers,
        PathValues.CLASSES_CLASS_IDENTIFIER_MEMBERS_MEMBERS_VERSIONS: ClassesClassIdentifierMembersMembersVersions,
        PathValues.CLASSES_CLASS_IDENTIFIER_MEMBEROF: ClassesClassIdentifierMemberOf,
        PathValues.CLASSES_CLASS_IDENTIFIER_MEMBEROF_VERSIONS: ClassesClassIdentifierMemberOfVersions,
        PathValues.CLASSES_CLASS_IDENTIFIER_MEMBEROF_MEMBEROF: ClassesClassIdentifierMemberOfMemberOf,
        PathValues.CLASSES_CLASS_IDENTIFIER_MEMBEROF_MEMBEROF_VERSIONS: ClassesClassIdentifierMemberOfMemberOfVersions,
        PathValues.PRODUCTS: Products,
        PathValues.PRODUCTS_IDENTIFIER: ProductsIdentifier,
        PathValues.PRODUCTS_IDENTIFIER_LATEST: ProductsIdentifierLatest,
        PathValues.PRODUCTS_IDENTIFIER_ALL: ProductsIdentifierAll,
        PathValues.PRODUCTS_IDENTIFIER_MEMBERS: ProductsIdentifierMembers,
        PathValues.PRODUCTS_IDENTIFIER_MEMBERS_VERSIONS: ProductsIdentifierMembersVersions,
        PathValues.PRODUCTS_IDENTIFIER_MEMBERS_MEMBERS: ProductsIdentifierMembersMembers,
        PathValues.PRODUCTS_IDENTIFIER_MEMBERS_MEMBERS_VERSIONS: ProductsIdentifierMembersMembersVersions,
        PathValues.PRODUCTS_IDENTIFIER_MEMBEROF: ProductsIdentifierMemberOf,
        PathValues.PRODUCTS_IDENTIFIER_MEMBEROF_VERSIONS: ProductsIdentifierMemberOfVersions,
        PathValues.PRODUCTS_IDENTIFIER_MEMBEROF_MEMBEROF: ProductsIdentifierMemberOfMemberOf,
        PathValues.PRODUCTS_IDENTIFIER_MEMBEROF_MEMBEROF_VERSIONS: ProductsIdentifierMemberOfMemberOfVersions,
        PathValues.BUNDLES: Bundles,
        PathValues.BUNDLES_IDENTIFIER: BundlesIdentifier,
        PathValues.BUNDLES_IDENTIFIER_ALL: BundlesIdentifierAll,
        PathValues.BUNDLES_IDENTIFIER_LATEST: BundlesIdentifierLatest,
        PathValues.BUNDLES_IDENTIFIER_COLLECTIONS: BundlesIdentifierCollections,
        PathValues.BUNDLES_IDENTIFIER_COLLECTIONS_ALL: BundlesIdentifierCollectionsAll,
        PathValues.BUNDLES_IDENTIFIER_COLLECTIONS_LATEST: BundlesIdentifierCollectionsLatest,
        PathValues.BUNDLES_IDENTIFIER_PRODUCTS: BundlesIdentifierProducts,
        PathValues.COLLECTIONS: Collections,
        PathValues.COLLECTIONS_IDENTIFIER: CollectionsIdentifier,
        PathValues.COLLECTIONS_IDENTIFIER_ALL: CollectionsIdentifierAll,
        PathValues.COLLECTIONS_IDENTIFIER_LATEST: CollectionsIdentifierLatest,
        PathValues.COLLECTIONS_IDENTIFIER_BUNDLES: CollectionsIdentifierBundles,
        PathValues.COLLECTIONS_IDENTIFIER_PRODUCTS: CollectionsIdentifierProducts,
        PathValues.COLLECTIONS_IDENTIFIER_PRODUCTS_ALL: CollectionsIdentifierProductsAll,
        PathValues.COLLECTIONS_IDENTIFIER_PRODUCTS_LATEST: CollectionsIdentifierProductsLatest,
        PathValues.PRODUCTS_IDENTIFIER_BUNDLES: ProductsIdentifierBundles,
        PathValues.PRODUCTS_IDENTIFIER_BUNDLES_ALL: ProductsIdentifierBundlesAll,
        PathValues.PRODUCTS_IDENTIFIER_BUNDLES_LATEST: ProductsIdentifierBundlesLatest,
        PathValues.PRODUCTS_IDENTIFIER_COLLECTIONS: ProductsIdentifierCollections,
        PathValues.PRODUCTS_IDENTIFIER_COLLECTIONS_ALL: ProductsIdentifierCollectionsAll,
        PathValues.PRODUCTS_IDENTIFIER_COLLECTIONS_LATEST: ProductsIdentifierCollectionsLatest,
    }
)
