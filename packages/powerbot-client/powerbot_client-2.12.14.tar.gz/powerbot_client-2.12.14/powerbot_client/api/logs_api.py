# coding: utf-8

"""
    PowerBot - Webservice for algotrading

    # TERMS AND CONDITIONS The PowerBot system provides B2B services for trading at intraday power markets. By using the PowerBot service, each user agrees to the terms and conditions of this licence: 1. The user confirms that they are familiar with the exchanges trading system and all relevant rules, is professionally qualified and in possession of a trading license for the relevant exchange. 2. The user will comply with the exchanges market rules (e.g. [EPEX Spot Market Rules](https://www.epexspot.com/en/downloads#rules-fees-processes) or [Nord Pool Market Rules](https://www.nordpoolgroup.com/trading/Rules-and-regulations/)) and will not endanger the exchange system at any time with heavy load from trading algorithms or by other use. 3. The user is aware of limits imposed by the exchange. 4. The user is solely liable for actions resulting from the use of PowerBot.   # INTRODUCTION PowerBot is a web-based software service enabling algorithmic trading on intraday power exchanges such as EPEX, Nord Pool, HUPX, BSP Southpool or TGE. The service is straightforward to integrate in an existing software environment and provides a variety of programming interfaces for development of individual trading algorithms and software tools. Besides enabling fully automated intraday trading, it can be used to create tools for human traders providing relevant information and trading opportunities or can be integrated in existing software tools. For further details see https://www.powerbot-trading.com  ## Knowledge Base In addition to this API guide, please find the documentation at https://docs.powerbot-trading.com - the password will be provided by the PowerBot team. If not, please reach out to us at support@powerbot-trading.com  ## Endpoints The PowerBot service is available at the following REST endpoints:  | Instance                | Base URL for REST Endpoints                                           | |-------------------------|-----------------------------------------------------------------------| | Test (EPEX)             | https://staging.powerbot-trading.com/playground/epex/v2/api           | | Test (Nord Pool)        | https://staging.powerbot-trading.com/playground/nordpool/v2/api       | | Test (HUPX)             | https://staging.powerbot-trading.com/playground/hupx/v2/api           | | Test (BSP Southpool)    | https://staging.powerbot-trading.com/playground/southpool/v2/api      | | Test (TGE)              | https://staging.powerbot-trading.com/playground/tge/v2/api            | | Test (IBEX)             | https://staging.powerbot-trading.com/playground/ibex/v2/api           | | Test (CROPEX)           | https://staging.powerbot-trading.com/playground/cropex/v2/api         | | Staging, Production     | Provided on request                                                   |  Access to endpoints is secured via an API Key, which needs to be passed as an \"api_key\" header in each request.   Notes on API Keys:  * API keys are specific to Test, Staging or Production.  * API keys are generated by the system administrator and need to be requested.  ## How to generate API clients (libraries) This OpenAPI specification can be used to generate API clients (programming libraries) for a wide range of programming languages using tools like [OpenAPI Generator](https://openapi-generator.tech/). A detailed guide can be found in the [knowledge base](https://docs.powerbot-trading.com/articles/getting-started/generating-clients/).  ## PowerBot Python client For Python, a ready-made client is also available on PyPI and can be downloaded locally via:  ```shell   pip install powerbot-client ```  ## Errors The API uses standard HTTP status codes to indicate the success or failure of the API call. The body of the response will be in JSON format as follows:  ``` {   \"message\": \"... an error message ...\" } ```  ## Paging The API uses offset and limit parameters for paged operations. An X-Total-Count header is added to responses to indicate the total number of items in a paged response.  ## Cross-Origin Resource Sharing This API features Cross-Origin Resource Sharing (CORS) implemented in compliance with  [W3C spec](https://www.w3.org/TR/cors/). This allows cross-domain communication from the browser. All responses have a wildcard same-origin which makes them completely public and accessible to everyone, including any code on any site.  ## API Rate Limiting The API limits the number of concurrent calls to 50 - when that limit is reached, the client will receive 503 http status codes (service unavailable) with the following text:  ``` {   \"message\": \"API rate limit exceeded\" } ``` Clients should ensure that they stay within the limit for concurrent API calls.    ## Additional code samples Additional information and code samples demonstrating the use of the API can be found at https://github.com/powerbot-trading.  # noqa: E501

    The version of the OpenAPI document: 2.12.14
    Contact: office@powerbot-trading.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from powerbot_client.api_client import ApiClient
from powerbot_client.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class LogsApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def add_log_entry(self, value, **kwargs):  # noqa: E501
        """Add system log entry  # noqa: E501

        We provide a logging system to record internal events. You can use this method to add a log entry, which is shown in the dashboard and can also be retrieved later.  There are three different types of logs (system, tenant, portfolio), these logs can be posted from different API key types as listed below:  - scheduling-API-key without tenant -> system logs (omit portfolio_id) - scheduling-API-key with tenant -> tenant logs (omit portfolio_id - standard-API-key -> portfolio logs (specify portfolio_id) AND tenant logs (omit portfolio_id) - tenant-master-API-key -> cannot submit any logs - master-API-key -> cannot submit any logs  A log entry belongs to a freely chosen category and has a defined severity as well as a timestamp (UTC) value.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.add_log_entry(value, async_req=True)
        >>> result = thread.get()

        :param value: (required)
        :type value: LogEntry
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """
        kwargs['_return_http_data_only'] = True
        return self.add_log_entry_with_http_info(value, **kwargs)  # noqa: E501

    def add_log_entry_with_http_info(self, value, **kwargs):  # noqa: E501
        """Add system log entry  # noqa: E501

        We provide a logging system to record internal events. You can use this method to add a log entry, which is shown in the dashboard and can also be retrieved later.  There are three different types of logs (system, tenant, portfolio), these logs can be posted from different API key types as listed below:  - scheduling-API-key without tenant -> system logs (omit portfolio_id) - scheduling-API-key with tenant -> tenant logs (omit portfolio_id - standard-API-key -> portfolio logs (specify portfolio_id) AND tenant logs (omit portfolio_id) - tenant-master-API-key -> cannot submit any logs - master-API-key -> cannot submit any logs  A log entry belongs to a freely chosen category and has a defined severity as well as a timestamp (UTC) value.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.add_log_entry_with_http_info(value, async_req=True)
        >>> result = thread.get()

        :param value: (required)
        :type value: LogEntry
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """

        local_var_params = locals()

        all_params = [
            'value'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method add_log_entry" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'value' is set
        if self.api_client.client_side_validation and local_var_params.get('value') is None:  # noqa: E501
            raise ApiValueError("Missing the required parameter `value` when calling `add_log_entry`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = dict(local_var_params.get('_headers', {}))

        form_params = []
        local_var_files = {}

        body_params = None
        if 'value' in local_var_params:
            body_params = local_var_params['value']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        content_types_list = local_var_params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json'],
                'POST', body_params))  # noqa: E501
        if content_types_list:
                header_params['Content-Type'] = content_types_list

        # Authentication setting
        auth_settings = ['api_key_security']  # noqa: E501

        response_types_map = {}

        return self.api_client.call_api(
            '/logs', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def get_audit_logs(self, **kwargs):  # noqa: E501
        """Get audit-logs  # noqa: E501

        Receive audit log entries that have been generated by the system. Only the master-api-key and tenant-master api-key is allowed to access audit-logs. When no parameters are specified, all audit logs from 24 hours ago until now will be retrieved.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_audit_logs(async_req=True)
        >>> result = thread.get()

        :param api_key_name: The name of the api-key
        :type api_key_name: str
        :param ip_address: The ip address
        :type ip_address: str
        :param tenant_id:
        :type tenant_id: str
        :param portfolio_id:
        :type portfolio_id: list[str]
        :param object_name: filter by object types
        :type object_name: list[str]
        :param received_from: from timestamp is 'inclusive' (i.e. >=), use UTC timezone, default to 24 hours ago
        :type received_from: datetime
        :param received_to: to timestamp is 'exclusive' (i.e. <), use UTC timezone, defaults to now
        :type received_to: datetime
        :param offset: Offset when loading a list of items
        :type offset: int
        :param limit: Limits the number of loaded items
        :type limit: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: list[AuditLogEntry]
        """
        kwargs['_return_http_data_only'] = True
        return self.get_audit_logs_with_http_info(**kwargs)  # noqa: E501

    def get_audit_logs_with_http_info(self, **kwargs):  # noqa: E501
        """Get audit-logs  # noqa: E501

        Receive audit log entries that have been generated by the system. Only the master-api-key and tenant-master api-key is allowed to access audit-logs. When no parameters are specified, all audit logs from 24 hours ago until now will be retrieved.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_audit_logs_with_http_info(async_req=True)
        >>> result = thread.get()

        :param api_key_name: The name of the api-key
        :type api_key_name: str
        :param ip_address: The ip address
        :type ip_address: str
        :param tenant_id:
        :type tenant_id: str
        :param portfolio_id:
        :type portfolio_id: list[str]
        :param object_name: filter by object types
        :type object_name: list[str]
        :param received_from: from timestamp is 'inclusive' (i.e. >=), use UTC timezone, default to 24 hours ago
        :type received_from: datetime
        :param received_to: to timestamp is 'exclusive' (i.e. <), use UTC timezone, defaults to now
        :type received_to: datetime
        :param offset: Offset when loading a list of items
        :type offset: int
        :param limit: Limits the number of loaded items
        :type limit: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(list[AuditLogEntry], status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'api_key_name',
            'ip_address',
            'tenant_id',
            'portfolio_id',
            'object_name',
            'received_from',
            'received_to',
            'offset',
            'limit'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_audit_logs" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        if self.api_client.client_side_validation and 'offset' in local_var_params and local_var_params['offset'] < 0:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `offset` when calling `get_audit_logs`, must be a value greater than or equal to `0`")  # noqa: E501
        if self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params['limit'] > 500:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `limit` when calling `get_audit_logs`, must be a value less than or equal to `500`")  # noqa: E501
        if self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params['limit'] < 1:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `limit` when calling `get_audit_logs`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if local_var_params.get('api_key_name') is not None:  # noqa: E501
            query_params.append(('api_key_name', local_var_params['api_key_name']))  # noqa: E501
        if local_var_params.get('ip_address') is not None:  # noqa: E501
            query_params.append(('ip_address', local_var_params['ip_address']))  # noqa: E501
        if local_var_params.get('tenant_id') is not None:  # noqa: E501
            query_params.append(('tenant_id', local_var_params['tenant_id']))  # noqa: E501
        if local_var_params.get('portfolio_id') is not None:  # noqa: E501
            query_params.append(('portfolio_id', local_var_params['portfolio_id']))  # noqa: E501
            collection_formats['portfolio_id'] = 'csv'  # noqa: E501
        if local_var_params.get('object_name') is not None:  # noqa: E501
            query_params.append(('object_name', local_var_params['object_name']))  # noqa: E501
            collection_formats['object_name'] = 'multi'  # noqa: E501
        if local_var_params.get('received_from') is not None:  # noqa: E501
            query_params.append(('received_from', local_var_params['received_from']))  # noqa: E501
        if local_var_params.get('received_to') is not None:  # noqa: E501
            query_params.append(('received_to', local_var_params['received_to']))  # noqa: E501
        if local_var_params.get('offset') is not None:  # noqa: E501
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if local_var_params.get('limit') is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501

        header_params = dict(local_var_params.get('_headers', {}))

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key_security']  # noqa: E501

        response_types_map = {
            200: "list[AuditLogEntry]",
        }

        return self.api_client.call_api(
            '/audit-logs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def get_logs(self, **kwargs):  # noqa: E501
        """Get system log entries  # noqa: E501

        Retrieves log entries which you have submitted earlier with \"POST /logs\". Logs can be retrieved for a set (array) of portfolios and categories. The query can be filtered by minimum severity and a time interval. Please note that this feature uses pagination.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_logs(async_req=True)
        >>> result = thread.get()

        :param portfolio_id:
        :type portfolio_id: list[str]
        :param offset: Offset when loading a list of items
        :type offset: int
        :param limit: Limits the number of loaded items
        :type limit: int
        :param severity_at_least:
        :type severity_at_least: Severity
        :param category:
        :type category: list[str]
        :param received_from: from timestamp is 'inclusive' (i.e. >=), use UTC time zone
        :type received_from: datetime
        :param received_to: to timestamp is 'exclusive' (i.e. <), use UTC time zone
        :type received_to: datetime
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: list[LogEntry]
        """
        kwargs['_return_http_data_only'] = True
        return self.get_logs_with_http_info(**kwargs)  # noqa: E501

    def get_logs_with_http_info(self, **kwargs):  # noqa: E501
        """Get system log entries  # noqa: E501

        Retrieves log entries which you have submitted earlier with \"POST /logs\". Logs can be retrieved for a set (array) of portfolios and categories. The query can be filtered by minimum severity and a time interval. Please note that this feature uses pagination.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_logs_with_http_info(async_req=True)
        >>> result = thread.get()

        :param portfolio_id:
        :type portfolio_id: list[str]
        :param offset: Offset when loading a list of items
        :type offset: int
        :param limit: Limits the number of loaded items
        :type limit: int
        :param severity_at_least:
        :type severity_at_least: Severity
        :param category:
        :type category: list[str]
        :param received_from: from timestamp is 'inclusive' (i.e. >=), use UTC time zone
        :type received_from: datetime
        :param received_to: to timestamp is 'exclusive' (i.e. <), use UTC time zone
        :type received_to: datetime
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(list[LogEntry], status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'portfolio_id',
            'offset',
            'limit',
            'severity_at_least',
            'category',
            'received_from',
            'received_to'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_logs" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        if self.api_client.client_side_validation and 'offset' in local_var_params and local_var_params['offset'] < 0:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `offset` when calling `get_logs`, must be a value greater than or equal to `0`")  # noqa: E501
        if self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params['limit'] > 500:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `limit` when calling `get_logs`, must be a value less than or equal to `500`")  # noqa: E501
        if self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params['limit'] < 1:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `limit` when calling `get_logs`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if local_var_params.get('portfolio_id') is not None:  # noqa: E501
            query_params.append(('portfolio_id', local_var_params['portfolio_id']))  # noqa: E501
            collection_formats['portfolio_id'] = 'csv'  # noqa: E501
        if local_var_params.get('offset') is not None:  # noqa: E501
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if local_var_params.get('limit') is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if local_var_params.get('severity_at_least') is not None:  # noqa: E501
            query_params.append(('severity_at_least', local_var_params['severity_at_least']))  # noqa: E501
        if local_var_params.get('category') is not None:  # noqa: E501
            query_params.append(('category', local_var_params['category']))  # noqa: E501
            collection_formats['category'] = 'csv'  # noqa: E501
        if local_var_params.get('received_from') is not None:  # noqa: E501
            query_params.append(('received_from', local_var_params['received_from']))  # noqa: E501
        if local_var_params.get('received_to') is not None:  # noqa: E501
            query_params.append(('received_to', local_var_params['received_to']))  # noqa: E501

        header_params = dict(local_var_params.get('_headers', {}))

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key_security']  # noqa: E501

        response_types_map = {
            200: "list[LogEntry]",
        }

        return self.api_client.call_api(
            '/logs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))
