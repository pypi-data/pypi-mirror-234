from enum import Enum
import os


MAX_NAME_LEN = 64
DEFAULT_USER_ID = int(os.environ.get('DEFAULT_USER_ID'))
READ_ONLY_ISOLATION_LEVEL_CONNECTION = '?isolation_level=READ%20ONLY'


class BaseEnum(Enum):

    def __get__(self, instance, owner):
        return self.value


class GoogleSheets(BaseEnum):

    DEFAULT_SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
    READ_ONLY_SCOPE = ['https://www.googleapis.com/auth/spreadsheets.readonly']


class ContactField(BaseEnum):
    MAX_KEY_LEN = 36
    MAX_NAME_LEN = 36

    TYPE_TEXT = "T"
    TYPE_NUMBER = "N"
    TYPE_DATETIME = "D"
    TYPE_STATE = "S"
    TYPE_DISTRICT = "I"
    TYPE_WARD = "W"

    TYPE_CHOICES = {
        TYPE_TEXT, "Text",
        TYPE_NUMBER, "Number",
        TYPE_DATETIME, "Date & Time",
        TYPE_STATE, "State",
        TYPE_DISTRICT, "District",
        TYPE_WARD, "Ward",
    }

    ENGINE_TYPES = {
        TYPE_TEXT: "text",
        TYPE_NUMBER: "number",
        TYPE_DATETIME: "datetime",
        TYPE_STATE: "state",
        TYPE_DISTRICT: "district",
        TYPE_WARD: "ward",
    }

    # fixed keys for system-fields
    KEY_ID = "id"
    KEY_NAME = "name"
    KEY_CREATED_ON = "created_on"
    KEY_LANGUAGE = "language"
    KEY_LAST_SEEN_ON = "last_seen_on"

    # fields that cannot be updated by user
    IMMUTABLE_FIELDS = (KEY_ID, KEY_CREATED_ON, KEY_LAST_SEEN_ON)

    SYSTEM_FIELDS = {
        KEY_ID: {"name": "ID", "value_type": TYPE_NUMBER},
        KEY_NAME: {"name": "Name", "value_type": TYPE_TEXT},
        KEY_CREATED_ON: {"name": "Created On", "value_type": TYPE_DATETIME},
        KEY_LANGUAGE: {"name": "Language", "value_type": TYPE_TEXT},
        KEY_LAST_SEEN_ON: {"name": "Last Seen On", "value_type": TYPE_DATETIME},
    }


class Flow(BaseEnum):
    BASE_LANGUAGE = "base"

    DEFINITION_UUID = "uuid"
    DEFINITION_NAME = "name"
    DEFINITION_SPEC_VERSION = "spec_version"
    DEFINITION_TYPE = "type"
    DEFINITION_LANGUAGE = "language"
    DEFINITION_REVISION = "revision"
    DEFINITION_EXPIRE_AFTER_MINUTES = "expire_after_minutes"
    DEFINITION_METADATA = "metadata"
    DEFINITION_NODES = "nodes"
    DEFINITION_UI = "_ui"

    INSPECT_DEPENDENCIES = "dependencies"

    EXPIRES_AFTER_MINUTES = 60 * 24 * 7  # 1 week

    CURRENT_SPEC_VERSION = "13.1.0"


class FlowType(BaseEnum):

    TYPE_MESSAGE = "M"
    TYPE_BACKGROUND = "B"
    TYPE_SURVEY = "S"
    TYPE_VOICE = "V"
    TYPE_USSD = "U"


class GoFlowTypes(BaseEnum):
    TYPE_MESSAGE = "messaging"
    TYPE_BACKGROUND = "messaging_background"
    TYPE_SURVEY = "messaging_offline"
    TYPE_VOICE = "voice"


class ExceptionMessages(BaseEnum):

    OBJECT_DOES_NOT_EXISTS = 'The object of class {} does not exists or had not been found.'
    OBJECT_DOES_NOT_UPDATED = 'The object of class {} does not updated.'

    FLOW_NAME_LONGER = 'Cannot be longer than {} characters.'
    FLOW_NAME_STARTS_OR_END_WITH_WHITESPACE = 'Cannot begin or end with whitespace.'
    FLOW_INVALID_CHARACTERS = 'Cannot contain the character: {}'
    FLOW_NAME_CONTAINS_NULL_CHARACTER = "Cannot contain null characters."
