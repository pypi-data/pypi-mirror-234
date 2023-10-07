from th2_common.schema.grpc.router.grpc_router import GrpcRouter
from th2_common_utils import dict_to_message
from th2_grpc_act_template.act_service import ActService
from th2_grpc_act_template.act_template_pb2 import PlaceMessageRequest


from run_one.action_handlers.abstract_action_handler import AbstractActionHandler
from run_one.action_handlers.context import Context
from run_one.util.util import Action
from run_one.processors.th2_processor import Th2ProcessorConfig


class TH2ActHandler(AbstractActionHandler):

    def __init__(self, config: Th2ProcessorConfig, grpc_router: GrpcRouter, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._config = config
        self._act_service: ActService = grpc_router.get_service(ActService)  # type: ignore

    def _get_act_method(self, message_type: str):
        return {'NewOrderSingle': self._act_service.placeOrderFIX,
                'OrderCancelRequest': self._act_service.placeOrderCancelRequest,
                'OrderCancelReplaceRequest': self._act_service.placeOrderCancelReplaceRequest,
                'OrderMassCancelRequest': self._act_service.placeOrderMassCancelRequestFIX}[message_type]

    def process(self, action: Action):
        message_type = action.extra_data['MessageType']
        message = PlaceMessageRequest(message=dict_to_message(fields=action.row,
                                                              message_type=message_type,
                                                              session_alias=action.extra_data['User']))

        if parent_event_id := Context.get('parent_event_id'):
            message.parent_event_id.CopyFrom(parent_event_id)

        if not self._config.use_place_method:
            response = self._act_service.sendMessage(message)
        else:
            response = self._get_act_method(message_type)(message, timeout=float(action.extra_data.get('Time', 0)))

        Context.set('checkpoint_id', response.checkpoint_id)

