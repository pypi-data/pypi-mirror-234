from __future__ import annotations

from typing import Optional, Union

from pydantic import StrictStr, Field, root_validator

from lumipy.lumiflex._common.node import Node
from lumipy.lumiflex._metadata import ParamMeta, TableParamMeta
from lumipy.lumiflex.column import Column


class Parameter(Node):

    meta: Union[ParamMeta, TableParamMeta]
    label_: StrictStr = Field('parameter', const=True, alias='label')
    sql: Optional[StrictStr] = None

    class Config:
        frozen = True
        extra = 'forbid'
        arbitrary_types_allowed = True

    @root_validator
    def validate_parameter(cls, values):

        from lumipy.lumiflex.table import Table
        if 'meta' not in values or 'parents_' not in values:
            return values

        parents = values['parents_']
        if len(parents) != 1 or any(not isinstance(p, (Column, Table)) for p in parents):
            if len(parents) > 1:
                detail = f'Parent types were ({", ".join(type(p).__name__ for p in  parents)}).'
            else:
                detail = f'Parents tuple was empty.'
            raise TypeError(
                'Parameter can only have a single parent Node which must be a Column or Table Var. ' + detail
            )

        in_val = parents[0]
        meta = values['meta']
        if isinstance(meta, ParamMeta):
            str_val = f'[{meta.field_name}] = {in_val.sql}'
        else:
            str_val = f'[{meta.field_name}] = {in_val.from_}'
        if meta.prefix is not None:
            str_val = f'{meta.prefix}.{str_val}'
        values['sql'] = str_val

        return values

    def with_prefix(self, prefix: str) -> Parameter:
        meta = self.meta.update(prefix=prefix)
        return Parameter(meta=meta, parents=self.get_parents())
