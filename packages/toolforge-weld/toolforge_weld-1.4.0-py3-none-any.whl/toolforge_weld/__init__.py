import pkg_resources

try:
    __version__: str = pkg_resources.get_distribution("toolforge_weld").version
except pkg_resources.DistributionNotFound:
    __version__ = "0.0.0"
