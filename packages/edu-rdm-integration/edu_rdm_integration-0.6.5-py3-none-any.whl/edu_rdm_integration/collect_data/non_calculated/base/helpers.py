from typing import (
    Type,
)

from edu_rdm_integration.adapters.helpers import (
    WebEduFunctionHelper,
    WebEduRunnerHelper,
)
from edu_rdm_integration.collect_data.non_calculated.base.caches import (
    BaseCollectingExportedDataFunctionCacheStorage,
    BaseCollectingExportedDataRunnerCacheStorage,
)


class BaseCollectingExportedDataRunnerHelper(WebEduRunnerHelper):
    """
    Базовый класс помощников ранеров функций сбора данных для интеграции с "Региональная витрина данных".
    """

    def _prepare_cache_class(self) -> Type[BaseCollectingExportedDataRunnerCacheStorage]:
        """
        Возвращает класс кеша помощника ранера.
        """
        return BaseCollectingExportedDataRunnerCacheStorage


class BaseCollectingExportedDataFunctionHelper(WebEduFunctionHelper):
    """
    Базовый класс помощников функций сбора данных для интеграции с "Региональная витрина данных".
    """

    def _prepare_cache_class(self) -> Type[BaseCollectingExportedDataFunctionCacheStorage]:
        """
        Возвращает класс кеша помощника функции.
        """
        return BaseCollectingExportedDataFunctionCacheStorage
