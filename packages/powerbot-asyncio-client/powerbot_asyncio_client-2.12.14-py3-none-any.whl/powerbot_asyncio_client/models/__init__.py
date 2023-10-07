# coding: utf-8

# flake8: noqa
"""
    PowerBot - Webservice for algotrading

    # TERMS AND CONDITIONS The PowerBot system provides B2B services for trading at intraday power markets. By using the PowerBot service, each user agrees to the terms and conditions of this licence: 1. The user confirms that they are familiar with the exchanges trading system and all relevant rules, is professionally qualified and in possession of a trading license for the relevant exchange. 2. The user will comply with the exchanges market rules (e.g. [EPEX Spot Market Rules](https://www.epexspot.com/en/downloads#rules-fees-processes) or [Nord Pool Market Rules](https://www.nordpoolgroup.com/trading/Rules-and-regulations/)) and will not endanger the exchange system at any time with heavy load from trading algorithms or by other use. 3. The user is aware of limits imposed by the exchange. 4. The user is solely liable for actions resulting from the use of PowerBot.   # INTRODUCTION PowerBot is a web-based software service enabling algorithmic trading on intraday power exchanges such as EPEX, Nord Pool, HUPX, BSP Southpool or TGE. The service is straightforward to integrate in an existing software environment and provides a variety of programming interfaces for development of individual trading algorithms and software tools. Besides enabling fully automated intraday trading, it can be used to create tools for human traders providing relevant information and trading opportunities or can be integrated in existing software tools. For further details see https://www.powerbot-trading.com  ## Knowledge Base In addition to this API guide, please find the documentation at https://docs.powerbot-trading.com - the password will be provided by the PowerBot team. If not, please reach out to us at support@powerbot-trading.com  ## Endpoints The PowerBot service is available at the following REST endpoints:  | Instance                | Base URL for REST Endpoints                                           | |-------------------------|-----------------------------------------------------------------------| | Test (EPEX)             | https://staging.powerbot-trading.com/playground/epex/v2/api           | | Test (Nord Pool)        | https://staging.powerbot-trading.com/playground/nordpool/v2/api       | | Test (HUPX)             | https://staging.powerbot-trading.com/playground/hupx/v2/api           | | Test (BSP Southpool)    | https://staging.powerbot-trading.com/playground/southpool/v2/api      | | Test (TGE)              | https://staging.powerbot-trading.com/playground/tge/v2/api            | | Test (IBEX)             | https://staging.powerbot-trading.com/playground/ibex/v2/api           | | Test (CROPEX)           | https://staging.powerbot-trading.com/playground/cropex/v2/api         | | Staging, Production     | Provided on request                                                   |  Access to endpoints is secured via an API Key, which needs to be passed as an \"api_key\" header in each request.   Notes on API Keys:  * API keys are specific to Test, Staging or Production.  * API keys are generated by the system administrator and need to be requested.  ## How to generate API clients (libraries) This OpenAPI specification can be used to generate API clients (programming libraries) for a wide range of programming languages using tools like [OpenAPI Generator](https://openapi-generator.tech/). A detailed guide can be found in the [knowledge base](https://docs.powerbot-trading.com/articles/getting-started/generating-clients/).  ## PowerBot Python client For Python, a ready-made client is also available on PyPI and can be downloaded locally via:  ```shell   pip install powerbot-client ```  ## Errors The API uses standard HTTP status codes to indicate the success or failure of the API call. The body of the response will be in JSON format as follows:  ``` {   \"message\": \"... an error message ...\" } ```  ## Paging The API uses offset and limit parameters for paged operations. An X-Total-Count header is added to responses to indicate the total number of items in a paged response.  ## Cross-Origin Resource Sharing This API features Cross-Origin Resource Sharing (CORS) implemented in compliance with  [W3C spec](https://www.w3.org/TR/cors/). This allows cross-domain communication from the browser. All responses have a wildcard same-origin which makes them completely public and accessible to everyone, including any code on any site.  ## API Rate Limiting The API limits the number of concurrent calls to 50 - when that limit is reached, the client will receive 503 http status codes (service unavailable) with the following text:  ``` {   \"message\": \"API rate limit exceeded\" } ``` Clients should ensure that they stay within the limit for concurrent API calls.    ## Additional code samples Additional information and code samples demonstrating the use of the API can be found at https://github.com/powerbot-trading.  # noqa: E501

    The version of the OpenAPI document: 2.12.14
    Contact: office@powerbot-trading.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

# import models into model package
from powerbot_asyncio_client.models.aggressor_indicator import AggressorIndicator
from powerbot_asyncio_client.models.algo_command import AlgoCommand
from powerbot_asyncio_client.models.algo_details import AlgoDetails
from powerbot_asyncio_client.models.algo_event import AlgoEvent
from powerbot_asyncio_client.models.algo_heartbeat import AlgoHeartbeat
from powerbot_asyncio_client.models.algo_instance import AlgoInstance
from powerbot_asyncio_client.models.algo_instance_change import AlgoInstanceChange
from powerbot_asyncio_client.models.algo_instance_event import AlgoInstanceEvent
from powerbot_asyncio_client.models.algo_instance_parameters import AlgoInstanceParameters
from powerbot_asyncio_client.models.algo_setup import AlgoSetup
from powerbot_asyncio_client.models.algo_status import AlgoStatus
from powerbot_asyncio_client.models.api_key import ApiKey
from powerbot_asyncio_client.models.api_key_details import ApiKeyDetails
from powerbot_asyncio_client.models.api_key_portfolio_update import ApiKeyPortfolioUpdate
from powerbot_asyncio_client.models.api_key_type import ApiKeyType
from powerbot_asyncio_client.models.atc_status import AtcStatus
from powerbot_asyncio_client.models.audit_log_entry import AuditLogEntry
from powerbot_asyncio_client.models.bulk_contract_statistics import BulkContractStatistics
from powerbot_asyncio_client.models.bulk_signal import BulkSignal
from powerbot_asyncio_client.models.bulk_signal_response import BulkSignalResponse
from powerbot_asyncio_client.models.capacity import Capacity
from powerbot_asyncio_client.models.capacity_changes import CapacityChanges
from powerbot_asyncio_client.models.cash_limit import CashLimit
from powerbot_asyncio_client.models.changed_credentials import ChangedCredentials
from powerbot_asyncio_client.models.contract import Contract
from powerbot_asyncio_client.models.contract_changed_event import ContractChangedEvent
from powerbot_asyncio_client.models.contract_history_item import ContractHistoryItem
from powerbot_asyncio_client.models.contract_item import ContractItem
from powerbot_asyncio_client.models.contract_reference import ContractReference
from powerbot_asyncio_client.models.contract_statistics import ContractStatistics
from powerbot_asyncio_client.models.contract_type import ContractType
from powerbot_asyncio_client.models.credentials import Credentials
from powerbot_asyncio_client.models.delivery_area import DeliveryArea
from powerbot_asyncio_client.models.delivery_area_state import DeliveryAreaState
from powerbot_asyncio_client.models.error_response import ErrorResponse
from powerbot_asyncio_client.models.exchange import Exchange
from powerbot_asyncio_client.models.exchange_cash_limit import ExchangeCashLimit
from powerbot_asyncio_client.models.execution_instruction import ExecutionInstruction
from powerbot_asyncio_client.models.ip_allowlist_entry import IPAllowlistEntry
from powerbot_asyncio_client.models.initialization import Initialization
from powerbot_asyncio_client.models.instance_heartbeat_status import InstanceHeartbeatStatus
from powerbot_asyncio_client.models.internal_trade import InternalTrade
from powerbot_asyncio_client.models.limit_violation import LimitViolation
from powerbot_asyncio_client.models.log_entry import LogEntry
from powerbot_asyncio_client.models.log_entry_added import LogEntryAdded
from powerbot_asyncio_client.models.market_mode import MarketMode
from powerbot_asyncio_client.models.market_options import MarketOptions
from powerbot_asyncio_client.models.market_state import MarketState
from powerbot_asyncio_client.models.market_status import MarketStatus
from powerbot_asyncio_client.models.market_status_changed_event import MarketStatusChangedEvent
from powerbot_asyncio_client.models.message import Message
from powerbot_asyncio_client.models.new_api_key import NewApiKey
from powerbot_asyncio_client.models.new_internal_trade import NewInternalTrade
from powerbot_asyncio_client.models.new_portfolio import NewPortfolio
from powerbot_asyncio_client.models.new_tenant import NewTenant
from powerbot_asyncio_client.models.notification import Notification
from powerbot_asyncio_client.models.on_missing_heartbeat import OnMissingHeartbeat
from powerbot_asyncio_client.models.order_action import OrderAction
from powerbot_asyncio_client.models.order_action_quota_limit import OrderActionQuotaLimit
from powerbot_asyncio_client.models.order_book import OrderBook
from powerbot_asyncio_client.models.order_book_bulk_statistics import OrderBookBulkStatistics
from powerbot_asyncio_client.models.order_book_changed_event import OrderBookChangedEvent
from powerbot_asyncio_client.models.order_book_changes import OrderBookChanges
from powerbot_asyncio_client.models.order_book_depth_value import OrderBookDepthValue
from powerbot_asyncio_client.models.order_book_entry import OrderBookEntry
from powerbot_asyncio_client.models.order_book_group import OrderBookGroup
from powerbot_asyncio_client.models.order_book_statistics import OrderBookStatistics
from powerbot_asyncio_client.models.order_book_statistics_contract import OrderBookStatisticsContract
from powerbot_asyncio_client.models.order_books import OrderBooks
from powerbot_asyncio_client.models.order_entry import OrderEntry
from powerbot_asyncio_client.models.order_execution_restriction import OrderExecutionRestriction
from powerbot_asyncio_client.models.order_modify import OrderModify
from powerbot_asyncio_client.models.order_modify_item import OrderModifyItem
from powerbot_asyncio_client.models.order_side import OrderSide
from powerbot_asyncio_client.models.order_state import OrderState
from powerbot_asyncio_client.models.order_type import OrderType
from powerbot_asyncio_client.models.orders import Orders
from powerbot_asyncio_client.models.otr_limit import OtrLimit
from powerbot_asyncio_client.models.own_order import OwnOrder
from powerbot_asyncio_client.models.own_order_changed_event import OwnOrderChangedEvent
from powerbot_asyncio_client.models.own_order_changes import OwnOrderChanges
from powerbot_asyncio_client.models.own_trade_changes import OwnTradeChanges
from powerbot_asyncio_client.models.portfolio import Portfolio
from powerbot_asyncio_client.models.portfolio_changes import PortfolioChanges
from powerbot_asyncio_client.models.portfolio_information import PortfolioInformation
from powerbot_asyncio_client.models.portfolio_type import PortfolioType
from powerbot_asyncio_client.models.position_limit import PositionLimit
from powerbot_asyncio_client.models.position_source import PositionSource
from powerbot_asyncio_client.models.position_source_value import PositionSourceValue
from powerbot_asyncio_client.models.product_information import ProductInformation
from powerbot_asyncio_client.models.public_trade import PublicTrade
from powerbot_asyncio_client.models.public_trade_changes import PublicTradeChanges
from powerbot_asyncio_client.models.related_contract import RelatedContract
from powerbot_asyncio_client.models.report import Report
from powerbot_asyncio_client.models.report_element import ReportElement
from powerbot_asyncio_client.models.requests import Requests
from powerbot_asyncio_client.models.resources import Resources
from powerbot_asyncio_client.models.risk_management_settings import RiskManagementSettings
from powerbot_asyncio_client.models.risk_settings_and_portfolio_information import RiskSettingsAndPortfolioInformation
from powerbot_asyncio_client.models.schedule_format import ScheduleFormat
from powerbot_asyncio_client.models.severity import Severity
from powerbot_asyncio_client.models.signal import Signal
from powerbot_asyncio_client.models.signal_changes import SignalChanges
from powerbot_asyncio_client.models.signal_entry import SignalEntry
from powerbot_asyncio_client.models.signal_entry_response import SignalEntryResponse
from powerbot_asyncio_client.models.signal_entry_result import SignalEntryResult
from powerbot_asyncio_client.models.signal_search_item import SignalSearchItem
from powerbot_asyncio_client.models.signal_search_result import SignalSearchResult
from powerbot_asyncio_client.models.signal_source_durations import SignalSourceDurations
from powerbot_asyncio_client.models.signal_time_slice import SignalTimeSlice
from powerbot_asyncio_client.models.subscription_endpoint import SubscriptionEndpoint
from powerbot_asyncio_client.models.tenant import Tenant
from powerbot_asyncio_client.models.text_matching_mode import TextMatchingMode
from powerbot_asyncio_client.models.time_slice_entry import TimeSliceEntry
from powerbot_asyncio_client.models.trade import Trade
from powerbot_asyncio_client.models.trade_changed_event import TradeChangedEvent
from powerbot_asyncio_client.models.trade_state import TradeState
from powerbot_asyncio_client.models.trading_area import TradingArea
from powerbot_asyncio_client.models.update_algo_setup import UpdateAlgoSetup
from powerbot_asyncio_client.models.update_instance_request import UpdateInstanceRequest
from powerbot_asyncio_client.models.update_status import UpdateStatus
from powerbot_asyncio_client.models.updated_api_key import UpdatedApiKey
from powerbot_asyncio_client.models.updated_portfolio import UpdatedPortfolio
from powerbot_asyncio_client.models.updated_tenant import UpdatedTenant
from powerbot_asyncio_client.models.validation_schema import ValidationSchema
from powerbot_asyncio_client.models.validation_schema_type import ValidationSchemaType
from powerbot_asyncio_client.models.validity_restriction import ValidityRestriction
