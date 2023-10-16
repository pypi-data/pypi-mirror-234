import abc

from pingsafe_cli.psgraph.common.output.record import Record
from pingsafe_cli.psgraph.policies_3d.syntax.syntax import Predicate


class SecretsPredicate(Predicate):
    def __init__(self, record: Record) -> None:
        super().__init__()
        self.record = record

    @abc.abstractmethod
    def __call__(self) -> bool:
        raise NotImplementedError()
