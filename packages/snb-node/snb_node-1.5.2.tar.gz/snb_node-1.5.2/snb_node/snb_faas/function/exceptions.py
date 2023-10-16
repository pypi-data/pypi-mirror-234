#  wangixnyi
# 2022-10-28


class FunctionsFrameworkException(Exception):
    pass


class InvalidConfigurationException(FunctionsFrameworkException):
    pass


class InvalidTargetTypeException(FunctionsFrameworkException):
    pass


class MissingSourceException(FunctionsFrameworkException):
    pass


class MissingTargetException(FunctionsFrameworkException):
    pass


class EventConversionException(FunctionsFrameworkException):
    pass
