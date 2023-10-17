"""
isort:skip_file
"""
from ._version import get_versions

# The sklearn-style client
from . import sklearn_client

# The swagger API
from .project_api_swagger_client import AnalyzeSwaggerClientWrapper
from . import swagger
from .client import create_project_api_client

# The published model API
from .client import PublishedApi


# pylint: disable-all
_versions_dict = get_versions()
__version__ = _versions_dict["version"]
__gitsha__ = _versions_dict["full-revisionid"]
del get_versions, _versions_dict

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
