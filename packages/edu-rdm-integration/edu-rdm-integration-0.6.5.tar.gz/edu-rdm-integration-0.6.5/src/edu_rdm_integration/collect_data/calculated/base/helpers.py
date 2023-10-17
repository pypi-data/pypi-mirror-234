from typing import (
    Type,
)

from edu_rdm_integration.adapters.helpers import (
    WebEduFunctionHelper,
    WebEduRunnerHelper,
)
from edu_rdm_integration.collect_data.calculated.base.caches import (
    BaseCollectingCalculatedExportedDataFunctionCacheStorage,
    BaseCollectingCalculatedExportedDataRunnerCacheStorage,
)


class BaseCollectingCalculatedExportedDataRunnerHelper(WebEduRunnerHelper):
    """
    Базовый класс помощников ранеров функций сбора расчетных данных для интеграции с "Региональная витрина данных".
    """

    def _prepare_cache_class(self) -> Type[BaseCollectingCalculatedExportedDataRunnerCacheStorage]:
        """
        Возвращает класс кеша помощника ранера.
        """
        return BaseCollectingCalculatedExportedDataRunnerCacheStorage


class BaseCollectingCalculatedExportedDataFunctionHelper(WebEduFunctionHelper):
    """
    Базовый класс помощников функций сбора расчетных данных для интеграции с "Региональная витрина данных".
    """

    def _prepare_cache_class(self) -> Type[BaseCollectingCalculatedExportedDataFunctionCacheStorage]:
        """
        Возвращает класс кеша помощника функции.
        """
        return BaseCollectingCalculatedExportedDataFunctionCacheStorage
