from abc import (
    ABCMeta,
)
from typing import (
    Type,
)

from edu_rdm_integration.collect_data.base.functions import (
    BaseCollectingCalculatedDataFunction,
)
from edu_rdm_integration.collect_data.non_calculated.base.helpers import (
    BaseCollectingExportedDataFunctionHelper,
)
from edu_rdm_integration.collect_data.non_calculated.base.results import (
    BaseCollectingExportedDataFunctionResult,
)
from edu_rdm_integration.collect_data.non_calculated.base.validators import (
    BaseCollectingExportedDataFunctionValidator,
)


class BaseCollectingExportedDataFunction(BaseCollectingCalculatedDataFunction, metaclass=ABCMeta):
    """
    Базовый класс функций сбора данных для интеграции с "Региональная витрина данных".
    """

    def _prepare_helper_class(self) -> Type[BaseCollectingExportedDataFunctionHelper]:
        """
        Возвращает класс помощника функции.
        """
        return BaseCollectingExportedDataFunctionHelper

    def _prepare_validator_class(self) -> Type[BaseCollectingExportedDataFunctionValidator]:
        """
        Возвращает класс валидатора функции.
        """
        return BaseCollectingExportedDataFunctionValidator

    def _prepare_result_class(self) -> Type[BaseCollectingExportedDataFunctionResult]:
        """
        Возвращает класс результата функции.
        """
        return BaseCollectingExportedDataFunctionResult
