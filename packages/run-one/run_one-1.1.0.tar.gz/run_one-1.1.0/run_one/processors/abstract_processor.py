from importlib import import_module
from typing import Type

from run_one.action_handlers.abstract_action_handler import AbstractActionHandler
from run_one.util.util import Action


class AbstractProcessor:

    def load_action_handlers(self, processed_actions_mapping: dict) -> dict[str, Type[AbstractActionHandler]]:
        result = {}
        for action, handler_name in processed_actions_mapping.items():
            try:
                action_handler_module = import_module(f'run_one.action_handlers.{handler_name}')
            except ModuleNotFoundError:
                try:
                    action_handler_module = import_module(f'action_handlers.{handler_name}')
                except ModuleNotFoundError:
                    raise ModuleNotFoundError(f'Action Handler class {handler_name} is not found')

            action_handler_class = getattr(action_handler_module, handler_name, None)

            if action_handler_class is None:
                raise ModuleNotFoundError(f'Action Handler class {handler_name} is not found')

            result[action] = action_handler_class

        return result

    def process(self, matrices_data: dict[str, dict[str, list[Action]]]):
        """
        Process test cases
        :param matrices_data: collection of parsed matrices data: matrix file name to test cases data
                              (test case name to list of its actions)
        """
        pass
