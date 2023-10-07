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


class AlgoInstanceParameters(object):
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
        'instance_id': 'str',
        'tenant_id': 'str',
        'portfolio_ids': 'list[str]',
        'parameters': 'object',
        'resources': 'Resources'
    }

    attribute_map = {
        'instance_id': 'instance_id',
        'tenant_id': 'tenant_id',
        'portfolio_ids': 'portfolio_ids',
        'parameters': 'parameters',
        'resources': 'resources'
    }

    def __init__(self, instance_id=None, tenant_id=None, portfolio_ids=None, parameters=None, resources=None, local_vars_configuration=None):  # noqa: E501
        """AlgoInstanceParameters - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._instance_id = None
        self._tenant_id = None
        self._portfolio_ids = None
        self._parameters = None
        self._resources = None
        self.discriminator = None

        self.instance_id = instance_id
        if tenant_id is not None:
            self.tenant_id = tenant_id
        if portfolio_ids is not None:
            self.portfolio_ids = portfolio_ids
        if parameters is not None:
            self.parameters = parameters
        if resources is not None:
            self.resources = resources

    @property
    def instance_id(self):
        """Gets the instance_id of this AlgoInstanceParameters.  # noqa: E501

        Unique id which needs to be provided to identify the algorithm instance.  # noqa: E501

        :return: The instance_id of this AlgoInstanceParameters.  # noqa: E501
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this AlgoInstanceParameters.

        Unique id which needs to be provided to identify the algorithm instance.  # noqa: E501

        :param instance_id: The instance_id of this AlgoInstanceParameters.  # noqa: E501
        :type instance_id: str
        """
        if self.local_vars_configuration.client_side_validation and instance_id is None:  # noqa: E501
            raise ValueError("Invalid value for `instance_id`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                instance_id is not None and not re.search(r'[a-zA-Z0-9._-]+', instance_id)):  # noqa: E501
            raise ValueError(r"Invalid value for `instance_id`, must be a follow pattern or equal to `/[a-zA-Z0-9._-]+/`")  # noqa: E501

        self._instance_id = instance_id

    @property
    def tenant_id(self):
        """Gets the tenant_id of this AlgoInstanceParameters.  # noqa: E501

        master-API-key needs to specify a tenant on creation. For tenant-master-API-keys this field is optional, as the tenant is already specified via the key.  # noqa: E501

        :return: The tenant_id of this AlgoInstanceParameters.  # noqa: E501
        :rtype: str
        """
        return self._tenant_id

    @tenant_id.setter
    def tenant_id(self, tenant_id):
        """Sets the tenant_id of this AlgoInstanceParameters.

        master-API-key needs to specify a tenant on creation. For tenant-master-API-keys this field is optional, as the tenant is already specified via the key.  # noqa: E501

        :param tenant_id: The tenant_id of this AlgoInstanceParameters.  # noqa: E501
        :type tenant_id: str
        """

        self._tenant_id = tenant_id

    @property
    def portfolio_ids(self):
        """Gets the portfolio_ids of this AlgoInstanceParameters.  # noqa: E501

        Specify the portfolios the algorithm should run in.  # noqa: E501

        :return: The portfolio_ids of this AlgoInstanceParameters.  # noqa: E501
        :rtype: list[str]
        """
        return self._portfolio_ids

    @portfolio_ids.setter
    def portfolio_ids(self, portfolio_ids):
        """Sets the portfolio_ids of this AlgoInstanceParameters.

        Specify the portfolios the algorithm should run in.  # noqa: E501

        :param portfolio_ids: The portfolio_ids of this AlgoInstanceParameters.  # noqa: E501
        :type portfolio_ids: list[str]
        """

        self._portfolio_ids = portfolio_ids

    @property
    def parameters(self):
        """Gets the parameters of this AlgoInstanceParameters.  # noqa: E501

        A freely defined JSON object with key/value pairs.  # noqa: E501

        :return: The parameters of this AlgoInstanceParameters.  # noqa: E501
        :rtype: object
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Sets the parameters of this AlgoInstanceParameters.

        A freely defined JSON object with key/value pairs.  # noqa: E501

        :param parameters: The parameters of this AlgoInstanceParameters.  # noqa: E501
        :type parameters: object
        """

        self._parameters = parameters

    @property
    def resources(self):
        """Gets the resources of this AlgoInstanceParameters.  # noqa: E501


        :return: The resources of this AlgoInstanceParameters.  # noqa: E501
        :rtype: Resources
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """Sets the resources of this AlgoInstanceParameters.


        :param resources: The resources of this AlgoInstanceParameters.  # noqa: E501
        :type resources: Resources
        """

        self._resources = resources

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
        if not isinstance(other, AlgoInstanceParameters):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AlgoInstanceParameters):
            return True

        return self.to_dict() != other.to_dict()
