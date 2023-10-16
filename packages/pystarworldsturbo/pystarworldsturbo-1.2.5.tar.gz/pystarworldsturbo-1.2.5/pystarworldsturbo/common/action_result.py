from .action_outcome import ActionOutcome


class ActionResult():
    def __init__(self, outcome: ActionOutcome) -> None:
        self.__outcome: ActionOutcome = outcome

        assert isinstance(self.__outcome, ActionOutcome)

    def get_outcome(self) -> ActionOutcome:
        return self.__outcome

    def amend_outcome(self, new_outcome: ActionOutcome) -> None:
        self.__outcome = new_outcome

        assert isinstance(self.__outcome, ActionOutcome)
