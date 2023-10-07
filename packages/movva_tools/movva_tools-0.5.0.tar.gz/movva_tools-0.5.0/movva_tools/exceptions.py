from movva_tools.base_exception import BaseCustomException
from movva_tools.constants import ExceptionMessages


class ObjectDoesNotUpdatedExeption(BaseCustomException):

    def __init__(self, dababase_object) -> None:
        self.database_object_name = dababase_object.__name__
        self.message = ExceptionMessages.OBJECT_DOES_NOT_UPDATED.format(
            self.dababase_object_name
        )
        super().__init__(self.message)


class ObjectDoesNotExistException(BaseCustomException):
    def __init__(self, dababase_object) -> None:
        self.database_object_name = dababase_object.__name__
        self.message = ExceptionMessages.OBJECT_DOES_NOT_EXISTS.format(
            self.dababase_object_name
        )
        super().__init__(self.message)


class FlowNameLongerException(BaseCustomException):

    def __init__(self, max_lenght) -> None:
        self.message = ExceptionMessages.FLOW_NAME_LONGER.format(max_lenght)
        super().__init__(self.message)


class FlowNameStartsOrEndWithWhitespaceException(BaseCustomException):

    def __init__(self) -> None:
        self.message = ExceptionMessages.FLOW_NAME_STARTS_OR_END_WITH_WHITESPACE
        super().__init__(self.message)


class FlowNameInvalidCharacterException(BaseCustomException):

    def __init__(self, invalid_char) -> None:
        self.message = ExceptionMessages.FLOW_INVALID_CHARACTERS.format(invalid_char)
        super().__init__(self.message)


class FlowNameContainsNullCharacterException(BaseCustomException):

    def __init__(self) -> None:
        self.message = ExceptionMessages.FLOW_NAME_CONTAINS_NULL_CHARACTER
        super().__init__(self.message)
