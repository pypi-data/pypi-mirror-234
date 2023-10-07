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


class PortfolioChanges(object):
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
        'message_class': 'str',
        'portfolio_id': 'str',
        'delivery_area': 'str',
        'algo_changes': 'list[AlgoEvent]',
        'signal_changes': 'list[SignalChanges]',
        'own_trade_changes': 'list[OwnTradeChanges]',
        'own_order_changes': 'list[OwnOrderChanges]',
        'order_book_changes': 'list[OrderBookChanges]',
        'contract_changes': 'list[ContractChangedEvent]',
        'public_trade_changes': 'list[PublicTradeChanges]'
    }

    attribute_map = {
        'message_class': 'messageClass',
        'portfolio_id': 'portfolio_id',
        'delivery_area': 'delivery_area',
        'algo_changes': 'algoChanges',
        'signal_changes': 'signalChanges',
        'own_trade_changes': 'ownTradeChanges',
        'own_order_changes': 'ownOrderChanges',
        'order_book_changes': 'orderBookChanges',
        'contract_changes': 'contractChanges',
        'public_trade_changes': 'publicTradeChanges'
    }

    def __init__(self, message_class=None, portfolio_id=None, delivery_area=None, algo_changes=None, signal_changes=None, own_trade_changes=None, own_order_changes=None, order_book_changes=None, contract_changes=None, public_trade_changes=None, local_vars_configuration=None):  # noqa: E501
        """PortfolioChanges - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._message_class = None
        self._portfolio_id = None
        self._delivery_area = None
        self._algo_changes = None
        self._signal_changes = None
        self._own_trade_changes = None
        self._own_order_changes = None
        self._order_book_changes = None
        self._contract_changes = None
        self._public_trade_changes = None
        self.discriminator = None

        if message_class is not None:
            self.message_class = message_class
        if portfolio_id is not None:
            self.portfolio_id = portfolio_id
        if delivery_area is not None:
            self.delivery_area = delivery_area
        if algo_changes is not None:
            self.algo_changes = algo_changes
        if signal_changes is not None:
            self.signal_changes = signal_changes
        if own_trade_changes is not None:
            self.own_trade_changes = own_trade_changes
        if own_order_changes is not None:
            self.own_order_changes = own_order_changes
        if order_book_changes is not None:
            self.order_book_changes = order_book_changes
        if contract_changes is not None:
            self.contract_changes = contract_changes
        if public_trade_changes is not None:
            self.public_trade_changes = public_trade_changes

    @property
    def message_class(self):
        """Gets the message_class of this PortfolioChanges.  # noqa: E501


        :return: The message_class of this PortfolioChanges.  # noqa: E501
        :rtype: str
        """
        return self._message_class

    @message_class.setter
    def message_class(self, message_class):
        """Sets the message_class of this PortfolioChanges.


        :param message_class: The message_class of this PortfolioChanges.  # noqa: E501
        :type message_class: str
        """

        self._message_class = message_class

    @property
    def portfolio_id(self):
        """Gets the portfolio_id of this PortfolioChanges.  # noqa: E501


        :return: The portfolio_id of this PortfolioChanges.  # noqa: E501
        :rtype: str
        """
        return self._portfolio_id

    @portfolio_id.setter
    def portfolio_id(self, portfolio_id):
        """Sets the portfolio_id of this PortfolioChanges.


        :param portfolio_id: The portfolio_id of this PortfolioChanges.  # noqa: E501
        :type portfolio_id: str
        """

        self._portfolio_id = portfolio_id

    @property
    def delivery_area(self):
        """Gets the delivery_area of this PortfolioChanges.  # noqa: E501


        :return: The delivery_area of this PortfolioChanges.  # noqa: E501
        :rtype: str
        """
        return self._delivery_area

    @delivery_area.setter
    def delivery_area(self, delivery_area):
        """Sets the delivery_area of this PortfolioChanges.


        :param delivery_area: The delivery_area of this PortfolioChanges.  # noqa: E501
        :type delivery_area: str
        """

        self._delivery_area = delivery_area

    @property
    def algo_changes(self):
        """Gets the algo_changes of this PortfolioChanges.  # noqa: E501


        :return: The algo_changes of this PortfolioChanges.  # noqa: E501
        :rtype: list[AlgoEvent]
        """
        return self._algo_changes

    @algo_changes.setter
    def algo_changes(self, algo_changes):
        """Sets the algo_changes of this PortfolioChanges.


        :param algo_changes: The algo_changes of this PortfolioChanges.  # noqa: E501
        :type algo_changes: list[AlgoEvent]
        """

        self._algo_changes = algo_changes

    @property
    def signal_changes(self):
        """Gets the signal_changes of this PortfolioChanges.  # noqa: E501


        :return: The signal_changes of this PortfolioChanges.  # noqa: E501
        :rtype: list[SignalChanges]
        """
        return self._signal_changes

    @signal_changes.setter
    def signal_changes(self, signal_changes):
        """Sets the signal_changes of this PortfolioChanges.


        :param signal_changes: The signal_changes of this PortfolioChanges.  # noqa: E501
        :type signal_changes: list[SignalChanges]
        """

        self._signal_changes = signal_changes

    @property
    def own_trade_changes(self):
        """Gets the own_trade_changes of this PortfolioChanges.  # noqa: E501


        :return: The own_trade_changes of this PortfolioChanges.  # noqa: E501
        :rtype: list[OwnTradeChanges]
        """
        return self._own_trade_changes

    @own_trade_changes.setter
    def own_trade_changes(self, own_trade_changes):
        """Sets the own_trade_changes of this PortfolioChanges.


        :param own_trade_changes: The own_trade_changes of this PortfolioChanges.  # noqa: E501
        :type own_trade_changes: list[OwnTradeChanges]
        """

        self._own_trade_changes = own_trade_changes

    @property
    def own_order_changes(self):
        """Gets the own_order_changes of this PortfolioChanges.  # noqa: E501


        :return: The own_order_changes of this PortfolioChanges.  # noqa: E501
        :rtype: list[OwnOrderChanges]
        """
        return self._own_order_changes

    @own_order_changes.setter
    def own_order_changes(self, own_order_changes):
        """Sets the own_order_changes of this PortfolioChanges.


        :param own_order_changes: The own_order_changes of this PortfolioChanges.  # noqa: E501
        :type own_order_changes: list[OwnOrderChanges]
        """

        self._own_order_changes = own_order_changes

    @property
    def order_book_changes(self):
        """Gets the order_book_changes of this PortfolioChanges.  # noqa: E501


        :return: The order_book_changes of this PortfolioChanges.  # noqa: E501
        :rtype: list[OrderBookChanges]
        """
        return self._order_book_changes

    @order_book_changes.setter
    def order_book_changes(self, order_book_changes):
        """Sets the order_book_changes of this PortfolioChanges.


        :param order_book_changes: The order_book_changes of this PortfolioChanges.  # noqa: E501
        :type order_book_changes: list[OrderBookChanges]
        """

        self._order_book_changes = order_book_changes

    @property
    def contract_changes(self):
        """Gets the contract_changes of this PortfolioChanges.  # noqa: E501


        :return: The contract_changes of this PortfolioChanges.  # noqa: E501
        :rtype: list[ContractChangedEvent]
        """
        return self._contract_changes

    @contract_changes.setter
    def contract_changes(self, contract_changes):
        """Sets the contract_changes of this PortfolioChanges.


        :param contract_changes: The contract_changes of this PortfolioChanges.  # noqa: E501
        :type contract_changes: list[ContractChangedEvent]
        """

        self._contract_changes = contract_changes

    @property
    def public_trade_changes(self):
        """Gets the public_trade_changes of this PortfolioChanges.  # noqa: E501


        :return: The public_trade_changes of this PortfolioChanges.  # noqa: E501
        :rtype: list[PublicTradeChanges]
        """
        return self._public_trade_changes

    @public_trade_changes.setter
    def public_trade_changes(self, public_trade_changes):
        """Sets the public_trade_changes of this PortfolioChanges.


        :param public_trade_changes: The public_trade_changes of this PortfolioChanges.  # noqa: E501
        :type public_trade_changes: list[PublicTradeChanges]
        """

        self._public_trade_changes = public_trade_changes

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
        if not isinstance(other, PortfolioChanges):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PortfolioChanges):
            return True

        return self.to_dict() != other.to_dict()
