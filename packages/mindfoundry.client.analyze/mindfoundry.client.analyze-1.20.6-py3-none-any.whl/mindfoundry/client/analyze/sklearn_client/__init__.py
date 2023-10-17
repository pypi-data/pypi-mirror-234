# The sklearn-like API
# Types for the sklearn-like API
from ..utils.typing import PathLike
from . import model, prediction, test
from .connection import Connection, ConnectionLike
from .data_set import DataLike, DataSet, load_data_set_from_server
from .model import load_model, load_model_from_server
from .prediction import load_prediction_from_server
from .test import load_test_from_server
