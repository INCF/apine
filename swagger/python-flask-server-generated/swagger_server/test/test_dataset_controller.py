# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.dataset import Dataset  # noqa: E501
from swagger_server.models.datasets import Datasets  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDatasetController(BaseTestCase):
    """DatasetController integration test stubs"""

    def test_get_dataset(self):
        """Test case for get_dataset

        Find a dataset
        """
        query_string = [('datasetID', 'available')]
        response = self.client.open(
            '/gkiar/apine-dev/0.0.1/dataset',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_datasets(self):
        """Test case for list_datasets

        List all accessable datasets
        """
        response = self.client.open(
            '/gkiar/apine-dev/0.0.1/datasets',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
