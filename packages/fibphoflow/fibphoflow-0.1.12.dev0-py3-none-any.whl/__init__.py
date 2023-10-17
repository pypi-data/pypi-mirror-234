#from importlib.metadata import version, PackageNotFoundError

#try:
#    __version__ = version("fibphoflow")
#except PackageNotFoundError:
    # If the package is not installed, don't add __version__
#    pass

#try:
#    from importlib.metadata import version, PackageNotFoundError
#except ImportError:
#    from importlib_metadata import version, PackageNotFoundError

#import setuptools_scm
from ._version import version as __version__
#from importlib.metadata import version, PackageNotFoundError

#try:
#    from importlib.metadata import version, PackageNotFoundError
#except ImportError:
#    from importlib_metadata import version, PackageNotFoundError

#try:
#    ver = version("fibphoflow")
#    print(ver)
#except PackageNotFoundError:
    # Package is not installed
#    pass