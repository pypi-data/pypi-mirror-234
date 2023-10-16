try:
    __import__("pkg_resources").declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path

    __path__ = extend_path(__path__, __name__)
# orangecontrib is a namespace modules shared by multiple Orange add-on so it
# needs to declare namespace.
