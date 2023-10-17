""" Get Code Evaluation Output. """
from __future__ import annotations

from concurrent.futures import Future
from typing import List, Optional, Union, overload

from mcli.api.engine.engine import get_return_response, run_singular_mapi_request
from mcli.api.model.lambda_response import LambdaResponse
from mcli.models import LambdaInput

__all__ = ['get_code_eval_output']

QUERY_FUNCTION = 'getCodeEvalOutput'
VARIABLE_DATA_GET_CODE_EVAL_OUTPUT = 'getCodeEvalOutputInput'
QUERY = f"""
query GetCodeEvalOutput(${VARIABLE_DATA_GET_CODE_EVAL_OUTPUT}: GetCodeEvalOutputInput!) {{
  {QUERY_FUNCTION}({VARIABLE_DATA_GET_CODE_EVAL_OUTPUT}: ${VARIABLE_DATA_GET_CODE_EVAL_OUTPUT}) {{
    data
  }}
}}"""


@overload
def get_code_eval_output(lambda_input: List[LambdaInput],
                         *,
                         timeout: Optional[float] = 12,
                         future: bool = False) -> LambdaResponse:
    ...


@overload
def get_code_eval_output(lambda_input: List[LambdaInput],
                         *,
                         timeout: Optional[float] = 12,
                         future: bool = False) -> Future[LambdaResponse]:
    ...


def get_code_eval_output(
    lambda_input: List[LambdaInput],
    *,
    timeout: Optional[float] = 12,  # set to 12 to be greater than Lambda timeout of 10 seconds
    future: bool = False
) -> Union[LambdaResponse, Future[LambdaResponse]]:
    """ Get the code evaluation output for a given lambda input on the MosaicML platform.

    Args:
        lambda_input (``List[Dict[str, any]]``): A list of test cases that the Lambda function evaluates.
            Each test case is of the form:
            {
                'code': # your code generation here
                'input': # your test case input here
                'output': # your test case output here
                'entry_point': # name of the function to test
                'language': # programming language
            }
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the call takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored. Set to be 12 seconds by default
            because the lambda timeout is 10 seconds.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to :func:`get_code_eval_output` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the list of :class:`~mcli.api.model.run.Run` output,
            use ``return_value.result()`` with an optional ``timeout`` argument.

    Raises:
        MAPIException: Raised if getting the requested outputs fails.

    Returns:
        A list of booleans (``List[bool]``), where each boolean represents whether the
        corresponding test case passed or failed.
    """

    variables = {
        VARIABLE_DATA_GET_CODE_EVAL_OUTPUT: {
            'data': lambda_input
        },
    }

    response = run_singular_mapi_request(
        query=QUERY,
        query_function=QUERY_FUNCTION,
        return_model_type=LambdaResponse,
        variables=variables,
    )

    return get_return_response(response, future=future, timeout=timeout)
