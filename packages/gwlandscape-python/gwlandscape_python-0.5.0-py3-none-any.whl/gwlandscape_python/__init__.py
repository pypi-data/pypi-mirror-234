from .gwlandscape import GWLandscape
from .keyword_type import Keyword
from .publication_type import Publication
from .model_type import Model
from .dataset_type import Dataset

from gwdc_python.files import FileReference, FileReferenceList


try:
    from importlib.metadata import version
except ModuleNotFoundError:
    from importlib_metadata import version
__version__ = version('gwlandscape_python')
