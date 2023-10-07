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


class AlgoEvent(object):
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
        'algorithm_id': 'str',
        'algo_name': 'str',
        'require_heartbeat_every_seconds': 'int',
        'instance_id': 'str',
        'instance_parameters': 'object',
        'portfolio_id': 'str',
        'emitted_at': 'datetime',
        'stop_status_text': 'str',
        'action': 'AlgoStatus'
    }

    attribute_map = {
        'message_class': 'messageClass',
        'algorithm_id': 'algorithm_id',
        'algo_name': 'algo_name',
        'require_heartbeat_every_seconds': 'require_heartbeat_every_seconds',
        'instance_id': 'instance_id',
        'instance_parameters': 'instance_parameters',
        'portfolio_id': 'portfolio_id',
        'emitted_at': 'emittedAt',
        'stop_status_text': 'stop_status_text',
        'action': 'action'
    }

    def __init__(self, message_class=None, algorithm_id=None, algo_name=None, require_heartbeat_every_seconds=None, instance_id=None, instance_parameters=None, portfolio_id=None, emitted_at=None, stop_status_text=None, action=None, local_vars_configuration=None):  # noqa: E501
        """AlgoEvent - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._message_class = None
        self._algorithm_id = None
        self._algo_name = None
        self._require_heartbeat_every_seconds = None
        self._instance_id = None
        self._instance_parameters = None
        self._portfolio_id = None
        self._emitted_at = None
        self._stop_status_text = None
        self._action = None
        self.discriminator = None

        if message_class is not None:
            self.message_class = message_class
        if algorithm_id is not None:
            self.algorithm_id = algorithm_id
        if algo_name is not None:
            self.algo_name = algo_name
        if require_heartbeat_every_seconds is not None:
            self.require_heartbeat_every_seconds = require_heartbeat_every_seconds
        if instance_id is not None:
            self.instance_id = instance_id
        if instance_parameters is not None:
            self.instance_parameters = instance_parameters
        if portfolio_id is not None:
            self.portfolio_id = portfolio_id
        if emitted_at is not None:
            self.emitted_at = emitted_at
        if stop_status_text is not None:
            self.stop_status_text = stop_status_text
        if action is not None:
            self.action = action

    @property
    def message_class(self):
        """Gets the message_class of this AlgoEvent.  # noqa: E501


        :return: The message_class of this AlgoEvent.  # noqa: E501
        :rtype: str
        """
        return self._message_class

    @message_class.setter
    def message_class(self, message_class):
        """Sets the message_class of this AlgoEvent.


        :param message_class: The message_class of this AlgoEvent.  # noqa: E501
        :type message_class: str
        """

        self._message_class = message_class

    @property
    def algorithm_id(self):
        """Gets the algorithm_id of this AlgoEvent.  # noqa: E501


        :return: The algorithm_id of this AlgoEvent.  # noqa: E501
        :rtype: str
        """
        return self._algorithm_id

    @algorithm_id.setter
    def algorithm_id(self, algorithm_id):
        """Sets the algorithm_id of this AlgoEvent.


        :param algorithm_id: The algorithm_id of this AlgoEvent.  # noqa: E501
        :type algorithm_id: str
        """

        self._algorithm_id = algorithm_id

    @property
    def algo_name(self):
        """Gets the algo_name of this AlgoEvent.  # noqa: E501


        :return: The algo_name of this AlgoEvent.  # noqa: E501
        :rtype: str
        """
        return self._algo_name

    @algo_name.setter
    def algo_name(self, algo_name):
        """Sets the algo_name of this AlgoEvent.


        :param algo_name: The algo_name of this AlgoEvent.  # noqa: E501
        :type algo_name: str
        """

        self._algo_name = algo_name

    @property
    def require_heartbeat_every_seconds(self):
        """Gets the require_heartbeat_every_seconds of this AlgoEvent.  # noqa: E501


        :return: The require_heartbeat_every_seconds of this AlgoEvent.  # noqa: E501
        :rtype: int
        """
        return self._require_heartbeat_every_seconds

    @require_heartbeat_every_seconds.setter
    def require_heartbeat_every_seconds(self, require_heartbeat_every_seconds):
        """Sets the require_heartbeat_every_seconds of this AlgoEvent.


        :param require_heartbeat_every_seconds: The require_heartbeat_every_seconds of this AlgoEvent.  # noqa: E501
        :type require_heartbeat_every_seconds: int
        """

        self._require_heartbeat_every_seconds = require_heartbeat_every_seconds

    @property
    def instance_id(self):
        """Gets the instance_id of this AlgoEvent.  # noqa: E501


        :return: The instance_id of this AlgoEvent.  # noqa: E501
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this AlgoEvent.


        :param instance_id: The instance_id of this AlgoEvent.  # noqa: E501
        :type instance_id: str
        """

        self._instance_id = instance_id

    @property
    def instance_parameters(self):
        """Gets the instance_parameters of this AlgoEvent.  # noqa: E501


        :return: The instance_parameters of this AlgoEvent.  # noqa: E501
        :rtype: object
        """
        return self._instance_parameters

    @instance_parameters.setter
    def instance_parameters(self, instance_parameters):
        """Sets the instance_parameters of this AlgoEvent.


        :param instance_parameters: The instance_parameters of this AlgoEvent.  # noqa: E501
        :type instance_parameters: object
        """

        self._instance_parameters = instance_parameters

    @property
    def portfolio_id(self):
        """Gets the portfolio_id of this AlgoEvent.  # noqa: E501


        :return: The portfolio_id of this AlgoEvent.  # noqa: E501
        :rtype: str
        """
        return self._portfolio_id

    @portfolio_id.setter
    def portfolio_id(self, portfolio_id):
        """Sets the portfolio_id of this AlgoEvent.


        :param portfolio_id: The portfolio_id of this AlgoEvent.  # noqa: E501
        :type portfolio_id: str
        """

        self._portfolio_id = portfolio_id

    @property
    def emitted_at(self):
        """Gets the emitted_at of this AlgoEvent.  # noqa: E501


        :return: The emitted_at of this AlgoEvent.  # noqa: E501
        :rtype: datetime
        """
        return self._emitted_at

    @emitted_at.setter
    def emitted_at(self, emitted_at):
        """Sets the emitted_at of this AlgoEvent.


        :param emitted_at: The emitted_at of this AlgoEvent.  # noqa: E501
        :type emitted_at: datetime
        """

        self._emitted_at = emitted_at

    @property
    def stop_status_text(self):
        """Gets the stop_status_text of this AlgoEvent.  # noqa: E501


        :return: The stop_status_text of this AlgoEvent.  # noqa: E501
        :rtype: str
        """
        return self._stop_status_text

    @stop_status_text.setter
    def stop_status_text(self, stop_status_text):
        """Sets the stop_status_text of this AlgoEvent.


        :param stop_status_text: The stop_status_text of this AlgoEvent.  # noqa: E501
        :type stop_status_text: str
        """

        self._stop_status_text = stop_status_text

    @property
    def action(self):
        """Gets the action of this AlgoEvent.  # noqa: E501


        :return: The action of this AlgoEvent.  # noqa: E501
        :rtype: AlgoStatus
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this AlgoEvent.


        :param action: The action of this AlgoEvent.  # noqa: E501
        :type action: AlgoStatus
        """

        self._action = action

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
        if not isinstance(other, AlgoEvent):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AlgoEvent):
            return True

        return self.to_dict() != other.to_dict()
