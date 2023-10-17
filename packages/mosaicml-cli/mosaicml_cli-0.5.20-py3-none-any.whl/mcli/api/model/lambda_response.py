""" GraphQL representation of MCLI query to Lambdas"""
from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus
from typing import Any, Dict, List

from mcli.api.exceptions import MAPIException
from mcli.api.schema.generic_model import DeserializableModel


@dataclass
class LambdaResponse(DeserializableModel):
    """Response from the Lambda function.

    Args:
        data (``List[bool]``): The return values from the Lambda function.
    """

    data: List[bool]

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> LambdaResponse:
        missing = {"data"} - set(response)
        if missing:
            raise MAPIException(HTTPStatus.INTERNAL_SERVER_ERROR, f'Missing fields in response: {", ".join(missing)}')
        return LambdaResponse(data=response["data"])

    def to_dict(self):
        return {"data": self.data}
