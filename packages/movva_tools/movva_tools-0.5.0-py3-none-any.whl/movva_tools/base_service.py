from movva_tools.databases import RapidProDatabase
from sqlalchemy.exc import SQLAlchemyError


class BaseService:

    def __init__(self, db_connection=None) -> None:
        self.db_connection = db_connection or self.__create_default_connection()

    def __create_default_connection(self):
        db = RapidProDatabase()
        db.set_session()
        return db

    def add(self, object):
        self.db_connection.session.add(object)

    def commit(self, object):
        self.db_connection.session.commit()

    def flush(self):
        """
            Flush para obter o ID gerado sem commit
        """
        self.db_connection.session.flush()

    def rollback_session(self):
        try:
            self.db_connection.session.rollback()
            return True
        except SQLAlchemyError as e:
            raise Exception(e)

    def close_session(self):
        self.db_connection.session.close()
