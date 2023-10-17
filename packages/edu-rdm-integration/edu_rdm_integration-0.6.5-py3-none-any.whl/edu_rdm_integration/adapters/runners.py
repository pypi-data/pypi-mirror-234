from abc import (
    ABCMeta,
)
from typing import (
    Type,
)

from function_tools.runners import (
    BaseRunner,
    GlobalHelperRunner,
)

from edu_rdm_integration.adapters.helpers import (
    WebEduRunnerHelper,
)
from edu_rdm_integration.adapters.results import (
    WebEduRunnerResult,
)
from edu_rdm_integration.adapters.validators import (
    WebEduRunnerValidator,
)


class WebEduRunner(BaseRunner, metaclass=ABCMeta):
    """
    Базовый класс ранеров функций продуктов Образования.
    """

    def _prepare_helper_class(self) -> Type[WebEduRunnerHelper]:
        """
        Возвращает класс помощника ранера функции.
        """
        return WebEduRunnerHelper

    def _prepare_validator_class(self) -> Type[WebEduRunnerValidator]:
        """
        Возвращает класс валидатора ранера функции.
        """
        return WebEduRunnerValidator

    def _prepare_result_class(self) -> Type[WebEduRunnerResult]:
        """
        Возвращает класс результата ранера функции.
        """
        return WebEduRunnerResult


class WebEduGlobalHelperRunner(GlobalHelperRunner, metaclass=ABCMeta):
    """
    Базовый класс для создания ранеров выполнения запускаемых объектов с
    глобальным помощником продуктов Образования.
    """

    def _prepare_helper_class(self) -> Type[WebEduRunnerHelper]:
        """
        Возвращает класс помощника ранера функции.
        """
        return WebEduRunnerHelper

    def _prepare_validator_class(self) -> Type[WebEduRunnerValidator]:
        """
        Возвращает класс валидатора ранера функции.
        """
        return WebEduRunnerValidator

    def _prepare_result_class(self) -> Type[WebEduRunnerResult]:
        """
        Возвращает класс результата ранера функции.
        """
        return WebEduRunnerResult
