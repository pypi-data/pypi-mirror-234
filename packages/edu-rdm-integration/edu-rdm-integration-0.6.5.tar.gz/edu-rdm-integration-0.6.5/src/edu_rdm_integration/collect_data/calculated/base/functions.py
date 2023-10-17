from abc import (
    ABCMeta,
)
from typing import (
    Type,
)

from edu_rdm_integration.collect_data.base.functions import (
    BaseCollectingCalculatedDataFunction,
)
from edu_rdm_integration.collect_data.calculated.base.helpers import (
    BaseCollectingCalculatedExportedDataFunctionHelper,
)
from edu_rdm_integration.collect_data.calculated.base.results import (
    BaseCollectingCalculatedExportedDataFunctionResult,
)
from edu_rdm_integration.collect_data.calculated.base.validators import (
    BaseCollectingCalculatedExportedDataFunctionValidator,
)


class BaseCollectingCalculatedExportedDataFunction(BaseCollectingCalculatedDataFunction, metaclass=ABCMeta):
    """
    Базовый класс функций сбора расчетных данных для интеграции с "Региональная витрина данных".
    """

    def _prepare_helper_class(self) -> Type[BaseCollectingCalculatedExportedDataFunctionHelper]:
        """
        Возвращает класс помощника функции.
        """
        return BaseCollectingCalculatedExportedDataFunctionHelper

    def _prepare_validator_class(self) -> Type[BaseCollectingCalculatedExportedDataFunctionValidator]:
        """
        Возвращает класс валидатора функции.
        """
        return BaseCollectingCalculatedExportedDataFunctionValidator

    def _prepare_result_class(self) -> Type[BaseCollectingCalculatedExportedDataFunctionResult]:
        """
        Возвращает класс результата функции.
        """
        return BaseCollectingCalculatedExportedDataFunctionResult
