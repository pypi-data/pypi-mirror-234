import enum
import pandas as pd


class Enum(enum.Enum):
    """An Enum class which allows Enum instance retrievals by Enum item names and/or values."""

    @classmethod
    def retrieve_by_name(cls, value):
        if value is None:
            return None

        for name, item in cls.__members__.items():
            if name.upper() == value.upper():
                return item

        raise ValueError('Failed to find Enum with value {}'.format(value))

    @classmethod
    def retrieve(cls, value):
        if value is None:
            return None

        for name, item in cls.__members__.items():
            if name.upper()==value.upper():
                return item

            if item.value.upper()==value.upper():
                return item

        raise ValueError('Failed to find Enum with value {}'.format(value))

    @classmethod
    def get_meta(cls):
        meta = dict()
        for name, item in cls.__members__.items():
            meta[name] = item.value

        meta = pd.Series(meta).to_frame(name='EnumValue')
        meta.index.name = 'EnumName'
        return meta