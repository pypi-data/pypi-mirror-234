import json
from typing import List

import pandas as pd
from movva_tools.organization_service import \
    OrganizationService
from movva_tools.user_service import UserService
from sqlalchemy import desc, update

from movva_tools.base_service import BaseService
from movva_tools.constants import MAX_NAME_LEN, Flow, FlowType, GoFlowTypes
from movva_tools.decorators import ensure_transaction
from movva_tools.exceptions import (
    ObjectDoesNotExistException,
    ObjectDoesNotUpdatedExeption
)
from movva_tools.flow_models import RapidProFlows, RapidProFlowsRevision
from movva_tools.organization_models import RapidProOrganization
from movva_tools.validators import FlowNameValidator


class FlowService(BaseService):

    def __init__(self, db_connection=None) -> None:

        super().__init__(db_connection=db_connection)

        # model table entities
        self.flow = RapidProFlows
        self.flow_revision = RapidProFlowsRevision
        self.org = RapidProOrganization

        # services
        self.user_service = UserService(
            db_connection=self.db_connection
        )
        self.organization_service = OrganizationService(
            db_connection=self.db_connection
        )

    def __set_default_flow_metadata(self):

        return {
            "results": [],
            "dependencies": [],
            "waiting_exit_uuids": [],
            "parent_refs": []
        }

    def __set_initial_flow_revision_definition(self, flow):
        return {
            Flow.DEFINITION_NAME: flow.name,
            Flow.DEFINITION_UUID: str(flow.uuid),
            Flow.DEFINITION_SPEC_VERSION: Flow.CURRENT_SPEC_VERSION,
            Flow.DEFINITION_LANGUAGE: Flow.BASE_LANGUAGE,
            Flow.DEFINITION_TYPE: GoFlowTypes.TYPE_MESSAGE,
            Flow.DEFINITION_NODES: [],
            Flow.DEFINITION_UI: {},
            Flow.DEFINITION_REVISION: 1,
            Flow.DEFINITION_EXPIRE_AFTER_MINUTES: Flow.EXPIRES_AFTER_MINUTES
        }

    def __set_flow_revision_definition(self, flow, setted_definition):

        setted_definition[Flow.DEFINITION_NAME] = flow.name
        setted_definition[Flow.DEFINITION_REVISION] = 1
        setted_definition[Flow.DEFINITION_UUID] = str(flow.uuid)

        return setted_definition

    def is_valid_name(cls, name: str) -> bool:
        try:
            FlowNameValidator()(value=name)
            return True
        except Exception:
            return False

    def get_flow(self, flow_name):

        flow = self.db_connection.session.query(self.flow).filter_by(
            name=flow_name
        ).first()

        if flow:
            return flow
        else:
            raise ObjectDoesNotExistException(dababase_object=self.flow)

    def create_new_flow_revision(self, flow, user, setted_definition=None):
        if setted_definition:
            definition = self.__set_flow_revision_definition(
                flow, setted_definition=setted_definition
            )
        else:
            definition = self.__set_initial_flow_revision_definition(flow=flow)

        new_flow_revision = self.flow_revision(
            created_by_id=user.id,
            flow_id=flow.id,
            definition=definition
        )

        self.add(new_flow_revision)
        self.flush()
        return new_flow_revision

    def _create_flow(
        self,
        org_name,
        flow_name,
        flow_type=FlowType.TYPE_MESSAGE,
        expires_after_minutes=Flow.EXPIRES_AFTER_MINUTES,
        create_revision: bool = False,
        external_context: bool = False
    ):
        new_flow_revision = None
        user = self.user_service.get_default_user()
        org = self.organization_service.get_org(org_name)

        new_flow = self.flow(
            org_id=org.id,
            created_by_id=user.id,
            name=flow_name,
            flow_type=flow_type,
            expires_after_minutes=expires_after_minutes,
            flow_metadata=self.__set_default_flow_metadata()
        )

        self.add(new_flow)
        self.flush()

        if create_revision:
            new_flow_revision = self.create_new_flow_revision(
                flow=new_flow,
                user=user
            )

        return new_flow, new_flow_revision

    def create(
        self,
        org_name,
        flow_name,
        flow_type=FlowType.TYPE_MESSAGE,
        expires_after_minutes=Flow.EXPIRES_AFTER_MINUTES,
        create_revision: bool = False,
        commit_after_create: bool = False,
        external_context: bool = True
    ):

        self.is_valid_name(flow_name)

        if not external_context:

            with self.db_connection.session.begin():
                new_flow, new_flow_revision = self._create_flow(
                    org_name=org_name,
                    flow_name=flow_name,
                    flow_type=flow_type,
                    expires_after_minutes=expires_after_minutes,
                    create_revision=create_revision,
                    external_context=external_context
                )
        else:
            new_flow, new_flow_revision = self._create_flow(
                org_name=org_name,
                flow_name=flow_name,
                flow_type=flow_type,
                expires_after_minutes=expires_after_minutes,
                create_revision=create_revision,
                external_context=external_context
            )

        if commit_after_create:
            # Commit a transação após os blocos 'with'
            self.commit()

        return new_flow, new_flow_revision


class FlowCopyService(BaseService):

    def __init__(self, db_connection=None) -> None:

        super().__init__(db_connection)

        # services
        self.flow_service = FlowService(
            db_connection=self.db_connection
        )
        self.organization_service = OrganizationService(
            db_connection=self.db_connection
        )
        self.user_service = UserService(
            db_connection=self.db_connection
        )

        # model table entities
        self.flow_revision = RapidProFlowsRevision

    def get_unique_name(self, org, base_name):

        name = f'{base_name[:MAX_NAME_LEN]}' if len(base_name) > MAX_NAME_LEN else base_name
        qs = self.db_connection.session.query(self.flow).filter_by(
            org_id=org.id,
            is_active=True,
            name=name
        ).all()

        if qs:
            name = 'Copy_of ' + name

        return name

    def get_last_flow_revision(self, flow):

        flow_revision = self.db_connection.session.query(
            self.flow_revision
        ).order_by(
            desc(self.flow_revision.created_on)
        ).filter_by(
            flow_id=flow.id
        ).first()

        if flow_revision:
            return flow_revision
        else:
            raise ObjectDoesNotExistException(
                dababase_object=self.flow_revision
            )

    def transfer_flow_revision_messages(self, json_string: str, df: pd.DataFrame):
        messages = df.loc[:, ['MENSAGENS ORIGINAIS', 'MENSAGENS NOVAS']]
        messages = messages.dropna(how='all')

        if messages.empty:
            raise Exception('Without Messages.')

        for _, actual, new in messages.itertuples():
            actual = actual.replace('\n', '\\n')
            new = new.replace('\n', '\\n')
            actual = f'"{actual}"'
            new = f'"{new}"'
            json_string = json_string.replace(actual, new)

        return json_string

    def transfer_flow_revision_data(self, flow_json: dict, spreadsheet_data: pd.DataFrame):
        flow_data = json.dumps(flow_json, ensure_ascii=False)

        flow_data = self.transfer_flow_revision_messages(
            json_string=flow_data,
            df=spreadsheet_data
        )
        return json.loads(flow_data)

    def migrate_definition(
        self, flow_json, flow, flow_revision_destination, user,
        data: pd.DataFrame = None
    ):
        flow_revision_copy = flow_json.copy()

        # aqui deve entrar as modificações do flow revision
        if not data.empty:
            flow_revision_copy = self.transfer_flow_revision_data(
                spreadsheet_data=data,
                flow_json=flow_revision_copy
            )

        if flow_revision_destination:
            definition_destination = json.loads(
                flow_revision_destination.definition
            )
            flow_revision_copy['name'] = definition_destination['name']

            flow_revision_copy_json = json.dumps(flow_revision_copy)

            query = update(
                self.flow_revision
            ).where(
                self.flow_revision.id == flow_revision_destination.id
            ).values(
                definition=flow_revision_copy_json
            ).returning(self.flow_revision)

            if result := self.db_connection.execute_query(query).fetchone():
                return result
            else:
                raise ObjectDoesNotUpdatedExeption(
                    dababase_object=self.flow_revision
                )
        else:
            flow_revision_destination = self.flow_service.create_new_flow_revision(
                flow=flow, user=user,
                setted_definition=flow_revision_copy
            )

        return flow_revision_destination.definition

    def import_definition(
        self,
        user, definition,
        flow_destination, flow_revision_destination, org_destination,
        data: pd.DataFrame = None
    ):
        """
            Allows setting the definition for a flow from another definition.
            All UUID's will be remapped.
        """

        flow_revision_migrated_data = self.migrate_definition(
            flow_json=definition,
            flow=flow_destination,
            user=user,
            flow_revision_destination=flow_revision_destination,
            data=data
        )

        flow_revision_migrated = self.get_last_flow_revision(
            flow=flow_destination
        )

        return flow_revision_migrated

    def get_definition(self, flow) -> dict:
        revision = self.get_last_flow_revision(
            flow=flow
        )

        definition = revision.definition

        return json.loads(definition)

    def _check_organization_data(self, org_flow, origin_org: str) -> bool:
        org_flow_name = org_flow.name
        if org_flow_name == origin_org:
            return True

        return False

    @ensure_transaction
    def clone(
        self,
        origin_organization_name: str, base_flow_name: str,
        flow_suggested_name: str,
        destiny_organization_name: str,
        data: List[List[str]] = None
    ):
        """
        Returns a clone of this flow
        """
        if data:
            data = pd.DataFrame(data[1:], columns=data[0])

        with self.db_connection.session.begin():
            user = self.user_service.get_default_user()
            org = self.organization_service.get_org(
                org_name=destiny_organization_name
            )

            if not self._check_organization_data(
                org_flow=org,
                origin_org=origin_organization_name
            ):
                raise Exception(
                    'A organização de origem informada não contém o fluxo de origem para cópia.'
                )

            copy, revision = self.flow_service.create(
                org_name=org.name,
                flow_name=flow_suggested_name
            )

            base_flow = self.flow_service.get_flow(
                flow_name=base_flow_name
            )

            base_flow_json = self.get_definition(
                flow=base_flow
            )

            self.import_definition(
                user=user,
                definition=base_flow_json,
                flow_destination=copy,
                flow_revision_destination=revision,
                org_destination=org,
                data=data
            )
