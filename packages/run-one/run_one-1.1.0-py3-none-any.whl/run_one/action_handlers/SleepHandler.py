import time

from run_one.action_handlers.abstract_action_handler import AbstractActionHandler
from run_one.util.util import Action


class SleepHandler(AbstractActionHandler):

    def process(self, action: Action):
        time.sleep(float(action.extra_data.get('Time', 0)) / 1000)
