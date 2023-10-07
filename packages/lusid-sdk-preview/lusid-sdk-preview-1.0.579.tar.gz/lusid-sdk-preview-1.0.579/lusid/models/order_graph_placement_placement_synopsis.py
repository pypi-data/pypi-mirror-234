# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 1.0.579
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from lusid.configuration import Configuration


class OrderGraphPlacementPlacementSynopsis(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'details': 'list[OrderGraphPlacementChildPlacementDetail]',
        'quantity': 'float'
    }

    attribute_map = {
        'details': 'details',
        'quantity': 'quantity'
    }

    required_map = {
        'details': 'required',
        'quantity': 'required'
    }

    def __init__(self, details=None, quantity=None, local_vars_configuration=None):  # noqa: E501
        """OrderGraphPlacementPlacementSynopsis - a model defined in OpenAPI"
        
        :param details:  Identifiers for each child placement for this placement. (required)
        :type details: list[lusid.OrderGraphPlacementChildPlacementDetail]
        :param quantity:  Total number of units placed. (required)
        :type quantity: float

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._details = None
        self._quantity = None
        self.discriminator = None

        self.details = details
        self.quantity = quantity

    @property
    def details(self):
        """Gets the details of this OrderGraphPlacementPlacementSynopsis.  # noqa: E501

        Identifiers for each child placement for this placement.  # noqa: E501

        :return: The details of this OrderGraphPlacementPlacementSynopsis.  # noqa: E501
        :rtype: list[lusid.OrderGraphPlacementChildPlacementDetail]
        """
        return self._details

    @details.setter
    def details(self, details):
        """Sets the details of this OrderGraphPlacementPlacementSynopsis.

        Identifiers for each child placement for this placement.  # noqa: E501

        :param details: The details of this OrderGraphPlacementPlacementSynopsis.  # noqa: E501
        :type details: list[lusid.OrderGraphPlacementChildPlacementDetail]
        """
        if self.local_vars_configuration.client_side_validation and details is None:  # noqa: E501
            raise ValueError("Invalid value for `details`, must not be `None`")  # noqa: E501

        self._details = details

    @property
    def quantity(self):
        """Gets the quantity of this OrderGraphPlacementPlacementSynopsis.  # noqa: E501

        Total number of units placed.  # noqa: E501

        :return: The quantity of this OrderGraphPlacementPlacementSynopsis.  # noqa: E501
        :rtype: float
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of this OrderGraphPlacementPlacementSynopsis.

        Total number of units placed.  # noqa: E501

        :param quantity: The quantity of this OrderGraphPlacementPlacementSynopsis.  # noqa: E501
        :type quantity: float
        """
        if self.local_vars_configuration.client_side_validation and quantity is None:  # noqa: E501
            raise ValueError("Invalid value for `quantity`, must not be `None`")  # noqa: E501

        self._quantity = quantity

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, OrderGraphPlacementPlacementSynopsis):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrderGraphPlacementPlacementSynopsis):
            return True

        return self.to_dict() != other.to_dict()
