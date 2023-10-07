from movva_tools.databases import RapidProDatabase
from movva_tools.contacts_models import RapidProContactFields


class ContactService:

    def __init__(self, db_connection: RapidProDatabase) -> None:

        # model table entities
        self.contact_fields = RapidProContactFields
        self.db_connection = db_connection

    def get_or_create(self, org, flow, user, key: str, name: str = None, value_type=None):

        self.db_connection.set_session()
        changed = False
        with self.db_connection.session.begin():
            existing = self.contact_fields.session.query(
                self.contact_fields
            ).filter(
                is_active=True,
                key=key
            ).first()

            if existing:
                if name and existing.name != name:
                    # existing.name = name
                    changed = True

                # update our type if we were given one
                if value_type and existing.value_type != value_type:

                    # existing.value_type = value_type
                    changed = True

                if changed:
                    existing.modified_by = user.id
                    existing.update().where(
                        self.contact_fields.id == existing.id
                    ).values(name=name, value_type=value_type)

                return existing
