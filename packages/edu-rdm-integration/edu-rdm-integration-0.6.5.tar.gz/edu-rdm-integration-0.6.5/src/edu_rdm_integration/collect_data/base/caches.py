from typing import (
    Any,
    Dict,
    NamedTuple,
)

from educommon.integration_entities.enums import (
    EntityLogOperation,
)


class LogChange(NamedTuple):
    """Операция и значения измененных полей из лога."""

    operation: EntityLogOperation
    fields: Dict[str, Any]

    @property
    def is_create(self) -> bool:
        """Лог создания."""
        return self.operation == EntityLogOperation.CREATE

    @property
    def is_update(self) -> bool:
        """Лог изменения."""
        return self.operation == EntityLogOperation.UPDATE

    @property
    def is_delete(self) -> bool:
        """Лог удаления."""
        return self.operation == EntityLogOperation.DELETE
