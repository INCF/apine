import connexion
import six

import json
import os

from swagger_server.models.dataset import Dataset  # noqa: E501
from swagger_server.models.datasets import Datasets  # noqa: E501
from swagger_server import util


dset_json_dir = os.path.join(os.path.dirname(__file__), '..', 'jsons')
dset_jsons = [fl for fl in os.listdir(dset_json_dir) if fl.endswith('.json')]


def get_dataset(datasetID):  # noqa: E501
    """Find a dataset

    Will return information about the specified dataset # noqa: E501

    :param datasetID: Identifier for the dataset(s) of interest
    :type datasetID: List[str]

    :rtype: List[Dataset]
    """
    datasets = [dset for di in datasetID for dset in dset_jsons if di in dset]
    contents = {}
    for dset in datasets:
        thing = json.load(open(os.path.join(dset_json_dir, dset)))
        with open(os.path.join(dset_json_dir, dset)) as fhandle:
            dset_contents = json.load(fhandle)
            modalities = []
            participants = []
            sessions = []
            for dset_obj in dset_contents:
                modalities   += [dset_obj.get('modality')] \
                                if dset_obj.get('modality') is not None \
                                else []
                participants += [dset_obj.get('participant')] \
                                if dset_obj.get('participant') is not None \
                                else []
                sessions     += [dset_obj.get('session')] \
                                if dset_obj.get('session') is not None \
                                else []

        dset = dset.strip('.json')
        contents[dset] = { 'modalities':   list(set(modalities)),
                           'participants': list(set(participants)),
                           'sessions':     list(set(sessions)) }
    return contents


def list_datasets():  # noqa: E501
    """List all accessable datasets

    Will return information about the available datasets # noqa: E501


    :rtype: List[Datasets]
    """
    return 'do some magic!'
