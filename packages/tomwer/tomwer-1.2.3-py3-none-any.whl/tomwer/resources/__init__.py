# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/


from __future__ import annotations
import os
import sys
import contextlib
import atexit
from typing import NamedTuple, Optional
import importlib
import functools

if sys.version_info < (3, 9):
    import pkg_resources

# For packaging purpose, patch this variable to use an alternative directory
# E.g., replace with _RESOURCES_DIR = '/usr/share/silx/data'
_RESOURCES_DIR = None

# For packaging purpose, patch this variable to use an alternative directory
# E.g., replace with _RESOURCES_DIR = '/usr/share/silx/doc'
# Not in use, uncomment when functionality is needed
# _RESOURCES_DOC_DIR = None

# cx_Freeze frozen support
# See http://cx-freeze.readthedocs.io/en/latest/faq.html#using-data-files
if getattr(sys, "frozen", False):
    # Running in a frozen application:
    # We expect resources to be located either in a silx/resources/ dir
    # relative to the executable or within this package.
    _dir = os.path.join(os.path.dirname(sys.executable), "tomwer", "resources")
    if os.path.isdir(_dir):
        _RESOURCES_DIR = _dir


# Manage resource files life-cycle
_file_manager = contextlib.ExitStack()
atexit.register(_file_manager.close)


class _ResourceDirectory(NamedTuple):
    """Store a source of resources"""

    package_name: str
    forced_path: Optional[str] = None


_TOMWER_DIRECTORY = _ResourceDirectory(
    package_name=__name__,
    forced_path=_RESOURCES_DIR,
)

_RESOURCE_DIRECTORIES = {}
_RESOURCE_DIRECTORIES["tomwer"] = _TOMWER_DIRECTORY


def _get_package_and_resource(resource, default_directory=None):
    """
    Return the resource directory class and a cleaned resource name without
    prefix.

    :param str: resource: Name of the resource with resource prefix.
    :param str default_directory: If the resource is not prefixed, the resource
        will be searched on this default directory of the silx resource
        directory.
    :rtype: tuple(_ResourceDirectory, str)
    :raises ValueError: If the resource name uses an unregistred resource
        directory name
    """
    if ":" in resource:
        prefix, resource = resource.split(":", 1)
    else:
        prefix = "tomwer"
        if default_directory is not None:
            resource = f"{default_directory}/{resource}"
    if prefix not in _RESOURCE_DIRECTORIES:
        raise ValueError("Resource '%s' uses an unregistred prefix", resource)
    resource_directory = _RESOURCE_DIRECTORIES[prefix]
    return resource_directory, resource


# Manage resource files life-cycle
_file_manager = contextlib.ExitStack()
atexit.register(_file_manager.close)


@functools.lru_cache(maxsize=None)
def _get_resource_filename(package: str, resource: str) -> str:
    """Returns path to requested resource in package

    :param package: Name of the package in which to look for the resource
    :param resource: Resource path relative to package using '/' path separator
    :return: Abolute resource path in the file system
    """
    if sys.version_info < (3, 9):
        return pkg_resources.resource_filename(package, resource)

    # Caching prevents extracting the resource twice
    file_context = importlib.resources.as_file(
        importlib.resources.files(package) / resource
    )
    path = _file_manager.enter_context(file_context)
    return str(path.absolute())


def _resource_filename(resource: str, default_directory: Optional[str] = None) -> str:
    """Return filename corresponding to resource.

    The existence of the resource is not checked.

    The resource name can be prefixed by the name of a resource directory. For
    example "silx:foo.png" identify the resource "foo.png" from the resource
    directory "silx". See also :func:`register_resource_directory`.

    :param resource: Resource path relative to resource directory
                     using '/' path separator. It can be either a file or
                     a directory.
    :param default_directory: If the resource is not prefixed, the resource
        will be searched on this default directory of the silx resource
        directory. It should only be used internally by silx.
    :return: Absolute resource path in the file system
    """
    resource_directory, resource_name = _get_package_and_resource(
        resource, default_directory=default_directory
    )

    if resource_directory.forced_path is not None:
        # if set, use this directory
        base_dir = resource_directory.forced_path
        resource_path = os.path.join(base_dir, *resource_name.split("/"))
        return resource_path

    return _get_resource_filename(resource_directory.package_name, resource_name)
