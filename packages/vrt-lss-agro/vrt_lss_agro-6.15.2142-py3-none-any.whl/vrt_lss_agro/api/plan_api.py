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
from pydantic import Field, StrictStr, constr

from typing import Optional

from vrt_lss_agro.models.calculation_async_result import CalculationAsyncResult
from vrt_lss_agro.models.calculation_state import CalculationState
from vrt_lss_agro.models.plan_result import PlanResult
from vrt_lss_agro.models.plan_task import PlanTask
from vrt_lss_agro.models.validate_result import ValidateResult

from vrt_lss_agro.api_client import ApiClient
from vrt_lss_agro.api_response import ApiResponse
from vrt_lss_agro.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class PlanApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_arguments
    def cancel_plan_calculation(self, id : Annotated[StrictStr, Field(..., description="Calculation identifier.")], **kwargs) -> None:  # noqa: E501
        """Cancel calculation  # noqa: E501

        Cancel calculation process by the calculation identifier.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.cancel_plan_calculation(id, async_req=True)
        >>> result = thread.get()

        :param id: Calculation identifier. (required)
        :type id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the cancel_plan_calculation_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.cancel_plan_calculation_with_http_info(id, **kwargs)  # noqa: E501

    @validate_arguments
    def cancel_plan_calculation_with_http_info(self, id : Annotated[StrictStr, Field(..., description="Calculation identifier.")], **kwargs) -> ApiResponse:  # noqa: E501
        """Cancel calculation  # noqa: E501

        Cancel calculation process by the calculation identifier.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.cancel_plan_calculation_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param id: Calculation identifier. (required)
        :type id: str
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
        :rtype: None
        """

        _params = locals()

        _all_params = [
            'id'
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
                    " to method cancel_plan_calculation" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['id']:
            _path_params['id'] = _params['id']


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
        _auth_settings = ['ApiKeyAuth']  # noqa: E501

        _response_types_map = {}

        return self.api_client.call_api(
            '/agro/plan/calculation_async/{id}', 'DELETE',
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
    def delete_plan_result(self, id : Annotated[StrictStr, Field(..., description="Calculation identifier.")], **kwargs) -> None:  # noqa: E501
        """Result removal  # noqa: E501

        Removal of the planning result by the calculation identifier.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.delete_plan_result(id, async_req=True)
        >>> result = thread.get()

        :param id: Calculation identifier. (required)
        :type id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the delete_plan_result_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.delete_plan_result_with_http_info(id, **kwargs)  # noqa: E501

    @validate_arguments
    def delete_plan_result_with_http_info(self, id : Annotated[StrictStr, Field(..., description="Calculation identifier.")], **kwargs) -> ApiResponse:  # noqa: E501
        """Result removal  # noqa: E501

        Removal of the planning result by the calculation identifier.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.delete_plan_result_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param id: Calculation identifier. (required)
        :type id: str
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
        :rtype: None
        """

        _params = locals()

        _all_params = [
            'id'
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
                    " to method delete_plan_result" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['id']:
            _path_params['id'] = _params['id']


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
        _auth_settings = ['ApiKeyAuth']  # noqa: E501

        _response_types_map = {}

        return self.api_client.call_api(
            '/agro/plan/result/{id}', 'DELETE',
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
    def read_plan_calculation_state(self, id : Annotated[StrictStr, Field(..., description="Calculation identifier.")], **kwargs) -> CalculationState:  # noqa: E501
        """Calculation state  # noqa: E501

        Read calculation state by the calculation identifier.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.read_plan_calculation_state(id, async_req=True)
        >>> result = thread.get()

        :param id: Calculation identifier. (required)
        :type id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: CalculationState
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the read_plan_calculation_state_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.read_plan_calculation_state_with_http_info(id, **kwargs)  # noqa: E501

    @validate_arguments
    def read_plan_calculation_state_with_http_info(self, id : Annotated[StrictStr, Field(..., description="Calculation identifier.")], **kwargs) -> ApiResponse:  # noqa: E501
        """Calculation state  # noqa: E501

        Read calculation state by the calculation identifier.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.read_plan_calculation_state_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param id: Calculation identifier. (required)
        :type id: str
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
        :rtype: tuple(CalculationState, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'id'
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
                    " to method read_plan_calculation_state" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['id']:
            _path_params['id'] = _params['id']


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
        _auth_settings = ['ApiKeyAuth']  # noqa: E501

        _response_types_map = {
            '200': "CalculationState",
            '400': "Custom400WithErrorsAndWarnings",
            '401': "General401",
            '402': "General402",
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
            '/agro/plan/calculation_async/{id}', 'GET',
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
    def read_plan_result(self, id : Annotated[StrictStr, Field(..., description="Calculation identifier.")], **kwargs) -> PlanResult:  # noqa: E501
        """Getting the result  # noqa: E501

        Getting the result based on the calculation identifier.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.read_plan_result(id, async_req=True)
        >>> result = thread.get()

        :param id: Calculation identifier. (required)
        :type id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PlanResult
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the read_plan_result_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.read_plan_result_with_http_info(id, **kwargs)  # noqa: E501

    @validate_arguments
    def read_plan_result_with_http_info(self, id : Annotated[StrictStr, Field(..., description="Calculation identifier.")], **kwargs) -> ApiResponse:  # noqa: E501
        """Getting the result  # noqa: E501

        Getting the result based on the calculation identifier.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.read_plan_result_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param id: Calculation identifier. (required)
        :type id: str
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
        :rtype: tuple(PlanResult, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'id'
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
                    " to method read_plan_result" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['id']:
            _path_params['id'] = _params['id']


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
        _auth_settings = ['ApiKeyAuth']  # noqa: E501

        _response_types_map = {
            '200': "PlanResult",
            '202': "PlanResult",
            '400': "Custom400WithErrorsAndWarnings",
            '401': "General401",
            '402': "General402",
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
            '/agro/plan/result/{id}', 'GET',
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
    def run_plan_calculation(self, plan_task : Annotated[PlanTask, Field(..., description="Data for calculation.")], **kwargs) -> PlanResult:  # noqa: E501
        """Planning (SYNC)  # noqa: E501

        Production plan calculation.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.run_plan_calculation(plan_task, async_req=True)
        >>> result = thread.get()

        :param plan_task: Data for calculation. (required)
        :type plan_task: PlanTask
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PlanResult
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the run_plan_calculation_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.run_plan_calculation_with_http_info(plan_task, **kwargs)  # noqa: E501

    @validate_arguments
    def run_plan_calculation_with_http_info(self, plan_task : Annotated[PlanTask, Field(..., description="Data for calculation.")], **kwargs) -> ApiResponse:  # noqa: E501
        """Planning (SYNC)  # noqa: E501

        Production plan calculation.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.run_plan_calculation_with_http_info(plan_task, async_req=True)
        >>> result = thread.get()

        :param plan_task: Data for calculation. (required)
        :type plan_task: PlanTask
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
        :rtype: tuple(PlanResult, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'plan_task'
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
                    " to method run_plan_calculation" % _key
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
        if _params['plan_task'] is not None:
            _body_params = _params['plan_task']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['ApiKeyAuth']  # noqa: E501

        _response_types_map = {
            '200': "PlanResult",
            '400': "Custom400WithErrorsAndWarnings",
            '401': "General401",
            '402': "General402",
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
            '/agro/plan/calculation', 'POST',
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
    def run_plan_calculation_async(self, plan_task : Annotated[PlanTask, Field(..., description="Data for calculation.")], **kwargs) -> CalculationAsyncResult:  # noqa: E501
        """Planning (ASYNC)  # noqa: E501

        The result can be obtained using the [result](#operation/read_plan_result) method, removing - with [delete](#operation/delete_plan_result).   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.run_plan_calculation_async(plan_task, async_req=True)
        >>> result = thread.get()

        :param plan_task: Data for calculation. (required)
        :type plan_task: PlanTask
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: CalculationAsyncResult
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the run_plan_calculation_async_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.run_plan_calculation_async_with_http_info(plan_task, **kwargs)  # noqa: E501

    @validate_arguments
    def run_plan_calculation_async_with_http_info(self, plan_task : Annotated[PlanTask, Field(..., description="Data for calculation.")], **kwargs) -> ApiResponse:  # noqa: E501
        """Planning (ASYNC)  # noqa: E501

        The result can be obtained using the [result](#operation/read_plan_result) method, removing - with [delete](#operation/delete_plan_result).   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.run_plan_calculation_async_with_http_info(plan_task, async_req=True)
        >>> result = thread.get()

        :param plan_task: Data for calculation. (required)
        :type plan_task: PlanTask
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
        :rtype: tuple(CalculationAsyncResult, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'plan_task'
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
                    " to method run_plan_calculation_async" % _key
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
        if _params['plan_task'] is not None:
            _body_params = _params['plan_task']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['ApiKeyAuth']  # noqa: E501

        _response_types_map = {
            '200': "CalculationAsyncResult",
            '400': "Custom400WithErrorsAndWarnings",
            '401': "General401",
            '402': "General402",
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
            '/agro/plan/calculation_async', 'POST',
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
    def run_plan_clip(self, clip_key : Annotated[constr(strict=True, max_length=1024, min_length=1), Field(..., description="Target essence key.")], plan_task : Annotated[PlanTask, Field(..., description="Data for clipping.")], clip_strategy : Annotated[Optional[StrictStr], Field(description="Data clipping strategy.")] = None, **kwargs) -> PlanTask:  # noqa: E501
        """Clipping (SYNC)  # noqa: E501

        Data clipping.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.run_plan_clip(clip_key, plan_task, clip_strategy, async_req=True)
        >>> result = thread.get()

        :param clip_key: Target essence key. (required)
        :type clip_key: str
        :param plan_task: Data for clipping. (required)
        :type plan_task: PlanTask
        :param clip_strategy: Data clipping strategy.
        :type clip_strategy: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: PlanTask
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the run_plan_clip_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.run_plan_clip_with_http_info(clip_key, plan_task, clip_strategy, **kwargs)  # noqa: E501

    @validate_arguments
    def run_plan_clip_with_http_info(self, clip_key : Annotated[constr(strict=True, max_length=1024, min_length=1), Field(..., description="Target essence key.")], plan_task : Annotated[PlanTask, Field(..., description="Data for clipping.")], clip_strategy : Annotated[Optional[StrictStr], Field(description="Data clipping strategy.")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """Clipping (SYNC)  # noqa: E501

        Data clipping.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.run_plan_clip_with_http_info(clip_key, plan_task, clip_strategy, async_req=True)
        >>> result = thread.get()

        :param clip_key: Target essence key. (required)
        :type clip_key: str
        :param plan_task: Data for clipping. (required)
        :type plan_task: PlanTask
        :param clip_strategy: Data clipping strategy.
        :type clip_strategy: str
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
        :rtype: tuple(PlanTask, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'clip_key',
            'plan_task',
            'clip_strategy'
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
                    " to method run_plan_clip" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['clip_key']:
            _path_params['clip_key'] = _params['clip_key']


        # process the query parameters
        _query_params = []
        if _params.get('clip_strategy') is not None:  # noqa: E501
            _query_params.append(('clip_strategy', _params['clip_strategy']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['plan_task'] is not None:
            _body_params = _params['plan_task']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['ApiKeyAuth']  # noqa: E501

        _response_types_map = {
            '200': "PlanTask",
            '400': "Custom400WithErrorsAndWarnings",
            '401': "General401",
            '402': "General402",
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
            '/agro/plan/clip/{clip_key}', 'POST',
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
    def run_plan_validation(self, plan_task : Annotated[PlanTask, Field(..., description="Data for calculation.")], **kwargs) -> ValidateResult:  # noqa: E501
        """Data validation  # noqa: E501

        Checking data before planning.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.run_plan_validation(plan_task, async_req=True)
        >>> result = thread.get()

        :param plan_task: Data for calculation. (required)
        :type plan_task: PlanTask
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: ValidateResult
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the run_plan_validation_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.run_plan_validation_with_http_info(plan_task, **kwargs)  # noqa: E501

    @validate_arguments
    def run_plan_validation_with_http_info(self, plan_task : Annotated[PlanTask, Field(..., description="Data for calculation.")], **kwargs) -> ApiResponse:  # noqa: E501
        """Data validation  # noqa: E501

        Checking data before planning.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.run_plan_validation_with_http_info(plan_task, async_req=True)
        >>> result = thread.get()

        :param plan_task: Data for calculation. (required)
        :type plan_task: PlanTask
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
        :rtype: tuple(ValidateResult, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'plan_task'
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
                    " to method run_plan_validation" % _key
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
        if _params['plan_task'] is not None:
            _body_params = _params['plan_task']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['ApiKeyAuth']  # noqa: E501

        _response_types_map = {
            '200': "ValidateResult",
            '400': "Custom400WithErrorsAndWarnings",
            '401': "General401",
            '402': "General402",
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
            '/agro/plan/validation', 'POST',
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
