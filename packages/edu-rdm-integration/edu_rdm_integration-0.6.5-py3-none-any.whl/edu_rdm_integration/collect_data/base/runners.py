from django.conf import (
    settings,
)

from educommon import (
    logger,
)
from educommon.utils.seqtools import (
    make_chunks,
)

from edu_rdm_integration.adapters.runners import (
    WebEduRunner,
)
from edu_rdm_integration.consts import (
    LOGS_DELIMITER,
)


class BaseCollectingDataRunner(WebEduRunner):
    """
    Базовый класс ранеров функций сбора данных для интеграции с "Региональная витрина данных".

    Поддерживается режим принудительного запуска функций без постановки в очередь на исполнение.
    """

    def __init__(self, *args, is_force_run: bool = False, **kwargs):
        self._is_force_run = is_force_run

        super().__init__(*args, **kwargs)

    def _populate_queue_by_runnable_classes(self, logs, *args, **kwargs):
        """
        Заполнение очереди запускаемыми объектами.
        """
        raw_logs_chunks = make_chunks(
            iterable=logs,
            size=settings.RDM_COLLECT_CHUNK_SIZE,
        )

        for chunk_index, raw_logs in enumerate(raw_logs_chunks, start=1):
            runnable_classes = self._prepare_runnable_classes()

            raw_logs = list(raw_logs)

            for runnable_class in runnable_classes:
                runnable = runnable_class(raw_logs=list(raw_logs), *args, **kwargs)

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
