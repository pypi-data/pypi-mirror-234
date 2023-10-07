import uuid
from datetime import datetime

from sqlalchemy import (
    UUID, Boolean, Column, DateTime,
    Integer, String
)

from movva_tools.databases import Base
from movva_tools.constants import ContactField


class RapidProContactFields(Base):
    __tablename__ = "contacts_contactfield"

    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean)
    created_on = Column(DateTime, default=datetime.utcnow)
    modified_on = Column(DateTime, default=datetime.utcnow)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    label = Column(String)
    key = Column(String)
    value_type = Column(String)
    show_in_table = Column(Boolean)
    priority = Column(Integer)
    field_type = Column(String)
    created_by_id = Column(Integer)
    modified_by_id = Column(Integer)
    org_id = Column(Integer)

    def __init__(
        self, created_by_id, org_id,
        key, label, field_type, priority=None
    ):
        self.value_type = ContactField.TYPE_TEXT
        self.show_in_table = False
        self.priority = 0 if not priority else priority

        self.created_by_id = created_by_id
        self.modified_by_id = created_by_id

        self.org_id = org_id
        self.key = key
        self.label = label
        self.field_type = field_type
        self.is_active = True  # Set default value

    def __repr__(self):
        return f'<{self.uuid}> key:{self.key} label:{self.label} org_id:{self.org_id}'
