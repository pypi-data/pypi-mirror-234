# coding: utf-8

"""
    VRt.Universal [UV]

    # Description  Software interface for universal trip planning.  ## Features  * Ability to pick up cargo from any location * Possibility of unloading in any location * Pair orders of several types: `PICKUP` (loading), `DROP` (unloading) * Single requests of several types: `DROP_FROM_BOX` (unloading cargo that is already in the body), `PICKUP_TO_BOX` (cargo pickup into the body without subsequent unloading), `WORK` (working at the location without moving the cargo) * A complex order can consist of any number of orders of any type * Transport and executors are divided into different entities, when planning, the optimal assignment of the executor to the transport occurs * The transport has several compartments - each of which can accommodate cargo and has its own characteristics * Accounting for the compatibility of cargo with transport in terms of cargo dimensions (length, width, height, additional capacity parameters) * Taking into account the compatibility of the cargo-compartment of transport (the ability to take into account the features of the compartment: refrigerator, thermal bag, fasteners, etc.) * Substitute applications, i.e. the ability to execute one of the substitute applications, the choice of which is based on its geographic location and time window  ## Restrictions support  **Performer** restrictions:  * Start/finish location * Accounting for the performer's way to the transport location * Performer's availability schedule is a list of time windows when the performer can move and work on locations * The maximum duration of the performer's work during the specified time period  **Transport** restrictions:  * Start/finish location * Transport availability schedule is a list of time windows when the transport is available * The maximum route distance * Several compartments in the transport, each with its own parameters * Capacity upper limit (weight, volume, number of orders, number of demands)  **Order** restrictions:  * Strict time windows * Ability to specify different valid time windows for a location and time windows to fulfil the desired demand * Accounting for the requests fulfillment order within the route * A list of desired time windows with different associated costs  ## Compatibilities  Entities are compatible if the capabilities list of one entity corresponds to the list of restrictions of another entity (example: fleet parameters corresponds to cargo parameters to be delivered).  Supported compatibilities:  | Name                    | Restrictions                     | Features                     | |-------------------------|----------------------------------|------------------------------| | Order - Performer       | order.performer_restrictions     | performer.performer_features | | Order - Not a performer | order.performer_blacklist        | performer.performer_features | | Cargo - Compartment     | order.cargo.box_restrictions     | transport.box.box_features   | | Location - Transport    | location.transport_restrictions  | transport.transport_features | | Transport - Performer   | transport.performer_restrictions | performer.performer_features | | Performer - Transport   | performer.transport_restrictions | transport.transport_features | | Order - Order           | order.order_restrictions         | order.order_features         |  Business rule examples:  | Name                    | Business rule example                                                                               | |-------------------------|-----------------------------------------------------------------------------------------------------| | Order - Performer       | The driver must have a special license to fulfil the order                                          | | Order - Not a performer | The driver is in the blacklist                                                                      | | Cargo - Box             | For transportation of frozen products, a compartment with a special temperature profile is required | | Location - Transport    | Restrictions on the transport height                                                                | | Transport - Performer   | The truck driver must have the class C driving license                                              | | Performer - Transport   | The driver is allowed to work on a specific transport                                               | | Order - Order           | It is not allowed to transport fish and fruits in the same compartment                              |  ## Cargo placement  List of possibilities of a object rotations (90 degree step):  * `ALL` - can rotate by any axis * `YAW` - can yaw * `PITCH` - can pitch * `ROLL` - can roll    ![rotation](../images/universal_cargo_yaw_pitch_roll.svg)  ## Trip model  The trip is described by the list of states of the executor, while the executor can be in several states at the same time (for example, to be inside the working time window of a location and fulfill an order at the same location).  Possible values ​​of the flags responsible for the geographical location:  * `AROUND_LOCATION` - the performer is located near the location - in the process of parking or leaving it. * `INSIDE_LOCATION` - the performer is at the location.  Possible values ​​of the flags responsible for being in time windows:  * `INSIDE_WORKING_WINDOW` - the executor is inside the working time window. * `INSIDE_LOCATION_WINDOW` - the executor is inside the location's working time. * `INSIDE_EVENT_HARD_WINDOW` - the executor is inside a hard time window. * `INSIDE_EVENT_SOFT_WINDOW` - the executor is inside the soft time window.  Possible values ​​of flags responsible for actions:  * `ON_DEMAND` - the executor is working on the request. * `WAITING` - the performer is in standby mode. * `RELOCATING` - the executor is moving to the next stop. * `BREAK` - the performer is on a break.  ### An example of a route with multiple states at each point in time  | time  | set of active flags                                                                                                                                                          | location / order / application / event | comment                                                                                        | |:------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------|:-----------------------------------------------------------------------------------------------| | 10:00 | INSIDE_LOCATION <br/> AROUND_LOCATION                                                                                                                                        | 2 / - / - / -                          | starting location                                                                              | | 10:10 | RELOCATING                                                                                                                                                                   | - / - / - / -                          | we go to the first order                                                                       | | 10:20 | AROUND_LOCATION                                                                                                                                                              | 2 / - / - / -                          | arrived at the first order                                                                     | | 10:40 | AROUND_LOCATION <br/> INSIDE_LOCATION <br/> WAITING                                                                                                                          | 2 / - / - / -                          | parked                                                                                         | | 11:00 | AROUND_LOCATION <br/> INSIDE_LOCATION <br/> INSIDE_LOCATION_WINDOW <br/> WAITING <br/> INSIDE_EVENT_HARD_WINDOW                                                              | 2 / - / - / -                          | waited for the start of the location window and at the same time the availability of the order | | 11:25 | AROUND_LOCATION <br/> INSIDE_LOCATION <br/> INSIDE_LOCATION_WINDOW <br/> ON_DEMAND <br/> INSIDE_WORKING_WINDOW <br/> INSIDE_EVENT_HARD_WINDOW                                | 2 / 1 / 2 / 3                          | waited for the change of artist                                                                | | 11:30 | AROUND_LOCATION <br/> INSIDE_LOCATION <br/> INSIDE_LOCATION_WINDOW <br/> ON_DEMAND <br/> INSIDE_WORKING_WINDOW <br/> INSIDE_EVENT_HARD_WINDOW <br/> INSIDE_EVENT_SOFT_WINDOW | 2 / 1 / 2 / 3                          | while working - a soft window happened                                                         | | 11:40 | AROUND_LOCATION <br/> INSIDE_LOCATION <br/> INSIDE_LOCATION_WINDOW <br/> INSIDE_WORKING_WINDOW                                                                               | 2 / - / - / -                          | finished working                                                                               | | 11:45 | AROUND_LOCATION <br/> INSIDE_WORKING_WINDOW                                                                                                                                  | 2 / - / - / -                          | drove out of the parking lot                                                                   | | 11:45 | RELOCATING <br/> INSIDE_WORKING_WINDOW                                                                                                                                       | - / - / - / -                          | we go to the next order                                                                        |  ## Planning configuration  For each planning, it is possible to specify a planning configuration that defines the objective function, the desired quality of the routes, and the calculation speed.  The name of the scheduling configuration is passed in the `trips_settings.configuration` field.  Main configurations:  | Title                           | Task                                                                                                                                                   | |---------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------| | **optimize_distance**           | Arrange as many orders as possible, then optimize the total mileage (the number of vehicles is selected based on the mileage), used by default         | | **optimize_transports**         | Place as many orders as possible, while using as little transport as possible, ceteris paribus, optimize the work time of performers                   | | **optimize_locality_grouping**  | Place as many orders as possible, while striving to optimize the visual grouping of routes, but not their number                                       | | **optimize_cars_then_distance** | Arrange as many orders as possible, then optimize the number of vehicles, then the mileage                                                             | | **optimize_time**               | Place as many orders as possible, then optimize the total work time of performers                                                                      | | **optimize_cars_then_time**     | Arrange as many orders as possible, then optimize the number of transport, then the total time of the performers                                       | | **optimize_money**              | Optimize the value of \"profit - costs\", consists of rewards for applications and costs for performers and transports (optimized value is non-negative) |  Additional configurations:  | Title                                                     | Task                                                                                                                                                                                            | |-----------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| | **visual_grouping**                                       | Arrange as many orders as possible while using as little transport as possible and routes should be visually grouped                                                                            | | **optimize_visual_grouping**                              | Arrange as many orders as possible, then evenly distribute orders taking into account transport accessibility zones (similar to visual_grouping, but visual grouping is calculated differently) | | **optimize_cars_then_locality_grouping**                  | Arrange as many orders as possible, then optimize the number of vehicles, then visually group the routes                                                                                        | | **optimize_cars_then_single_location_grouping_sequenced** | Place as many orders as possible, then optimize the number of machines, then reliability                                                                                                        |  In addition to the existing planning options, it is possible to create an objective function directly for the client's business processes ([request configuration](mailto:servicedesk@veeroute.com)).  For development, it is recommended to use **optimize_cars_then_distance**, since this configuration does not require detailed selection of rates and order values.  ## Data validation  Input data validation consists of several steps, which are described below.  Validation of planning results (including the search for possible reasons why orders were not planned) is located in the `analytics` method.  ### 1. Schema check  If the request does not follow the schema, then scheduling is not fully started and such an error is returned along with a 400 code in `schema_errors`.  We recommend validating the request against the schema (or yaml file) before sending it to the server.  ### 2. Check for logical errors that prevent planning from continuing  Schema-correct data passes the second stage of checking for the possibility of starting planning.  An example of errors at this stage are keys leading to empty entities, or if all orders are incompatible with all performers, i.e. something that makes the planning task pointless.  These errors are returned along with a 400 code in `logical_errors`.  ### 3. Check for logical errors that prevent planning from continuing  At the third stage, each entity is checked separately.  All entities that have not passed validation are cut out from the original task and are not sent for planning.  Depending on the setting of `treat_warnings_as_errors`, the results of this type of validation are returned to `warnings` either with a 400 code or with the scheduling result.  ### 4. Checks in the planning process  Part of the checks can only be carried out in the planning process.  For example - that according to the specified tariffs and according to the current traffic forecast, it is physically impossible to reach a certain point.  The results of these checks are returned in `warnings` or together with the scheduling result.  ## Entity relationship diagram  ![erd](../uml/universal.svg)  # Xlsx  <!-- AUTO-GENERATED-CONTENT:START (FILE:src=xlsx.md) --> <!-- The below content is automatically added from xlsx.md --> Description of VRt.Universal XLSX format for import / data export.  This format is a complete display of data JSON models and is used for:  * initial data * process settings * calculation results * statistics on the calculation result  Below is a description of each sheet separately.  ## Locations  The name of the sheet `locations`.  List of locations that are used in orders and shifts.  The described object: <SchemaDefinition schemaRef=\"#/components/schemas/location\" />  ## Performers  The name of the sheet is `performers`.  List of available performers.  The described object: <SchemaDefinition schemaRef=\"#/components/schemas/performer\" />  ## Transports  The name of the sheet `transports`.  List of available transport.  The described object: <SchemaDefinition schemaRef=\"#/components/schemas/transport\" />  ## Boxes  The name of the sheet is `transports.boxes`.  List of transport boxes that can accommodate the load. The table is mandatory if there are orders with applications of types of `PICKUP` and `DROP`. In the description of the compartments, those fields that describe cargo are required.  The described object: <SchemaDefinition schemaRef=\"#/components/schemas/box\" />  ## Orders  The name of the sheet is `orders`.  List of orders.  The described object: <SchemaDefinition schemaRef=\"#/components/schemas/order\" />  ## Cargos  The name of the sheet is `orders.cargos`.  List of goods. It may contain one load for `DROP`, a list for `PICKUP`, empty for `WORK`. The table is not obligatory if all applications have the type `WORK`.  The described object: <SchemaDefinition schemaRef=\"#/components/schemas/cargo\" />  ## Hardlinks  The name of the sheet is `hardlinks`.  List of hardlinks.  The described object: <SchemaDefinition schemaRef=\"#/components/schemas/hardlink\" />  ## Trips  The name of the sheet `trips`.  List of trips.  The described object: <SchemaDefinition schemaRef=\"#/components/schemas/trip\" />  ## Facts  The name of the sheet is `facts`.  List of facts.  The described object: <SchemaDefinition schemaRef=\"#/components/schemas/facts\" />  ## Plan settings  The name of the sheet `plan_settings`.  The described object: <SchemaDefinition schemaRef=\"#/components/schemas/plan_settings\" />  ## Actualize settings  The name of the sheet is `actualize_settings`.  The described object: <SchemaDefinition schemaRef=\"#/components/schemas/actualize_settings\" />  ## Replan settings  The name of the sheet is `replan_settings`.  The described object: <SchemaDefinition schemaRef=\"#/components/schemas/replan_settings\" /> <!-- AUTO-GENERATED-CONTENT:END -->

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
from pydantic import Field, StrictBytes, StrictStr

from typing import Union

from vrt_lss_universal.models.universal_data import UniversalData

from vrt_lss_universal.api_client import ApiClient
from vrt_lss_universal.api_response import ApiResponse
from vrt_lss_universal.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class ConvertApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_arguments
    def run_convert_json_to_thrift(self, universal_data : Annotated[UniversalData, Field(..., description="Conversion request to the THRIFT.")], **kwargs) -> str:  # noqa: E501
        """JSON >> THRIFT  # noqa: E501

        Used for conversion of input data to the THRIFT format.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.run_convert_json_to_thrift(universal_data, async_req=True)
        >>> result = thread.get()

        :param universal_data: Conversion request to the THRIFT. (required)
        :type universal_data: UniversalData
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
            message = "Error! Please call the run_convert_json_to_thrift_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.run_convert_json_to_thrift_with_http_info(universal_data, **kwargs)  # noqa: E501

    @validate_arguments
    def run_convert_json_to_thrift_with_http_info(self, universal_data : Annotated[UniversalData, Field(..., description="Conversion request to the THRIFT.")], **kwargs) -> ApiResponse:  # noqa: E501
        """JSON >> THRIFT  # noqa: E501

        Used for conversion of input data to the THRIFT format.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.run_convert_json_to_thrift_with_http_info(universal_data, async_req=True)
        >>> result = thread.get()

        :param universal_data: Conversion request to the THRIFT. (required)
        :type universal_data: UniversalData
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
            'universal_data'
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
                    " to method run_convert_json_to_thrift" % _key
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
        if _params['universal_data'] is not None:
            _body_params = _params['universal_data']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['ApiKeyAuth']  # noqa: E501

        _response_types_map = {
            '200': "str",
            '400': "Custom400WithErrorsAndWarnings",
            '401': "General401",
            '402': "General402",
            '403': "General403",
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
            '/universal/convert/json_to_thrift', 'POST',
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
    def run_convert_json_to_xlsx(self, universal_data : Annotated[UniversalData, Field(..., description="Conversion request to the XLSX.")], **kwargs) -> bytearray:  # noqa: E501
        """JSON >> XLSX  # noqa: E501

        Used for conversion of input and output data to the [VRt.Universal XLSX](#section/Xlsx) format.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.run_convert_json_to_xlsx(universal_data, async_req=True)
        >>> result = thread.get()

        :param universal_data: Conversion request to the XLSX. (required)
        :type universal_data: UniversalData
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: bytearray
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the run_convert_json_to_xlsx_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.run_convert_json_to_xlsx_with_http_info(universal_data, **kwargs)  # noqa: E501

    @validate_arguments
    def run_convert_json_to_xlsx_with_http_info(self, universal_data : Annotated[UniversalData, Field(..., description="Conversion request to the XLSX.")], **kwargs) -> ApiResponse:  # noqa: E501
        """JSON >> XLSX  # noqa: E501

        Used for conversion of input and output data to the [VRt.Universal XLSX](#section/Xlsx) format.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.run_convert_json_to_xlsx_with_http_info(universal_data, async_req=True)
        >>> result = thread.get()

        :param universal_data: Conversion request to the XLSX. (required)
        :type universal_data: UniversalData
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
        :rtype: tuple(bytearray, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'universal_data'
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
                    " to method run_convert_json_to_xlsx" % _key
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
        if _params['universal_data'] is not None:
            _body_params = _params['universal_data']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/octet-stream', 'application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['ApiKeyAuth']  # noqa: E501

        _response_types_map = {
            '200': "bytearray",
            '400': "Custom400WithErrorsAndWarnings",
            '401': "General401",
            '402': "General402",
            '403': "General403",
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
            '/universal/convert/json_to_xlsx', 'POST',
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
    def run_convert_xlsx_to_json(self, body : Annotated[Union[StrictBytes, StrictStr], Field(..., description="Conversion request to the JSON format.")], **kwargs) -> UniversalData:  # noqa: E501
        """XLSX >> JSON  # noqa: E501

        Used for data conversion from the [VRt.Universal XLSX](#section/Xlsx) format to the VRt.Universal JSON format.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.run_convert_xlsx_to_json(body, async_req=True)
        >>> result = thread.get()

        :param body: Conversion request to the JSON format. (required)
        :type body: bytearray
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: UniversalData
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the run_convert_xlsx_to_json_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.run_convert_xlsx_to_json_with_http_info(body, **kwargs)  # noqa: E501

    @validate_arguments
    def run_convert_xlsx_to_json_with_http_info(self, body : Annotated[Union[StrictBytes, StrictStr], Field(..., description="Conversion request to the JSON format.")], **kwargs) -> ApiResponse:  # noqa: E501
        """XLSX >> JSON  # noqa: E501

        Used for data conversion from the [VRt.Universal XLSX](#section/Xlsx) format to the VRt.Universal JSON format.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.run_convert_xlsx_to_json_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param body: Conversion request to the JSON format. (required)
        :type body: bytearray
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
        :rtype: tuple(UniversalData, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'body'
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
                    " to method run_convert_xlsx_to_json" % _key
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
        if _params['body'] is not None:
            _body_params = _params['body']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['ApiKeyAuth']  # noqa: E501

        _response_types_map = {
            '200': "UniversalData",
            '400': "Custom400WithErrorsAndWarnings",
            '401': "General401",
            '402': "General402",
            '403': "General403",
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
            '/universal/convert/xlsx_to_json', 'POST',
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
