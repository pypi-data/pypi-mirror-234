
from dataclasses import dataclass, _MISSING_TYPE, fields
import os
from typing import Any, Optional, get_type_hints


class EnvVarPopulater:
    _converts = {
        int: lambda d: int(d),
        float: lambda d: float(d),
        Optional[int]: lambda d: int(d) if d else None,
        Optional[float]: lambda d: float(d) if d else None,
    }

    @classmethod
    def populate(cls) -> Any:
        values = {}
        typehints = get_type_hints(cls)
        for field in fields(cls):
            conv = cls._converts[typehints[field.name]]
            valstr = os.environ.get(field.name.upper())
            if valstr is not None:
                try:
                    values[field.name] = conv(valstr)
                except Exception as ex:
                    raise Exception(f'Error converting environment variable "{field.name.upper()}" as {field.type}') from ex
            else:
                if isinstance(field.default, _MISSING_TYPE) and isinstance(field.default_factory, _MISSING_TYPE):
                    # not provided and no default value
                    raise Exception(f'Environment variable "{field.name.upper()}" is required')
        return cls(** values)


@dataclass
class BatchingConfig(EnvVarPopulater):
    pyraisdk_max_batch_size: int
    pyraisdk_idle_batch_size: int
    pyraisdk_max_batch_interval: float
