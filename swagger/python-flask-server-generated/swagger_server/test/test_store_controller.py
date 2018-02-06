# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.order import Order  # noqa: E501
from swagger_server.test import BaseTestCase


class TestStoreController(BaseTestCase):
    """StoreController integration test stubs"""

    def test_get_inventory(self):
        """Test case for get_inventory

        Returns pet inventories by status
        """
        response = self.client.open(
            '/gkiar/apine-dev/0.0.1/store/inventory',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_order_by_id(self):
        """Test case for get_order_by_id

        Find purchase order by ID
        """
        response = self.client.open(
            '/gkiar/apine-dev/0.0.1/store/order/{orderId}'.format(orderId=10),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
