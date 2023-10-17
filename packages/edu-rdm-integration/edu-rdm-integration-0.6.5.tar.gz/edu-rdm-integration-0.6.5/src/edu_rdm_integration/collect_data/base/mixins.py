from educommon.audit_log.utils import (
    get_model_by_table,
)
from educommon.integration_entities.consts import (
    LOG_OPERATION_MAP,
)
from educommon.integration_entities.enums import (
    EntityLogOperation,
)

from edu_rdm_integration.collect_data.base.caches import (
    LogChange,
)
from edu_rdm_integration.mapping import (
    MODEL_FIELDS_LOG_FILTER,
)


class ReformatLogsMixin:
    """Миксин для преобразования логов к удобному для работы виду в кешах помощников функций."""

    def _reformat_logs(self):
        """
        Производится преобразование логов к удобному для работы виду.

        Предполагается вложенные словари. На первом уровне ключом будет название
        модели, на втором идентификатор записи.
        """
        for log in self.raw_logs:
            model = get_model_by_table(log.table)._meta.label

            if getattr(self, '_log_only_models', None) and (model not in self._log_only_models):
                # Пропускаем, если модель не входит в список отслеживаемых
                continue

            operation = LOG_OPERATION_MAP[log.operation]

            if operation in EntityLogOperation.values:
                fields = log.data
            else:
                fields = {}

            log_change = LogChange(
                operation=operation,
                fields=fields,
            )

            if not self._filter_log(model, log_change):
                # Если модель не отслеживается, то запись лога не сохраняем
                continue

            if log_change.operation == EntityLogOperation.DELETE:
                self.logs[model][log.object_id] = [log_change, ]
            else:
                self.logs[model][log.object_id].append(log_change)

    @staticmethod
    def _filter_log(model: str, log_change: LogChange) -> bool:
        """
        Производится проверка изменений на отслеживаемые поля.
        """
        is_filtered = False

        if model in MODEL_FIELDS_LOG_FILTER[log_change.operation]:
            filter_fields = MODEL_FIELDS_LOG_FILTER[log_change.operation][model]
            if filter_fields:
                # Если заданы конкретные поля, которые должны отслеживать
                for field in log_change.fields:
                    if field in filter_fields:
                        # Достаточно, чтобы хотя бы одно поле попало под фильтр
                        is_filtered = True
                        break
            else:
                # Модель отслеживается, но перечень фильтруемых полей не задан,
                # значит фильтруем все поля модели
                is_filtered = True

        return is_filtered
