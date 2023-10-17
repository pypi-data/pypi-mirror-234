# pylint: disable=protected-access
"""
Omnata Plugin Runtime.
Includes data container classes and defines the contract for a plugin.
"""
from __future__ import annotations

import datetime
import http
import json
import queue
import threading
from abc import ABC, abstractmethod
from decimal import Decimal
from functools import partial, wraps
from logging import getLogger
from typing import Any, Callable, Dict, Iterable, List, Literal, Optional, Type, cast

import jinja2
import pandas
import pydantic
import pydantic.json
from dateutil.parser import parse
from jinja2 import Environment
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from snowflake.connector.pandas_tools import write_pandas
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

from .api import (
    PluginMessage,
    PluginMessageAbandonedStreams,
    PluginMessageCancelledStreams,
    PluginMessageCurrentActivity,
    PluginMessageStreamProgressUpdate,
    PluginMessageStreamState,
    handle_proc_result,
)
from .configuration import (
    STANDARD_OUTBOUND_SYNC_ACTIONS,
    ConnectionConfigurationParameters,
    InboundSyncConfigurationParameters,
    OutboundSyncAction,
    OutboundSyncConfigurationParameters,
    OutboundSyncStrategy,
    StoredConfigurationValue,
    StoredMappingValue,
    StoredStreamConfiguration,
    StreamConfiguration,
    SubscriptableBaseModel,
    SyncConfigurationParameters,
)
from .forms import (
    ConnectionMethod,
    InboundSyncConfigurationForm,
    OutboundSyncConfigurationForm,
)
from .rate_limiting import (
    ApiLimits,
    HttpMethodType,
    InterruptedWhileWaitingException,
    RateLimitState,
)

logger = getLogger(__name__)
SortDirectionType = Literal["asc", "desc"]


class PluginManifest(SubscriptableBaseModel):
    """
    Constructs a Plugin Manifest, which identifies the application, describes how it can work, and defines any runtime code dependancies.
        :param str plugin_id: A short, string identifier for the application, a combination of lowercase alphanumeric and underscores, e.g. "google_sheets"
        :param str plugin_name: A descriptive name for the application, e.g. "Google Sheets"
        :param str developer_id: A short, string identifier for the developer, a combination of lowercase alphanumeric and underscores, e.g. "acme_corp"
        :param str developer_name: A descriptive name for the developer, e.g. "Acme Corp"
        :param str docs_url: The URL where plugin documentation can be found, e.g. "https://docs.omnata.com"
        :param bool supports_inbound: A flag to indicate whether or not the plugin supports inbound sync. Support for inbound sync behaviours (full/incremental) is defined per inbound stream.
        :param List[OutboundSyncStrategy] supported_outbound_strategies: A list of sync strategies that the plugin can support, e.g. create,upsert.
    """

    plugin_id: str
    plugin_name: str
    developer_id: str
    developer_name: str
    docs_url: str
    supports_inbound: bool
    supported_outbound_strategies: List[OutboundSyncStrategy]


class PluginInfo(BaseModel):
    """
    Manifest plus other derived information about a plugin which is determined during upload.
    :param str manifest: The manifest from the plugin's code
    :param List[str] anaconda_packages: A list of anaconda packages required by the plugin
    :param List[str] bundled_packages: A list of bundled packages required by the plugin
    :param str icon_source: The base64 encoded icon for the plugin
    :param str plugin_class_name: The name of the plugin class
    :param bool has_custom_validator: Whether or not the plugin has a custom validator
    :param str plugin_runtime_version: The version of the Omnata plugin runtime that the current version of the plugin was built against
    :param str tier: The tier of the plugin. 
        Setting this to 'byo' means that the plugin is internally developed or a free community plugin. The sync engine does not bill for the first plugin of this type, nor are billing events created for it.
        Setting this to 'partner' means that the plugin was developed and distributed by a partner. 
        All other values only carry meaning for Omnata plugins, to indicate which iconography to apply within the application.
    :param str package_source: Whether the plugin is packaged as a function or a stage
    """

    manifest: PluginManifest
    anaconda_packages: List[str]
    bundled_packages: List[str]
    icon_source: Optional[str]
    plugin_class_name: str
    has_custom_validator: bool
    plugin_runtime_version: str
    tier: str
    package_source: Literal["function", "stage"]


def jinja_filter(func):
    """
    This annotation designates a function as a jinja filter.
    Adding it will put the function into the jinja globals so that it can be used in templates.
    """
    func.is_jinja_filter = True
    return func


class SyncRequest(ABC):
    """
    Functionality common to inbound and outbound syncs requests.

    Both inbound and outbound syncs have records to apply back to Snowflake (outbound have load results, inbound have records).
    So there's common functionality for feeding them in, as well as logging, other housekeeping tasks, and rate limiting.
    """

    def __init__(
        self,
        run_id: int,
        session: Session,
        source_app_name: str,
        results_schema_name: str,
        results_table_name: str,
        plugin_instance: OmnataPlugin,
        api_limits: List[ApiLimits],
        rate_limit_state: Dict[str, RateLimitState],
        run_deadline: datetime.datetime,
        development_mode: bool = False,
        test_replay_mode: bool = False,
    ):
        """
        Constructs a SyncRequest.

        :param int run_id: The ID number for the run, used to report back status to the engine
        :param any session: The snowpark session object, only used internally
        :param OmnataPlugin plugin_instance: The instance of the Omnata Plugin this request is for
        :param ApiLimits api_limits: Constraints to observe when performing HTTP requests
        :param bool development_mode: In development mode, apply_results_queue does not load into Snowflake, instead they are cached locally and can be retrieved via get_queued_results
        :return: nothing
        """
        logger.info(f"Initiating SyncRequest for sync run {run_id}")
        self._run_deadline = run_deadline
        self.plugin_instance = plugin_instance
        self._source_app_name = source_app_name
        self._results_schema_name = results_schema_name
        self._results_table_name = results_table_name
        self._full_results_table_name = (
            f"{source_app_name}.{results_schema_name}.{results_table_name}"
        )
        if self.plugin_instance is not None:
            self.plugin_instance._sync_request = self
        self._session: Session = session
        self._run_id = run_id
        self.api_limits = api_limits
        self.rate_limit_state = rate_limit_state
        self._apply_results = None  # this will be re-initialised by subclasses
        # these deal with applying the results, not sure they belong here
        self._apply_results_lock = threading.Lock()
        # Snowflake connector appears to not be thread safe
        # # File \"/var/task/snowflake/snowpark/table.py\", line 221, in _get_update_result\n
        #     return UpdateResult(int(rows[0][0]), int(rows[0][1]))\nIndexError: list index out of range"
        self._snowflake_query_lock = threading.Lock()
        self._loadbatch_id = 0
        self._loadbatch_id_lock = threading.Lock()
        self.development_mode = development_mode
        self.test_replay_mode = test_replay_mode
        # This is used internally by the testing framework, when we're loading records in a behave test
        self._prebaked_record_state: Optional[pandas.DataFrame] = None
        # create a stop requestor to cease thread activity
        self._thread_cancellation_token = threading.Event()
        self._thread_exception_thrown = None
        self._apply_results_task = None
        self._cancel_checking_task = None

        # create an exception handler for the threads
        def thread_exception_hook(args):
            logger.error("Thread exception", exc_info=True)
            self._thread_cancellation_token.set()  # this will tell the other threads to stop working
            logger.info(
                f"thread_cancellation_token: {self._thread_cancellation_token.is_set()}"
            )
            # nonlocal thread_exception_thrown
            self._thread_exception_thrown = args

        threading.excepthook = thread_exception_hook
        # start another worker thread to handle uploads of results every 10 seconds
        # we don't join on this thread, instead we cancel it once the workers have finished
        if self.development_mode is False:
            if self._apply_results_task is None:
                self._apply_results_task = threading.Thread(
                    target=self.__apply_results_worker,
                    args=(self._thread_cancellation_token,),
                )
                self._apply_results_task.start()
            if self._cancel_checking_task is None:
                self._cancel_checking_task = threading.Thread(
                    target=self.__cancel_checking_worker,
                    args=(self._thread_cancellation_token,),
                )
                self._cancel_checking_task.start()
        # also spin up a thread to monitor for run cancellation

    def __apply_results_worker(self, cancellation_token):
        """
        Designed to be run in a thread, this method polls the results every 10 seconds and sends them back to Snowflake.
        """
        while not cancellation_token.is_set():
            logger.info("apply results worker checking for results")
            self.apply_results_queue()
            cancellation_token.wait(10)
        logger.info("apply results worker exiting")

    def __cancel_checking_worker(self, cancellation_token):
        """
        Designed to be run in a thread, this method checks to see if the sync run has been cancelled.
        """
        while not cancellation_token.is_set():
            logger.info("cancel checking worker checking for results")

            with self._snowflake_query_lock:
                try:
                    # this is not ideal, but "Bind variable in stored procedure is not supported yet"
                    query_result = self._session.sql(
                        f"call {self._source_app_name}.API.PLUGIN_CANCELLATION_CHECK({self._run_id})"
                    ).collect()
                    cancellation_result = handle_proc_result(query_result)
                    is_cancelled: bool = cancellation_result["is_cancelled"]
                    if is_cancelled:
                        self.apply_cancellation()
                except Exception as e:
                    logger.error(f"Error updating activity: {e}")
            cancellation_token.wait(10)
        logger.info("cancel checking worker exiting")

    @abstractmethod
    def apply_results_queue(self):
        """
        Abstract method to apply the queued results. Inbound and Outbound syncs will each implement their own results
        processing logic
        """
        logger.error(
            "apply_results_queue called on SyncRequest base class, this should never occur"
        )

    @abstractmethod
    def apply_cancellation(self):
        """
        Abstract method to handle run cancellation.
        """

    @abstractmethod
    def apply_deadline_reached(self):
        """
        Abstract method to handle a run deadline being reached
        """

    def register_http_request(self, endpoint_category: str):
        """
        Registers a request as having just occurred, for rate limiting purposes.
        You only need to use this if your HTTP requests are not automatically being
        registered, which happens if http.client.HTTPConnection is not being used.
        """
        if endpoint_category in self.rate_limit_state:
            self.rate_limit_state[endpoint_category].register_http_request()

    def wait_for_rate_limiting(self, api_limit: ApiLimits) -> bool:
        """
        Waits for rate limits to pass before returning. Uses the api_limits and the history of
        request timestamps to determine how long to wait.

        :return: true if wait for rate limits was successful, otherwise false (thread was interrupted)
        :raises: DeadlineReachedException if rate limiting is going to require us to wait past the run deadline
        """
        if api_limit is None:
            return True
        wait_until = api_limit.calculate_wait(
            self.rate_limit_state[api_limit.endpoint_category]
        )
        if wait_until > self._run_deadline:
            # if the rate limiting is going to require us to wait past the run deadline, we bail out now
            raise DeadlineReachedException()
        time_now = datetime.datetime.utcnow()
        logger.info(
            f"calculated wait until date was {wait_until}, comparing to {time_now}"
        )

        while wait_until > time_now:
            seconds_to_sleep = (wait_until - time_now).total_seconds()
            if self._thread_cancellation_token.wait(seconds_to_sleep):
                return False
            wait_until = api_limit.calculate_wait(
                self.rate_limit_state[api_limit.endpoint_category]
            )
            time_now = datetime.datetime.utcnow()
        return True

    def wait(self, seconds: float) -> bool:
        """
        Waits for a given number of seconds, provided the current sync run isn't cancelled in the meantime.
        Returns True if no cancellation occurred, otherwise False.
        If False is returned, the plugin should exit immediately.
        """
        return not self._thread_cancellation_token.wait(seconds)

    def update_activity(self, current_activity: str):
        """
        Provides an update to the user on what's happening inside the sync run. It should
        be used before commencing a potential long-running phase, like polling and waiting or
        calling an API (keep in mind, rate limiting may delay even a fast API).
        Keep this to a very consise string, like 'Fetching records from API'.
        Avoid lengthy diagnostic messages, anything like this should be logged the normal way.
        """
        logger.info(f"Activity update: {current_activity}")
        self._plugin_message(
            PluginMessageCurrentActivity(current_activity=current_activity)
        )

    def _plugin_message(self, message: PluginMessage):
        """
        Sends a message back to the plugin. This is used to send back the results of a sync run.
        """
        logger.info(f"Sending plugin message: {message}")
        with self._snowflake_query_lock:
            try:
                # this is not ideal, but "Bind variable in stored procedure is not supported yet"
                handle_proc_result(
                    self._session.sql(
                        f"""call {self._source_app_name}.API.PLUGIN_MESSAGE(
                                  {self._run_id},
                                  PARSE_JSON($${json.dumps(message,default=pydantic.json.pydantic_encoder)}$$))"""
                    ).collect()
                )
            except Exception as e:
                logger.error(
                    f"Error sending plugin message: {e}", exc_info=True, stack_info=True
                )


class HttpRateLimiting:
    """
    A custom context manager which applies rate limiting automatically.
    Not thread safe but shouldn't need to be, since it'll be used once spanning all HTTP activity
    """

    def __init__(
        self, sync_request: SyncRequest, parameters: SyncConfigurationParameters
    ):
        self.sync_request = sync_request
        self.original_putrequest = None
        self.parameters = parameters

    def __enter__(self):
        """
        Used to manage the outbound http requests made by Omnata Plugins.
        It does this by patching http.client.HTTPConnection.putrequest
        """
        self_outer = self
        self.original_putrequest = http.client.HTTPConnection.putrequest  # type: ignore

        def new_putrequest(
            self,
            method: HttpMethodType,
            url: str,
            skip_host: bool = False,
            skip_accept_encoding: bool = False,
        ):
            # first, we do any waiting that we need to do (possibly none)
            matched_api_limit = ApiLimits.request_match(
                self_outer.sync_request.api_limits, method, url
            )
            if matched_api_limit is not None:
                if not self_outer.sync_request.wait_for_rate_limiting(
                    matched_api_limit
                ):
                    logger.info("Interrupted while waiting for rate limiting")
                    raise InterruptedWhileWaitingException()
                # and also register this current request in its limit category
                self_outer.sync_request.register_http_request(
                    matched_api_limit.endpoint_category
                )
            assert self_outer.original_putrequest is not None
            return self_outer.original_putrequest(
                self, method, url, skip_host, skip_accept_encoding
            )

        http.client.HTTPConnection.putrequest = new_putrequest  # type: ignore

    def __exit__(self, exc_type, exc_value, traceback):
        http.client.HTTPConnection.putrequest = self.original_putrequest  # type: ignore


class OutboundSyncRequest(SyncRequest):
    """
    A request to sync data outbound (from Snowflake to an app)
    """

    def __init__(
        self,
        run_id: int,
        session: Session,
        source_app_name: str,
        records_schema_name: str,
        records_table_name: str,
        results_schema_name: str,
        results_table_name: str,
        plugin_instance: OmnataPlugin,
        api_limits: List[ApiLimits],
        rate_limit_state: Dict[str, RateLimitState],
        run_deadline: datetime.datetime,
        development_mode: bool = False,
        test_replay_mode: bool = False,
    ):
        """
        Constructs an OutboundSyncRequest.

        :param int run_id: The ID number for the run, only used to report back on status
        :param any session: The snowpark session object, only used internally
        :param OmnataPlugin plugin_instance: The instance of the Omnata Plugin this request is for
        :param ApiLimits api_limits: Constraints to observe when performing HTTP requests
        :param bool development_mode: In development mode, apply_results_queue does not load into Snowflake, instead they are cached locally and can be retrieved via get_queued_results
        :param bool test_replay_mode: When enabled, it is safe to assume that HTTP requests are hitting a re-recorded log, so there is no need to wait in between polling
        :return: nothing
        """
        SyncRequest.__init__(
            self,
            run_id,
            session,
            source_app_name,
            results_schema_name,
            results_table_name,
            plugin_instance,
            api_limits,
            rate_limit_state,
            run_deadline,
            development_mode,
            test_replay_mode,
        )
        self._full_records_table_name = (
            f"{source_app_name}.{records_schema_name}.{records_table_name}"
        )
        self._apply_results: List[pandas.DataFrame] = []

    def _get_next_loadbatch_id(self):
        with self._loadbatch_id_lock:
            self._loadbatch_id = self._loadbatch_id + 1
            return self._loadbatch_id

    def apply_results_queue(self):
        """
        Merges all of the queued results and applies them
        """
        logger.info("OutboundSyncRequest apply_results_queue")
        if self._apply_results is not None:
            with self._apply_results_lock:
                self._apply_results = [
                    x for x in self._apply_results if x is not None and len(x) > 0
                ]  # remove any None/empty dataframes
                if len(self._apply_results) > 0:
                    logger.info(
                        f"Applying {len(self._apply_results)} batches of queued results"
                    )
                    # upload all cached apply results
                    all_dfs = pandas.concat(self._apply_results)
                    logger.info(f"applying: {all_dfs}")
                    self._apply_results_dataframe(all_dfs)
                    self._apply_results.clear()
                else:
                    logger.info("No queued results to apply")

    def apply_cancellation(self):
        """
        Handles a cancellation of an outbound sync.
        1. Signals an interruption to the load process for the other threads
        2. Applies remaining queued results
        3. Marks remaining active records as delayed
        """
        # set the token so that the other threads stop
        logger.info("Applying cancellation for OutboundSyncRequest")
        self._thread_cancellation_token.set()
        self.apply_results_queue()

    def apply_deadline_reached(self):
        """
        Handles the reaching of a deadline for an outbound sync.
        The behaviour is the same as for a cancellation, since the record state looks the same
        """
        logger.info("Apply deadline reached for OutboundSyncRequest")
        self.apply_cancellation()

    def enqueue_results(self, results: pandas.DataFrame):
        """
        Adds some results to the queue for applying asynchronously
        """
        logger.info(f"Enqueueing {len(results)} results for upload")
        for required_column in ["IDENTIFIER", "RESULT", "SUCCESS"]:
            if required_column not in results.columns:
                raise ValueError(
                    f"{required_column} column was not included in results"
                )
        with self._apply_results_lock:
            self._apply_results.append(results)

    def get_queued_results(self):
        """
        Returns results queued during processing
        """
        if len(self._apply_results) == 0:
            raise ValueError(
                "get_queued_results was called, but no results have been queued"
            )
        concat_results = pandas.concat(self._apply_results)
        return concat_results

    def _preprocess_results_dataframe(self, results_df: pandas.DataFrame):
        """
        Validates and pre-processes outbound sync results dataframe.
        The result is a dataframe contain all (and only):
        'IDENTIFIER' string
        'APP_IDENTIFIER' string
        'APPLY_STATE' string
        'APPLY_STATE_DATETIME' datetime (UTC)
        'LOADBATCH_ID' int
        'RESULT' object
        """
        results_df.set_index("IDENTIFIER", inplace=True, drop=False)
        results_df["APPLY_STATE_DATETIME"] = str(datetime.datetime.now().astimezone())
        if results_df is not None:
            logger.info(
                f"Applying a queued results dataframe of {len(results_df)} records"
            )
            # change the success flag to an appropriate APPLY STATUS
            results_df.loc[results_df["SUCCESS"] == True, "APPLY_STATE"] = "SUCCESS"
            results_df.loc[
                results_df["SUCCESS"] == False, "APPLY_STATE"
            ] = "DESTINATION_FAILURE"
            results_df = results_df.drop("SUCCESS", axis=1)
            # if results weren't added by enqueue_results, we'll add the status datetime column now
            if "APPLY_STATE_DATETIME" not in results_df.columns:
                results_df["APPLY_STATE_DATETIME"] = str(
                    datetime.datetime.now().astimezone()
                )
            if "APP_IDENTIFIER" not in results_df:
                results_df["APP_IDENTIFIER"] = None
            if "LOADBATCH_ID" not in results_df:
                results_df["LOADBATCH_ID"] = self._get_next_loadbatch_id()
        # trim out the columns we don't need to return
        return results_df[
            results_df.columns.intersection(
                [
                    "IDENTIFIER",
                    "APP_IDENTIFIER",
                    "APPLY_STATE",
                    "APPLY_STATE_DATETIME",
                    "LOADBATCH_ID",
                    "RESULT",
                ]
            )
        ]

    def _apply_results_dataframe(self, results_df: pandas.DataFrame):
        """
        Applies results for an outbound sync. This involves merging back onto the record state table
        """
        logger.info("applying results to table")
        # use a random table name with a random string to avoid collisions
        with self._snowflake_query_lock:
            success, nchunks, nrows, _ = write_pandas(
                conn=self._session._conn._cursor.connection,  # pylint: disable=protected-access
                df=self._preprocess_results_dataframe(results_df),
                quote_identifiers=False,
                table_name=self._full_results_table_name,
                auto_create_table=False,
            )
            if not success:
                raise ValueError(
                    f"Failed to write results to table {self._full_results_table_name}"
                )
            logger.info(
                f"Wrote {nrows} rows and {nchunks} chunks to table {self._full_results_table_name}"
            )

    def __dataframe_wrapper(
        self, data_frame: pandas.DataFrame, render_jinja: bool = True
    ) -> pandas.DataFrame:
        """
        Takes care of some common stuff we need to do for each dataframe for outbound syncs.
        Parses the JSON in the transformed record column (Snowflake passes it as a string).
        Also when the mapper is a jinja template, renders it.
        """
        # if data_frame is None:
        #    logger.info(
        #        "Dataframe wrapper skipping pre-processing as dataframe is None"
        #    )
        #    return None
        logger.info(
            f"Dataframe wrapper pre-processing {len(data_frame)} records: {data_frame}"
        )
        if len(data_frame) > 0:
            try:
                data_frame["TRANSFORMED_RECORD"] = data_frame[
                    "TRANSFORMED_RECORD"
                ].apply(json.loads)
            except TypeError as type_error:
                logger.error(
                    "Error parsing transformed record output as JSON", exc_info=True
                )
                if (
                    "the JSON object must be str, bytes or bytearray, not NoneType"
                    in str(type_error)
                ):
                    raise ValueError(
                        "null was returned from the record transformer, an object must always be returned"
                    ) from type_error
            if (
                render_jinja
                and "jinja_template" in data_frame.iloc[0]["TRANSFORMED_RECORD"]
            ):
                logger.info("Rendering jinja template")
                env = Environment()
                # examine the plugin instance for jinja_filter decorated methods
                if self.plugin_instance is not None:
                    for name in dir(self.plugin_instance):
                        member = getattr(self.plugin_instance, name)
                        if callable(member) and hasattr(member, "is_jinja_filter"):
                            logger.info(f"Adding jinja filter to environment: {name}")
                            env.filters[name] = member

                def do_jinja_render(jinja_env, row_value):
                    logger.info(f"do_jinja_render: {row_value}")
                    jinja_template = jinja_env.from_string(row_value["jinja_template"])
                    try:
                        rendered_result = jinja_template.render(
                            {"row": row_value["source_record"]}
                        )
                        logger.info(
                            f"Individual jinja rendering result: {rendered_result}"
                        )
                        return rendered_result
                    except TypeError as type_error:
                        # re-throw as a template error so that we can handle it nicely
                        logger.error("Error during jinja render", exc_info=True)
                        raise jinja2.TemplateError(str(type_error)) from type_error

                # bit iffy about using apply since historically it's not guaranteed only-once, apparently tries to be clever with vectorizing
                data_frame["TRANSFORMED_RECORD"] = data_frame.apply(
                    lambda row: do_jinja_render(env, row["TRANSFORMED_RECORD"]), axis=1
                )
                # if it breaks things in future, switch to iterrows() and at[]
        return data_frame

    def get_records(
        self,
        sync_actions: Optional[List[OutboundSyncAction]] = None,
        batched: bool = False,
        render_jinja: bool = True,
        sort_column: Optional[str] = None,
        sort_direction: SortDirectionType = "desc",
    ) -> pandas.DataFrame | Iterable[pandas.DataFrame]:
        """
        Retrieves a dataframe of records to create,update or delete in the app.
        :param List[OutboundSyncAction] sync_action: Which sync actions to included (includes all standard actions by default)
        :param bool batched: If set to true, requests an iterator for a batch of dataframes. This is needed if a large data size (multiple GBs or more) is expected, so that the whole dataset isn't held in memory at one time.
        :param bool render_jinja: If set to true and a jinja template is used, renders it automatically.
        :param str sort_column: Applies a sort order to the dataframe.
        :param SortDirectionType sort_direction: The sort direction, 'asc' or 'desc'
        :type SortDirectionType: Literal['asc','desc']
        :return: A pandas dataframe if batched is False (the default), otherwise an iterator of pandas dataframes
        :rtype: pandas.DataFrame or iterator
        """
        if sync_actions is None:
            sync_actions = [
                action() for action in list(STANDARD_OUTBOUND_SYNC_ACTIONS.values())
            ]
        # ignore null sync actions
        sync_action_names: List[str] = [s.action_name for s in sync_actions if s]
        # only used by testing framework when running a behave test
        if self._prebaked_record_state is not None:
            logger.info("returning prebaked record state")
            dataframe = self._prebaked_record_state[
                self._prebaked_record_state["SYNC_ACTION"].isin(sync_action_names)
            ]  # pylint: disable=unsubscriptable-object
            if len(dataframe) == 0 or not batched:
                # no need to do the whole FixedSizeGenerator thing for 0 records
                return self.__dataframe_wrapper(dataframe, render_jinja)
            # we use map to create an iterable wrapper around the pandas batches which are also iterable
            # we use an intermediate partial to allow us to pass the extra parameter
            mapfunc = partial(self.__dataframe_wrapper, render_jinja=render_jinja)
            return map(mapfunc, [dataframe])
        with self._snowflake_query_lock:
            dataframe = (
                self._session.table(self._full_records_table_name)
                .filter((col("SYNC_ACTION").in_(sync_action_names)))  # type: ignore
                .select(
                    col("IDENTIFIER"), col("SYNC_ACTION"), col("TRANSFORMED_RECORD")
                )
            )
        # apply sorting
        if sort_column is not None:
            sort_col = col(sort_column)
            sorted_col = sort_col.desc() if sort_direction == "desc" else sort_col.asc()
            dataframe = dataframe.sort(sorted_col)
        if batched:
            # we use map to create an iterable wrapper around the pandas batches which are also iterable
            # we use an intermediate partial to allow us to pass the extra parameter
            mapfunc = partial(self.__dataframe_wrapper, render_jinja=render_jinja)
            return map(mapfunc, dataframe.to_pandas_batches())
            # return map(self.__dataframe_wrapper,dataframe.to_pandas_batches(),render_jinja)
        return self.__dataframe_wrapper(dataframe.to_pandas(), render_jinja)


class InboundSyncRequest(SyncRequest):
    """
    Encapsulates a request to retrieve records from an application.
    """

    def __init__(
        self,
        run_id: int,
        session: Session,
        source_app_name: str,
        results_schema_name: str,
        results_table_name: str,
        plugin_instance: OmnataPlugin,
        api_limits: List[ApiLimits],
        rate_limit_state: Dict[str, RateLimitState],
        run_deadline: datetime.datetime,
        streams: List[StoredStreamConfiguration],
        development_mode: bool = False,
        test_replay_mode: bool = False,
    ):
        """
        Constructs a record apply request.

        :param int sync_id: The ID number for the sync, only used internally
        :param int sync_slug: The slug for the sync, only used internally
        :param int sync_branch_id: The ID number for the sync branch (optional), only used internally
        :param int sync_branch_name: The name of the branch (main or otherwise), only used internally
        :param int run_id: The ID number for the run, only used internally
        :param any session: The snowpark session object, only used internally
        :param OmnataPlugin plugin_instance: The instance of the Omnata Plugin this request is for
        :param ApiLimits api_limits: Constraints to observe when performing HTTP requests
        :param bool development_mode: In development mode, apply_results_queue does not load into Snowflake, instead they are cached locally and can be retrieved via get_queued_results
        :param StoredStreamConfiguration streams: The configuration for each stream to fetch
        :param bool test_replay_mode: When enabled, it is safe to assume that HTTP requests are hitting a re-recorded log, so there is no need to wait in between polling
        :return: nothing
        """
        SyncRequest.__init__(
            self,
            run_id,
            session,
            source_app_name,
            results_schema_name,
            results_table_name,
            plugin_instance,
            api_limits,
            rate_limit_state,
            run_deadline,
            development_mode,
            test_replay_mode,
        )
        self.streams = streams
        self._streams_dict: Dict[str, StoredStreamConfiguration] = {
            s.stream_name: s for s in streams
        }
        self._apply_results: Dict[str, List[pandas.DataFrame]] = {}
        self._latest_states: Dict[str, Any] = {}
        self._temp_tables = {}
        self._temp_table_lock = threading.Lock()
        self._results_exist: Dict[
            str, bool
        ] = {}  # track whether or not results exist for stream
        self._stream_record_counts: Dict[str, int] = {
            stream_name: 0 for stream_name in self._streams_dict.keys()
        }
        self._stream_change_counts: Dict[str, int] = {
            stream_name: 0 for stream_name in self._streams_dict.keys()
        }
        self._completed_streams: List[str] = []

    def apply_results_queue(self):
        """
        Merges all of the queued results and applies them
        """
        logger.info("InboundSyncRequest apply_results_queue ")
        if self._apply_results is not None:
            with self._apply_results_lock:
                for stream_name, stream_results in self._apply_results.items():
                    results = [
                        x for x in stream_results if x is not None and len(x) > 0
                    ]  # remove any None/empty dataframes
                    if len(results) > 0:
                        logger.info(
                            f"Applying {len(results)} batches of queued results"
                        )
                        # upload all cached apply results
                        all_dfs = pandas.concat(results)
                        logger.info(f"applying: {all_dfs}")
                        self._apply_results_dataframe(stream_name, all_dfs)
                        # add the count of this batch to the total for this stream
                        self._stream_record_counts[
                            stream_name
                        ] = self._stream_record_counts[stream_name] + len(all_dfs)
                    # update the stream state object too
                    self._apply_latest_states()
                    self._apply_results[stream_name] = None
                self._apply_results = {}
                # update the inbound stream record counts, so we can see progress
                self._plugin_message(
                    message=PluginMessageStreamProgressUpdate(
                        stream_total_counts=self._stream_record_counts,
                        completed_streams=self._completed_streams,
                    )
                )

    def apply_cancellation(self):
        """
        Signals an interruption to the load process for the other threads.
        Also updates the Sync Run to include which streams were cancelled.
        """
        # set the token so that the other threads stop
        self._thread_cancellation_token.set()
        # any stream which didn't complete at this point is considered cancelled
        cancelled_streams = [
            stream.stream_name
            for stream in self.streams
            if stream.stream_name not in self._completed_streams
        ]
        self._plugin_message(
            message=PluginMessageCancelledStreams(cancelled_streams=cancelled_streams)
        )

    def apply_deadline_reached(self):
        """
        Signals an interruption to the load process for the other threads.
        Also updates the Sync Run to include which streams were abandoned.
        """
        # set the token so that the other threads stop
        self._thread_cancellation_token.set()
        # any stream which didn't complete at this point is considered abandoned
        abandoned_streams = [
            stream.stream_name
            for stream in self.streams
            if stream.stream_name not in self._completed_streams
        ]
        self._plugin_message(
            message=PluginMessageAbandonedStreams(abandoned_streams=abandoned_streams)
        )

    def enqueue_results(self, stream_name: str, results: List[Dict], new_state: Any):
        """
        Adds some results to the queue for applying asynchronously
        """
        # TODO: maybe also have a mechanism to apply immediately if the queued results are getting too large
        logger.info(f"Enqueueing {len(results)} results for upload")
        if stream_name is None or len(stream_name) == 0:
            raise ValueError("Stream name cannot be empty")
        with self._apply_results_lock:
            existing_results: List[pandas.DataFrame] = []
            if stream_name in self._apply_results:
                existing_results = self._apply_results[stream_name]
            existing_results.append(self._preprocess_results_list(stream_name, results))
            self._apply_results[stream_name] = existing_results
            current_latest = self._latest_states or {}
            self._latest_states = {**current_latest, **{stream_name: new_state}}

    def mark_stream_complete(self, stream_name: str):
        """
        Marks a stream as completed, this is called automatically per stream when using @managed_inbound_processing.
        If @managed_inbound_processing is not used, call this whenever a stream has finished recieving records.
        """
        self._completed_streams.append(stream_name)
        # dedup just in case it's called twice
        self._completed_streams = list(set(self._completed_streams))

    def _enqueue_state(self, stream_name: str, new_state: Any):
        """
        Enqueues some new stream state to be stored. This method should not be called directly,
        instead you should store state using the new_state parameter in the enqueue_results
        method to ensure it's applied along with the associated new records.
        """
        with self._apply_results_lock:
            current_latest = self._latest_states or {}
            self._latest_states = {**current_latest, **{stream_name: new_state}}

    def get_queued_results(self, stream_name: str):
        """
        Returns results queued during processing
        """
        if (
            stream_name not in self._apply_results
            or len(self._apply_results[stream_name]) == 0
        ):
            raise ValueError(
                "get_queued_results was called, but no results have been queued"
            )
        concat_results = pandas.concat(self._apply_results[stream_name])
        return concat_results

    def _convert_by_json_schema(
        self, stream_name: str, data: Dict, json_schema: Dict
    ) -> Dict:
        """
        Apply opportunistic normalization before loading into Snowflake
        """
        try:
            datetime_properties = [
                k
                for k, v in json_schema["properties"].items()
                if "format" in v and v["format"] == "date-time"
            ]
            for datetime_property in datetime_properties:
                try:
                    if datetime_property in data:
                        data[datetime_property] = parse(
                            data[datetime_property]
                        ).isoformat()
                except Exception as exception2:
                    logger.debug(
                        f"Failure to convert inbound data property {datetime_property} on stream {stream_name}: {str(exception2)}"
                    )
        except Exception as exception:
            logger.debug(f"Failure to convert inbound data: {str(exception)}")
        return data

    def _preprocess_results_list(self, stream_name: str, results: List[Dict]):
        """
        Creates a dataframe from the enqueued list, ready to upload.
        The result is a dataframe contain all (and only):
        'APP_IDENTIFIER' string
        'STREAM_NAME' string
        'RETRIEVE_DATE' datetime (UTC)
        'RECORD_DATA' object
        """
        # for required_column in ['RECORD_DATA']:
        #    if required_column not in results_df.columns:
        #        raise ValueError(f'{required_column} column was not included in results')
        if stream_name not in self._streams_dict:
            raise ValueError(
                f"Cannot preprocess results for stream {stream_name} as its configuration doesn't exist"
            )
        logger.info(f"preprocessing for stream: {self._streams_dict[stream_name]}")
        if len(results) > 0:
            # we need to check that each record in the results contains the primary key field,
            # and also remove any values (included nesting) which are empty dicts
            # The latter is to prevent the arror error: Cannot write struct type '<field_name>' with no child field to Parquet. Consider adding a dummy child field.
            for result in results:
                if primary_key_field not in result:
                    raise ValueError(
                        f"Primary key field {primary_key_field} was not present in all records for stream {stream_name}"
                    )
            results = [remove_empty_dict_values(result) for result in results]
            stream_obj: StreamConfiguration = self._streams_dict[stream_name].stream
            results_df = pandas.DataFrame.from_dict(
                [
                    {
                        "RECORD_DATA": self._convert_by_json_schema(
                            stream_name, data, stream_obj.json_schema  # type: ignore
                        )
                    }
                    for data in results
                ]
            )
            if (
                self._streams_dict[stream_name].stream.source_defined_primary_key
                is not None
            ):
                primary_key_field = self._streams_dict[
                    stream_name
                ].stream.source_defined_primary_key
                results_df["APP_IDENTIFIER"] = results_df["RECORD_DATA"].apply(
                    lambda x: x[primary_key_field]
                )
            elif self._streams_dict[stream_name].primary_key_field is not None:
                primary_key_field = self._streams_dict[stream_name].primary_key_field
                results_df["APP_IDENTIFIER"] = results_df["RECORD_DATA"].apply(
                    lambda x: x[primary_key_field]
                )
            else:
                results_df["APP_IDENTIFIER"] = None
            # the timestamps in Snowflake are TIMESTAMP_LTZ, so we upload in string format to ensure the
            # timezone information is present.
            results_df["RETRIEVE_DATE"] = str(datetime.datetime.now().astimezone())
            results_df["STREAM_NAME"] = stream_name
        else:
            results_df = pandas.DataFrame(
                [],
                columns=[
                    "APP_IDENTIFIER",
                    "STREAM_NAME",
                    "RECORD_DATA",
                    "RETRIEVE_DATE",
                ],
            )
        # trim out the columns we don't need to return
        return results_df[
            results_df.columns.intersection(
                ["APP_IDENTIFIER", "STREAM_NAME", "RECORD_DATA", "RETRIEVE_DATE"]
            )
        ]

    def _apply_results_dataframe(self, stream_name: str, results_df: pandas.DataFrame):
        """
        Applies results for an inbound sync. The results are staged into a temporary
        table in Snowflake, so that we can make an atomic commit at the end.
        """
        if len(results_df) > 0:
            with self._snowflake_query_lock:
                logger.info(
                    f"Applying {len(results_df)} results to {self._full_results_table_name}"
                )
                success, nchunks, nrows, _ = write_pandas(
                    conn=self._session._conn._cursor.connection,  # pylint: disable=protected-access
                    df=results_df,
                    table_name=self._full_results_table_name,
                    quote_identifiers=False,  # already done in get_temp_table_name
                    # schema='INBOUND_RAW', # it seems to be ok to provide schema in the table name
                    table_type="transient",
                )
                if not success:
                    raise ValueError(
                        f"Failed to write results to table {self._full_results_table_name}"
                    )
                logger.info(
                    f"Wrote {nrows} rows and {nchunks} chunks to table {self._full_results_table_name}"
                )
                # temp tables aren't allowed
                # snowflake_df = self._session.create_dataframe(results_df)
                # snowflake_df.write.save_as_table(table_name=temp_table,
                #                                mode='append',
                #                                column_order='index',
                #                                #create_temp_table=True
                #                                )
                self._results_exist[stream_name] = True
        else:
            logger.info("Results dataframe is empty, not applying")

    def _apply_latest_states(self):
        """
        Updates the SYNC table to have the latest stream states.
        TODO: This should be done in concert with the results, revisit
        """
        self._plugin_message(PluginMessageStreamState(stream_state=self._latest_states))


class ConnectResponse(SubscriptableBaseModel):
    """
    Encapsulates the response to a connection request. This is used to pass back any additional
    information that may be discovered during connection that's relevant to the plugin (e.g. Account Identifiers).
    You can also specifies any additional network addresses that are needed to connect to the app, that might not
    have been known until the connection was made.
    """

    connection_parameters: dict = {}
    connection_secrets: dict = {}
    network_addresses: List[str] = []


class SnowflakeBillingEvent(BaseModel):
    """
    The inputs to Snowflake's SYSTEM$CREATE_BILLING_EVENT function.
    See https://docs.snowflake.com/en/sql-reference/functions/system_create_billing_event
    """

    billing_class: str
    base_charge: Decimal
    timestamp: datetime.datetime = datetime.datetime.now()
    sub_class: Optional[str] = None
    start_timestamp: Optional[datetime.datetime] = None
    objects: List[str] = []
    additional_info: Dict[str, Any] = {}

class BillingEventRequest(BaseModel):
    """
    Represents a request to provide billing events for that day.
    """

    billing_schedule: Literal["DAILY"]
    has_active_inbound: bool
    has_active_outbound: bool


# BillingEventRequest = Annotated[Union[DailyBillingEventRequest,...],Field(discriminator='billing_schedule')]


class OmnataPlugin(ABC):
    """
    Class which defines the contract for an Omnata Push Plugin
    """

    def __init__(self):
        """
        Plugin constructors must never take parameters
        """
        self._sync_request: Optional[SyncRequest] = None

    @abstractmethod
    def get_manifest(self) -> PluginManifest:
        """
        Returns a manifest object to describe the plugin and its capabilities
        """
        raise NotImplementedError(
            "Your plugin class must implement the get_manifest method"
        )

    @abstractmethod
    def connection_form(self) -> List[ConnectionMethod]:
        """
        Returns a form definition so that user input can be collected, in order to connect to an app

        :return A list of ConnectionMethods, each of which offer a way of authenticating to the app and describing what information must be captured
        :rtype List[ConnectionMethod]
        """
        raise NotImplementedError(
            "Your plugin class must implement the connection_form method"
        )

    @abstractmethod
    def network_addresses(
        self, parameters: ConnectionConfigurationParameters
    ) -> List[str]:
        """
        Returns a list of network addresses that are required to connect to the app.
        This will be called after the connection form is completed, so that collected information can be used to build the list.
        Note that at this point, no external access is possible.

        :param ConnectionConfigurationParameters parameters the parameters of the connection, configured so far.
        :return A list of domains that will be added to a network rule to permit outbound access from Snowflake
        for the authentication step. Note that for OAuth Authorization flows, it is not necessary to provide the
        initial URL that the user agent is directed to.
        :rtype List[str]
        """
        raise NotImplementedError(
            "Your plugin class must implement the network_addresses method"
        )

    def outbound_configuration_form(
        self, parameters: OutboundSyncConfigurationParameters
    ) -> OutboundSyncConfigurationForm:
        """
        Returns a form definition so that user input can be collected. This function may be called repeatedly with new parameter values
        when dependant fields are used

        :param OutboundSyncConfigurationParameters parameters the parameters of the sync, configured so far.
        :return A OutboundSyncConfigurationForm, which describes what information must be collected to configure the sync
        :rtype OutboundSyncConfigurationForm
        """
        raise NotImplementedError(
            "Your plugin class must implement the outbound_configuration_form method"
        )

    def inbound_configuration_form(
        self, parameters: InboundSyncConfigurationParameters
    ) -> InboundSyncConfigurationForm:
        """
        Returns a form definition so that user input can be collected. This function may be called repeatedly with new parameter values
        when dependant fields are used

        :param InboundSyncConfigurationParameters parameters the parameters of the sync, configured so far.
        :return A InboundSyncConfigurationForm, which describes what information must be collected to configure the sync
        :rtype InboundSyncConfigurationForm
        """
        raise NotImplementedError(
            "Your plugin class must implement the inbound_configuration_form method"
        )
    
    def inbound_stream_list(
        self, parameters: InboundSyncConfigurationParameters
    ) -> List[StreamConfiguration]:
        """
        Returns a list of streams which can be sync'd from the app. This function is called after the form returned by inbound_configuration_form
        has been completed, so that collected information can be used to build the list.

        :param InboundSyncConfigurationParameters parameters the parameters of the sync
        :return A list of streams which can be sync'd from the app. This may vary based on the parameters provided.
        :rtype List[StreamConfiguration]
        """
        raise NotImplementedError(
            "Your plugin class must implement the inbound_stream_list method"
        )

    @abstractmethod
    def connect(self, parameters: ConnectionConfigurationParameters) -> ConnectResponse:
        """
        Connects to an app, validating that the information provided by the user was correct.
        For OAuth connection methods, this will be called after the OAuth flow has completed, so the
        access token will be available in the parameters.

        :param PluginConfigurationParameters parameters the parameters of the sync, as configured by the user
        :return A ConnectResponse, which may provide further information about the app instance for storing
        :rtype ConnectResponse
        :raises ValueError: if issues were encountered during connection
        """
        raise NotImplementedError("Your plugin class must implement the connect method")

    def sync_outbound(
        self,
        parameters: OutboundSyncConfigurationParameters,
        outbound_sync_request: OutboundSyncRequest,
    ):
        """
        Applies a set of changed records to an app. This function is called whenever a run occurs and changed records
        are found.
        To return results, invoke outbound_sync_request.enqueue_results() during the load process.

        :param PluginConfigurationParameters parameters the parameters of the sync, as configured by the user
        :param OutboundSyncRequest outbound_sync_request an object describing what has changed
        :return None
        :raises ValueError: if issues were encountered during connection
        """
        raise NotImplementedError(
            "Your plugin class must implement the sync_outbound method"
        )

    def outbound_record_validator(
        self,
        sync_parameters: Dict[str, StoredConfigurationValue],
        field_mappings: StoredMappingValue,
        transformed_record: Dict[str, Any],
        source_types: Dict[str, str],
    ) -> Optional[Dict[str, str]]:
        """
        Performs validation on a transformed record, returning errors by field name (from the transformed record) if the record is invalid, or None if the record is valid
        Parameters:
            sync_parameters: the configured sync parameters, this will be the same for all records
            field_mappings: the configured field mappings, this will be the same for all records.
                If this is an instance of StoredFieldMappings, there may be target system metadata used for validation (e.g. an ID field that must conform to a specific format)
            transformed_record: the transformed record, which is either a source column value, literal value or expression, mapped to a target field name
            source_types: a dictionary of field names to the original SQL type of the source column/literal/expression (before conversion to variant), as returned by SYSTEM$TYPEOF.
                Leveraging this information may be simpler than trying to parse the transformed values to determine if the original type is compatible
        """

    def sync_inbound(
        self,
        parameters: InboundSyncConfigurationParameters,
        inbound_sync_request: InboundSyncRequest,
    ):
        """
        Retrieves the next set of records from an application.
        The inbound_sync_request contains the list of streams to be synchronized.
        To return results, invoke inbound_sync_request.enqueue_results() during the load process.

        :param PluginConfigurationParameters parameters the parameters of the sync, as configured by the user
        :param InboundSyncRequest inbound_sync_request an object describing what needs to be sync'd
        :return None
        :raises ValueError: if issues were encountered during connection
        """
        raise NotImplementedError(
            "Your plugin class must implement the sync_inbound method"
        )

    def api_limits(self, parameters: ConnectionConfigurationParameters) -> List[ApiLimits]:
        """
        Defines the API limits in place for the app's API
        """
        return []

    def create_billing_events(self, request: BillingEventRequest) -> List[SnowflakeBillingEvent]:
        """
        Creates billing events for the day, these will be submitted to the Snowflake event billing API.
        Note that the Snowflake API is strictly rate limited, so only a very small number of events
        should be returned.
        """
        return []

    def additional_loggers(self) -> List[str]:
        """
        Ordinarily, your plugin code will log to a logger named 'omnata_plugin' and these
        messages will automatically be stored in Snowflake and associated with the current
        sync run, so that they appear in the UI's logs.
        However, if you leverage third party python libraries, it may be useful to capture
        log messages from those as well. Overriding this method and returning the names of
        any additional loggers, will cause them to be captured as well.
        For example, if the source code of a third party libary includes:
        logging.getLogger(name='our_api_wrapper'), then returning ['our_api_wrapper']
        will capture its log messages.
        The capture level of third party loggers will be whatever is configured for the sync.
        """
        return []


class FixedSizeGenerator:
    """
    A thread-safe class which wraps the pandas batches generator provided by Snowflake,
    but provides batches of a fixed size.
    """

    def __init__(self, generator, batch_size):
        self.generator = generator
        # handle dataframe as well as a dataframe generator, just to be more flexible
        if self.generator.__class__.__name__ == "DataFrame":
            logger.info(
                f"Wrapping a dataframe of length {len(self.generator)} in a map so it acts as a generator"
            )
            self.generator = map(lambda x: x, [self.generator])
        self.leftovers = None
        self.batch_size = batch_size
        self.thread_lock = threading.Lock()

    def __next__(self):
        with self.thread_lock:
            logger.info(f"initial leftovers: {self.leftovers}")
            records_df = self.leftovers
            self.leftovers = None
            try:
                # build up a dataframe until we reach the batch size
                while records_df is None or len(records_df) < self.batch_size:
                    current_count = 0 if records_df is None else len(records_df)
                    logger.info(
                        f"fetching another dataframe from the generator, got {current_count} out of a desired {self.batch_size}"
                    )
                    next_df = next(self.generator)
                    if next_df is not None and next_df.__class__.__name__ not in (
                        "DataFrame"
                    ):
                        logger.error(
                            f"Dataframe generator provided an unexpected object, type {next_df.__class__.__name__}"
                        )
                        raise ValueError(
                            f"Dataframe generator provided an unexpected object, type {next_df.__class__.__name__}"
                        )
                    if next_df is None and records_df is None:
                        logger.info(
                            "Original and next dataframes were None, returning None"
                        )
                        return None
                    records_df = pandas.concat([records_df, next_df])
                    logger.info(
                        f"after concatenation, dataframe has {len(records_df)} records"
                    )
            except StopIteration:
                logger.info("FixedSizeGenerator consumed the last pandas batch")

            if records_df is None:
                logger.info("No records left, returning None")
                return None
            elif records_df is not None and len(records_df) > self.batch_size:
                logger.info(
                    f"putting {len(records_df[self.batch_size:])} records back ({len(records_df)} > {self.batch_size})"
                )
                self.leftovers = records_df[self.batch_size :].reset_index(drop=True)
                records_df = records_df[0 : self.batch_size].reset_index(drop=True)
            else:
                current_count = 0 if records_df is None else len(records_df)
                logger.info(
                    f"{current_count} records does not exceed batch size, not putting any back"
                )
            logger.info(f"FixedSizeGenerator about to return dataframe {records_df}")
            return records_df

    def __iter__(self):
        """Returns the Iterator object"""
        return self


def __managed_outbound_processing_worker(
    plugin_class_obj: OmnataPlugin,
    method: Callable,
    worker_index: int,
    dataframe_generator: FixedSizeGenerator,
    cancellation_token: threading.Event,
    method_args,
    method_kwargs,
):
    """
    A worker thread for the managed_outbound_processing annotation.
    Consumes a fixed sized set of records by passing them to the wrapped function,
    while adhering to the defined API constraints.
    """
    logger.info(
        f"worker {worker_index} processing. Cancelled: {cancellation_token.is_set()}"
    )
    while not cancellation_token.is_set():
        # Get our generator object out of the queue
        assert (
            plugin_class_obj._sync_request is not None
        )  # pylint: disable=protected-access
        if (
            datetime.datetime.now() > plugin_class_obj._sync_request._run_deadline
        ):  # pylint: disable=protected-access
            # if we've reached the deadline for the run, end it
            plugin_class_obj._sync_request.apply_deadline_reached()  # pylint: disable=protected-access
            return
        records_df = next(dataframe_generator)
        logger.info(f"records returned from dataframe generator: {records_df}")
        if records_df is None:
            logger.info(f"worker {worker_index} has no records left to process")
            return
        elif len(records_df) == 0:
            logger.info(f"worker {worker_index} has 0 records left to process")
            return

        logger.info(
            f"worker {worker_index} fetched {len(records_df)} records for processing"
        )
        # threads block while waiting for their allocation of records, it's possible there's been
        # a cancellation in the meantime
        if cancellation_token.is_set():
            logger.info(
                f"worker {worker_index} exiting before applying records, due to cancellation"
            )
            return
        logger.info(f"worker {worker_index} processing {len(records_df)} records")
        # restore the first argument, was originally the dataframe/generator but now it's the appropriately sized dataframe
        try:
            results_df = method(
                plugin_class_obj, *(records_df, *method_args), **method_kwargs
            )
        except InterruptedWhileWaitingException:
            # If an outbound run is cancelled while waiting for rate limiting, this should mean that
            # the cancellation is handled elsewhere, so we don't need to do anything special here other than stop waiting
            logger.info(
                f"worker {worker_index} interrupted while waiting for rate limiting, exiting"
            )
            return
        logger.info(
            f"worker {worker_index} received {len(results_df)} results, applying"
        )

        # we want to write the results of the batch back to Snowflake, so we
        # enqueue them and they'll be picked up by the apply_results worker
        outbound_sync_request = cast(
            OutboundSyncRequest, plugin_class_obj._sync_request
        )  # pylint: disable=protected-access
        outbound_sync_request.enqueue_results(
            results_df
        )  # pylint: disable=protected-access
        logger.info(
            f"worker {worker_index} applied results, marking queue task as done"
        )


def managed_outbound_processing(concurrency: int, batch_size: int):
    """
    This is a decorator which can be added to a method on an OmnataPlugin class.
    It expects to be invoked with either a DataFrame or a DataFrame generator, and
    the method will receive a DataFrame of the correct size based on the batch_size parameter.

    The decorator itself must be used as a function call with tuning parameters like so:
    @managed_outbound_processing(concurrency=5, batch_size=100)
    def my_function(param1,param2)

    Threaded workers will be used to invoke in parallel, according to the concurrency constraints.

    The decorated method is expected to return a DataFrame with the outcome of each record that was provided.
    """

    def actual_decorator(method):
        @wraps(method)
        def _impl(self: OmnataPlugin, *method_args, **method_kwargs):
            logger.info(f"method_args: {method_args}")
            logger.info(f"method_kwargs: {method_kwargs}")
            if self._sync_request is None:  # pylint: disable=protected-access
                raise ValueError(
                    "To use the managed_outbound_processing decorator, you must attach a sync request to the plugin instance (via the _sync_request property)"
                )
            # if self._sync_request.api_limits is None:
            #    raise ValueError('To use the managed_outbound_processing decorator, API constraints must be defined. These can be provided in the response to the connect method')
            logger.info(f"Batch size: {batch_size}. Concurrency: {concurrency}")
            if len(method_args) == 0:
                raise ValueError(
                    "You must provide at least one method argument, and the first argument must be a DataFrame or DataFrame generator (from outbound_sync_request.get_records)"
                )
            first_arg = method_args[0]
            logger.info(first_arg.__class__.__name__)
            if first_arg.__class__.__name__ == "DataFrame":
                logger.info("managed_outbound_processing received a DataFrame")
            elif hasattr(first_arg, "__next__"):
                logger.info("managed_outbound_processing received an iterator function")
            else:
                raise ValueError(
                    f"The first argument to a @managed_outbound_processing method must be a DataFrame or DataFrame generator (from outbound_sync_request.get_records). Instead, a {first_arg.__class__.__name__} was provided."
                )

            # put the record iterator on the queue, ready for the first task to read it
            fixed_size_generator = FixedSizeGenerator(first_arg, batch_size=batch_size)
            tasks = []
            logger.info(f"Creating {concurrency} worker(s) for applying records")
            for i in range(concurrency):
                # the dataframe/generator was put on the queue, so we remove it from the method args
                task = threading.Thread(
                    target=__managed_outbound_processing_worker,
                    args=(
                        self,
                        method,
                        i,
                        fixed_size_generator,
                        self._sync_request._thread_cancellation_token,
                        method_args[1:],
                        method_kwargs,
                    ),
                )
                tasks.append(task)
                task.start()

            # wait for workers to finish
            for task in tasks:
                task.join()
                logger.info("Task joined")
            logger.info("All workers completed processing")

            # it's possible that some records weren't applied, since they are processed asynchronously on a timer
            #if self._sync_request.development_mode is False:
            #    self._sync_request.apply_results_queue()

            # these checks are done in the sync method of plugin_entrypoints
            # we don't want to do them here anymore, because there could be multiple calls to different @managed_outbound_processing
            # methods, so we don't want the apply results task to end until after the sync completes
            #self._sync_request._thread_cancellation_token.set()
            ## the thread cancellation should be detected by the apply results tasks, so it finishes gracefully
            #if (
            #    self._sync_request.development_mode is False
            #    and self._sync_request._apply_results_task is not None
            #):
            #    self._sync_request._apply_results_task.join()
            logger.info("Checking for thread exception")
            if self._sync_request._thread_exception_thrown:
                raise self._sync_request._thread_exception_thrown.exc_value

            logger.info("Main managed_outbound_processing thread completing")
            return

        return _impl

    return actual_decorator


def __managed_inbound_processing_worker(
    plugin_class_obj: Type[OmnataPlugin],
    method: Callable,
    worker_index: int,
    streams_queue: queue.Queue,
    cancellation_token: threading.Event,
    method_args,
    method_kwargs,
):
    """
    A worker thread for the managed_outbound_processing annotation.
    Consumes a fixed sized set of records by passing them to the wrapped function,
    while adhering to the defined API constraints.
    """
    while not cancellation_token.is_set():
        # Get our generator object out of the queue
        logger.info(
            f"worker {worker_index} processing. Cancelled: {cancellation_token.is_set()}"
        )
        if datetime.datetime.now() > plugin_class_obj._sync_request._run_deadline:
            # if we've reached the deadline for the run, end it
            plugin_class_obj._sync_request.apply_deadline_reached()
            return
        try:
            stream: StoredStreamConfiguration = streams_queue.get_nowait()
            logger.info(f"stream returned from queue: {stream}")
            # restore the first argument, was originally the dataframe/generator but now it's the appropriately sized dataframe
            try:
                method(plugin_class_obj, *(stream, *method_args), **method_kwargs)
                plugin_class_obj._sync_request.mark_stream_complete(stream.stream_name)
            except InterruptedWhileWaitingException:
                # If an inbound run is cancelled while waiting for rate limiting, this should mean that
                # the cancellation is handled elsewhere, so we don't need to do anything special here other than stop waiting
                return
        except queue.Empty:
            logger.info("streams queue is empty")
            return


def managed_inbound_processing(concurrency: int):
    """
    This is a decorator which can be added to a method on an OmnataPlugin class.
    It expects to be invoked with a list of StoredStreamConfiguration objects as the
    first parameter.
    The method will receive a single StoredStreamConfiguration object at a time as its
    first parameter, and is expected to publish its results via
    inbound_sync_request.enqueue_results() during the load process.

    The decorator itself must be used as a function call with a tuning parameter like so:
    @managed_inbound_processing(concurrency=5)
    def my_function(param1,param2)

    Based on the concurrency constraints, it will create threaded workers to retrieve
    the streams in parallel.
    """

    def actual_decorator(method):
        @wraps(method)
        def _impl(self, *method_args, **method_kwargs):
            logger.info(f"method_args: {method_args}")
            logger.info(f"method_kwargs: {method_kwargs}")
            if self._sync_request is None:
                raise ValueError(
                    "To use the managed_inbound_processing decorator, you must attach an apply request to the plugin instance (via the _sync_request property)"
                )
            # if self._sync_request.api_limits is None:
            #    raise ValueError('To use the managed_inbound_processing decorator, API constraints must be defined. These can be provided in the response to the connect method')
            if len(method_args) == 0:
                raise ValueError(
                    "You must provide at least one method argument, and the first argument must be a list of StoredStreamConfigurations (from inbound_sync_request.streams)"
                )
            first_arg: List[StoredStreamConfiguration] = method_args[0]
            logger.info(first_arg.__class__.__name__)
            if first_arg.__class__.__name__ == "list":
                logger.info("managed_inbound_processing received a list")
            else:
                raise ValueError(
                    f"The first argument to a @managed_inbound_processing method must be a list of StoredStreamConfigurations. Instead, a {first_arg.__class__.__name__} was provided."
                )

            streams_list: List[StoredStreamConfiguration] = first_arg
            # create a queue full of all the streams to process
            streams_queue = queue.Queue()
            for stream in streams_list:
                streams_queue.put(stream)

            tasks = []
            logger.info(f"Creating {concurrency} worker(s) for retrieving records")

            for i in range(concurrency):
                # the dataframe/generator was put on the queue, so we remove it from the method args
                task = threading.Thread(
                    target=__managed_inbound_processing_worker,
                    args=(
                        self,
                        method,
                        i,
                        streams_queue,
                        self._sync_request._thread_cancellation_token,
                        method_args[1:],
                        method_kwargs,
                    ),
                )
                tasks.append(task)
                task.start()

            # wait for workers to finish
            for task in tasks:
                task.join()
                logger.info("Task joined")
            logger.info("All workers completed processing")

            # it's possible that some records weren't applied, since they are processed asynchronously on a timer
            #if self._sync_request.development_mode is False:
            #    self._sync_request.apply_results_queue()
            #self._sync_request._thread_cancellation_token.set()
            ## the thread cancellation should be detected by the apply results tasks, so it finishes gracefully
            #if (
            #    self._sync_request.development_mode is False
            #    and self._sync_request._apply_results_task is not None
            #):
            #    self._sync_request._apply_results_task.join()
            logger.info("Checking for thread exception")
            if self._sync_request._thread_exception_thrown:
                raise self._sync_request._thread_exception_thrown.exc_value

            logger.info("Main managed_inbound_processing thread completing")
            return

        return _impl

    return actual_decorator


class DeadlineReachedException(Exception):
    """
    Indicates that a sync needed to be abandoned due to reaching a deadline, or needing to wait past a future
    deadline.
    """

def remove_empty_dict_values(data: Dict) -> Dict:
    """
    Recursively removes any empty dicts from the data
    """
    if isinstance(data, dict):
        return {
            k: remove_empty_dict_values(v)
            for k, v in data.items()
            if v != {}
        }
    return data