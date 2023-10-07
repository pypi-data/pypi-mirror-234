from th2_common.schema.grpc.router.grpc_router import GrpcRouter
from th2_common_utils.converters.filter_converters import FieldFilter, dict_to_root_message_filter
from th2_grpc_check1.check1_pb2 import CheckRuleRequest
from th2_grpc_check1.check1_service import Check1Service
from th2_grpc_common.common_pb2 import Direction, FailUnexpected, FilterOperation, ConnectionID, ComparisonSettings

from run_one.action_handlers.abstract_action_handler import AbstractActionHandler
from run_one.action_handlers.context import Context
from run_one.processors.th2_processor import Th2ProcessorConfig
from run_one.util.util import Action


class TH2Check1Handler(AbstractActionHandler):

    def __init__(self, config: Th2ProcessorConfig, grpc_router: GrpcRouter, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._config = config
        self._check1_service: Check1Service = grpc_router.get_service(Check1Service)  # type: ignore

    def process(self, action: Action):
        message_type = action.extra_data['MessageType']
        user = action.extra_data['User']
        direction = getattr(Direction, action.extra_data.get('Direction', 'FIRST').upper(), Direction.FIRST)
        cl_ord_id = action.row.get("OrigClOrdID", action.row.get("ClOrdID", "none"))
        user_and_direction = (user, direction, cl_ord_id)

        key_fields_common: dict = self._config.key_fields.get('common', {})
        key_fields_by_message_type: dict = self._config.key_fields.get(message_type, {})
        key_fields = key_fields_common | key_fields_by_message_type

        ignore_fields: list = self._config.ignore_fields.get('common', [])
        ignore_fields_by_message_type: list = self._config.ignore_fields.get(message_type, [])
        ignore_fields.extend(ignore_fields_by_message_type)

        message_filter = {}
        for k, v in action.row.items():
            if v == '*':
                message_filter[k] = FieldFilter(operation=FilterOperation.NOT_EMPTY)

            elif k in key_fields:
                if isinstance(v, str):
                    is_not_equal_operation = v.startswith('!=')
                    message_filter[k] = FieldFilter(
                        value=v[2:] if is_not_equal_operation else v,
                        key=True,
                        operation=FilterOperation.NOT_EQUAL if is_not_equal_operation else FilterOperation.EQUAL
                    )

                if isinstance(v, dict):
                    message_filter[k] = {ik: FieldFilter(value=iv, key=ik in key_fields[k]) for ik, iv in v.items()}

            else:
                value = (FieldFilter(value=v[2:], operation=FilterOperation.NOT_EQUAL)
                         if isinstance(v, str) and v.startswith('!=')
                         else v)
                message_filter[k] = value

        root_message_filter = dict_to_root_message_filter(
            message_type=message_type,
            message_filter=message_filter,
            ignore_fields=ignore_fields if ignore_fields else None)

        if self._config.fail_unexpected:
            comparison_settings = ComparisonSettings(fail_unexpected=getattr(FailUnexpected,
                                                                             self._config.fail_unexpected.upper(),
                                                                             FailUnexpected.NO))
            root_message_filter.message_filter.comparison_settings.CopyFrom(comparison_settings)

        check_rule_request = CheckRuleRequest(
            connectivity_id=ConnectionID(session_alias=user),
            root_filter=root_message_filter,
            # message_timeout=5000,
            timeout=int(action.extra_data.get('Time', 20000)),
            parent_event_id=Context.get('root_event_id'),
            description=f'{message_type} for {user} (ID: {action.extra_data["ID"]})',
            direction=direction,
            book_name=self._config.book)

        if parent_event_id := Context.get('parent_event_id'):
            check_rule_request.parent_event_id.CopyFrom(parent_event_id)

        if checkpoint_id := Context.get('checkpoint_id'):
            check_rule_request.checkpoint.CopyFrom(checkpoint_id)

        chain_id_mapping = Context.get('chain_id_mapping')
        chain_id = chain_id_mapping.get(user_and_direction) if chain_id_mapping is not None else None
        if chain_id is not None:
            check_rule_request.chain_id.CopyFrom(chain_id)

        response = self._check1_service.submitCheckRule(check_rule_request)
        if chain_id_mapping is None:
            Context.set('chain_id_mapping', {user_and_direction: response.chain_id})
        else:
            Context.get('chain_id_mapping')[user_and_direction] = response.chain_id
