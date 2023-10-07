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


class ExDividendConfiguration(object):
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
        'use_business_days': 'bool',
        'ex_dividend_days': 'int',
        'return_negative_accrued': 'bool',
        'apply_thirty360_pay_delay': 'bool'
    }

    attribute_map = {
        'use_business_days': 'useBusinessDays',
        'ex_dividend_days': 'exDividendDays',
        'return_negative_accrued': 'returnNegativeAccrued',
        'apply_thirty360_pay_delay': 'applyThirty360PayDelay'
    }

    required_map = {
        'use_business_days': 'optional',
        'ex_dividend_days': 'required',
        'return_negative_accrued': 'optional',
        'apply_thirty360_pay_delay': 'optional'
    }

    def __init__(self, use_business_days=None, ex_dividend_days=None, return_negative_accrued=None, apply_thirty360_pay_delay=None, local_vars_configuration=None):  # noqa: E501
        """ExDividendConfiguration - a model defined in OpenAPI"
        
        :param use_business_days:  Is the ex-dividend period counted in business days or calendar days.  Defaults to true if not set.
        :type use_business_days: bool
        :param ex_dividend_days:  Number of days in the ex-dividend period.  If the settlement date falls in the ex-dividend period then the coupon paid is zero and the accrued interest is negative.  If set, this must be a non-negative number.  If not set, or set to 0, than there is no ex-dividend period. (required)
        :type ex_dividend_days: int
        :param return_negative_accrued:  Does the accrued interest go negative in the ex-dividend period, or does it go to zero.  Defaults to true if not set.
        :type return_negative_accrued: bool
        :param apply_thirty360_pay_delay:  Set this flag to true if the ex-dividend days represent a pay delay from the accrual end date in calendar  days under the 30/360 day count convention. The typical use case for this flag are Mortgage Backed Securities  with pay delay between 1 and 60 days, such as FreddieMac and FannieMae. If this flag is set, the useBusinessDays  setting will be ignored.  Defaults to false if not provided.
        :type apply_thirty360_pay_delay: bool

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._use_business_days = None
        self._ex_dividend_days = None
        self._return_negative_accrued = None
        self._apply_thirty360_pay_delay = None
        self.discriminator = None

        if use_business_days is not None:
            self.use_business_days = use_business_days
        self.ex_dividend_days = ex_dividend_days
        if return_negative_accrued is not None:
            self.return_negative_accrued = return_negative_accrued
        if apply_thirty360_pay_delay is not None:
            self.apply_thirty360_pay_delay = apply_thirty360_pay_delay

    @property
    def use_business_days(self):
        """Gets the use_business_days of this ExDividendConfiguration.  # noqa: E501

        Is the ex-dividend period counted in business days or calendar days.  Defaults to true if not set.  # noqa: E501

        :return: The use_business_days of this ExDividendConfiguration.  # noqa: E501
        :rtype: bool
        """
        return self._use_business_days

    @use_business_days.setter
    def use_business_days(self, use_business_days):
        """Sets the use_business_days of this ExDividendConfiguration.

        Is the ex-dividend period counted in business days or calendar days.  Defaults to true if not set.  # noqa: E501

        :param use_business_days: The use_business_days of this ExDividendConfiguration.  # noqa: E501
        :type use_business_days: bool
        """

        self._use_business_days = use_business_days

    @property
    def ex_dividend_days(self):
        """Gets the ex_dividend_days of this ExDividendConfiguration.  # noqa: E501

        Number of days in the ex-dividend period.  If the settlement date falls in the ex-dividend period then the coupon paid is zero and the accrued interest is negative.  If set, this must be a non-negative number.  If not set, or set to 0, than there is no ex-dividend period.  # noqa: E501

        :return: The ex_dividend_days of this ExDividendConfiguration.  # noqa: E501
        :rtype: int
        """
        return self._ex_dividend_days

    @ex_dividend_days.setter
    def ex_dividend_days(self, ex_dividend_days):
        """Sets the ex_dividend_days of this ExDividendConfiguration.

        Number of days in the ex-dividend period.  If the settlement date falls in the ex-dividend period then the coupon paid is zero and the accrued interest is negative.  If set, this must be a non-negative number.  If not set, or set to 0, than there is no ex-dividend period.  # noqa: E501

        :param ex_dividend_days: The ex_dividend_days of this ExDividendConfiguration.  # noqa: E501
        :type ex_dividend_days: int
        """
        if self.local_vars_configuration.client_side_validation and ex_dividend_days is None:  # noqa: E501
            raise ValueError("Invalid value for `ex_dividend_days`, must not be `None`")  # noqa: E501

        self._ex_dividend_days = ex_dividend_days

    @property
    def return_negative_accrued(self):
        """Gets the return_negative_accrued of this ExDividendConfiguration.  # noqa: E501

        Does the accrued interest go negative in the ex-dividend period, or does it go to zero.  Defaults to true if not set.  # noqa: E501

        :return: The return_negative_accrued of this ExDividendConfiguration.  # noqa: E501
        :rtype: bool
        """
        return self._return_negative_accrued

    @return_negative_accrued.setter
    def return_negative_accrued(self, return_negative_accrued):
        """Sets the return_negative_accrued of this ExDividendConfiguration.

        Does the accrued interest go negative in the ex-dividend period, or does it go to zero.  Defaults to true if not set.  # noqa: E501

        :param return_negative_accrued: The return_negative_accrued of this ExDividendConfiguration.  # noqa: E501
        :type return_negative_accrued: bool
        """

        self._return_negative_accrued = return_negative_accrued

    @property
    def apply_thirty360_pay_delay(self):
        """Gets the apply_thirty360_pay_delay of this ExDividendConfiguration.  # noqa: E501

        Set this flag to true if the ex-dividend days represent a pay delay from the accrual end date in calendar  days under the 30/360 day count convention. The typical use case for this flag are Mortgage Backed Securities  with pay delay between 1 and 60 days, such as FreddieMac and FannieMae. If this flag is set, the useBusinessDays  setting will be ignored.  Defaults to false if not provided.  # noqa: E501

        :return: The apply_thirty360_pay_delay of this ExDividendConfiguration.  # noqa: E501
        :rtype: bool
        """
        return self._apply_thirty360_pay_delay

    @apply_thirty360_pay_delay.setter
    def apply_thirty360_pay_delay(self, apply_thirty360_pay_delay):
        """Sets the apply_thirty360_pay_delay of this ExDividendConfiguration.

        Set this flag to true if the ex-dividend days represent a pay delay from the accrual end date in calendar  days under the 30/360 day count convention. The typical use case for this flag are Mortgage Backed Securities  with pay delay between 1 and 60 days, such as FreddieMac and FannieMae. If this flag is set, the useBusinessDays  setting will be ignored.  Defaults to false if not provided.  # noqa: E501

        :param apply_thirty360_pay_delay: The apply_thirty360_pay_delay of this ExDividendConfiguration.  # noqa: E501
        :type apply_thirty360_pay_delay: bool
        """

        self._apply_thirty360_pay_delay = apply_thirty360_pay_delay

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
        if not isinstance(other, ExDividendConfiguration):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ExDividendConfiguration):
            return True

        return self.to_dict() != other.to_dict()
