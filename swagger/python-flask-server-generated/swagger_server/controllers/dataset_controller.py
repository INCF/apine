import connexion
import six

import json
import os

from swagger_server.models.dataset import Dataset  # noqa: E501
from swagger_server.models.datasets import Datasets  # noqa: E501
from swagger_server import util

json_dir = os.path.join(os.path.dirname(__file__), '..', 'jsons')
contents = os.listdir(json_dir)


def get_dataset(datasetID):  # noqa: E501
    """Find a dataset

    Will return information about the specified dataset # noqa: E501

    :param datasetID: Identifier for the dataset(s) of interest
    :type datasetID: List[str]

    :rtype: List[Dataset]
    """
    return "({}) These ARE the IDs you're looking for: ".format(contents) + ", ".join(datasetID)


def list_datasets():  # noqa: E501
    """List all accessable datasets

    Will return information about the available datasets # noqa: E501


    :rtype: List[Datasets]
    """
    return 'do some magic!'
