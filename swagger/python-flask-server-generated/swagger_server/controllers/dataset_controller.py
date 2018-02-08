import connexion
import six

import json
import os

from swagger_server.models.dataset import Dataset  # noqa: E501
from swagger_server.models.datasets import Datasets  # noqa: E501
from swagger_server import util


dset_json_dir = os.path.join(os.path.dirname(__file__), '..', 'jsons')
dset_jsons = [fl for fl in os.listdir(dset_json_dir) if fl.endswith('.json')]


def get_dataset(datasetID, modality=[''], session=[''], filename_key=['']):
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
            dset_fnamekeys = []
            for dset_obj in dset_contents:
                dset_modalities    += [dset_obj.get('modality')] \
                                      if dset_obj.get('modality') is not None \
                                      else []
                dset_participants  += [dset_obj.get('participant')] \
                                      if dset_obj.get('participant') is not None \
                                      else []
                dset_sessions      += [dset_obj.get('session')] \
                                      if dset_obj.get('session') is not None \
                                      else []
                dset_fnamekeys     += dset_obj.get('filename_keys') \
                                      if dset_obj.get('filename_keys') is not None \
                                      else []

        print(filename_key, len(filename_key))
        if modality != ['']:  # Requires all of the modalities to be present
            valid_modality = all(mod in dset_modalities for mod in modality)
            if not valid_modality:
                continue;

        if session != ['']:  # Requires any of the sessions to be present
            valid_session = any(ses in dset_sessions for ses in session)
            if not valid_session:
                continue

        if filename_key != ['']:  # Requires all of the keys to be present
            valid_fkey = all(any(fkey in dset_fkey for dset_fkey in dset_fnamekeys)
                             for fkey in set(filename_key))
            if not valid_fkey:
                continue

        dset = dset.strip('.json')
        contents[dset] = { 'modalities':       list(set(dset_modalities)),
                           'num_participants': len(set(dset_participants)),
                           'sessions':         list(set(dset_sessions)),
                           'filename_keys':    list(set(dset_fnamekeys))}
    return contents


def list_datasets():  # noqa: E501
    """List all accessable datasets

    Will return information about the available datasets # noqa: E501


    :rtype: List[Datasets]
    """
    return 'do some magic!'
