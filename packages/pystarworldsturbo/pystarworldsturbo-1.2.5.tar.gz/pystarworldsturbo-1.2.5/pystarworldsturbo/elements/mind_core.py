from typing import Iterable

from ..common.action import Action


class MindCore():
    def revise(self) -> None:
        # Abstract.
        raise NotImplementedError()

    def decide(self) -> Iterable[Action]:
        # Abstract.
        raise NotImplementedError()
