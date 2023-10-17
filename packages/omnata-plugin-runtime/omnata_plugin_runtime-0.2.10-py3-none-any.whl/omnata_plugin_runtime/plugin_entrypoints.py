import datetime
import importlib
import json
import logging
import os
import sys
import time
from typing import Dict, List, Optional

from pydantic import BaseModel, parse_obj_as  # pylint: disable=no-name-in-module
import pydantic.json
from snowflake.snowpark import Session

from .api import SyncRequestPayload, handle_proc_result
from .configuration import (
    ConnectionConfigurationParameters,
    InboundSyncConfigurationParameters,
    OutboundSyncConfigurationParameters,
    OutboundSyncStrategy,
    StoredConfigurationValue,
    StoredMappingValue,
    StoredStreamConfiguration,
    StreamConfiguration,
    SyncConfigurationParameters,
)
from .forms import ConnectionMethod, FormOption
from .logging import OmnataPluginLogHandler
from .omnata_plugin import (
    SnowflakeBillingEvent,
    BillingEventRequest,
    HttpRateLimiting,
    InboundSyncRequest,
    OmnataPlugin,
    OutboundSyncRequest,
)
from .rate_limiting import ApiLimits, RateLimitState

# set the logger class to our custom logger so that pydantic errors are handled correctly
logger = logging.getLogger(__name__)

IMPORT_DIRECTORY_NAME = "snowflake_import_directory"


class PluginEntrypoint:
    """
    This class gives each plugin's stored procs an initial point of contact.
    It will only work within Snowflake because it uses the _snowflake module.
    """

    def __init__(
        self, plugin_fqn: str, session: Session, module_name: str, class_name: str
    ):
        logger.info(f"Initialising plugin entrypoint for {plugin_fqn}")
        self._session = session
        import_dir = sys._xoptions[IMPORT_DIRECTORY_NAME]
        sys.path.append(os.path.join(import_dir, "app.zip"))
        module = importlib.import_module(module_name)
        class_obj = getattr(module, class_name)
        self._plugin_instance: OmnataPlugin = class_obj()

    def sync(self, sync_request: Dict):
        logger.info("Entered sync method")
        request = parse_obj_as(SyncRequestPayload, sync_request)
        connection_secrets = self.get_secrets(
            request.oauth_secret_name, request.other_secrets_name
        )
        omnata_log_handler = OmnataPluginLogHandler(
            session=self._session,
            sync_id=request.sync_id,
            sync_branch_id=request.sync_branch_id,
            connection_id=request.connection_id,
            sync_run_id=request.run_id,
        )
        omnata_log_handler.register(
            request.logging_level, self._plugin_instance.additional_loggers()
        )
        # construct some connection parameters for the purpose of getting the api limits
        connection_parameters = ConnectionConfigurationParameters(
            connection_method=request.connection_method,
            connection_parameters=request.connection_parameters,
            connection_secrets=connection_secrets
        )
        all_api_limits = self._plugin_instance.api_limits(connection_parameters)
        logger.info(
            f"Default API limits: {json.dumps(all_api_limits, default=pydantic.json.pydantic_encoder)}"
        )
        all_api_limits_by_category = {
            api_limit.endpoint_category: api_limit for api_limit in all_api_limits
        }
        all_api_limits_by_category.update(
            {
                k: v
                for k, v in [
                    (x.endpoint_category, x) for x in request.api_limit_overrides
                ]
            }
        )
        api_limits = list(all_api_limits_by_category.values())
        # if any endpoint categories have no state, give them an empty state
        for api_limit in api_limits:
            if api_limit.endpoint_category not in request.rate_limits_state:
                request.rate_limits_state[api_limit.endpoint_category] = RateLimitState(
                    wait_until=None, previous_request_timestamps=None
                )
        logger.info(
            f"Rate limits state: {json.dumps(request.rate_limits_state, default=pydantic.json.pydantic_encoder)}"
        )
        return_dict = {}
        if request.sync_direction == "outbound":
            parameters = OutboundSyncConfigurationParameters(
                connection_method=request.connection_method,
                connection_parameters=request.connection_parameters,
                connection_secrets=connection_secrets,
                sync_parameters=request.sync_parameters,
                current_form_parameters={},
                sync_strategy=request.sync_strategy,
                field_mappings=request.field_mappings,
            )

            outbound_sync_request = OutboundSyncRequest(
                run_id=request.run_id,
                session=self._session,
                source_app_name=request.source_app_name,
                records_schema_name=request.records_schema_name,
                records_table_name=request.records_table_name,
                results_schema_name=request.results_schema_name,
                results_table_name=request.results_table_name,
                plugin_instance=self._plugin_instance,
                api_limits=request.api_limit_overrides,
                rate_limit_state=request.rate_limits_state,
                run_deadline=datetime.datetime.now() + datetime.timedelta(hours=4),
                development_mode=False,
            )

            with HttpRateLimiting(outbound_sync_request, parameters):
                self._plugin_instance.sync_outbound(parameters, outbound_sync_request)
                outbound_sync_request.apply_results_queue()
            # cancel the thread so we don't leave anything hanging around and cop a nasty error
            outbound_sync_request._thread_cancellation_token.set()  # pylint: disable=protected-access
            outbound_sync_request._apply_results_task.join()  # pylint: disable=protected-access
            outbound_sync_request._cancel_checking_task.join()  # pylint: disable=protected-access

        elif request.sync_direction == "inbound":
            logger.info("Running inbound sync")
            parameters = InboundSyncConfigurationParameters(
                connection_method=request.connection_method,
                connection_parameters=request.connection_parameters,
                connection_secrets=connection_secrets,
                sync_parameters=request.sync_parameters,
                current_form_parameters={},
            )
            
            inbound_sync_request = InboundSyncRequest(
                run_id=request.run_id,
                session=self._session,
                source_app_name=request.source_app_name,
                results_schema_name=request.results_schema_name,
                results_table_name=request.results_table_name,
                plugin_instance=self._plugin_instance,
                api_limits=request.api_limit_overrides,
                rate_limit_state=request.rate_limits_state,
                run_deadline=datetime.datetime.now() + datetime.timedelta(hours=4),
                development_mode=False,
                streams=list(request.streams_configuration.included_streams.values()),
            )

            inbound_sync_request.update_activity("Invoking plugin")
            logger.info(f"inbound sync request: {inbound_sync_request}")
            # plugin_instance._inbound_sync_request = outbound_sync_request
            with HttpRateLimiting(inbound_sync_request, parameters):
                self._plugin_instance.sync_inbound(parameters, inbound_sync_request)
            logger.info("Finished invoking plugin")
            inbound_sync_request.update_activity("Staging remaining records")
            logger.info("Calling apply_results_queue")
            inbound_sync_request.apply_results_queue()
            # cancel the thread so we don't leave anything hanging around and cop a nasty error
            inbound_sync_request._thread_cancellation_token.set()  # pylint: disable=protected-access
            inbound_sync_request._apply_results_task.join()  # pylint: disable=protected-access
            inbound_sync_request._cancel_checking_task.join()  # pylint: disable=protected-access
            return_dict["errored_streams"] = list(
                omnata_log_handler.stream_has_errors.keys()
            )
            # we need to calculate counts for:
            # CHANGED_COUNT by counting up the records in INBOUND_STREAM_RECORD_COUNTS
        logger.info("Finished applying records")
        return return_dict

    def configuration_form(
        self,
        connection_method: str,
        connection_parameters: Dict,
        oauth_secret_name: Optional[str],
        other_secrets_name: Optional[str],
        sync_direction: str,
        sync_strategy: Dict,
        function_name: str,
        sync_parameters: Dict,
        current_form_parameters: Optional[Dict],
    ):
        logger.info("Entered configuration_form method")
        sync_strategy = normalise_nulls(sync_strategy)
        oauth_secret_name = normalise_nulls(oauth_secret_name)
        other_secrets_name = normalise_nulls(other_secrets_name)
        connection_secrets = self.get_secrets(oauth_secret_name, other_secrets_name)
        connection_parameters = parse_obj_as(
            Dict[str, StoredConfigurationValue], connection_parameters
        )
        sync_parameters = parse_obj_as(
            Dict[str, StoredConfigurationValue], sync_parameters
        )
        form_parameters = None
        if current_form_parameters is not None:
            form_parameters = parse_obj_as(
                Dict[str, StoredConfigurationValue], current_form_parameters
            )
        if sync_direction == "outbound":
            sync_strat = OutboundSyncStrategy.parse_obj(sync_strategy) if sync_strategy is not None else None
            parameters = OutboundSyncConfigurationParameters(
                connection_parameters=connection_parameters,
                connection_secrets=connection_secrets,
                sync_strategy=sync_strat,
                sync_parameters=sync_parameters,
                connection_method=connection_method,
                current_form_parameters=form_parameters,
            )
        elif sync_direction == "inbound":
            parameters = InboundSyncConfigurationParameters(
                connection_parameters=connection_parameters,
                connection_secrets=connection_secrets,
                sync_parameters=sync_parameters,
                connection_method=connection_method,
                current_form_parameters=form_parameters,
            )
        else:
            raise ValueError(f"Unknown direction {sync_direction}")
        the_function = getattr(
            self._plugin_instance,
            function_name or f"{sync_direction}_configuration_form",
        )
        script_result = the_function(parameters)
        if isinstance(script_result, BaseModel):
            script_result = script_result.dict()
        elif isinstance(script_result, List):
            if len(script_result) > 0 and isinstance(script_result[0], BaseModel):
                script_result = [r.dict() for r in script_result]
        return script_result
        
    def inbound_list_streams(
        self,
        connection_method: str,
        connection_parameters: Dict,
        oauth_secret_name: Optional[str],
        other_secrets_name: Optional[str],
        sync_parameters: Dict,
        selected_streams: Optional[List[str]], # None to return all streams without requiring schema
    ):
        logger.info("Entered list_streams method")
        oauth_secret_name = normalise_nulls(oauth_secret_name)
        other_secrets_name = normalise_nulls(other_secrets_name)
        connection_secrets = self.get_secrets(oauth_secret_name, other_secrets_name)
        connection_parameters = parse_obj_as(
            Dict[str, StoredConfigurationValue], connection_parameters
        )
        sync_parameters = parse_obj_as(
            Dict[str, StoredConfigurationValue], sync_parameters
        )
        parameters = InboundSyncConfigurationParameters(
            connection_parameters=connection_parameters,
            connection_secrets=connection_secrets,
            sync_parameters=sync_parameters,
            connection_method=connection_method,
            current_form_parameters=None,
            currently_selected_streams=selected_streams
        )

        script_result = self._plugin_instance.inbound_stream_list(parameters)
        if isinstance(script_result, BaseModel):
            script_result = script_result.dict()
        elif isinstance(script_result, List):
            if len(script_result) > 0 and isinstance(script_result[0], BaseModel):
                script_result = [r.dict() for r in script_result]
        return script_result


    def construct_form_option(
        self,
        function_name: str,
        stored_values: List[Dict],
    ):
        logger.info("Entered construct_form_option method")
        stored_values_parsed = parse_obj_as(
            List[StoredConfigurationValue], stored_values
        )
        the_function = getattr(
            self._plugin_instance,
            function_name,
        )
        results:List[FormOption] = []
        for stored_value in stored_values_parsed:
            script_result = the_function(stored_value)
            if not isinstance(script_result, FormOption):
                raise ValueError(f"Expected a FormOption from function {function_name}, got {type(script_result)}")
            results.append(script_result.dict())
        return results

    def connection_form(self):
        logger.info("Entered connection_form method")
        form: List[ConnectionMethod] = self._plugin_instance.connection_form()
        return [f.dict() for f in form]

    def create_billing_events(self, session, event_request: Dict):
        logger.info("Entered create_billing_events method")
        request = parse_obj_as(BillingEventRequest, event_request)
        events: List[SnowflakeBillingEvent] = self._plugin_instance.create_billing_events(
            request
        )
        # create each billing event, waiting a second between each one
        first_time = True
        for billing_event in events:
            if not first_time:
                time.sleep(1)
            else:
                first_time = False
            timestamp_value = int(billing_event.timestamp.timestamp()*1000)
            if billing_event.start_timestamp is None:
                billing_event.start_timestamp = billing_event.timestamp
            start_timestamp_value=int(billing_event.start_timestamp.timestamp()*1000)
            try:
                event_query = f"""call SYSTEM$CREATE_BILLING_EVENT(
                        $${billing_event.billing_class}$$,
                        $${billing_event.sub_class}$$,
                        {start_timestamp_value},
                        {timestamp_value},
                        {str(billing_event.base_charge)},
                        $${json.dumps(billing_event.objects)}$$,
                        $${json.dumps(billing_event.additional_info)}$$)
                        """
                logger.info(f"Executing billing event query: {event_query}")
                result = session.sql(event_query).collect()
                logger.info(f"Billing event result: {result}")
            except Exception as e:
                if '370001:3159209004' in str(e):
                    logger.warn('Billing event creation failed due to running internally to Omnata')
                else:
                    raise e
        return [e.dict() for e in events]

    def get_secrets(
        self, oauth_secret_name: Optional[str], other_secrets_name: Optional[str]
    ) -> Dict[str, StoredConfigurationValue]:
        connection_secrets = {}
        # this is the new API for secrets access (https://docs.snowflake.com/en/LIMITEDACCESS/secret-api-reference)
        import _snowflake  # pylint: disable=import-error, import-outside-toplevel # type: ignore

        if oauth_secret_name is not None:
            connection_secrets["access_token"] = StoredConfigurationValue(
                value=_snowflake.get_oauth_access_token(oauth_secret_name)
            )
        if other_secrets_name is not None:
            try:
                secret_string_content = _snowflake.get_generic_secret_string(
                    other_secrets_name
                )
                if len(secret_string_content) > 2:
                    other_secrets = json.loads(secret_string_content)
                    connection_secrets = {
                        **connection_secrets,
                        **parse_obj_as(Dict[str, StoredConfigurationValue], other_secrets),
                    }
            except Exception as exception:
                logger.error(f"Error parsing secrets content for secret {other_secrets_name}: {str(exception)}")
                raise ValueError("Error parsing secrets content:") from exception
        return connection_secrets

    def network_addresses(self, method: str, connection_parameters: Dict) -> List[str]:
        logger.info("Entered network_addresses method")
        logger.info(f"Connection parameters: {connection_parameters}")
        from omnata_plugin_runtime.omnata_plugin import (
            ConnectionConfigurationParameters,
        )

        return self._plugin_instance.network_addresses(
            ConnectionConfigurationParameters(
                connection_method=method,
                connection_parameters=parse_obj_as(
                    Dict[str, StoredConfigurationValue], connection_parameters
                ),
                connection_secrets={},
            )
        )

    def connect(
        self,
        method:str,
        connection_parameters: Dict,
        network_rule_name: str,
        oauth_secret_name: Optional[str],
        other_secrets_name: Optional[str],
    ):
        logger.info("Entered connect method")
        logger.info(f"Connection parameters: {connection_parameters}")
        connection_secrets = self.get_secrets(oauth_secret_name, other_secrets_name)

        from omnata_plugin_runtime.omnata_plugin import (
            ConnectionConfigurationParameters,
        )

        connect_response = self._plugin_instance.connect(
            ConnectionConfigurationParameters(
                connection_method=method,
                connection_parameters=parse_obj_as(
                    Dict[str, StoredConfigurationValue], connection_parameters
                ),
                connection_secrets=connection_secrets
            )
        )
        # the connect method can also return more network addresses. If so, we need to update the
        # network rule associated with the external access integration
        if connect_response is None:
            raise ValueError("Plugin did not return a ConnectResponse object from the connect method")
        if connect_response.network_addresses is not None:
            existing_rule_result = self._session.sql(
                f"desc network rule {network_rule_name}"
            ).collect()
            rule_values: List[str] = existing_rule_result[0].value_list.split(",")
            for network_address in connect_response.network_addresses:
                if network_address not in rule_values:
                    rule_values.append(network_address)
            rule_values_string = ",".join([f"'{value}'" for value in rule_values])
            self._session.sql(
                f"alter network rule {network_rule_name} set value_list = ({rule_values_string})"
            ).collect()

        return connect_response.dict()

    def api_limits(self,
                   method:str,
                    connection_parameters: Dict,
                    oauth_secret_name: Optional[str],
                    other_secrets_name: Optional[str]):
        logger.info("Entered api_limits method")
        connection_secrets = self.get_secrets(oauth_secret_name, other_secrets_name)
        from omnata_plugin_runtime.omnata_plugin import (
            ConnectionConfigurationParameters,
        )
        connection_parameters = ConnectionConfigurationParameters(
            connection_method=method,
            connection_parameters=parse_obj_as(
                Dict[str, StoredConfigurationValue], connection_parameters
            ),
            connection_secrets=connection_secrets
        )
        response: List[ApiLimits] = self._plugin_instance.api_limits(connection_parameters)
        return [api_limit.dict() for api_limit in response]

    def outbound_record_validator(
        self,
        sync_parameters: Dict,
        field_mappings: Dict,
        transformed_record: Dict,
        source_types: Dict[str, str],
    ):
        # There's a bit of parsing here that could possibly be done outside of the handler function, but this shouldn't be too expensive
        sync_parameters: Dict[str, StoredConfigurationValue] = parse_obj_as(
            Dict[str, StoredConfigurationValue], sync_parameters
        )
        field_mappings: StoredMappingValue = parse_obj_as(
            StoredMappingValue, field_mappings
        )
        return self._plugin_instance.outbound_record_validator(
            sync_parameters, field_mappings, transformed_record, source_types
        )


def normalise_nulls(obj):
    """
    If an object came through a SQL interface with a null value, we convert it to a regular None here
    """
    if type(obj).__name__ == "sqlNullWrapper":
        return None
    # handle a bunch of objects being given at once
    if type(obj).__name__ == "list":
        return [normalise_nulls(x) for x in obj]
    return obj
