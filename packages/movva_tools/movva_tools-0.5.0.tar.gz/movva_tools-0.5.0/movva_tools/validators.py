from movva_tools.constants import MAX_NAME_LEN
from movva_tools.exceptions import (
    FlowNameLongerException,
    FlowNameInvalidCharacterException,
    FlowNameContainsNullCharacterException,
    FlowNameStartsOrEndWithWhitespaceException
)


class FlowNameValidator:
    """
    Validator for names of flows and their dependencies.
    """

    def __init__(self, max_length=MAX_NAME_LEN):
        self.max_length = max_length

    def __call__(self, value):
        # model forms will add their own validator based on max_length but we need this for validating for imports etc
        if len(value) > self.max_length:
            raise FlowNameLongerException(self.max_length)

        if value != value.strip():
            raise FlowNameStartsOrEndWithWhitespaceException()

        for ch in '"\\':
            if ch in value:
                raise FlowNameInvalidCharacterException(ch)

        if "\0" in value:
            raise FlowNameContainsNullCharacterException()
