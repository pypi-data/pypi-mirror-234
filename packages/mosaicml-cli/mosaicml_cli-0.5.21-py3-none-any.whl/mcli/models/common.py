""" Common models
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Generic, Iterator, List, TypeVar

from mcli.models.mcli_secret import Secret

O = TypeVar('O', bound=type(dataclass))


def generate_html_table(data: List[O], columns: Dict[str, str]):
    res = []
    res.append("<table border=\"1\" class=\"dataframe\">")

    # header
    res.append("<thead>")
    res.append("<tr style=\"text-align: right;\">")
    for col in columns.values():
        res.append(f"<th>{col}</th>")
    res.append("</tr>")
    res.append("</thead>")

    # body
    res.append("<tbody>")
    for row in data:
        res.append("<tr>")
        for col in columns:
            value = getattr(row, col, '')
            res.append(f"<td>{value}</td>")
        res.append("</tr>")
    res.append("</tbody>")

    res.append("</table>")
    return "\n".join(res)


class ObjectType(Enum):
    """ Enum for Types of Objects Allowed """

    SECRET = 'secret'

    def get_display_columns(self) -> Dict[str, str]:
        if self == ObjectType.SECRET:
            return {
                'name': 'Name',
                'secret_type': 'Type',
                'created_at': 'Created At',
            }

        raise ValueError(f'Unknown object type {self}')

    @classmethod
    def from_model_type(cls, model) -> ObjectType:
        if model == Secret:
            return ObjectType.SECRET

        raise ValueError(f'Unknown model type {model}')


class ObjectList(Generic[O]):
    """Common helper for list of objects
    """

    def __init__(self, data: List[O], obj_type: ObjectType):
        self.data = data
        self.type = obj_type

    def __repr__(self) -> str:
        return f"List{self.data}"

    def __iter__(self) -> Iterator[O]:
        return iter(self.data)

    def __getitem__(self, index: int) -> O:
        return self.data[index]

    def __len__(self) -> int:
        return len(self.data)

    @property
    def display_columns(self) -> Dict[str, str]:
        return self.type.get_display_columns()

    def _repr_html_(self) -> str:
        return generate_html_table(self.data, self.display_columns)

    def to_pandas(self):
        try:
            # pylint: disable=import-outside-toplevel
            import pandas as pd  # type: ignore
        except ImportError as e:
            raise ImportError("Please install pandas to use this feature") from e

        cols = self.display_columns
        res = {col: [] for col in cols}
        for row in self.data:
            for col in cols:
                value = getattr(row, col)
                res[col].append(value)

        return pd.DataFrame(data=res)
