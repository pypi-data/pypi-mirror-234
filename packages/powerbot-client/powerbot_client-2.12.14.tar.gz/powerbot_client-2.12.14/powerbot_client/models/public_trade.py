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


class PublicTrade(object):
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
        'trade_id': 'str',
        'buy_delivery_area': 'str',
        'sell_delivery_area': 'str',
        'api_timestamp': 'datetime',
        'exec_time': 'datetime',
        'contract_id': 'str',
        'price': 'float',
        'quantity': 'float',
        'self_trade': 'bool',
        'active': 'bool',
        'state': 'str'
    }

    attribute_map = {
        'trade_id': 'trade_id',
        'buy_delivery_area': 'buy_delivery_area',
        'sell_delivery_area': 'sell_delivery_area',
        'api_timestamp': 'api_timestamp',
        'exec_time': 'exec_time',
        'contract_id': 'contract_id',
        'price': 'price',
        'quantity': 'quantity',
        'self_trade': 'self_trade',
        'active': 'active',
        'state': 'state'
    }

    def __init__(self, trade_id=None, buy_delivery_area=None, sell_delivery_area=None, api_timestamp=None, exec_time=None, contract_id=None, price=None, quantity=None, self_trade=None, active=None, state=None, local_vars_configuration=None):  # noqa: E501
        """PublicTrade - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._trade_id = None
        self._buy_delivery_area = None
        self._sell_delivery_area = None
        self._api_timestamp = None
        self._exec_time = None
        self._contract_id = None
        self._price = None
        self._quantity = None
        self._self_trade = None
        self._active = None
        self._state = None
        self.discriminator = None

        if trade_id is not None:
            self.trade_id = trade_id
        if buy_delivery_area is not None:
            self.buy_delivery_area = buy_delivery_area
        if sell_delivery_area is not None:
            self.sell_delivery_area = sell_delivery_area
        if api_timestamp is not None:
            self.api_timestamp = api_timestamp
        if exec_time is not None:
            self.exec_time = exec_time
        if contract_id is not None:
            self.contract_id = contract_id
        if price is not None:
            self.price = price
        if quantity is not None:
            self.quantity = quantity
        if self_trade is not None:
            self.self_trade = self_trade
        if active is not None:
            self.active = active
        if state is not None:
            self.state = state

    @property
    def trade_id(self):
        """Gets the trade_id of this PublicTrade.  # noqa: E501


        :return: The trade_id of this PublicTrade.  # noqa: E501
        :rtype: str
        """
        return self._trade_id

    @trade_id.setter
    def trade_id(self, trade_id):
        """Sets the trade_id of this PublicTrade.


        :param trade_id: The trade_id of this PublicTrade.  # noqa: E501
        :type trade_id: str
        """

        self._trade_id = trade_id

    @property
    def buy_delivery_area(self):
        """Gets the buy_delivery_area of this PublicTrade.  # noqa: E501


        :return: The buy_delivery_area of this PublicTrade.  # noqa: E501
        :rtype: str
        """
        return self._buy_delivery_area

    @buy_delivery_area.setter
    def buy_delivery_area(self, buy_delivery_area):
        """Sets the buy_delivery_area of this PublicTrade.


        :param buy_delivery_area: The buy_delivery_area of this PublicTrade.  # noqa: E501
        :type buy_delivery_area: str
        """

        self._buy_delivery_area = buy_delivery_area

    @property
    def sell_delivery_area(self):
        """Gets the sell_delivery_area of this PublicTrade.  # noqa: E501


        :return: The sell_delivery_area of this PublicTrade.  # noqa: E501
        :rtype: str
        """
        return self._sell_delivery_area

    @sell_delivery_area.setter
    def sell_delivery_area(self, sell_delivery_area):
        """Sets the sell_delivery_area of this PublicTrade.


        :param sell_delivery_area: The sell_delivery_area of this PublicTrade.  # noqa: E501
        :type sell_delivery_area: str
        """

        self._sell_delivery_area = sell_delivery_area

    @property
    def api_timestamp(self):
        """Gets the api_timestamp of this PublicTrade.  # noqa: E501

        The timestamp (UTC) of the information being received from the exchange  # noqa: E501

        :return: The api_timestamp of this PublicTrade.  # noqa: E501
        :rtype: datetime
        """
        return self._api_timestamp

    @api_timestamp.setter
    def api_timestamp(self, api_timestamp):
        """Sets the api_timestamp of this PublicTrade.

        The timestamp (UTC) of the information being received from the exchange  # noqa: E501

        :param api_timestamp: The api_timestamp of this PublicTrade.  # noqa: E501
        :type api_timestamp: datetime
        """

        self._api_timestamp = api_timestamp

    @property
    def exec_time(self):
        """Gets the exec_time of this PublicTrade.  # noqa: E501

        The timestamp (UTC) when the public trade was executed  # noqa: E501

        :return: The exec_time of this PublicTrade.  # noqa: E501
        :rtype: datetime
        """
        return self._exec_time

    @exec_time.setter
    def exec_time(self, exec_time):
        """Sets the exec_time of this PublicTrade.

        The timestamp (UTC) when the public trade was executed  # noqa: E501

        :param exec_time: The exec_time of this PublicTrade.  # noqa: E501
        :type exec_time: datetime
        """

        self._exec_time = exec_time

    @property
    def contract_id(self):
        """Gets the contract_id of this PublicTrade.  # noqa: E501

        The id of the contract on which the public trade was executed  # noqa: E501

        :return: The contract_id of this PublicTrade.  # noqa: E501
        :rtype: str
        """
        return self._contract_id

    @contract_id.setter
    def contract_id(self, contract_id):
        """Sets the contract_id of this PublicTrade.

        The id of the contract on which the public trade was executed  # noqa: E501

        :param contract_id: The contract_id of this PublicTrade.  # noqa: E501
        :type contract_id: str
        """

        self._contract_id = contract_id

    @property
    def price(self):
        """Gets the price of this PublicTrade.  # noqa: E501

        The price (usually in EUR, but depends on the contract) of the public trade  # noqa: E501

        :return: The price of this PublicTrade.  # noqa: E501
        :rtype: float
        """
        return self._price

    @price.setter
    def price(self, price):
        """Sets the price of this PublicTrade.

        The price (usually in EUR, but depends on the contract) of the public trade  # noqa: E501

        :param price: The price of this PublicTrade.  # noqa: E501
        :type price: float
        """

        self._price = price

    @property
    def quantity(self):
        """Gets the quantity of this PublicTrade.  # noqa: E501

        The quantity (usually in MW, but depends on the contract) of the public trade  # noqa: E501

        :return: The quantity of this PublicTrade.  # noqa: E501
        :rtype: float
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of this PublicTrade.

        The quantity (usually in MW, but depends on the contract) of the public trade  # noqa: E501

        :param quantity: The quantity of this PublicTrade.  # noqa: E501
        :type quantity: float
        """

        self._quantity = quantity

    @property
    def self_trade(self):
        """Gets the self_trade of this PublicTrade.  # noqa: E501


        :return: The self_trade of this PublicTrade.  # noqa: E501
        :rtype: bool
        """
        return self._self_trade

    @self_trade.setter
    def self_trade(self, self_trade):
        """Sets the self_trade of this PublicTrade.


        :param self_trade: The self_trade of this PublicTrade.  # noqa: E501
        :type self_trade: bool
        """

        self._self_trade = self_trade

    @property
    def active(self):
        """Gets the active of this PublicTrade.  # noqa: E501


        :return: The active of this PublicTrade.  # noqa: E501
        :rtype: bool
        """
        return self._active

    @active.setter
    def active(self, active):
        """Sets the active of this PublicTrade.


        :param active: The active of this PublicTrade.  # noqa: E501
        :type active: bool
        """

        self._active = active

    @property
    def state(self):
        """Gets the state of this PublicTrade.  # noqa: E501


        :return: The state of this PublicTrade.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this PublicTrade.


        :param state: The state of this PublicTrade.  # noqa: E501
        :type state: str
        """

        self._state = state

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
        if not isinstance(other, PublicTrade):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PublicTrade):
            return True

        return self.to_dict() != other.to_dict()
