"""
This module is a singleton that provides the data from Conductor endpoints. Specifically, it provides projects, instance types, and software package data. It is also possible to use cached fixture data for development purposes.

Since the data is stored at the module level, you can access it from anywhere in your code without the need to pass it around.
"""

import json
import os
from ciocore.package_tree import PackageTree
from ciocore import api_client
from ciocore.hardware_set import HardwareSet
__data__ = {}
__products__ = None
__fixtures_dir__ = None
__platforms__ = None

def init(*products, **kwargs):
    """
    Initialize the module and let it know what host products to provide.

    Args:
        products (str): Provide a list of products for which to get software packages. If no products are given, the software data contains all products from the packages endpoint. If you provide more than one product, they must all be host level products.

    Keyword Args:
        product (str): `DEPRECATED` Provide one product for which to get software packages.

    Examples:
        >>> from ciocore import data as coredata
        >>> coredata.init()
        # OR
        >>> coredata.init("maya-io")
        # OR LEGACY
        >>> coredata.init(product="all")
        # OR
        >>> coredata.init(product="maya-io")
    """
    global __products__
    global __platforms__
    if products:
        if kwargs.get("product"):
            raise ValueError(
                "Arguments: `products` and `product` specified. Please don't use both together. The `product` arg is deprecated."
            )
        __products__ = list(products)
    elif kwargs.get("product"):
        if kwargs.get("product") == "all":
            __products__ = []
        else:
            __products__ = [kwargs.get("product")]
    else:
        __products__ = []

    __platforms__ = set(kwargs.get("platforms", ["windows", "linux"]))

def data(force=False):
    """
    Provide projects, instance types, and software package data.

    Keyword Args:
        force: (bool) If `True`, then fetch fresh data -- Defaults to `False`.

    Raises:
        ValueError:  Module was not initialized with [init()](/data/#ciocore.data.init).

    Returns:
        dict: Keys are `projects`, `instance_types`, `software`.

    When you access the data, if it has already been fetched, it will be returned. Otherwise,
    requests will be made to fetch the data. You may need to authenticate in order to access the
    data.

    The set of instance types and software can be pruned to match the available platforms
    represented by each other. For example, if the instance types come from an orchestrator that
    provides both Windows and Linux machines, and the software product(s) are available on both
    platforms, no pruning occurs. However, if there are no Windows machines available, any Windows
    software will be removed from the package tree. Similarly, if a product is chosen that only runs
    on Windows, Linux instance types will not appearin the list of available hardware.

    Here is a breakdown of each key in the dictionary:

    * **projects** is a list of project names for your authenticated account.

    * **instance_types** is an instance of HardwareSet, providing you with access to the list of
    available machines configurations.

    * **software** is a PackageTree object containing either all
    the software available at Conductor, or a subset based on specified products.


    Examples:
        >>> from ciocore import data as coredata
        >>> coredata.init(product="maya-io")

        >>> coredata.data()["software"]
        <ciocore.package_tree.PackageTree object at 0x10e9a4040>

        >>> coredata.data()["projects"][0]
        ATestForScott

        >>> coredata.data()["instance_types"]
        <ciocore.hardware_set.HardwareSet object at 0x0000028941CD9DC0>
    """

    global __data__
    global __products__
    global __platforms__

    if __products__ is None:
        raise ValueError(
            'Data must be initialized before use, e.g. data.init("maya-io") or data.init().'
        )
    products_copy = __products__.copy()
    if force:
        clear()
        init(*products_copy)

    if __data__ == {}:
        # PROJECTS
        projects_json = _get_json_fixture("projects")
        if projects_json:
            __data__["projects"] = projects_json
        else:
            __data__["projects"] = sorted(api_client.request_projects())

        # INST_TYPES
        instance_types = _get_json_fixture("instance_types")
        if not instance_types:
            instance_types = api_client.request_instance_types()

        it_platforms = set([it["operating_system"] for it in instance_types])
        valid_platforms = it_platforms.intersection(__platforms__)

        # SOFTWARE
        software = _get_json_fixture("software")
        if not software:
            software = api_client.request_software_packages()

        kwargs = {"platforms": valid_platforms}

        # If there's only one product, it's possible to initialize the software tree with a plugin.
        # So we set the product kwarg. Otherwise, we set the host_products kwarg
        host_products = __products__
        if len(__products__) == 1:
            host_products = []
            kwargs["product"] = __products__[0]

        software_tree = PackageTree(software, *host_products, **kwargs)

        if software_tree:
            __data__["software"] = software_tree
            # Revisit instance types to filter out any that are not needed for any software package.
            sw_platforms = software_tree.platforms()

            instance_types = [
                it for it in instance_types if it["operating_system"] in sw_platforms
            ]

        __platforms__ = set([it["operating_system"] for it in instance_types])

        __data__["instance_types"] = HardwareSet(instance_types)

    return __data__


def valid():
    """
    Check validity.

    Returns:
        bool: True if `projects`, `instance_types`, and `software` are valid.

    Examples:
        >>> from ciocore import data as coredata
        >>> coredata.valid()
        True
    """

    if not __data__.get("projects"):
        return False
    if not __data__.get("instance_types"):
        return False
    if not __data__.get("software"):
        return False
    return True


def clear():
    """
    Clear out data.

    [valid()](/data/#ciocore.data.valid) returns False after clear().
    """
    global __data__
    global __products__
    global __platforms__
    __data__ = {}
    __products__ = None
    __platforms__ = None


def products():
    """

    Returns:
        list(str): The product names. An empty list signifies all products.
    """
    return __products__


def set_fixtures_dir(path):
    """
    Specify a directory in which to find JSON files representing the three sets of data to provide.
    The individual filenames are:

    * `projects.json`
    * `instance_types.json`
    * `software.json`

    These files could be used in an environment where machines can't access the internet. They are
    also useful as a cache for developers who need to reload often as it avoids waiting for the
    network.

    In order to get the content for the fixtures files, use the following Example

    Examples:
        >>> from ciocore import api_client
        >>> projects = api_client.request_projects()
        >>> instance_types = api_client.request_instance_types()
        >>> software = api_client.request_software_packages()

    Write that data as JSON to the filenames listed above.

    Arguments:
        path (str): Directory in which to find the above files.

    """

    global __fixtures_dir__
    __fixtures_dir__ = path or ""


def _get_json_fixture(resource):
    if __fixtures_dir__:
        cache_path = os.path.join(__fixtures_dir__, "{}.json".format(resource))
        if os.path.isfile(cache_path):
            try:
                with open(cache_path) as f:
                    return json.load(f)
            except BaseException:
                pass


def platforms():
    """
    The set of platforms that both software and instance types are valid on.

    Returns:
        set: A set containing platforms: windows and/or linux.
    """
    return __platforms__

