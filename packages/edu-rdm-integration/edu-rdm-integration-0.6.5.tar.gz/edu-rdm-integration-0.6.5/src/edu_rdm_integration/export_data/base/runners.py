from typing import (
    Type,
)

from educommon import (
    logger,
)

from edu_rdm_integration.adapters.runners import (
    WebEduRunner,
)
from edu_rdm_integration.consts import (
    LOGS_DELIMITER,
)
from edu_rdm_integration.export_data.base.helpers import (
    BaseExportDataRunnerHelper,
)
from edu_rdm_integration.export_data.base.results import (
    BaseExportDataRunnerResult,
)
from edu_rdm_integration.export_data.base.validators import (
    BaseExportDataRunnerValidator,
)


class BaseExportDataRunner(WebEduRunner):
    """
    Базовый класс ранеров функций выгрузки данных для интеграции с "Региональная витрина данных".
    """

    def __init__(self, *args, is_force_run: bool = False, **kwargs):
        self._is_force_run = is_force_run

        super().__init__(*args, **kwargs)

    def _prepare_helper_class(self) -> Type[BaseExportDataRunnerHelper]:
        """
        Возвращает класс помощника ранера функции.
        """
        return BaseExportDataRunnerHelper

    def _prepare_validator_class(self) -> Type[BaseExportDataRunnerValidator]:
        """
        Возвращает класс валидатора ранера функции.
        """
        return BaseExportDataRunnerValidator

    def _prepare_result_class(self) -> Type[BaseExportDataRunnerResult]:
        """
        Возвращает класс результата ранера функции.
        """
        return BaseExportDataRunnerResult

    def _prepare_model_ids_chunks(self, *args, model_ids_map=None, **kwargs):
        """
        Формирование чанков идентификаторов записей моделей для дальнейшей работы в рамках функций.
        """
        # model_ids_chunks = make_chunks(
        #     iterable=model_ids,
        #     size=settings.RDM_EXPORT_CHUNK_SIZE,
        # )

        return ()

    def _populate_queue_by_runnable_classes(self, *args, **kwargs):
        """
        Заполнение очереди запускаемыми объектами.
        """
        model_ids_chunks = self._prepare_model_ids_chunks(*args, **kwargs)

        for chunk_index, model_ids_chunk in enumerate(model_ids_chunks, start=1):
            runnable_classes = self._prepare_runnable_classes()

            model_ids_chunk = list(model_ids_chunk)

            for runnable_class in runnable_classes:
                runnable = runnable_class(model_ids=model_ids_chunk, *args, **kwargs)

                # TODO EDUSCHL-20274 Реализация форсированного выполнения функций
                if self._is_force_run:
                    logger.info(
                        f'{LOGS_DELIMITER * 2}force run {runnable_class.__name__} with logs chunk {chunk_index}..'
                    )
                    self.force_run(runnable=runnable, *args, **kwargs)
                else:

                    logger.info(
                        f'{LOGS_DELIMITER * 2}enqueue {runnable_class.__name__} with logs chunk {chunk_index}..'
                    )

                    self.enqueue(runnable=runnable, *args, **kwargs)

    # TODO EDUSCHL-20274 Реализация форсированного выполнения функций
    def force_run(self, runnable, *args, **kwargs):
        """Принудительное выполнение запускаемого объекта."""
        self.before_validate()
        self.validate()
        self.after_validate()

        if self.result.has_not_errors:
            runnable.before_validate()
            runnable.validate()
            runnable.after_validate()

            runnable.before_run(*args, **kwargs)
            runnable.run(*args, **kwargs)
            runnable.after_run(*args, **kwargs)

            self.result.append_entity(runnable.result)