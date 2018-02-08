import connexion
import six

import json
import os

from swagger_server.models.dataset import Dataset  # noqa: E501
from swagger_server.models.datasets import Datasets  # noqa: E501
from swagger_server import util


dset_json_dir = os.path.join(os.path.dirname(__file__), '..', 'jsons')
dset_jsons = [fl for fl in os.listdir(dset_json_dir) if fl.endswith('.json')]


def get_dataset(datasetID, modality=['']):  # noqa: E501
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
            dset_modalities = []
            dset_participants = []
            dset_sessions = []
            for dset_obj in dset_contents:
                dset_modalities   += [dset_obj.get('modality')] \
                                     if dset_obj.get('modality') is not None \
                                     else []
                dset_participants += [dset_obj.get('participant')] \
                                     if dset_obj.get('participant') is not None \
                                     else []
                dset_sessions     += [dset_obj.get('session')] \
                                     if dset_obj.get('session') is not None \
                                     else []
        print(modality, len(modality))
        if modality != ['']:
            valid_modality = all(mod in dset_modalities for mod in modality)
            print(valid_modality)
            if not valid_modality:
                continue;

        dset = dset.strip('.json')
        contents[dset] = { 'modalities':   list(set(dset_modalities)),
                           'num_participants': len(set(dset_participants)),
                           'sessions':     list(set(dset_sessions)) }
    return contents


def list_datasets():  # noqa: E501
    """List all accessable datasets

    Will return information about the available datasets # noqa: E501


    :rtype: List[Datasets]
    """
    return 'do some magic!'
