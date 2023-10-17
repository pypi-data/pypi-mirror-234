from datetime import (
    date,
    datetime,
)
from itertools import (
    chain,
)
from typing import (
    List,
    Type,
)

from django.conf import (
    settings,
)

from educommon.utils.conversion import (
    str_without_control_chars,
)
from educommon.utils.crypto import (
    HashData,
)

from edu_rdm_integration.adapters.helpers import (
    WebEduFunctionHelper,
    WebEduRunnerHelper,
)
from edu_rdm_integration.consts import (
    DATE_FORMAT,
    EXPORT_DATETIME_FORMAT,
    HASH_ALGORITHM,
)
from edu_rdm_integration.export_data.base.caches import (
    BaseExportDataFunctionCacheStorage,
    BaseExportDataRunnerCacheStorage,
)


class BaseExportDataRunnerHelper(WebEduRunnerHelper):
    """
    Базовый класс помощников ранеров функций выгрузки данных для интеграции с "Региональная витрина данных".
    """

    def _prepare_cache_class(self) -> Type[BaseExportDataRunnerCacheStorage]:
        """
        Возвращает класс кеша помощника ранера.
        """
        return BaseExportDataRunnerCacheStorage


class BaseExportDataFunctionHelper(WebEduFunctionHelper):
    """
    Базовый класс помощников функций выгрузки данных для интеграции с "Региональная витрина данных".
    """

    cryptographer = HashData(hash_algorithm=HASH_ALGORITHM)

    @classmethod
    def prepare_record(
        cls,
        entity_instance,
        ordered_fields,
        primary_key_fields,
        foreign_key_fields,
        hashable_fields
    ) -> List[str]:
        """
        Формирование списка строковых значений полей.
        """
        field_values = []
        key_fields = set(chain(primary_key_fields, foreign_key_fields))

        for field in ordered_fields:
            field_value = getattr(entity_instance, field)

            if isinstance(field_value, str):
                # Очистка строковых полей от управляющих символов
                field_value = str_without_control_chars(field_value)
            elif isinstance(field_value, datetime):
                # Дату/время передаём в формате: YYYY-MM-DD hh:mm:ss
                field_value = field_value.strftime(EXPORT_DATETIME_FORMAT)
            elif isinstance(field_value, date):
                field_value = field_value.strftime(DATE_FORMAT)
            else:
                field_value = str(field_value if field_value is not None else '')

            if field_value and field in key_fields:
                field_value = f'{settings.RDM_EXPORT_ENTITY_ID_PREFIX}-{field_value}'

            if field_value and field in hashable_fields:
                field_value = cls.cryptographer.get_hash(field_value)

            # Экранирование двойных кавычек
            field_value = field_value.replace('"', '""')

            field_values.append(field_value)

        return [f'"{v}"' for v in field_values]

    def _prepare_cache_class(self) -> Type[BaseExportDataFunctionCacheStorage]:
        """
        Возвращает класс кеша помощника функции.
        """
        return BaseExportDataFunctionCacheStorage
