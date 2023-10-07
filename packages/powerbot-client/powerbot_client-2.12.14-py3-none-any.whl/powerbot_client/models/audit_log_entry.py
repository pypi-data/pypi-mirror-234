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


class AuditLogEntry(object):
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
        'id': 'str',
        'received': 'datetime',
        'api_key_name': 'str',
        'ip_address': 'str',
        'tenant_id': 'str',
        'portfolio_id': 'str',
        'comment': 'str',
        'object_name': 'str',
        'old_value': 'object',
        'new_value': 'object'
    }

    attribute_map = {
        'id': 'id',
        'received': 'received',
        'api_key_name': 'api_key_name',
        'ip_address': 'ip_address',
        'tenant_id': 'tenant_id',
        'portfolio_id': 'portfolio_id',
        'comment': 'comment',
        'object_name': 'object_name',
        'old_value': 'old_value',
        'new_value': 'new_value'
    }

    def __init__(self, id=None, received=None, api_key_name=None, ip_address=None, tenant_id=None, portfolio_id=None, comment=None, object_name=None, old_value=None, new_value=None, local_vars_configuration=None):  # noqa: E501
        """AuditLogEntry - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._received = None
        self._api_key_name = None
        self._ip_address = None
        self._tenant_id = None
        self._portfolio_id = None
        self._comment = None
        self._object_name = None
        self._old_value = None
        self._new_value = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if received is not None:
            self.received = received
        if api_key_name is not None:
            self.api_key_name = api_key_name
        if ip_address is not None:
            self.ip_address = ip_address
        if tenant_id is not None:
            self.tenant_id = tenant_id
        if portfolio_id is not None:
            self.portfolio_id = portfolio_id
        if comment is not None:
            self.comment = comment
        if object_name is not None:
            self.object_name = object_name
        if old_value is not None:
            self.old_value = old_value
        if new_value is not None:
            self.new_value = new_value

    @property
    def id(self):
        """Gets the id of this AuditLogEntry.  # noqa: E501

        The unique id of the log entry  # noqa: E501

        :return: The id of this AuditLogEntry.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this AuditLogEntry.

        The unique id of the log entry  # noqa: E501

        :param id: The id of this AuditLogEntry.  # noqa: E501
        :type id: str
        """

        self._id = id

    @property
    def received(self):
        """Gets the received of this AuditLogEntry.  # noqa: E501

        The timestamp when the trading API has received the log entry. UTC timezone is used.  # noqa: E501

        :return: The received of this AuditLogEntry.  # noqa: E501
        :rtype: datetime
        """
        return self._received

    @received.setter
    def received(self, received):
        """Sets the received of this AuditLogEntry.

        The timestamp when the trading API has received the log entry. UTC timezone is used.  # noqa: E501

        :param received: The received of this AuditLogEntry.  # noqa: E501
        :type received: datetime
        """

        self._received = received

    @property
    def api_key_name(self):
        """Gets the api_key_name of this AuditLogEntry.  # noqa: E501

        The api_key from which the audit log was generated  # noqa: E501

        :return: The api_key_name of this AuditLogEntry.  # noqa: E501
        :rtype: str
        """
        return self._api_key_name

    @api_key_name.setter
    def api_key_name(self, api_key_name):
        """Sets the api_key_name of this AuditLogEntry.

        The api_key from which the audit log was generated  # noqa: E501

        :param api_key_name: The api_key_name of this AuditLogEntry.  # noqa: E501
        :type api_key_name: str
        """

        self._api_key_name = api_key_name

    @property
    def ip_address(self):
        """Gets the ip_address of this AuditLogEntry.  # noqa: E501

        The IP-address from which the audit log was generated  # noqa: E501

        :return: The ip_address of this AuditLogEntry.  # noqa: E501
        :rtype: str
        """
        return self._ip_address

    @ip_address.setter
    def ip_address(self, ip_address):
        """Sets the ip_address of this AuditLogEntry.

        The IP-address from which the audit log was generated  # noqa: E501

        :param ip_address: The ip_address of this AuditLogEntry.  # noqa: E501
        :type ip_address: str
        """

        self._ip_address = ip_address

    @property
    def tenant_id(self):
        """Gets the tenant_id of this AuditLogEntry.  # noqa: E501

        The tenant for which the log entry is applicable  # noqa: E501

        :return: The tenant_id of this AuditLogEntry.  # noqa: E501
        :rtype: str
        """
        return self._tenant_id

    @tenant_id.setter
    def tenant_id(self, tenant_id):
        """Sets the tenant_id of this AuditLogEntry.

        The tenant for which the log entry is applicable  # noqa: E501

        :param tenant_id: The tenant_id of this AuditLogEntry.  # noqa: E501
        :type tenant_id: str
        """

        self._tenant_id = tenant_id

    @property
    def portfolio_id(self):
        """Gets the portfolio_id of this AuditLogEntry.  # noqa: E501

        The portfolio for which the log entry is applicable  # noqa: E501

        :return: The portfolio_id of this AuditLogEntry.  # noqa: E501
        :rtype: str
        """
        return self._portfolio_id

    @portfolio_id.setter
    def portfolio_id(self, portfolio_id):
        """Sets the portfolio_id of this AuditLogEntry.

        The portfolio for which the log entry is applicable  # noqa: E501

        :param portfolio_id: The portfolio_id of this AuditLogEntry.  # noqa: E501
        :type portfolio_id: str
        """

        self._portfolio_id = portfolio_id

    @property
    def comment(self):
        """Gets the comment of this AuditLogEntry.  # noqa: E501

        information about the cause of the change  # noqa: E501

        :return: The comment of this AuditLogEntry.  # noqa: E501
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """Sets the comment of this AuditLogEntry.

        information about the cause of the change  # noqa: E501

        :param comment: The comment of this AuditLogEntry.  # noqa: E501
        :type comment: str
        """

        self._comment = comment

    @property
    def object_name(self):
        """Gets the object_name of this AuditLogEntry.  # noqa: E501

        the changed object  # noqa: E501

        :return: The object_name of this AuditLogEntry.  # noqa: E501
        :rtype: str
        """
        return self._object_name

    @object_name.setter
    def object_name(self, object_name):
        """Sets the object_name of this AuditLogEntry.

        the changed object  # noqa: E501

        :param object_name: The object_name of this AuditLogEntry.  # noqa: E501
        :type object_name: str
        """

        self._object_name = object_name

    @property
    def old_value(self):
        """Gets the old_value of this AuditLogEntry.  # noqa: E501

        The old value of the changed entry  # noqa: E501

        :return: The old_value of this AuditLogEntry.  # noqa: E501
        :rtype: object
        """
        return self._old_value

    @old_value.setter
    def old_value(self, old_value):
        """Sets the old_value of this AuditLogEntry.

        The old value of the changed entry  # noqa: E501

        :param old_value: The old_value of this AuditLogEntry.  # noqa: E501
        :type old_value: object
        """

        self._old_value = old_value

    @property
    def new_value(self):
        """Gets the new_value of this AuditLogEntry.  # noqa: E501

        The new value of the changed entry  # noqa: E501

        :return: The new_value of this AuditLogEntry.  # noqa: E501
        :rtype: object
        """
        return self._new_value

    @new_value.setter
    def new_value(self, new_value):
        """Sets the new_value of this AuditLogEntry.

        The new value of the changed entry  # noqa: E501

        :param new_value: The new_value of this AuditLogEntry.  # noqa: E501
        :type new_value: object
        """

        self._new_value = new_value

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
        if not isinstance(other, AuditLogEntry):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AuditLogEntry):
            return True

        return self.to_dict() != other.to_dict()
