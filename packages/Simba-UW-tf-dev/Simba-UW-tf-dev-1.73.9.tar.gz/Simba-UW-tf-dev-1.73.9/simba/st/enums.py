from enum import Enum

class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

class SIDEBAR_OPTIONS(ExtendedEnum):
    WELCOME = 'WELCOME'
    DEFINE_GROUPS = 'DEFINE GROUPS'
    AGGREGATE_STATISTICS = 'AGGREGATE STATISTICS'
