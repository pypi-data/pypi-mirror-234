""" Code Eval Input """

from typing_extensions import TypedDict


class LambdaInput(TypedDict, total=False):
    """Typed dictionary for lambda inputs"""
    code: str
    input: str
    output: str
    entry_point: str
    language: str
