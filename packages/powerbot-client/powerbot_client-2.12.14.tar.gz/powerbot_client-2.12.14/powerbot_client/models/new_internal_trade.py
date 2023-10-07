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


class NewInternalTrade(object):
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
        'exchange': 'str',
        'delivery_start': 'datetime',
        'delivery_end': 'datetime',
        'exec_time': 'datetime',
        'buy_delivery_area': 'str',
        'buy_txt': 'str',
        'buy_portfolio_id': 'str',
        'buy_aggressor_indicator': 'AggressorIndicator',
        'sell_delivery_area': 'str',
        'sell_txt': 'str',
        'sell_portfolio_id': 'str',
        'sell_aggressor_indicator': 'AggressorIndicator',
        'contract_id': 'str',
        'price': 'float',
        'quantity': 'float'
    }

    attribute_map = {
        'exchange': 'exchange',
        'delivery_start': 'delivery_start',
        'delivery_end': 'delivery_end',
        'exec_time': 'exec_time',
        'buy_delivery_area': 'buy_delivery_area',
        'buy_txt': 'buy_txt',
        'buy_portfolio_id': 'buy_portfolio_id',
        'buy_aggressor_indicator': 'buy_aggressor_indicator',
        'sell_delivery_area': 'sell_delivery_area',
        'sell_txt': 'sell_txt',
        'sell_portfolio_id': 'sell_portfolio_id',
        'sell_aggressor_indicator': 'sell_aggressor_indicator',
        'contract_id': 'contract_id',
        'price': 'price',
        'quantity': 'quantity'
    }

    def __init__(self, exchange=None, delivery_start=None, delivery_end=None, exec_time=None, buy_delivery_area=None, buy_txt=None, buy_portfolio_id=None, buy_aggressor_indicator=None, sell_delivery_area=None, sell_txt=None, sell_portfolio_id=None, sell_aggressor_indicator=None, contract_id=None, price=None, quantity=None, local_vars_configuration=None):  # noqa: E501
        """NewInternalTrade - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._exchange = None
        self._delivery_start = None
        self._delivery_end = None
        self._exec_time = None
        self._buy_delivery_area = None
        self._buy_txt = None
        self._buy_portfolio_id = None
        self._buy_aggressor_indicator = None
        self._sell_delivery_area = None
        self._sell_txt = None
        self._sell_portfolio_id = None
        self._sell_aggressor_indicator = None
        self._contract_id = None
        self._price = None
        self._quantity = None
        self.discriminator = None

        if exchange is not None:
            self.exchange = exchange
        if delivery_start is not None:
            self.delivery_start = delivery_start
        if delivery_end is not None:
            self.delivery_end = delivery_end
        self.exec_time = exec_time
        if buy_delivery_area is not None:
            self.buy_delivery_area = buy_delivery_area
        if buy_txt is not None:
            self.buy_txt = buy_txt
        if buy_portfolio_id is not None:
            self.buy_portfolio_id = buy_portfolio_id
        if buy_aggressor_indicator is not None:
            self.buy_aggressor_indicator = buy_aggressor_indicator
        if sell_delivery_area is not None:
            self.sell_delivery_area = sell_delivery_area
        if sell_txt is not None:
            self.sell_txt = sell_txt
        if sell_portfolio_id is not None:
            self.sell_portfolio_id = sell_portfolio_id
        if sell_aggressor_indicator is not None:
            self.sell_aggressor_indicator = sell_aggressor_indicator
        if contract_id is not None:
            self.contract_id = contract_id
        self.price = price
        self.quantity = quantity

    @property
    def exchange(self):
        """Gets the exchange of this NewInternalTrade.  # noqa: E501

        The exchange where the trade was executed  # noqa: E501

        :return: The exchange of this NewInternalTrade.  # noqa: E501
        :rtype: str
        """
        return self._exchange

    @exchange.setter
    def exchange(self, exchange):
        """Sets the exchange of this NewInternalTrade.

        The exchange where the trade was executed  # noqa: E501

        :param exchange: The exchange of this NewInternalTrade.  # noqa: E501
        :type exchange: str
        """

        self._exchange = exchange

    @property
    def delivery_start(self):
        """Gets the delivery_start of this NewInternalTrade.  # noqa: E501


        :return: The delivery_start of this NewInternalTrade.  # noqa: E501
        :rtype: datetime
        """
        return self._delivery_start

    @delivery_start.setter
    def delivery_start(self, delivery_start):
        """Sets the delivery_start of this NewInternalTrade.


        :param delivery_start: The delivery_start of this NewInternalTrade.  # noqa: E501
        :type delivery_start: datetime
        """

        self._delivery_start = delivery_start

    @property
    def delivery_end(self):
        """Gets the delivery_end of this NewInternalTrade.  # noqa: E501


        :return: The delivery_end of this NewInternalTrade.  # noqa: E501
        :rtype: datetime
        """
        return self._delivery_end

    @delivery_end.setter
    def delivery_end(self, delivery_end):
        """Sets the delivery_end of this NewInternalTrade.


        :param delivery_end: The delivery_end of this NewInternalTrade.  # noqa: E501
        :type delivery_end: datetime
        """

        self._delivery_end = delivery_end

    @property
    def exec_time(self):
        """Gets the exec_time of this NewInternalTrade.  # noqa: E501

        The timestamp when the trade was executed (UTC time zone)  # noqa: E501

        :return: The exec_time of this NewInternalTrade.  # noqa: E501
        :rtype: datetime
        """
        return self._exec_time

    @exec_time.setter
    def exec_time(self, exec_time):
        """Sets the exec_time of this NewInternalTrade.

        The timestamp when the trade was executed (UTC time zone)  # noqa: E501

        :param exec_time: The exec_time of this NewInternalTrade.  # noqa: E501
        :type exec_time: datetime
        """
        if self.local_vars_configuration.client_side_validation and exec_time is None:  # noqa: E501
            raise ValueError("Invalid value for `exec_time`, must not be `None`")  # noqa: E501

        self._exec_time = exec_time

    @property
    def buy_delivery_area(self):
        """Gets the buy_delivery_area of this NewInternalTrade.  # noqa: E501


        :return: The buy_delivery_area of this NewInternalTrade.  # noqa: E501
        :rtype: str
        """
        return self._buy_delivery_area

    @buy_delivery_area.setter
    def buy_delivery_area(self, buy_delivery_area):
        """Sets the buy_delivery_area of this NewInternalTrade.


        :param buy_delivery_area: The buy_delivery_area of this NewInternalTrade.  # noqa: E501
        :type buy_delivery_area: str
        """

        self._buy_delivery_area = buy_delivery_area

    @property
    def buy_txt(self):
        """Gets the buy_txt of this NewInternalTrade.  # noqa: E501

        The custom text of the buy order  # noqa: E501

        :return: The buy_txt of this NewInternalTrade.  # noqa: E501
        :rtype: str
        """
        return self._buy_txt

    @buy_txt.setter
    def buy_txt(self, buy_txt):
        """Sets the buy_txt of this NewInternalTrade.

        The custom text of the buy order  # noqa: E501

        :param buy_txt: The buy_txt of this NewInternalTrade.  # noqa: E501
        :type buy_txt: str
        """

        self._buy_txt = buy_txt

    @property
    def buy_portfolio_id(self):
        """Gets the buy_portfolio_id of this NewInternalTrade.  # noqa: E501


        :return: The buy_portfolio_id of this NewInternalTrade.  # noqa: E501
        :rtype: str
        """
        return self._buy_portfolio_id

    @buy_portfolio_id.setter
    def buy_portfolio_id(self, buy_portfolio_id):
        """Sets the buy_portfolio_id of this NewInternalTrade.


        :param buy_portfolio_id: The buy_portfolio_id of this NewInternalTrade.  # noqa: E501
        :type buy_portfolio_id: str
        """

        self._buy_portfolio_id = buy_portfolio_id

    @property
    def buy_aggressor_indicator(self):
        """Gets the buy_aggressor_indicator of this NewInternalTrade.  # noqa: E501


        :return: The buy_aggressor_indicator of this NewInternalTrade.  # noqa: E501
        :rtype: AggressorIndicator
        """
        return self._buy_aggressor_indicator

    @buy_aggressor_indicator.setter
    def buy_aggressor_indicator(self, buy_aggressor_indicator):
        """Sets the buy_aggressor_indicator of this NewInternalTrade.


        :param buy_aggressor_indicator: The buy_aggressor_indicator of this NewInternalTrade.  # noqa: E501
        :type buy_aggressor_indicator: AggressorIndicator
        """

        self._buy_aggressor_indicator = buy_aggressor_indicator

    @property
    def sell_delivery_area(self):
        """Gets the sell_delivery_area of this NewInternalTrade.  # noqa: E501


        :return: The sell_delivery_area of this NewInternalTrade.  # noqa: E501
        :rtype: str
        """
        return self._sell_delivery_area

    @sell_delivery_area.setter
    def sell_delivery_area(self, sell_delivery_area):
        """Sets the sell_delivery_area of this NewInternalTrade.


        :param sell_delivery_area: The sell_delivery_area of this NewInternalTrade.  # noqa: E501
        :type sell_delivery_area: str
        """

        self._sell_delivery_area = sell_delivery_area

    @property
    def sell_txt(self):
        """Gets the sell_txt of this NewInternalTrade.  # noqa: E501

        the custom text of the sell order  # noqa: E501

        :return: The sell_txt of this NewInternalTrade.  # noqa: E501
        :rtype: str
        """
        return self._sell_txt

    @sell_txt.setter
    def sell_txt(self, sell_txt):
        """Sets the sell_txt of this NewInternalTrade.

        the custom text of the sell order  # noqa: E501

        :param sell_txt: The sell_txt of this NewInternalTrade.  # noqa: E501
        :type sell_txt: str
        """

        self._sell_txt = sell_txt

    @property
    def sell_portfolio_id(self):
        """Gets the sell_portfolio_id of this NewInternalTrade.  # noqa: E501


        :return: The sell_portfolio_id of this NewInternalTrade.  # noqa: E501
        :rtype: str
        """
        return self._sell_portfolio_id

    @sell_portfolio_id.setter
    def sell_portfolio_id(self, sell_portfolio_id):
        """Sets the sell_portfolio_id of this NewInternalTrade.


        :param sell_portfolio_id: The sell_portfolio_id of this NewInternalTrade.  # noqa: E501
        :type sell_portfolio_id: str
        """

        self._sell_portfolio_id = sell_portfolio_id

    @property
    def sell_aggressor_indicator(self):
        """Gets the sell_aggressor_indicator of this NewInternalTrade.  # noqa: E501


        :return: The sell_aggressor_indicator of this NewInternalTrade.  # noqa: E501
        :rtype: AggressorIndicator
        """
        return self._sell_aggressor_indicator

    @sell_aggressor_indicator.setter
    def sell_aggressor_indicator(self, sell_aggressor_indicator):
        """Sets the sell_aggressor_indicator of this NewInternalTrade.


        :param sell_aggressor_indicator: The sell_aggressor_indicator of this NewInternalTrade.  # noqa: E501
        :type sell_aggressor_indicator: AggressorIndicator
        """

        self._sell_aggressor_indicator = sell_aggressor_indicator

    @property
    def contract_id(self):
        """Gets the contract_id of this NewInternalTrade.  # noqa: E501

        The contract_id against which the trade was executed  # noqa: E501

        :return: The contract_id of this NewInternalTrade.  # noqa: E501
        :rtype: str
        """
        return self._contract_id

    @contract_id.setter
    def contract_id(self, contract_id):
        """Sets the contract_id of this NewInternalTrade.

        The contract_id against which the trade was executed  # noqa: E501

        :param contract_id: The contract_id of this NewInternalTrade.  # noqa: E501
        :type contract_id: str
        """

        self._contract_id = contract_id

    @property
    def price(self):
        """Gets the price of this NewInternalTrade.  # noqa: E501

        Price of the trade  # noqa: E501

        :return: The price of this NewInternalTrade.  # noqa: E501
        :rtype: float
        """
        return self._price

    @price.setter
    def price(self, price):
        """Sets the price of this NewInternalTrade.

        Price of the trade  # noqa: E501

        :param price: The price of this NewInternalTrade.  # noqa: E501
        :type price: float
        """
        if self.local_vars_configuration.client_side_validation and price is None:  # noqa: E501
            raise ValueError("Invalid value for `price`, must not be `None`")  # noqa: E501

        self._price = price

    @property
    def quantity(self):
        """Gets the quantity of this NewInternalTrade.  # noqa: E501


        :return: The quantity of this NewInternalTrade.  # noqa: E501
        :rtype: float
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of this NewInternalTrade.


        :param quantity: The quantity of this NewInternalTrade.  # noqa: E501
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
        if not isinstance(other, NewInternalTrade):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, NewInternalTrade):
            return True

        return self.to_dict() != other.to_dict()
