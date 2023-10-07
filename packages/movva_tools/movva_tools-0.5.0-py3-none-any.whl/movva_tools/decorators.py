from functools import wraps


def ensure_transaction(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        db_session_instance = self.db_connection.session
        try:
            result = func(self, *args, **kwargs)
            db_session_instance.commit()  # Commit a transação se tudo estiver correto
            return result
        except Exception as e:
            db_session_instance.rollback()  # Reverta a transação em caso de exceção
            raise e  # Relevante a exceção após o rollback
    return wrapper
