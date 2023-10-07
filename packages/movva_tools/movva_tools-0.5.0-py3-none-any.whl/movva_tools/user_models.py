from movva_tools.databases import Base

from sqlalchemy import (
    Boolean, Column, DateTime,
    Integer, String,
)


class RapidProUser(Base):

    __tablename__ = 'auth_user'

    id = Column(Integer, primary_key=True)
    password = Column(String)
    last_login = Column(DateTime)
    is_superuser = Column(Boolean)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    is_staff = Column(Boolean)
    is_active = Column(Boolean)
    date_joined = Column(DateTime)

    def __repr__(self):
        return f'id:{self.id} username: {self.username} <{self.email}>'
