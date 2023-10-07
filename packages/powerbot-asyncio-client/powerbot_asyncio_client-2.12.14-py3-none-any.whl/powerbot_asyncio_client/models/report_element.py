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

from powerbot_asyncio_client.configuration import Configuration


class ReportElement(object):
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
        'delivery_start': 'datetime',
        'delivery_end': 'datetime',
        'net_position': 'float',
        'absolute_position': 'float',
        'net_cash_position': 'float',
        'buy_quantity': 'float',
        'sell_quantity': 'float',
        'average_buy_price': 'float',
        'average_sell_price': 'float',
        'trades': 'list[Trade]',
        'internal_trades': 'list[InternalTrade]',
        'position_short_hour': 'float',
        'position_short_half_hour': 'float',
        'position_short_quarter_hour': 'float',
        'position_long_hour': 'float',
        'position_long_half_hour': 'float',
        'position_long_quarter_hour': 'float',
        'position_short': 'float',
        'position_long': 'float',
        'position_sources': 'list[PositionSource]'
    }

    attribute_map = {
        'delivery_start': 'delivery_start',
        'delivery_end': 'delivery_end',
        'net_position': 'net_position',
        'absolute_position': 'absolute_position',
        'net_cash_position': 'net_cash_position',
        'buy_quantity': 'buy_quantity',
        'sell_quantity': 'sell_quantity',
        'average_buy_price': 'average_buy_price',
        'average_sell_price': 'average_sell_price',
        'trades': 'trades',
        'internal_trades': 'internal_trades',
        'position_short_hour': 'position_short_hour',
        'position_short_half_hour': 'position_short_half_hour',
        'position_short_quarter_hour': 'position_short_quarter_hour',
        'position_long_hour': 'position_long_hour',
        'position_long_half_hour': 'position_long_half_hour',
        'position_long_quarter_hour': 'position_long_quarter_hour',
        'position_short': 'position_short',
        'position_long': 'position_long',
        'position_sources': 'position_sources'
    }

    def __init__(self, delivery_start=None, delivery_end=None, net_position=None, absolute_position=None, net_cash_position=None, buy_quantity=None, sell_quantity=None, average_buy_price=None, average_sell_price=None, trades=None, internal_trades=None, position_short_hour=None, position_short_half_hour=None, position_short_quarter_hour=None, position_long_hour=None, position_long_half_hour=None, position_long_quarter_hour=None, position_short=None, position_long=None, position_sources=None, local_vars_configuration=None):  # noqa: E501
        """ReportElement - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._delivery_start = None
        self._delivery_end = None
        self._net_position = None
        self._absolute_position = None
        self._net_cash_position = None
        self._buy_quantity = None
        self._sell_quantity = None
        self._average_buy_price = None
        self._average_sell_price = None
        self._trades = None
        self._internal_trades = None
        self._position_short_hour = None
        self._position_short_half_hour = None
        self._position_short_quarter_hour = None
        self._position_long_hour = None
        self._position_long_half_hour = None
        self._position_long_quarter_hour = None
        self._position_short = None
        self._position_long = None
        self._position_sources = None
        self.discriminator = None

        if delivery_start is not None:
            self.delivery_start = delivery_start
        if delivery_end is not None:
            self.delivery_end = delivery_end
        if net_position is not None:
            self.net_position = net_position
        if absolute_position is not None:
            self.absolute_position = absolute_position
        if net_cash_position is not None:
            self.net_cash_position = net_cash_position
        if buy_quantity is not None:
            self.buy_quantity = buy_quantity
        if sell_quantity is not None:
            self.sell_quantity = sell_quantity
        if average_buy_price is not None:
            self.average_buy_price = average_buy_price
        if average_sell_price is not None:
            self.average_sell_price = average_sell_price
        if trades is not None:
            self.trades = trades
        if internal_trades is not None:
            self.internal_trades = internal_trades
        if position_short_hour is not None:
            self.position_short_hour = position_short_hour
        if position_short_half_hour is not None:
            self.position_short_half_hour = position_short_half_hour
        if position_short_quarter_hour is not None:
            self.position_short_quarter_hour = position_short_quarter_hour
        if position_long_hour is not None:
            self.position_long_hour = position_long_hour
        if position_long_half_hour is not None:
            self.position_long_half_hour = position_long_half_hour
        if position_long_quarter_hour is not None:
            self.position_long_quarter_hour = position_long_quarter_hour
        if position_short is not None:
            self.position_short = position_short
        if position_long is not None:
            self.position_long = position_long
        if position_sources is not None:
            self.position_sources = position_sources

    @property
    def delivery_start(self):
        """Gets the delivery_start of this ReportElement.  # noqa: E501


        :return: The delivery_start of this ReportElement.  # noqa: E501
        :rtype: datetime
        """
        return self._delivery_start

    @delivery_start.setter
    def delivery_start(self, delivery_start):
        """Sets the delivery_start of this ReportElement.


        :param delivery_start: The delivery_start of this ReportElement.  # noqa: E501
        :type delivery_start: datetime
        """

        self._delivery_start = delivery_start

    @property
    def delivery_end(self):
        """Gets the delivery_end of this ReportElement.  # noqa: E501


        :return: The delivery_end of this ReportElement.  # noqa: E501
        :rtype: datetime
        """
        return self._delivery_end

    @delivery_end.setter
    def delivery_end(self, delivery_end):
        """Sets the delivery_end of this ReportElement.


        :param delivery_end: The delivery_end of this ReportElement.  # noqa: E501
        :type delivery_end: datetime
        """

        self._delivery_end = delivery_end

    @property
    def net_position(self):
        """Gets the net_position of this ReportElement.  # noqa: E501


        :return: The net_position of this ReportElement.  # noqa: E501
        :rtype: float
        """
        return self._net_position

    @net_position.setter
    def net_position(self, net_position):
        """Sets the net_position of this ReportElement.


        :param net_position: The net_position of this ReportElement.  # noqa: E501
        :type net_position: float
        """

        self._net_position = net_position

    @property
    def absolute_position(self):
        """Gets the absolute_position of this ReportElement.  # noqa: E501


        :return: The absolute_position of this ReportElement.  # noqa: E501
        :rtype: float
        """
        return self._absolute_position

    @absolute_position.setter
    def absolute_position(self, absolute_position):
        """Sets the absolute_position of this ReportElement.


        :param absolute_position: The absolute_position of this ReportElement.  # noqa: E501
        :type absolute_position: float
        """

        self._absolute_position = absolute_position

    @property
    def net_cash_position(self):
        """Gets the net_cash_position of this ReportElement.  # noqa: E501


        :return: The net_cash_position of this ReportElement.  # noqa: E501
        :rtype: float
        """
        return self._net_cash_position

    @net_cash_position.setter
    def net_cash_position(self, net_cash_position):
        """Sets the net_cash_position of this ReportElement.


        :param net_cash_position: The net_cash_position of this ReportElement.  # noqa: E501
        :type net_cash_position: float
        """

        self._net_cash_position = net_cash_position

    @property
    def buy_quantity(self):
        """Gets the buy_quantity of this ReportElement.  # noqa: E501

        Total buy quantity for this time period in MW  # noqa: E501

        :return: The buy_quantity of this ReportElement.  # noqa: E501
        :rtype: float
        """
        return self._buy_quantity

    @buy_quantity.setter
    def buy_quantity(self, buy_quantity):
        """Sets the buy_quantity of this ReportElement.

        Total buy quantity for this time period in MW  # noqa: E501

        :param buy_quantity: The buy_quantity of this ReportElement.  # noqa: E501
        :type buy_quantity: float
        """

        self._buy_quantity = buy_quantity

    @property
    def sell_quantity(self):
        """Gets the sell_quantity of this ReportElement.  # noqa: E501

        Total sell quantity for this time period in MW  # noqa: E501

        :return: The sell_quantity of this ReportElement.  # noqa: E501
        :rtype: float
        """
        return self._sell_quantity

    @sell_quantity.setter
    def sell_quantity(self, sell_quantity):
        """Sets the sell_quantity of this ReportElement.

        Total sell quantity for this time period in MW  # noqa: E501

        :param sell_quantity: The sell_quantity of this ReportElement.  # noqa: E501
        :type sell_quantity: float
        """

        self._sell_quantity = sell_quantity

    @property
    def average_buy_price(self):
        """Gets the average_buy_price of this ReportElement.  # noqa: E501


        :return: The average_buy_price of this ReportElement.  # noqa: E501
        :rtype: float
        """
        return self._average_buy_price

    @average_buy_price.setter
    def average_buy_price(self, average_buy_price):
        """Sets the average_buy_price of this ReportElement.


        :param average_buy_price: The average_buy_price of this ReportElement.  # noqa: E501
        :type average_buy_price: float
        """

        self._average_buy_price = average_buy_price

    @property
    def average_sell_price(self):
        """Gets the average_sell_price of this ReportElement.  # noqa: E501


        :return: The average_sell_price of this ReportElement.  # noqa: E501
        :rtype: float
        """
        return self._average_sell_price

    @average_sell_price.setter
    def average_sell_price(self, average_sell_price):
        """Sets the average_sell_price of this ReportElement.


        :param average_sell_price: The average_sell_price of this ReportElement.  # noqa: E501
        :type average_sell_price: float
        """

        self._average_sell_price = average_sell_price

    @property
    def trades(self):
        """Gets the trades of this ReportElement.  # noqa: E501


        :return: The trades of this ReportElement.  # noqa: E501
        :rtype: list[Trade]
        """
        return self._trades

    @trades.setter
    def trades(self, trades):
        """Sets the trades of this ReportElement.


        :param trades: The trades of this ReportElement.  # noqa: E501
        :type trades: list[Trade]
        """

        self._trades = trades

    @property
    def internal_trades(self):
        """Gets the internal_trades of this ReportElement.  # noqa: E501


        :return: The internal_trades of this ReportElement.  # noqa: E501
        :rtype: list[InternalTrade]
        """
        return self._internal_trades

    @internal_trades.setter
    def internal_trades(self, internal_trades):
        """Sets the internal_trades of this ReportElement.


        :param internal_trades: The internal_trades of this ReportElement.  # noqa: E501
        :type internal_trades: list[InternalTrade]
        """

        self._internal_trades = internal_trades

    @property
    def position_short_hour(self):
        """Gets the position_short_hour of this ReportElement.  # noqa: E501

        DEPRECATED, replaced by position_sources  # noqa: E501

        :return: The position_short_hour of this ReportElement.  # noqa: E501
        :rtype: float
        """
        return self._position_short_hour

    @position_short_hour.setter
    def position_short_hour(self, position_short_hour):
        """Sets the position_short_hour of this ReportElement.

        DEPRECATED, replaced by position_sources  # noqa: E501

        :param position_short_hour: The position_short_hour of this ReportElement.  # noqa: E501
        :type position_short_hour: float
        """

        self._position_short_hour = position_short_hour

    @property
    def position_short_half_hour(self):
        """Gets the position_short_half_hour of this ReportElement.  # noqa: E501

        DEPRECATED, replaced by position_sources  # noqa: E501

        :return: The position_short_half_hour of this ReportElement.  # noqa: E501
        :rtype: float
        """
        return self._position_short_half_hour

    @position_short_half_hour.setter
    def position_short_half_hour(self, position_short_half_hour):
        """Sets the position_short_half_hour of this ReportElement.

        DEPRECATED, replaced by position_sources  # noqa: E501

        :param position_short_half_hour: The position_short_half_hour of this ReportElement.  # noqa: E501
        :type position_short_half_hour: float
        """

        self._position_short_half_hour = position_short_half_hour

    @property
    def position_short_quarter_hour(self):
        """Gets the position_short_quarter_hour of this ReportElement.  # noqa: E501

        DEPRECATED, replaced by position_sources  # noqa: E501

        :return: The position_short_quarter_hour of this ReportElement.  # noqa: E501
        :rtype: float
        """
        return self._position_short_quarter_hour

    @position_short_quarter_hour.setter
    def position_short_quarter_hour(self, position_short_quarter_hour):
        """Sets the position_short_quarter_hour of this ReportElement.

        DEPRECATED, replaced by position_sources  # noqa: E501

        :param position_short_quarter_hour: The position_short_quarter_hour of this ReportElement.  # noqa: E501
        :type position_short_quarter_hour: float
        """

        self._position_short_quarter_hour = position_short_quarter_hour

    @property
    def position_long_hour(self):
        """Gets the position_long_hour of this ReportElement.  # noqa: E501

        DEPRECATED, replaced by position_sources  # noqa: E501

        :return: The position_long_hour of this ReportElement.  # noqa: E501
        :rtype: float
        """
        return self._position_long_hour

    @position_long_hour.setter
    def position_long_hour(self, position_long_hour):
        """Sets the position_long_hour of this ReportElement.

        DEPRECATED, replaced by position_sources  # noqa: E501

        :param position_long_hour: The position_long_hour of this ReportElement.  # noqa: E501
        :type position_long_hour: float
        """

        self._position_long_hour = position_long_hour

    @property
    def position_long_half_hour(self):
        """Gets the position_long_half_hour of this ReportElement.  # noqa: E501

        DEPRECATED, replaced by position_sources  # noqa: E501

        :return: The position_long_half_hour of this ReportElement.  # noqa: E501
        :rtype: float
        """
        return self._position_long_half_hour

    @position_long_half_hour.setter
    def position_long_half_hour(self, position_long_half_hour):
        """Sets the position_long_half_hour of this ReportElement.

        DEPRECATED, replaced by position_sources  # noqa: E501

        :param position_long_half_hour: The position_long_half_hour of this ReportElement.  # noqa: E501
        :type position_long_half_hour: float
        """

        self._position_long_half_hour = position_long_half_hour

    @property
    def position_long_quarter_hour(self):
        """Gets the position_long_quarter_hour of this ReportElement.  # noqa: E501

        DEPRECATED, replaced by position_sources  # noqa: E501

        :return: The position_long_quarter_hour of this ReportElement.  # noqa: E501
        :rtype: float
        """
        return self._position_long_quarter_hour

    @position_long_quarter_hour.setter
    def position_long_quarter_hour(self, position_long_quarter_hour):
        """Sets the position_long_quarter_hour of this ReportElement.

        DEPRECATED, replaced by position_sources  # noqa: E501

        :param position_long_quarter_hour: The position_long_quarter_hour of this ReportElement.  # noqa: E501
        :type position_long_quarter_hour: float
        """

        self._position_long_quarter_hour = position_long_quarter_hour

    @property
    def position_short(self):
        """Gets the position_short of this ReportElement.  # noqa: E501


        :return: The position_short of this ReportElement.  # noqa: E501
        :rtype: float
        """
        return self._position_short

    @position_short.setter
    def position_short(self, position_short):
        """Sets the position_short of this ReportElement.


        :param position_short: The position_short of this ReportElement.  # noqa: E501
        :type position_short: float
        """

        self._position_short = position_short

    @property
    def position_long(self):
        """Gets the position_long of this ReportElement.  # noqa: E501


        :return: The position_long of this ReportElement.  # noqa: E501
        :rtype: float
        """
        return self._position_long

    @position_long.setter
    def position_long(self, position_long):
        """Sets the position_long of this ReportElement.


        :param position_long: The position_long of this ReportElement.  # noqa: E501
        :type position_long: float
        """

        self._position_long = position_long

    @property
    def position_sources(self):
        """Gets the position_sources of this ReportElement.  # noqa: E501


        :return: The position_sources of this ReportElement.  # noqa: E501
        :rtype: list[PositionSource]
        """
        return self._position_sources

    @position_sources.setter
    def position_sources(self, position_sources):
        """Sets the position_sources of this ReportElement.


        :param position_sources: The position_sources of this ReportElement.  # noqa: E501
        :type position_sources: list[PositionSource]
        """

        self._position_sources = position_sources

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
        if not isinstance(other, ReportElement):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ReportElement):
            return True

        return self.to_dict() != other.to_dict()
