# coding: utf-8

"""
    VRt.Agro [AG]

    Veeroute Agro API.  # Description  The service is designed to calculate the work plan of production facilities.  ## Objects overview  ![objects](../images/agro_objects.svg)  ### Field  - produces a certain crop of a certain moisture content - products from the field can only be moved to the Elevator or Factory  ### Elevator  - consists of Gates, Dryers, short-term and long-term storage areas - dries the grain (if the moisture content of the crop is more than acceptable) - stores dry grain in short-term storage places (warehouses), while unloading and loading grain is allowed within one day - stores dry grain in long-term storage places (sleeves, trenches, mounds) - when stored in one storage, only one type of culture can be located - sells surplus grain to the Market - production processes inside the facility: drying, loading / unloading to a storage location, storage  ### Factory  - consists of Gates, Dryers, Bunkers, Consumers - [if drying is present] dries the grain (if the moisture content of the crop is more than allowed) - stores dry grain in Bunkers (short-term storage tied to a specific crop) - maintains a minimum supply of grain for consumption in the Bunkers - Consumes grain from Bunkers - buys the missing grain from the Market - production processes inside the facility: drying, loading / unloading to a storage location, storage, consumption  ### Market  - buys grain from elevators - sells grain to factories  ## Project  The project reflects the planned sequence of operations on agricultural crops, the types of operations are described below.  ### HARVEST  Crop harvesting:  - between production facilities (Field and Elevator or Field) - the operation takes place within one day - on the Field there is a determination of grain moisture  |             | Object (target_key) | Subobject (target_detail_key) | |-------------|---------------------|-------------------------------| | Source      | Field               | -                             | | Destination | Elevator or Factory | Gate                          |  ### DRY  Drying culture:  - inside the production facility (Elevator or Field) - duration of the operation - days - during the drying process, the mass and type of humidity changes (WET -> DRY) - the source indicates the mass of raw culture - in the appointment, the resulting mass of dry culture is indicated  |             | Object (target_key) | Subobject (target_detail_key) | |-------------|---------------------|-------------------------------| | Source      | Elevator or Factory | Gate                          | | Destination | Elevator or Factory | Dryer                         |  ### LOAD  Loading culture from the Gate to the Storage Location (long-term, short-term, silo):  - between parts of one production facility (Elevator or Field) - the operation takes place within one day  |             | Object (target_key) | Subobject (target_detail_key)                    | |-------------|---------------------|--------------------------------------------------| | Source      | Elevator or Factory | Gate or Dryer                                    | | Destination | Elevator or Factory | Storage location (long-term, short-term, bunker) |  ### UNLOAD  Unloading the culture from the storage place to the gate:  - between parts of one production facility (Elevator) - the operation takes place within one day  |             | Object (target_key) | Subobject (target_detail_key)                    | |-------------|---------------------|--------------------------------------------------| | Source      | Elevator            | Storage location (long-term, short-term, bunker) | | Destination | Elevator            | Gate                                             |  ### STORE  Culture storage:  - the operation takes place within one day - storage location does not change  |             | Object (target_key) | Subobject (target_detail_key)                    | |-------------|---------------------|--------------------------------------------------| | Source      | Elevator or Factory | Storage location (long-term, short-term, bunker) | | Destination | Elevator or Factory | The same storage location                        |  ### RELOCATE  Transportation between production facilities:  - between production facilities (Elevator and Field) - the operation takes place within one day  |             | Object (target_key) | Subobject (target_detail_key) | |-------------|---------------------|-------------------------------| | Source      | Elevator            | Gate                          | | Destination | Factory             | Gate                          |  ### CONSUMPTION  Field crop consumption:  - between parts of one production facility (Field) - the operation takes place within one day - consumption comes from the Bunker - in addition, we can consume directly from the Gate or Dryer without laying in the Bunker  |             | Object (target_key) | Subobject (target_detail_key) | |-------------|---------------------|-------------------------------| | Source      | Factory             | Hopper or Gate or Dryer       | | Destination | Factory             | Consumer                      |  ### SELL  Sale of culture:  - between production facilities (Elevator and Market) - the operation takes place within one day  |             | Object (target_key) | Subobject (target_detail_key) | |-------------|---------------------|-------------------------------| | Source      | Elevator            | Gate                          | | Destination | Market              | Contract                      |  ### BUY  Buying culture:  - between production facilities (Market and Factory) - the operation takes place within one day  |             | Object (target_key) | Subobject (target_detail_key) | |-------------|---------------------|-------------------------------| | Source      | Market              | Contract                      | | Destination | Factory             | Gate                          |  ## Entity relationship diagram  ![erd](../uml/agro.svg) 

    The version of the OpenAPI document: 6.15.2142
    Contact: servicedesk@veeroute.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import re  # noqa: F401
import io
import warnings

from pydantic import validate_arguments, ValidationError

from typing_extensions import Annotated
from pydantic import Field, constr

from vrt_lss_agro.models.check_result import CheckResult
from vrt_lss_agro.models.version_result import VersionResult

from vrt_lss_agro.api_client import ApiClient
from vrt_lss_agro.api_response import ApiResponse
from vrt_lss_agro.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class SystemApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_arguments
    def check(self, **kwargs) -> CheckResult:  # noqa: E501
        """Checking the availability  # noqa: E501

        Checking the service availability.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.check(async_req=True)
        >>> result = thread.get()

        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: CheckResult
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the check_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.check_with_http_info(**kwargs)  # noqa: E501

    @validate_arguments
    def check_with_http_info(self, **kwargs) -> ApiResponse:  # noqa: E501
        """Checking the availability  # noqa: E501

        Checking the service availability.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.check_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
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
        :rtype: tuple(CheckResult, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
        ]
        _all_params.extend(
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

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method check" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = []  # noqa: E501

        _response_types_map = {
            '200': "CheckResult",
            '404': "General404",
            '405': None,
            '406': None,
            '415': None,
            '429': "General429",
            '500': "General500",
            '501': None,
            '502': None,
            '503': None,
            '504': None,
        }

        return self.api_client.call_api(
            '/agro/system/check', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def file(self, filename : Annotated[constr(strict=True, max_length=128, min_length=6), Field(..., description="File name.")], **kwargs) -> str:  # noqa: E501
        """Getting the documentation  # noqa: E501

        Getting the file with this service documentation.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.file(filename, async_req=True)
        >>> result = thread.get()

        :param filename: File name. (required)
        :type filename: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: str
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the file_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.file_with_http_info(filename, **kwargs)  # noqa: E501

    @validate_arguments
    def file_with_http_info(self, filename : Annotated[constr(strict=True, max_length=128, min_length=6), Field(..., description="File name.")], **kwargs) -> ApiResponse:  # noqa: E501
        """Getting the documentation  # noqa: E501

        Getting the file with this service documentation.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.file_with_http_info(filename, async_req=True)
        >>> result = thread.get()

        :param filename: File name. (required)
        :type filename: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
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
        :rtype: tuple(str, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'filename'
        ]
        _all_params.extend(
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

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method file" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['filename']:
            _path_params['filename'] = _params['filename']


        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['text/html', 'text/plain', 'application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = []  # noqa: E501

        _response_types_map = {
            '200': "str",
            '404': "General404",
            '405': None,
            '406': None,
            '415': None,
            '429': "General429",
            '500': "General500",
            '501': None,
            '502': None,
            '503': None,
            '504': None,
        }

        return self.api_client.call_api(
            '/agro/file/{filename}', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def version(self, **kwargs) -> VersionResult:  # noqa: E501
        """Getting the service version  # noqa: E501

        Getting the service version.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.version(async_req=True)
        >>> result = thread.get()

        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: VersionResult
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the version_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.version_with_http_info(**kwargs)  # noqa: E501

    @validate_arguments
    def version_with_http_info(self, **kwargs) -> ApiResponse:  # noqa: E501
        """Getting the service version  # noqa: E501

        Getting the service version.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.version_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
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
        :rtype: tuple(VersionResult, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
        ]
        _all_params.extend(
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

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method version" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # authentication setting
        _auth_settings = []  # noqa: E501

        _response_types_map = {
            '200': "VersionResult",
            '404': "General404",
            '405': None,
            '406': None,
            '415': None,
            '429': "General429",
            '500': "General500",
            '501': None,
            '502': None,
            '503': None,
            '504': None,
        }

        return self.api_client.call_api(
            '/agro/system/version', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))
