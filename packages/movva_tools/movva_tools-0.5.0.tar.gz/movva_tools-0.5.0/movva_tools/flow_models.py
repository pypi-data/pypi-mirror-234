import json
import uuid
from datetime import datetime

from sqlalchemy import (
    JSON, UUID, Boolean, Column, DateTime,
    Integer, String
)

from movva_tools.databases import Base


class RapidProFlows(Base):
    __tablename__ = 'flows_flow'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    name = Column(String)
    is_active = Column(Boolean)
    is_system = Column(Boolean)
    created_by_id = Column(Integer)
    modified_by_id = Column(Integer)
    saved_by_id = Column(Integer)
    saved_on = Column(DateTime, default=datetime.utcnow)
    created_on = Column(DateTime, default=datetime.utcnow)
    modified_on = Column(DateTime, default=datetime.utcnow)
    flow_type = Column(String)
    flow_metadata = Column('metadata', JSON, default={"results": [], "dependencies": [], "waiting_exit_uuids": [], "parent_refs": []})
    is_archived = Column(Boolean)
    expires_after_minutes = Column(Integer)
    base_language = Column(String)
    org_id = Column(Integer)
    ignore_triggers = Column(Boolean)
    has_issues = Column(Boolean)
    version_number = Column(String)

    def __init__(
        self, created_by_id, expires_after_minutes, org_id, name,
        flow_metadata, flow_type
    ):
        self.name = name
        self.created_by_id = created_by_id
        self.saved_by_id = created_by_id
        self.modified_by_id = created_by_id
        self.expires_after_minutes = expires_after_minutes
        self.org_id = org_id
        self.flow_metadata = flow_metadata
        self.base_language = 'base'
        self.is_active = True  # Set default value
        self.flow_type = flow_type
        self.is_archived = False  # Set default value
        self.is_system = False
        self.ignore_triggers = False
        self.has_issues = False
        self.version_number = '13.1.0'

    def __repr__(self):
        return f'id:{self.id} <{self.name}>'


class RapidProFlowsRevision(Base):
    __tablename__ = 'flows_flowrevision'

    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean)
    created_on = Column(DateTime, default=datetime.utcnow)
    modified_on = Column(DateTime, default=datetime.utcnow)
    definition = Column(JSON, default={"name": "Fluxo Interface", "uuid": "flow id", "spec_version": "13.1.0", "language": "base", "type": "messaging", "nodes": [], "_ui": {}, "revision": 1, "expire_after_minutes": 10080})
    spec_version = Column(String)
    revision = Column(Integer)
    created_by_id = Column(Integer)
    flow_id = Column(Integer)
    modified_by_id = Column(Integer)

    # constants

    MSG_TYPE = 'send_message'
    WAITING_RESPONSE_TYPE = 'switch'
    OPERAND = '@input.text'

    def __init__(
        self, created_by_id, flow_id,
        definition
    ):
        self.created_by_id = created_by_id
        self.modified_by_id = created_by_id
        self.flow_id = flow_id
        self.definition = definition
        self.revision = 1
        self.spec_version = '13.1.0'
        self.is_active = True  # Set default value

    def __repr__(self):
        flow_name = json.loads(self.definition)["name"]
        return f'id:{self.id} <{flow_name}> Revision:{self.revision}'

    @staticmethod
    def filter_node(node_uuid: str, definition: list) -> tuple:
        for idx, uid in enumerate(definition['nodes']):
            if uid['uuid'] == node_uuid:
                return (uid, idx)
        return ([], None)

    @staticmethod
    def search_node_by_pos(node_pos, definition: list) -> tuple:
        for idx, uid in enumerate(definition['nodes']):
            if idx == node_pos:
                return (uid, idx)
        return ([], None)

    def set_exits(
            self, node_uuid_to=None, node_uuid_for_destination=None
    ) -> list:

        exits_uuid = str(uuid.uuid4())

        exits_initial = [{}]

        exits_initial[0].update(
            {
                "destination_uuid": node_uuid_for_destination,
                'uuid': exits_uuid
            }
        )

        if node_uuid_to:
            node, position = self.filter_node(
                node_uuid=node_uuid_to, definition=self.definition
            )

            if not node:
                raise Exception('Node não encontrado.')

            if node.get('exits', None):
                self.definition['nodes'][position] = exits_initial
            else:
                self.definition['nodes'][position]['exits'].append(exits_initial)
        else:
            self.definition['nodes'][-1].update(
                {'exits': exits_initial}
            )

        return self.definition

    def set_action(self, text: str, type: str, quick_replies=[], attachments=[]) -> dict:
        action_dict = {}

        action_uuid = str(uuid.uuid4())

        action_dict.update(
            {
                'type': type,
                'text': text,
                'quick_replies': quick_replies,
                'uuid': action_uuid,
                'attachments': attachments
            }
        )

        return action_dict

    def set_send_message_node(self, text: str) -> dict:

        node_uuid = str(uuid.uuid4())

        action_dict = self.set_action(text=text, type=self.MSG_TYPE)

        self.definition['nodes'].append(
            {}
        )

        self.definition['nodes'][0].update(
            {
                'uuid': node_uuid
            }
        )
        self.definition['nodes'][0]['actions'] = []

        self.definition['nodes'][0]['actions'].append(action_dict)

        return self.definition

    def set_categories_wait_for_response_node(self, categories: list, definition: list):

        # categories must be [{name: nome, exit_node_pos: 1}]

        # node, position = self.filter_node(
        #     node_uuid=node_uuid,
        #     definition=definition
        # )

        categories = []

        for category in categories:

            node_exit, position_exit = self.search_node_by_pos(
                node_pos=category['exit_node_pos'],
                definition=definition
            )

            categories.append(
                {
                    'uuid': str(uuid.uuid4()),
                    'name': category['name'],
                    'exit_uuid': node_exit['uuid'],
                    'position_node_exit': position_exit
                }
            )

        return categories

    def set_cases_waiting_for_response_node(
        self, types: list, arguments: list
    ) -> list:

        # types and arguments format must be list of strings
        # arguments can be list of lists

        if len(types) != len(arguments):
            raise Exception('Incompatible')

        cases = []
        for type_case, args in zip(types, arguments):
            cases.append(
                {
                    'uuid': str(uuid.uuid4()),
                    'type': type_case,
                    'arguments': args
                }
            )

        return cases

    def set_waiting_for_response_node(
        self, text: str, name: str, exit_uuid: str, definition: list, categories: list,
        result_name: str
    ) -> dict:

        # categories must be [{key1: value1}]

        uuid_node = str(uuid.uuid4())

        router = {
            'type': self.WAITING_RESPONSE_TYPE,
            'cases': [],
            'default_category_uuid': str(uuid.uuid4()),
            'categories': [{}],
            'operand': self.OPERAND,
            'wait': {
                'type': 'msg'
            },
            'result_name': result_name
        }

        router['categories'] = self.set_categories_wait_for_response_node(
            categories=categories,
            definition=definition
        )

        router['cases'] = []

        waiting_response_node = {
            'uuid': uuid_node,
            'router': router
        }

        definition['router'].append(waiting_response_node)

        return definition

    def create(self, flow_name, flow_uuid, user_id):

        return {
            "name": flow_name,
            "uuid": flow_uuid,
            "spec_version": "13.1.0",
            "language": "base",
            "type": "messaging",
            "nodes": [],
            "_ui": {},
            "revision": 1,
            "expire_after_minutes": 10080,
            "localization": {}
        }


class RapidProFlowChannelDependencies(Base):
    __tablename__ = 'flows_flow_channel_dependencies'

    id = Column(Integer, primary_key=True)
    flow_id = Column(Integer)
    channel_id = Column(Integer)


class RapidProFlowFieldDependencies(Base):
    __tablename__ = 'flows_flow_field_dependencies'

    id = Column(Integer, primary_key=True)
    flow_id = Column(Integer)
    contactfield_id = Column(Integer)


class RapidProFlowLabel(Base):
    __tablename__ = 'flows_flowlabel'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    name = Column(String)
    org_id = Column(Integer)
    parent_id = Column(Integer)
