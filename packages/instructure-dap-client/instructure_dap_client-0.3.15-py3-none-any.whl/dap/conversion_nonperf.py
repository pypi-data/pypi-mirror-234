from typing import Any, Optional

from sqlalchemy.sql.type_api import TypeEngine
from strong_typing.core import JsonType

from .conversion_common_json import JsonTypeCast, JsonValueConverter, get_json_type_cast


def create_value_converter(value_type: TypeEngine) -> JsonValueConverter:
    type_cast: Optional[JsonTypeCast] = get_json_type_cast(type(value_type))

    if type_cast is None:
        return lambda value: value
    else:
        cast = type_cast  # hint to type checker

        def _convert_value(value: JsonType) -> Optional[Any]:
            if value is None:
                return None
            return cast(value)

        return _convert_value
