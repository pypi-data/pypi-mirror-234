from typing import Iterable, Any

from ..common.action import Action
from ..utils.utils import ignore


class Mind():
    def perceive(self, *args: Any, **kwargs: Any) -> None:
        # Abstract.

        for p in args:
            ignore(p)

        for k, v in kwargs.items():
            ignore(k)
            ignore(v)

        raise NotImplementedError()

    def revise(self) -> None:
        # Abstract.
        raise NotImplementedError()

    def decide(self) -> None:
        # Abstract.
        raise NotImplementedError()

    def execute(self) -> Iterable[Action]:
        # Abstract.
        raise NotImplementedError()
