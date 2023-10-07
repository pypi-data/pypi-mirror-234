import uuid

from movva_tools.databases import Base

from sqlalchemy import (
    JSON, UUID, Boolean, Column, DateTime,
    Integer, String,
)


class RapidProOrganization(Base):
    __tablename__ = 'orgs_org'

    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean)
    created_on = Column(DateTime)
    modified_on = Column(DateTime)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    name = Column(String)
    plan = Column(String)
    stripe_customer = Column(String)
    language = Column(String)
    timezone = Column(String)
    date_format = Column(String)
    config = Column(String)
    slug = Column(String)
    is_anon = Column(Boolean)
    brand = Column(String)
    surveyor_password = Column(String)
    country_id = Column(Integer)
    created_by_id = Column(Integer)
    modified_by_id = Column(Integer)
    parent_id = Column(Integer)
    is_flagged = Column(Boolean)
    is_suspended = Column(Boolean)
    uses_topups = Column(Boolean)
    is_multi_org = Column(Boolean)
    is_multi_user = Column(Boolean)
    plan_end = Column(DateTime)
    plan_start = Column(DateTime)
    limits = Column(JSON)
    released_on = Column(DateTime)
    deleted_on = Column(DateTime)
    flow_languages = Column(String)
    api_rates = Column(JSON)

    def __repr__(self):
        return f'<{self.uuid}:{self.name}> slug:{self.slug}'
