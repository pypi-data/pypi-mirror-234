from th2_common.schema.grpc.router.grpc_router import GrpcRouter
from th2_grpc_act_ssh.act_ssh_pb2 import ExecutionRequest
from th2_grpc_act_ssh.act_ssh_service import ActSshService

from run_one.action_handlers.abstract_action_handler import AbstractActionHandler
from run_one.action_handlers.context import Context
from run_one.processors.th2_processor import Th2ProcessorConfig
from run_one.util.util import Action


class TH2ActSSHHandler(AbstractActionHandler):

    def __init__(self, config: Th2ProcessorConfig, grpc_router: GrpcRouter, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._config = config
        self._act_ssh_service: ActSshService = grpc_router.get_service(ActSshService)  # type: ignore

    def process(self, action: Action):
        execution_request = ExecutionRequest(endpoint_alias=action.extra_data['User'],
                                             execution_alias=action.extra_data['ExecutionAlias'],
                                             parameters=action.row)

        if parent_event_id := Context.get('parent_event_id'):
            execution_request.event_info.parent_event_id.CopyFrom(parent_event_id)

        self._act_ssh_service.execute(execution_request)
