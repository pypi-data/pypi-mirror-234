from run_one.util.util import Action


class AbstractActionHandler:

    def __init__(self, *args, **kwargs) -> None:
        pass

    def process(self, action: Action):
        pass

    def on_action_change(self, previous_action: Action, current_action: Action):
        pass

    def on_test_case_end(self):
        pass
