from abc import (
    ABCMeta,
)

from educommon import (
    logger,
)
from educommon.integration_entities.mixins import (
    EntitiesMixin,
)

from edu_rdm_integration.adapters.functions import (
    WebEduLazySavingPredefinedQueueFunction,
)
from edu_rdm_integration.consts import (
    LOGS_DELIMITER,
)
from edu_rdm_integration.models import (
    CollectingDataSubStageStatus,
    CollectingExportedDataStage,
    CollectingExportedDataSubStage,
)


class BaseCollectingCalculatedDataFunction(
    EntitiesMixin,
    WebEduLazySavingPredefinedQueueFunction,
    metaclass=ABCMeta,
):
    """
    Базовый класс функций сбора данных для интеграции с "Региональная витрина данных".
    """

    def __init__(self, *args, stage: CollectingExportedDataStage, **kwargs):
        super().__init__(*args, stage=stage, **kwargs)

        previous_sub_stage = CollectingExportedDataSubStage.objects.filter(
            function_id=self.uuid,
        ).order_by('started_at').only('pk').first()

        self._sub_stage = CollectingExportedDataSubStage.objects.create(
            stage=stage,
            function_id=self.uuid,
            previous_id=getattr(previous_sub_stage, 'pk', None),
        )

        logger.info(f'{LOGS_DELIMITER * 3}created {repr(self._sub_stage)}')

    def _before_prepare(self, *args, **kwargs):
        """
        Выполнение действий функций системы.
        """
        self._sub_stage.status_id = CollectingDataSubStageStatus.IN_PROGRESS.key
        self._sub_stage.save()

        logger.info(f'{LOGS_DELIMITER * 3}change status {repr(self._sub_stage)}')

    def run(self, *args, **kwargs):
        """
        Выполнение действий функции с дальнейшим сохранением объектов в базу при отсутствии ошибок.
        """
        super().run(*args, **kwargs)

        if self.result.errors:
            self._sub_stage.status_id = CollectingDataSubStageStatus.FAILED.key
        else:
            self._sub_stage.status_id = CollectingDataSubStageStatus.READY_TO_EXPORT.key

        self._sub_stage.save()

        logger.info(f'{LOGS_DELIMITER * 3}change status {repr(self._sub_stage)}')

        logger.info(f'{LOGS_DELIMITER * 3}{self.__class__.__name__} finished.')
