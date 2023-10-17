from abc import (
    ABCMeta,
)
from typing import (
    Type,
)

from function_tools.managers import (
    RunnerManager,
)

from edu_rdm_integration.adapters.runners import (
    WebEduRunner,
)


class WebEduRunnerManager(RunnerManager, metaclass=ABCMeta):
    """
    Базовый класс менеджеров пускателей функций продуктов Образования.
    """

    @classmethod
    def _prepare_runner_class(cls) -> Type[WebEduRunner]:
        """
        Возвращает класс ранера.
        """
        return WebEduRunner

