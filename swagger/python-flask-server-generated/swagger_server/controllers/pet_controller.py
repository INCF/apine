import connexion
import six

from swagger_server.models.pet import Pet  # noqa: E501
from swagger_server import util


def find_pets_by_tags(tags):  # noqa: E501
    """Finds Pets by tags

    Muliple tags can be provided with comma separated strings. Use\\ \\ tag1, tag2, tag3 for testing. # noqa: E501

    :param tags: Tags to filter by
    :type tags: List[str]

    :rtype: List[Pet]
    """
    return 'do some magic!'


def get_pet_by_id(petId):  # noqa: E501
    """Find pet by ID

    Returns a single pet # noqa: E501

    :param petId: ID of pet to return
    :type petId: int

    :rtype: Pet
    """
    return 'do some magic!'
