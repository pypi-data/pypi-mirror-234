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


class OwnOrder(object):
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
        'order_id': 'str',
        'revision_no': 'int',
        'api_timestamp': 'datetime',
        'state': 'OrderState',
        'delivery_area': 'str',
        'last_change_timestamp': 'datetime',
        'buy': 'bool',
        'sell': 'bool',
        'side': 'OrderSide',
        'contracts': 'list[ContractReference]',
        'delivery_start': 'datetime',
        'delivery_end': 'datetime',
        'cl_ordr_id': 'str',
        'txt': 'str',
        'portfolio_id': 'str',
        'price': 'float',
        'quantity': 'float',
        'hidden_quantity': 'float',
        'display_quantity': 'float',
        'peak_price_delta': 'float',
        'action': 'OrderAction',
        'type': 'OrderType',
        'details': 'object',
        'user_code': 'str',
        'pre_arranged': 'bool',
        'pre_arranged_acct': 'str',
        'error_message': 'str',
        'location': 'str',
        'valid_until': 'datetime',
        'account_id': 'str'
    }

    attribute_map = {
        'order_id': 'order_id',
        'revision_no': 'revision_no',
        'api_timestamp': 'api_timestamp',
        'state': 'state',
        'delivery_area': 'delivery_area',
        'last_change_timestamp': 'last_change_timestamp',
        'buy': 'buy',
        'sell': 'sell',
        'side': 'side',
        'contracts': 'contracts',
        'delivery_start': 'delivery_start',
        'delivery_end': 'delivery_end',
        'cl_ordr_id': 'clOrdrId',
        'txt': 'txt',
        'portfolio_id': 'portfolio_id',
        'price': 'price',
        'quantity': 'quantity',
        'hidden_quantity': 'hidden_quantity',
        'display_quantity': 'display_quantity',
        'peak_price_delta': 'peak_price_delta',
        'action': 'action',
        'type': 'type',
        'details': 'details',
        'user_code': 'user_code',
        'pre_arranged': 'pre_arranged',
        'pre_arranged_acct': 'pre_arranged_acct',
        'error_message': 'error_message',
        'location': 'location',
        'valid_until': 'valid_until',
        'account_id': 'account_id'
    }

    def __init__(self, order_id=None, revision_no=None, api_timestamp=None, state=None, delivery_area=None, last_change_timestamp=None, buy=None, sell=None, side=None, contracts=None, delivery_start=None, delivery_end=None, cl_ordr_id=None, txt=None, portfolio_id=None, price=None, quantity=None, hidden_quantity=None, display_quantity=None, peak_price_delta=None, action=None, type=None, details=None, user_code=None, pre_arranged=None, pre_arranged_acct=None, error_message=None, location=None, valid_until=None, account_id=None, local_vars_configuration=None):  # noqa: E501
        """OwnOrder - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._order_id = None
        self._revision_no = None
        self._api_timestamp = None
        self._state = None
        self._delivery_area = None
        self._last_change_timestamp = None
        self._buy = None
        self._sell = None
        self._side = None
        self._contracts = None
        self._delivery_start = None
        self._delivery_end = None
        self._cl_ordr_id = None
        self._txt = None
        self._portfolio_id = None
        self._price = None
        self._quantity = None
        self._hidden_quantity = None
        self._display_quantity = None
        self._peak_price_delta = None
        self._action = None
        self._type = None
        self._details = None
        self._user_code = None
        self._pre_arranged = None
        self._pre_arranged_acct = None
        self._error_message = None
        self._location = None
        self._valid_until = None
        self._account_id = None
        self.discriminator = None

        if order_id is not None:
            self.order_id = order_id
        if revision_no is not None:
            self.revision_no = revision_no
        if api_timestamp is not None:
            self.api_timestamp = api_timestamp
        self.state = state
        self.delivery_area = delivery_area
        if last_change_timestamp is not None:
            self.last_change_timestamp = last_change_timestamp
        if buy is not None:
            self.buy = buy
        if sell is not None:
            self.sell = sell
        self.side = side
        self.contracts = contracts
        if delivery_start is not None:
            self.delivery_start = delivery_start
        if delivery_end is not None:
            self.delivery_end = delivery_end
        if cl_ordr_id is not None:
            self.cl_ordr_id = cl_ordr_id
        if txt is not None:
            self.txt = txt
        if portfolio_id is not None:
            self.portfolio_id = portfolio_id
        if price is not None:
            self.price = price
        if quantity is not None:
            self.quantity = quantity
        if hidden_quantity is not None:
            self.hidden_quantity = hidden_quantity
        if display_quantity is not None:
            self.display_quantity = display_quantity
        if peak_price_delta is not None:
            self.peak_price_delta = peak_price_delta
        self.action = action
        if type is not None:
            self.type = type
        if details is not None:
            self.details = details
        if user_code is not None:
            self.user_code = user_code
        if pre_arranged is not None:
            self.pre_arranged = pre_arranged
        if pre_arranged_acct is not None:
            self.pre_arranged_acct = pre_arranged_acct
        if error_message is not None:
            self.error_message = error_message
        if location is not None:
            self.location = location
        if valid_until is not None:
            self.valid_until = valid_until
        if account_id is not None:
            self.account_id = account_id

    @property
    def order_id(self):
        """Gets the order_id of this OwnOrder.  # noqa: E501

        the unique id of the order. **Note** if you modify an order, the id will change!  # noqa: E501

        :return: The order_id of this OwnOrder.  # noqa: E501
        :rtype: str
        """
        return self._order_id

    @order_id.setter
    def order_id(self, order_id):
        """Sets the order_id of this OwnOrder.

        the unique id of the order. **Note** if you modify an order, the id will change!  # noqa: E501

        :param order_id: The order_id of this OwnOrder.  # noqa: E501
        :type order_id: str
        """

        self._order_id = order_id

    @property
    def revision_no(self):
        """Gets the revision_no of this OwnOrder.  # noqa: E501

        The revision number of the order. Will have to be provided in addition with the order_id when order is modified.  # noqa: E501

        :return: The revision_no of this OwnOrder.  # noqa: E501
        :rtype: int
        """
        return self._revision_no

    @revision_no.setter
    def revision_no(self, revision_no):
        """Sets the revision_no of this OwnOrder.

        The revision number of the order. Will have to be provided in addition with the order_id when order is modified.  # noqa: E501

        :param revision_no: The revision_no of this OwnOrder.  # noqa: E501
        :type revision_no: int
        """

        self._revision_no = revision_no

    @property
    def api_timestamp(self):
        """Gets the api_timestamp of this OwnOrder.  # noqa: E501

        the time (UTC) the last update of the order was received.  # noqa: E501

        :return: The api_timestamp of this OwnOrder.  # noqa: E501
        :rtype: datetime
        """
        return self._api_timestamp

    @api_timestamp.setter
    def api_timestamp(self, api_timestamp):
        """Sets the api_timestamp of this OwnOrder.

        the time (UTC) the last update of the order was received.  # noqa: E501

        :param api_timestamp: The api_timestamp of this OwnOrder.  # noqa: E501
        :type api_timestamp: datetime
        """

        self._api_timestamp = api_timestamp

    @property
    def state(self):
        """Gets the state of this OwnOrder.  # noqa: E501


        :return: The state of this OwnOrder.  # noqa: E501
        :rtype: OrderState
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this OwnOrder.


        :param state: The state of this OwnOrder.  # noqa: E501
        :type state: OrderState
        """
        if self.local_vars_configuration.client_side_validation and state is None:  # noqa: E501
            raise ValueError("Invalid value for `state`, must not be `None`")  # noqa: E501

        self._state = state

    @property
    def delivery_area(self):
        """Gets the delivery_area of this OwnOrder.  # noqa: E501

        Defines the delivery area of the order (EIC).  # noqa: E501

        :return: The delivery_area of this OwnOrder.  # noqa: E501
        :rtype: str
        """
        return self._delivery_area

    @delivery_area.setter
    def delivery_area(self, delivery_area):
        """Sets the delivery_area of this OwnOrder.

        Defines the delivery area of the order (EIC).  # noqa: E501

        :param delivery_area: The delivery_area of this OwnOrder.  # noqa: E501
        :type delivery_area: str
        """
        if self.local_vars_configuration.client_side_validation and delivery_area is None:  # noqa: E501
            raise ValueError("Invalid value for `delivery_area`, must not be `None`")  # noqa: E501

        self._delivery_area = delivery_area

    @property
    def last_change_timestamp(self):
        """Gets the last_change_timestamp of this OwnOrder.  # noqa: E501


        :return: The last_change_timestamp of this OwnOrder.  # noqa: E501
        :rtype: datetime
        """
        return self._last_change_timestamp

    @last_change_timestamp.setter
    def last_change_timestamp(self, last_change_timestamp):
        """Sets the last_change_timestamp of this OwnOrder.


        :param last_change_timestamp: The last_change_timestamp of this OwnOrder.  # noqa: E501
        :type last_change_timestamp: datetime
        """

        self._last_change_timestamp = last_change_timestamp

    @property
    def buy(self):
        """Gets the buy of this OwnOrder.  # noqa: E501

        Set to true if the order is a BUY order, false otherwise  # noqa: E501

        :return: The buy of this OwnOrder.  # noqa: E501
        :rtype: bool
        """
        return self._buy

    @buy.setter
    def buy(self, buy):
        """Sets the buy of this OwnOrder.

        Set to true if the order is a BUY order, false otherwise  # noqa: E501

        :param buy: The buy of this OwnOrder.  # noqa: E501
        :type buy: bool
        """

        self._buy = buy

    @property
    def sell(self):
        """Gets the sell of this OwnOrder.  # noqa: E501

        set to true if the order is a SELL order, false otherwise  # noqa: E501

        :return: The sell of this OwnOrder.  # noqa: E501
        :rtype: bool
        """
        return self._sell

    @sell.setter
    def sell(self, sell):
        """Sets the sell of this OwnOrder.

        set to true if the order is a SELL order, false otherwise  # noqa: E501

        :param sell: The sell of this OwnOrder.  # noqa: E501
        :type sell: bool
        """

        self._sell = sell

    @property
    def side(self):
        """Gets the side of this OwnOrder.  # noqa: E501


        :return: The side of this OwnOrder.  # noqa: E501
        :rtype: OrderSide
        """
        return self._side

    @side.setter
    def side(self, side):
        """Sets the side of this OwnOrder.


        :param side: The side of this OwnOrder.  # noqa: E501
        :type side: OrderSide
        """
        if self.local_vars_configuration.client_side_validation and side is None:  # noqa: E501
            raise ValueError("Invalid value for `side`, must not be `None`")  # noqa: E501

        self._side = side

    @property
    def contracts(self):
        """Gets the contracts of this OwnOrder.  # noqa: E501


        :return: The contracts of this OwnOrder.  # noqa: E501
        :rtype: list[ContractReference]
        """
        return self._contracts

    @contracts.setter
    def contracts(self, contracts):
        """Sets the contracts of this OwnOrder.


        :param contracts: The contracts of this OwnOrder.  # noqa: E501
        :type contracts: list[ContractReference]
        """
        if self.local_vars_configuration.client_side_validation and contracts is None:  # noqa: E501
            raise ValueError("Invalid value for `contracts`, must not be `None`")  # noqa: E501

        self._contracts = contracts

    @property
    def delivery_start(self):
        """Gets the delivery_start of this OwnOrder.  # noqa: E501

        DEPRECATED. Use the delivery_start field of the contract array (an order may be associated with multiple contracts!)  # noqa: E501

        :return: The delivery_start of this OwnOrder.  # noqa: E501
        :rtype: datetime
        """
        return self._delivery_start

    @delivery_start.setter
    def delivery_start(self, delivery_start):
        """Sets the delivery_start of this OwnOrder.

        DEPRECATED. Use the delivery_start field of the contract array (an order may be associated with multiple contracts!)  # noqa: E501

        :param delivery_start: The delivery_start of this OwnOrder.  # noqa: E501
        :type delivery_start: datetime
        """

        self._delivery_start = delivery_start

    @property
    def delivery_end(self):
        """Gets the delivery_end of this OwnOrder.  # noqa: E501

        DEPRECATED. Use the delivery_end field of the contract array (an order may be associated with multiple contracts!)  # noqa: E501

        :return: The delivery_end of this OwnOrder.  # noqa: E501
        :rtype: datetime
        """
        return self._delivery_end

    @delivery_end.setter
    def delivery_end(self, delivery_end):
        """Sets the delivery_end of this OwnOrder.

        DEPRECATED. Use the delivery_end field of the contract array (an order may be associated with multiple contracts!)  # noqa: E501

        :param delivery_end: The delivery_end of this OwnOrder.  # noqa: E501
        :type delivery_end: datetime
        """

        self._delivery_end = delivery_end

    @property
    def cl_ordr_id(self):
        """Gets the cl_ordr_id of this OwnOrder.  # noqa: E501

        The client's order number (if set during the placement of the order)  # noqa: E501

        :return: The cl_ordr_id of this OwnOrder.  # noqa: E501
        :rtype: str
        """
        return self._cl_ordr_id

    @cl_ordr_id.setter
    def cl_ordr_id(self, cl_ordr_id):
        """Sets the cl_ordr_id of this OwnOrder.

        The client's order number (if set during the placement of the order)  # noqa: E501

        :param cl_ordr_id: The cl_ordr_id of this OwnOrder.  # noqa: E501
        :type cl_ordr_id: str
        """

        self._cl_ordr_id = cl_ordr_id

    @property
    def txt(self):
        """Gets the txt of this OwnOrder.  # noqa: E501

        The client's custom text (if set during the placement of the order)  # noqa: E501

        :return: The txt of this OwnOrder.  # noqa: E501
        :rtype: str
        """
        return self._txt

    @txt.setter
    def txt(self, txt):
        """Sets the txt of this OwnOrder.

        The client's custom text (if set during the placement of the order)  # noqa: E501

        :param txt: The txt of this OwnOrder.  # noqa: E501
        :type txt: str
        """

        self._txt = txt

    @property
    def portfolio_id(self):
        """Gets the portfolio_id of this OwnOrder.  # noqa: E501


        :return: The portfolio_id of this OwnOrder.  # noqa: E501
        :rtype: str
        """
        return self._portfolio_id

    @portfolio_id.setter
    def portfolio_id(self, portfolio_id):
        """Sets the portfolio_id of this OwnOrder.


        :param portfolio_id: The portfolio_id of this OwnOrder.  # noqa: E501
        :type portfolio_id: str
        """

        self._portfolio_id = portfolio_id

    @property
    def price(self):
        """Gets the price of this OwnOrder.  # noqa: E501

        The price of the order in the contract's currency (usually EUR)  # noqa: E501

        :return: The price of this OwnOrder.  # noqa: E501
        :rtype: float
        """
        return self._price

    @price.setter
    def price(self, price):
        """Sets the price of this OwnOrder.

        The price of the order in the contract's currency (usually EUR)  # noqa: E501

        :param price: The price of this OwnOrder.  # noqa: E501
        :type price: float
        """

        self._price = price

    @property
    def quantity(self):
        """Gets the quantity of this OwnOrder.  # noqa: E501

        The quantity of the order (in the contract's quantity unit - usually MW)  # noqa: E501

        :return: The quantity of this OwnOrder.  # noqa: E501
        :rtype: float
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of this OwnOrder.

        The quantity of the order (in the contract's quantity unit - usually MW)  # noqa: E501

        :param quantity: The quantity of this OwnOrder.  # noqa: E501
        :type quantity: float
        """

        self._quantity = quantity

    @property
    def hidden_quantity(self):
        """Gets the hidden_quantity of this OwnOrder.  # noqa: E501

        Contains the hidden quantity of the Iceberg order. The total executable quantity may be calculated by adding the hidden_quantity to the quantity.  # noqa: E501

        :return: The hidden_quantity of this OwnOrder.  # noqa: E501
        :rtype: float
        """
        return self._hidden_quantity

    @hidden_quantity.setter
    def hidden_quantity(self, hidden_quantity):
        """Sets the hidden_quantity of this OwnOrder.

        Contains the hidden quantity of the Iceberg order. The total executable quantity may be calculated by adding the hidden_quantity to the quantity.  # noqa: E501

        :param hidden_quantity: The hidden_quantity of this OwnOrder.  # noqa: E501
        :type hidden_quantity: float
        """

        self._hidden_quantity = hidden_quantity

    @property
    def display_quantity(self):
        """Gets the display_quantity of this OwnOrder.  # noqa: E501

        Used to define display the quantity of an Iceberg Order.  # noqa: E501

        :return: The display_quantity of this OwnOrder.  # noqa: E501
        :rtype: float
        """
        return self._display_quantity

    @display_quantity.setter
    def display_quantity(self, display_quantity):
        """Sets the display_quantity of this OwnOrder.

        Used to define display the quantity of an Iceberg Order.  # noqa: E501

        :param display_quantity: The display_quantity of this OwnOrder.  # noqa: E501
        :type display_quantity: float
        """

        self._display_quantity = display_quantity

    @property
    def peak_price_delta(self):
        """Gets the peak_price_delta of this OwnOrder.  # noqa: E501

        The peak price delta for Iceberg orders.  # noqa: E501

        :return: The peak_price_delta of this OwnOrder.  # noqa: E501
        :rtype: float
        """
        return self._peak_price_delta

    @peak_price_delta.setter
    def peak_price_delta(self, peak_price_delta):
        """Sets the peak_price_delta of this OwnOrder.

        The peak price delta for Iceberg orders.  # noqa: E501

        :param peak_price_delta: The peak_price_delta of this OwnOrder.  # noqa: E501
        :type peak_price_delta: float
        """

        self._peak_price_delta = peak_price_delta

    @property
    def action(self):
        """Gets the action of this OwnOrder.  # noqa: E501


        :return: The action of this OwnOrder.  # noqa: E501
        :rtype: OrderAction
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this OwnOrder.


        :param action: The action of this OwnOrder.  # noqa: E501
        :type action: OrderAction
        """
        if self.local_vars_configuration.client_side_validation and action is None:  # noqa: E501
            raise ValueError("Invalid value for `action`, must not be `None`")  # noqa: E501

        self._action = action

    @property
    def type(self):
        """Gets the type of this OwnOrder.  # noqa: E501


        :return: The type of this OwnOrder.  # noqa: E501
        :rtype: OrderType
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this OwnOrder.


        :param type: The type of this OwnOrder.  # noqa: E501
        :type type: OrderType
        """

        self._type = type

    @property
    def details(self):
        """Gets the details of this OwnOrder.  # noqa: E501

        All details of the order (as received from the underlying backend system)  # noqa: E501

        :return: The details of this OwnOrder.  # noqa: E501
        :rtype: object
        """
        return self._details

    @details.setter
    def details(self, details):
        """Sets the details of this OwnOrder.

        All details of the order (as received from the underlying backend system)  # noqa: E501

        :param details: The details of this OwnOrder.  # noqa: E501
        :type details: object
        """

        self._details = details

    @property
    def user_code(self):
        """Gets the user_code of this OwnOrder.  # noqa: E501

        the exchange's user code  # noqa: E501

        :return: The user_code of this OwnOrder.  # noqa: E501
        :rtype: str
        """
        return self._user_code

    @user_code.setter
    def user_code(self, user_code):
        """Sets the user_code of this OwnOrder.

        the exchange's user code  # noqa: E501

        :param user_code: The user_code of this OwnOrder.  # noqa: E501
        :type user_code: str
        """

        self._user_code = user_code

    @property
    def pre_arranged(self):
        """Gets the pre_arranged of this OwnOrder.  # noqa: E501


        :return: The pre_arranged of this OwnOrder.  # noqa: E501
        :rtype: bool
        """
        return self._pre_arranged

    @pre_arranged.setter
    def pre_arranged(self, pre_arranged):
        """Sets the pre_arranged of this OwnOrder.


        :param pre_arranged: The pre_arranged of this OwnOrder.  # noqa: E501
        :type pre_arranged: bool
        """

        self._pre_arranged = pre_arranged

    @property
    def pre_arranged_acct(self):
        """Gets the pre_arranged_acct of this OwnOrder.  # noqa: E501


        :return: The pre_arranged_acct of this OwnOrder.  # noqa: E501
        :rtype: str
        """
        return self._pre_arranged_acct

    @pre_arranged_acct.setter
    def pre_arranged_acct(self, pre_arranged_acct):
        """Sets the pre_arranged_acct of this OwnOrder.


        :param pre_arranged_acct: The pre_arranged_acct of this OwnOrder.  # noqa: E501
        :type pre_arranged_acct: str
        """

        self._pre_arranged_acct = pre_arranged_acct

    @property
    def error_message(self):
        """Gets the error_message of this OwnOrder.  # noqa: E501


        :return: The error_message of this OwnOrder.  # noqa: E501
        :rtype: str
        """
        return self._error_message

    @error_message.setter
    def error_message(self, error_message):
        """Sets the error_message of this OwnOrder.


        :param error_message: The error_message of this OwnOrder.  # noqa: E501
        :type error_message: str
        """

        self._error_message = error_message

    @property
    def location(self):
        """Gets the location of this OwnOrder.  # noqa: E501

        Location within the delivery area.  # noqa: E501

        :return: The location of this OwnOrder.  # noqa: E501
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location):
        """Sets the location of this OwnOrder.

        Location within the delivery area.  # noqa: E501

        :param location: The location of this OwnOrder.  # noqa: E501
        :type location: str
        """

        self._location = location

    @property
    def valid_until(self):
        """Gets the valid_until of this OwnOrder.  # noqa: E501

        The timestamp (UTC) until the order is valid. Only applicable for good for session orders.  # noqa: E501

        :return: The valid_until of this OwnOrder.  # noqa: E501
        :rtype: datetime
        """
        return self._valid_until

    @valid_until.setter
    def valid_until(self, valid_until):
        """Sets the valid_until of this OwnOrder.

        The timestamp (UTC) until the order is valid. Only applicable for good for session orders.  # noqa: E501

        :param valid_until: The valid_until of this OwnOrder.  # noqa: E501
        :type valid_until: datetime
        """

        self._valid_until = valid_until

    @property
    def account_id(self):
        """Gets the account_id of this OwnOrder.  # noqa: E501

        The exchange account this order belongs to.  # noqa: E501

        :return: The account_id of this OwnOrder.  # noqa: E501
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """Sets the account_id of this OwnOrder.

        The exchange account this order belongs to.  # noqa: E501

        :param account_id: The account_id of this OwnOrder.  # noqa: E501
        :type account_id: str
        """

        self._account_id = account_id

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
        if not isinstance(other, OwnOrder):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OwnOrder):
            return True

        return self.to_dict() != other.to_dict()
