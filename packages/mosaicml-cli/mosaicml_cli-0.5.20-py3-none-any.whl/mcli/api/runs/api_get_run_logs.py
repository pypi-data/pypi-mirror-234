"""Get a run's logs from the MosaicML platform"""
from __future__ import annotations

import base64
from concurrent.futures import Future
from typing import Any, Dict, Generator, Optional, Union, overload

import gql
from typing_extensions import Literal

from mcli.api.engine.engine import MAPIConnection
from mcli.api.model.run import Run
from mcli.config import MCLIConfig
from mcli.utils.utils_message_decoding import MessageDecoder

QUERY_FUNCTION = 'getRunLogsV2'
VARIABLE_DATA_NAME = 'getRunLogsInput'
QUERY = f"""
subscription Subscription(${VARIABLE_DATA_NAME}: GetRunLogsInput!) {{
    {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME}) {{
        chunk
        endOffset
    }}
}}"""


@overload
def get_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    *,
    timeout: Optional[float] = None,
    future: Literal[False] = False,
    failed: Optional[bool] = False,
    resumption: Optional[int] = None,
    tail: Optional[int] = None,
) -> Generator[str, None, None]:
    ...


@overload
def get_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    *,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
    failed: Optional[bool] = False,
    resumption: Optional[int] = None,
    tail: Optional[int] = None,
) -> Generator[Future[str], None, None]:
    ...


def get_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    *,
    timeout: Optional[float] = None,
    future: bool = False,
    failed: Optional[bool] = False,
    resumption: Optional[int] = None,
    tail: Optional[int] = None,
) -> Union[Generator[str, None, None], Generator[Future[str], None, None]]:
    """Get the current logs for an active or completed run

    Get the current logs for an active or completed run in the MosaicML platform.
    This returns the full logs as a ``str``, as they exist at the time the request is
    made. If you want to follow the logs for an active run line-by-line, use
    :func:`follow_run_logs`.

    Args:
        run (:obj:`str` | :class:`~mcli.api.model.run.Run`): The run to get logs for. If a
            name is provided, the remaining required run details will be queried with :func:`~mcli.get_runs`.
        rank (``Optional[int]``): Node rank of a run to get logs for. Defaults to the lowest
            available rank. This will usually be rank 0 unless something has gone wrong.
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the the call takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future` . If True, the
            call to :func:`get_run_logs` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the log text, use ``return_value.result()`` with an optional
            ``timeout`` argument.
        failed (``bool``): Return the logs of the first failed rank for the provided resumption if ``True``.
            ``False`` by default.
        resumption (``Optional[int]``): Resumption (0-indexed) of a run to get logs for. Defaults to the last resumption

    Returns:
        If future is False:
            The full log text for a run at the time of the request as a :obj:`str`
        Otherwise:
            A :class:`~concurrent.futures.Future` for the log text
    """
    # Convert to strings
    run_name = run.name if isinstance(run, Run) else run

    filters: Dict[str, Any] = {'name': run_name, 'follow': False, 'failed': failed}
    if rank is not None:
        filters['nodeRank'] = rank

    if resumption is not None:
        filters['attemptIndex'] = resumption

    if tail is not None:
        filters['tail'] = tail

    cfg = MCLIConfig.load_config()
    cfg.update_entity(filters)

    variables = {VARIABLE_DATA_NAME: filters}
    for message in _get_logs(QUERY, variables, QUERY_FUNCTION):
        if not future:
            try:
                yield message.result(timeout)
            except StopAsyncIteration:
                break
        else:
            yield message


@overload
def follow_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    *,
    timeout: Optional[float] = None,
    future: Literal[False] = False,
    resumption: Optional[int] = None,
    tail: Optional[int] = None,
) -> Generator[str, None, None]:
    ...


@overload
def follow_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    *,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
    resumption: Optional[int] = None,
    tail: Optional[int] = None,
) -> Generator[Future[str], None, None]:
    ...


def follow_run_logs(
    run: Union[str, Run],
    rank: Optional[int] = None,
    *,
    timeout: Optional[float] = None,
    future: bool = False,
    resumption: Optional[int] = None,
    tail: Optional[int] = None,
) -> Union[Generator[str, None, None], Generator[Future[str], None, None]]:
    """Follow the logs for an active or completed run in the MosaicML platform

    This returns a :obj:`generator` of individual log lines, line-by-line, and will wait until
    new lines are produced if the run is still active.

    Args:
        run (:obj:`str` | :class:`~mcli.api.model.run.Run`): The run to get logs for. If a
            name is provided, the remaining required run details will be queried with
            :func:`~mcli.get_runs`.
        rank (``Optional[int]``): Node rank of a run to get logs for. Defaults to the lowest
            available rank. This will usually be rank 0 unless something has gone wrong.
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the call takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored. A run may
            take some time to generate logs, so you likely do not want to set a timeout.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future` . If True, the
            call to :func:`follow_run_logs` will return immediately and the request will be
            processed in the background. The generator returned by the `~concurrent.futures.Future`
            will yield a `~concurrent.futures.Future` for each new log string returned from the cloud.
            This takes precedence over the ``timeout`` argument. To get the generator,
            use ``return_value.result()`` with an optional ``timeout`` argument and
            ``log_future.result()`` for each new log string.

    Returns:
        If future is False:
            A line-by-line :obj:`Generator` of the logs for a run
        Otherwise:
            A :class:`~concurrent.futures.Future` of a line-by-line generator of the logs for a run
    """
    # Convert to strings
    run_name = run.name if isinstance(run, Run) else run

    filters: Dict[str, Any] = {'name': run_name, 'follow': True}
    if rank is not None:
        filters['nodeRank'] = rank

    if resumption is not None:
        filters['attemptIndex'] = resumption

    if tail is not None:
        filters['tail'] = tail

    cfg = MCLIConfig.load_config()
    cfg.update_entity(filters)

    variables = {VARIABLE_DATA_NAME: filters}
    for message in _get_logs(QUERY, variables, QUERY_FUNCTION):
        if not future:
            try:
                yield message.result(timeout)
            except StopAsyncIteration:
                break
        else:
            yield message


def _get_logs(query: str, variables: Dict[str, Any], return_key: str) -> Generator[Future[str], None, None]:

    gql_query = gql.gql(query)
    connection = MAPIConnection.get_current_connection()
    decoder = LogsDecoder(return_key=return_key)

    for message in connection.subscribe(
            query=gql_query,
            variables=variables,
            callback=decoder.parse_message,
            retry_callback=decoder.update_offset,
    ):
        yield message


class LogsDecoder(MessageDecoder):
    """Decode log messages and update read offset
    """
    end_offset: int = 0

    def __init__(self, return_key: str):
        self.return_key = return_key
        super().__init__()

    def update_offset(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        resolver_input = variables['getRunLogsInput'] if self.return_key == 'getRunLogsV2' else variables[
            'getInferenceDeploymentLogsInput']
        # We set the offset to read from the end of the last message, or zero if this is the first message
        resolver_input['offset'] = self.end_offset
        # If we have already read some bytes with the tail parameter set, we must have already calculated
        # the tail offset. Thus, we can simply continue reading normally, without the tail parameter.
        if self.end_offset != 0 and 'tail' in resolver_input:
            del resolver_input['tail']
        return variables

    def parse_message(self, data: Dict[str, Any]) -> str:
        """Get the next message from the GraphQL logging subscription
        """
        # Convert from base64 string to a bytestring
        message_data = data['getRunLogsV2'] if self.return_key == 'getRunLogsV2' else data[
            'getInferenceDeploymentLogsV2']
        b64_message = message_data['chunk']
        b64_bytes = b64_message.encode('utf8')
        message_bytes = base64.b64decode(b64_bytes)
        self.end_offset = message_data['endOffset']

        return self.decode(message_bytes)
