from typing import (
    Dict,
    Tuple,
)

from educommon.integration_entities.enums import (
    EntityLogOperation,
)


# Перечень отслеживаемых моделей и перечней полей по операциям лога. Расширяется в продуктах
MODEL_FIELDS_LOG_FILTER: Dict[EntityLogOperation, Dict[str, Tuple]] = {
    EntityLogOperation.CREATE: {},
    EntityLogOperation.UPDATE: {},
    EntityLogOperation.DELETE: {}
}
