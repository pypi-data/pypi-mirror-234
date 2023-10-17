from typing import (
    Type,
)

from edu_rdm_integration.collect_data.base.runners import (
    BaseCollectingDataRunner,
)
from edu_rdm_integration.collect_data.non_calculated.base.helpers import (
    BaseCollectingExportedDataRunnerHelper,
)
from edu_rdm_integration.collect_data.non_calculated.base.results import (
    BaseCollectingExportedDataRunnerResult,
)
from edu_rdm_integration.collect_data.non_calculated.base.validators import (
    BaseCollectingExportedDataRunnerValidator,
)


class BaseCollectingExportedDataRunner(BaseCollectingDataRunner):
    """
    Базовый класс ранеров функций сбора данных для интеграции с "Региональная витрина данных".
    """

    def _prepare_helper_class(self) -> Type[BaseCollectingExportedDataRunnerHelper]:
        """
        Возвращает класс помощника ранера функции.
        """
        return BaseCollectingExportedDataRunnerHelper

    def _prepare_validator_class(self) -> Type[BaseCollectingExportedDataRunnerValidator]:
        """
        Возвращает класс валидатора ранера функции.
        """
        return BaseCollectingExportedDataRunnerValidator

    def _prepare_result_class(self) -> Type[BaseCollectingExportedDataRunnerResult]:
        """
        Возвращает класс результата ранера функции.
        """
        return BaseCollectingExportedDataRunnerResult
