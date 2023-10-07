# coding: utf-8

"""
    PowerBot - Webservice for algotrading

    # TERMS AND CONDITIONS The PowerBot system provides B2B services for trading at intraday power markets. By using the PowerBot service, each user agrees to the terms and conditions of this licence: 1. The user confirms that they are familiar with the exchanges trading system and all relevant rules, is professionally qualified and in possession of a trading license for the relevant exchange. 2. The user will comply with the exchanges market rules (e.g. [EPEX Spot Market Rules](https://www.epexspot.com/en/downloads#rules-fees-processes) or [Nord Pool Market Rules](https://www.nordpoolgroup.com/trading/Rules-and-regulations/)) and will not endanger the exchange system at any time with heavy load from trading algorithms or by other use. 3. The user is aware of limits imposed by the exchange. 4. The user is solely liable for actions resulting from the use of PowerBot.   # INTRODUCTION PowerBot is a web-based software service enabling algorithmic trading on intraday power exchanges such as EPEX, Nord Pool, HUPX, BSP Southpool or TGE. The service is straightforward to integrate in an existing software environment and provides a variety of programming interfaces for development of individual trading algorithms and software tools. Besides enabling fully automated intraday trading, it can be used to create tools for human traders providing relevant information and trading opportunities or can be integrated in existing software tools. For further details see https://www.powerbot-trading.com  ## Knowledge Base In addition to this API guide, please find the documentation at https://docs.powerbot-trading.com - the password will be provided by the PowerBot team. If not, please reach out to us at support@powerbot-trading.com  ## Endpoints The PowerBot service is available at the following REST endpoints:  | Instance                | Base URL for REST Endpoints                                           | |-------------------------|-----------------------------------------------------------------------| | Test (EPEX)             | https://staging.powerbot-trading.com/playground/epex/v2/api           | | Test (Nord Pool)        | https://staging.powerbot-trading.com/playground/nordpool/v2/api       | | Test (HUPX)             | https://staging.powerbot-trading.com/playground/hupx/v2/api           | | Test (BSP Southpool)    | https://staging.powerbot-trading.com/playground/southpool/v2/api      | | Test (TGE)              | https://staging.powerbot-trading.com/playground/tge/v2/api            | | Test (IBEX)             | https://staging.powerbot-trading.com/playground/ibex/v2/api           | | Test (CROPEX)           | https://staging.powerbot-trading.com/playground/cropex/v2/api         | | Staging, Production     | Provided on request                                                   |  Access to endpoints is secured via an API Key, which needs to be passed as an \"api_key\" header in each request.   Notes on API Keys:  * API keys are specific to Test, Staging or Production.  * API keys are generated by the system administrator and need to be requested.  ## How to generate API clients (libraries) This OpenAPI specification can be used to generate API clients (programming libraries) for a wide range of programming languages using tools like [OpenAPI Generator](https://openapi-generator.tech/). A detailed guide can be found in the [knowledge base](https://docs.powerbot-trading.com/articles/getting-started/generating-clients/).  ## PowerBot Python client For Python, a ready-made client is also available on PyPI and can be downloaded locally via:  ```shell   pip install powerbot-client ```  ## Errors The API uses standard HTTP status codes to indicate the success or failure of the API call. The body of the response will be in JSON format as follows:  ``` {   \"message\": \"... an error message ...\" } ```  ## Paging The API uses offset and limit parameters for paged operations. An X-Total-Count header is added to responses to indicate the total number of items in a paged response.  ## Cross-Origin Resource Sharing This API features Cross-Origin Resource Sharing (CORS) implemented in compliance with  [W3C spec](https://www.w3.org/TR/cors/). This allows cross-domain communication from the browser. All responses have a wildcard same-origin which makes them completely public and accessible to everyone, including any code on any site.  ## API Rate Limiting The API limits the number of concurrent calls to 50 - when that limit is reached, the client will receive 503 http status codes (service unavailable) with the following text:  ``` {   \"message\": \"API rate limit exceeded\" } ``` Clients should ensure that they stay within the limit for concurrent API calls.    ## Additional code samples Additional information and code samples demonstrating the use of the API can be found at https://github.com/powerbot-trading.  # noqa: E501

    The version of the OpenAPI document: 2.12.14
    Contact: office@powerbot-trading.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from powerbot_client.configuration import Configuration


class SignalTimeSlice(object):
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
    """
    openapi_types = {
        'active': 'bool',
        'historic': 'bool',
        'deleted': 'bool',
        'received_at': 'datetime',
        'updated_at': 'datetime',
        'minutes_to_delivery': 'int',
        'revision': 'int',
        'locked': 'bool',
        'parameters': 'object'
    }

    attribute_map = {
        'active': 'active',
        'historic': 'historic',
        'deleted': 'deleted',
        'received_at': 'received_at',
        'updated_at': 'updated_at',
        'minutes_to_delivery': 'minutes_to_delivery',
        'revision': 'revision',
        'locked': 'locked',
        'parameters': 'parameters'
    }

    def __init__(self, active=None, historic=None, deleted=None, received_at=None, updated_at=None, minutes_to_delivery=None, revision=None, locked=None, parameters=None, local_vars_configuration=None):  # noqa: E501
        """SignalTimeSlice - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._active = None
        self._historic = None
        self._deleted = None
        self._received_at = None
        self._updated_at = None
        self._minutes_to_delivery = None
        self._revision = None
        self._locked = None
        self._parameters = None
        self.discriminator = None

        if active is not None:
            self.active = active
        if historic is not None:
            self.historic = historic
        if deleted is not None:
            self.deleted = deleted
        if received_at is not None:
            self.received_at = received_at
        if updated_at is not None:
            self.updated_at = updated_at
        if minutes_to_delivery is not None:
            self.minutes_to_delivery = minutes_to_delivery
        if revision is not None:
            self.revision = revision
        if locked is not None:
            self.locked = locked
        if parameters is not None:
            self.parameters = parameters

    @property
    def active(self):
        """Gets the active of this SignalTimeSlice.  # noqa: E501

        Indicates that this time slice is currently active.  # noqa: E501

        :return: The active of this SignalTimeSlice.  # noqa: E501
        :rtype: bool
        """
        return self._active

    @active.setter
    def active(self, active):
        """Sets the active of this SignalTimeSlice.

        Indicates that this time slice is currently active.  # noqa: E501

        :param active: The active of this SignalTimeSlice.  # noqa: E501
        :type active: bool
        """

        self._active = active

    @property
    def historic(self):
        """Gets the historic of this SignalTimeSlice.  # noqa: E501

        Indicates that the time slice has been overwritten by a newer revision.  # noqa: E501

        :return: The historic of this SignalTimeSlice.  # noqa: E501
        :rtype: bool
        """
        return self._historic

    @historic.setter
    def historic(self, historic):
        """Sets the historic of this SignalTimeSlice.

        Indicates that the time slice has been overwritten by a newer revision.  # noqa: E501

        :param historic: The historic of this SignalTimeSlice.  # noqa: E501
        :type historic: bool
        """

        self._historic = historic

    @property
    def deleted(self):
        """Gets the deleted of this SignalTimeSlice.  # noqa: E501

        Indicates that the time slice was deleted.  # noqa: E501

        :return: The deleted of this SignalTimeSlice.  # noqa: E501
        :rtype: bool
        """
        return self._deleted

    @deleted.setter
    def deleted(self, deleted):
        """Sets the deleted of this SignalTimeSlice.

        Indicates that the time slice was deleted.  # noqa: E501

        :param deleted: The deleted of this SignalTimeSlice.  # noqa: E501
        :type deleted: bool
        """

        self._deleted = deleted

    @property
    def received_at(self):
        """Gets the received_at of this SignalTimeSlice.  # noqa: E501

        The timestamp when the signal was received.  # noqa: E501

        :return: The received_at of this SignalTimeSlice.  # noqa: E501
        :rtype: datetime
        """
        return self._received_at

    @received_at.setter
    def received_at(self, received_at):
        """Sets the received_at of this SignalTimeSlice.

        The timestamp when the signal was received.  # noqa: E501

        :param received_at: The received_at of this SignalTimeSlice.  # noqa: E501
        :type received_at: datetime
        """

        self._received_at = received_at

    @property
    def updated_at(self):
        """Gets the updated_at of this SignalTimeSlice.  # noqa: E501

        The timestamp when the signal was last updated. If an identical signal is received, this value will be updated without increasing the revision.  # noqa: E501

        :return: The updated_at of this SignalTimeSlice.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this SignalTimeSlice.

        The timestamp when the signal was last updated. If an identical signal is received, this value will be updated without increasing the revision.  # noqa: E501

        :param updated_at: The updated_at of this SignalTimeSlice.  # noqa: E501
        :type updated_at: datetime
        """

        self._updated_at = updated_at

    @property
    def minutes_to_delivery(self):
        """Gets the minutes_to_delivery of this SignalTimeSlice.  # noqa: E501

        The offset in minutes until delivery start, after which the signal becomes valid.  # noqa: E501

        :return: The minutes_to_delivery of this SignalTimeSlice.  # noqa: E501
        :rtype: int
        """
        return self._minutes_to_delivery

    @minutes_to_delivery.setter
    def minutes_to_delivery(self, minutes_to_delivery):
        """Sets the minutes_to_delivery of this SignalTimeSlice.

        The offset in minutes until delivery start, after which the signal becomes valid.  # noqa: E501

        :param minutes_to_delivery: The minutes_to_delivery of this SignalTimeSlice.  # noqa: E501
        :type minutes_to_delivery: int
        """

        self._minutes_to_delivery = minutes_to_delivery

    @property
    def revision(self):
        """Gets the revision of this SignalTimeSlice.  # noqa: E501

        The number of times the trading signal has been updated. If the signal has never received any updates, then revision is 0.  # noqa: E501

        :return: The revision of this SignalTimeSlice.  # noqa: E501
        :rtype: int
        """
        return self._revision

    @revision.setter
    def revision(self, revision):
        """Sets the revision of this SignalTimeSlice.

        The number of times the trading signal has been updated. If the signal has never received any updates, then revision is 0.  # noqa: E501

        :param revision: The revision of this SignalTimeSlice.  # noqa: E501
        :type revision: int
        """

        self._revision = revision

    @property
    def locked(self):
        """Gets the locked of this SignalTimeSlice.  # noqa: E501

        Locked signals can not be modified, unless the `ignore_lock` parameter is set to `true`.  # noqa: E501

        :return: The locked of this SignalTimeSlice.  # noqa: E501
        :rtype: bool
        """
        return self._locked

    @locked.setter
    def locked(self, locked):
        """Sets the locked of this SignalTimeSlice.

        Locked signals can not be modified, unless the `ignore_lock` parameter is set to `true`.  # noqa: E501

        :param locked: The locked of this SignalTimeSlice.  # noqa: E501
        :type locked: bool
        """

        self._locked = locked

    @property
    def parameters(self):
        """Gets the parameters of this SignalTimeSlice.  # noqa: E501

        The content of the signal, as key/value pairs.  # noqa: E501

        :return: The parameters of this SignalTimeSlice.  # noqa: E501
        :rtype: object
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Sets the parameters of this SignalTimeSlice.

        The content of the signal, as key/value pairs.  # noqa: E501

        :param parameters: The parameters of this SignalTimeSlice.  # noqa: E501
        :type parameters: object
        """

        self._parameters = parameters

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
        if not isinstance(other, SignalTimeSlice):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SignalTimeSlice):
            return True

        return self.to_dict() != other.to_dict()
