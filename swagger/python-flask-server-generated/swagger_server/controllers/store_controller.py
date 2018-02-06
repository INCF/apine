import connexion
import six

from swagger_server.models.order import Order  # noqa: E501
from swagger_server import util


def get_inventory():  # noqa: E501
    """Returns pet inventories by status

    Returns a map of status codes to quantities # noqa: E501


    :rtype: Dict[str, int]
    """
    return 'do some magic!'


def get_order_by_id(orderId):  # noqa: E501
    """Find purchase order by ID

    For valid response try integer IDs with value &gt;&#x3D; 1 and &lt;&#x3D; 10.\\ \\ Other values will generated exceptions # noqa: E501

    :param orderId: ID of pet that needs to be fetched
    :type orderId: int

    :rtype: Order
    """
    return 'do some magic!'
