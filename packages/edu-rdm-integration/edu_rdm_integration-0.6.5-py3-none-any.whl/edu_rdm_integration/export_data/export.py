from collections import (
    defaultdict,
)
from datetime import (
    date,
    datetime,
    time,
    timedelta,
)
from typing import (
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Type,
)

from django.conf import (
    settings,
)
from django.db.models import (
    F,
    Max,
    Model,
    Q,
    Value,
)
from django.db.models.base import (
    ModelBase,
)
from django.db.models.functions import (
    Concat,
)
from django.utils import (
    timezone,
)
from django.utils.datastructures import (
    OrderedSet,
)

from educommon import (
    logger,
)
from educommon.utils.date import (
    get_today_max_datetime,
    get_today_min_datetime,
)
from function_tools.managers import (
    RunnerManager,
)
from m3_db_utils.consts import (
    DEFAULT_ORDER_NUMBER,
)
from m3_db_utils.models import (
    ModelEnumValue,
)

from edu_rdm_integration.consts import (
    REGIONAL_DATA_MART_INTEGRATION_EXPORTING_DATA,
)
from edu_rdm_integration.enums import (
    FileUploadStatusEnum,
)
from edu_rdm_integration.models import (
    ExportingDataStage,
    ExportingDataSubStage,
    ExportingDataSubStageStatus,
    RegionalDataMartEntityEnum,
)
from edu_rdm_integration.signals import (
    manager_created,
)
from edu_rdm_integration.storages import (
    RegionalDataMartEntityStorage,
)


class BaseExportEntitiesData:
    """Базовый класс экспорта сущностей РВД за указанных период."""

    def __init__(
        self,
        entities: Iterable[str],
        period_started_at=datetime.combine(date.today(), time.min),
        period_ended_at=datetime.combine(date.today(), time.min),
        **kwargs,
    ):
        # Если сущности не указаны, берется значение по умолчанию - все сущности:
        entities = entities if entities else RegionalDataMartEntityEnum.get_enum_data().keys()
        self.entities: List[ModelEnumValue] = [
            RegionalDataMartEntityEnum.get_model_enum_value(entity) for entity in entities
        ]

        self.period_started_at = period_started_at
        self.period_ended_at = period_ended_at

        # Классы менеджеров Функций, которые должны быть запущены для выгрузки данных
        self._exporting_data_managers: Set[Type[RunnerManager]] = set()

        # Результаты работы Функций выгрузки данных
        self._exporting_data_results = []

        # Карта соответствия manager_id сущности и его основной модели
        self.manager_main_model_map: Dict[str, ModelBase] = {}

        # Идентификатор CollectDataCommandProgress для передачи сигналу manager_created
        self.command_id: Optional[int] = kwargs.get('command_id')

        self._configure_agent_client()

    def _configure_agent_client(self):
        """
        Конфигурирование клиента загрузчика данных в Витрину.

        #TODO Вынужденная мера, т.к. при запуске команды не производится проверка готовности конфигов приложений.
          # Нужно переработать механизм конфигурирования клиента загрузчика.
        """
        import uploader_client
        from uploader_client.contrib.rdm.interfaces.configurations import (
            RegionalDataMartUploaderConfig,
        )
        if settings.RDM_UPLOADER_CLIENT_ENABLE_REQUEST_EMULATION:
            uploader_client.set_config(
                RegionalDataMartUploaderConfig(
                    interface='uploader_client.contrib.rdm.interfaces.rest.OpenAPIInterfaceEmulation',
                    url=settings.RDM_UPLOADER_CLIENT_URL,
                    datamart_name=settings.RDM_UPLOADER_CLIENT_DATAMART_NAME,
                    timeout=1,
                    request_retries=1,
                )
            )
        else:
            uploader_client.set_config(
                RegionalDataMartUploaderConfig(
                    url=settings.RDM_UPLOADER_CLIENT_URL,
                    datamart_name=settings.RDM_UPLOADER_CLIENT_DATAMART_NAME,
                    timeout=settings.RDM_UPLOADER_CLIENT_REQUEST_TIMEOUT,
                    request_retries=settings.RDM_UPLOADER_CLIENT_REQUEST_RETRIES,
                )
            )

    def _has_stage_created_or_in_progress(self, manager_id: str, entity: str) -> bool:
        """Проверяет есть ли готовый к работе stage или в работе для данной сущности."""
        stage_created_or_in_progress = ExportingDataStage.objects.filter(
            manager_id=manager_id,
            status_id__in=(ExportingDataSubStageStatus.CREATED.key, ExportingDataSubStageStatus.IN_PROGRESS.key),
        ).exists()

        if stage_created_or_in_progress:
            logger.info(f'entity {entity} is skipped because it is already created or in progress!')

        return stage_created_or_in_progress

    def _fill_manager_entities_map(self, entity_storage: RegionalDataMartEntityStorage) -> None:
        """
        Заполнение словаря данных с классами менеджеров и их сущностями.
        """

    def _find_exporting_entities_data_managers(self):
        """
        Поиск менеджеров Функций выгрузки данных по сущностям РВД.
        """
        logger.info('find exporting entities data manager..')

        entity_storage = RegionalDataMartEntityStorage()
        entity_storage.prepare()

        exporting_entities_data_managers_map = entity_storage.prepare_entities_manager_map(
            tags={REGIONAL_DATA_MART_INTEGRATION_EXPORTING_DATA},
        )
        self._fill_manager_entities_map(entity_storage)

        entities = filter(lambda entity: entity.order_number != DEFAULT_ORDER_NUMBER, self.entities)

        for entity_enum in entities:
            manager_class = exporting_entities_data_managers_map.get(entity_enum.key)

            if manager_class and not self._has_stage_created_or_in_progress(manager_class.uuid, entity_enum.key):
                self.manager_main_model_map[manager_class.uuid] = entity_enum.main_model_enum.model
                self._exporting_data_managers.add(manager_class)

        logger.info('finding exporting entities data manager finished.')

    def _export_entities_data(self, *args, **kwargs):
        """
        Выгрузка данных по указанным сущностям.
        """
        logger.info('start exporting entities data..')

        kwargs['period_started_at'] = self.period_started_at
        kwargs['period_ended_at'] = self.period_ended_at

        for manager_class in self._exporting_data_managers:
            manager = manager_class(*args, is_only_main_model=True, **kwargs)

            if self.command_id:
                # Подается сигнал, что менеджер создан:
                manager_created.send(sender=manager,
                                     command_id=self.command_id)

            manager.run()

            self._exporting_data_results.append(manager.result)

        logger.info('exporting entities data finished.')

    def export(self, *args, **kwargs):
        """
        Выполнение действий команды.
        """
        logger.info(
            f'start exporting data of entities - {", ".join([entity.key for entity in self.entities])}..'
        )

        self._find_exporting_entities_data_managers()
        self._export_entities_data(*args, **kwargs)

        logger.info('exporting entities data finished.')


class BaseExportLatestEntitiesData(BaseExportEntitiesData):
    """Базовый класс выгрузки сущностей с момента последней успешной выгрузки."""

    def __init__(
        self,
        entities: Iterable[str],
        period_started_at=datetime.combine(date.today(), time.min),
        period_ended_at=datetime.combine(date.today(), time.min),
        update_modified: bool = True,
        **kwargs,
    ):
        super().__init__(entities, period_started_at, period_ended_at, **kwargs)

        self._exporting_data_managers: Set[Type[RunnerManager]] = OrderedSet()

        # Словарь данных с классами менеджеров и их сущностями
        self._manager_entities_map: Dict[Type[object], List[str]] = defaultdict(set)

        self.async_task = self._get_async_task()
        self.task_id = kwargs.get('task_id')

        self.update_modified = update_modified

    def _get_async_task(self) -> Model:
        """Возвращает модель асинхронной задачи."""
        raise NotImplementedError

    def _set_description_to_async_task(self, exported_entities: Iterable[str]) -> None:
        """Добавляет в описание асинхронной задачи список выгруженных сущностей."""
        if exported_entities and self.task_id:
            self.async_task.objects.filter(
                task_id=self.task_id,
            ).update(
                description=Concat(
                    'description',
                    Value(f': {", ".join(exported_entities)}')
                ),
            )

    def _fill_manager_entities_map(self, entity_storage: RegionalDataMartEntityStorage) -> None:
        """
        Заполнение словаря данных с классами менеджеров и их сущностями.
        """
        self._manager_entities_map = entity_storage.prepare_manager_entities_map(
            tags={REGIONAL_DATA_MART_INTEGRATION_EXPORTING_DATA},
        )

    def _update_model_modified_field(self, manager_id: str, last_finished_export_data: datetime) -> None:
        """Обновляет поле modified у невыгруженных записей."""
        if not self.update_modified:
            return
        
        model = self.manager_main_model_map[manager_id]
        
        queryset_to_update = model.objects.filter(
            # 1. Не заполнен подэтап выгрузки и modified записи модели < левой границы периода команды latest:
            Q(
                exporting_sub_stage_id__isnull=True,
                modified__lt=last_finished_export_data,
            )
            # 2. Подэтап выгрузки заполнен
            # и modified записи > даты выгрузки указанной в записи модели сбора (ended_at подэтапа выгрузки)
            # и modified записи модели < левой границы периода команды latest (даты последней удачной выгрузки):
            | Q(
                exporting_sub_stage__isnull=False,
                modified__gt=F('exporting_sub_stage__ended_at'),
                modified__lt=last_finished_export_data,
            )
            # 3. Подэтап выгрузки указанной в записи модели имеет статус FAILED:
            | Q(
                exporting_sub_stage__status_id=ExportingDataSubStageStatus.FAILED.key,
            )
            # 4. Связь лога подэтапа выгрузки с логом загрузки данных (ExportingDataSubStageUploaderClientLog)
            # имеет статус FileUploadStatusEnum.ERROR:
            | Q(
                exporting_sub_stage__exportingdatasubstageuploaderclientlog__file_upload_status=(
                    FileUploadStatusEnum.ERROR),
            )
        )
        queryset_to_update.update(modified=timezone.now())

    def _calculate_last_finished_entity_export(self) -> Dict[str, datetime]:
        """Находит левую границу экспорта данных для сущностей."""
        manager_to_last_date = ExportingDataSubStage.objects.values(
            'stage__manager_id',
        ).annotate(
            max_ended_at=Max('ended_at'),
            entity_uuid=F('stage__manager_id'),
        ).filter(
            status_id=ExportingDataSubStageStatus.FINISHED.key,
            entity_uuid__in=[m.uuid for m in self._exporting_data_managers],
        ).values('entity_uuid', 'max_ended_at')

        return {str(m['entity_uuid']): m['max_ended_at'] for m in manager_to_last_date}

    def _export_entities_data(self, *args, **kwargs) -> None:
        """
        Запуск Функций по для экспорта данных.
        """
        logger.info('export entities data..')

        # Массив с выгружаемыми сущностями для поля "Описание" в асинхронной задаче
        exported_entities = []

        last_finished_entity_export = self._calculate_last_finished_entity_export()

        for manager_class in self._exporting_data_managers:
            last_finished_export_data = last_finished_entity_export.get(
                manager_class.uuid,
                timezone.now(),
            )
            # Обновить поля modified у модели сущности:
            self._update_model_modified_field(
                manager_id=manager_class.uuid, 
                last_finished_export_data=last_finished_export_data,
            )

            kwargs['period_started_at'] = last_finished_export_data
            kwargs['period_ended_at'] = get_today_max_datetime()

            if kwargs['period_started_at'] > kwargs['period_ended_at']:
                kwargs['period_started_at'] = kwargs['period_ended_at'] - timedelta(
                    seconds=settings.RDM_TRANSFER_TASK_TIMEDELTA
                )

            manager = manager_class(*args, **kwargs)

            if self.command_id:
                # Подается сигнал, что менеджер создан:
                manager_created.send(sender=manager,
                                     command_id=self.command_id)

            manager.run()

            self._exporting_data_results.append(manager.result)

            # Если сущность была выгружена, то добавим ее в список exported_entities
            if manager.result.entities and self.task_id:
                exported_entities.extend(self._manager_entities_map.get(manager_class))

        self._set_description_to_async_task(exported_entities)

        logger.info('collecting entities data finished.')


class ExportEntitiesData(BaseExportEntitiesData):
    """Экспорт сущностей РВД за указанных период."""
