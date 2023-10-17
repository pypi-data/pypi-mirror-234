import json
from abc import (
    ABCMeta,
)
from pathlib import (
    Path,
)
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    Union,
)

from django.conf import (
    settings,
)
from django.core.files.base import (
    ContentFile,
)
from django.core.files.storage import (
    default_storage,
)
from transliterate import (
    slugify,
)
from uploader_client.adapters import (
    adapter,
)

from educommon import (
    logger,
)
from educommon.integration_entities.enums import (
    EntityLogOperation,
)
from educommon.integration_entities.mixins import (
    EntitiesMixin,
)

from edu_rdm_integration.adapters.functions import (
    WebEduLazySavingPredefinedQueueGlobalHelperFunction,
)
from edu_rdm_integration.consts import (
    LOGS_DELIMITER,
)
from edu_rdm_integration.enums import (
    FileUploadStatusEnum,
)
from edu_rdm_integration.export_data.base.consts import (
    OPERATIONS_METHODS_MAP,
    OPERATIONS_URLS_MAP,
)
from edu_rdm_integration.export_data.base.errors import (
    BaseExportDataError,
)
from edu_rdm_integration.export_data.base.helpers import (
    BaseExportDataFunctionHelper,
)
from edu_rdm_integration.export_data.base.requests import (
    RegionalDataMartEntityRequest,
)
from edu_rdm_integration.export_data.base.results import (
    BaseExportDataFunctionResult,
)
from edu_rdm_integration.export_data.base.validators import (
    BaseExportDataFunctionValidator,
)
from edu_rdm_integration.export_data.consts import (
    DELIMITER,
)
from edu_rdm_integration.models import (
    ExportingDataStage,
    ExportingDataSubStage,
    ExportingDataSubStageAttachment,
    ExportingDataSubStageStatus,
    ExportingDataSubStageUploaderClientLog,
)
from edu_rdm_integration.utils import (
    get_exporting_data_stage_attachment_path,
)


class BaseExportDataFunction(
    EntitiesMixin,
    WebEduLazySavingPredefinedQueueGlobalHelperFunction,
    metaclass=ABCMeta,
):
    """
    Базовый класс функций выгрузки данных для интеграции с "Региональная витрина данных".
    """

    def __init__(self, *args, stage: ExportingDataStage, model_ids: List[Union[int, str]], **kwargs):
        super().__init__(*args, entities=self.entities, model_ids=model_ids, **kwargs)

        self._sub_stage = ExportingDataSubStage.objects.create(
            stage=stage,
            function_id=self.uuid,
        )

        # Проставление подэтапа выгрузки
        self.entities[0].main_model_enum.model.objects.filter(pk__in=model_ids).update(
            exporting_sub_stage=self._sub_stage,
        )

        logger.info(f'{LOGS_DELIMITER * 3}{repr(self._sub_stage)} created.')

        self._file_name = f'rdm_{self.first_entity.key.lower()}.csv'

        self._data = {
            EntityLogOperation.CREATE: [],
            EntityLogOperation.UPDATE: [],
            EntityLogOperation.DELETE: [],
        }

        self._file_contents: Dict[int, Optional[Tuple[Optional[str], Optional[ExportingDataSubStageAttachment]]]] = {
            EntityLogOperation.CREATE: (None, None),
            EntityLogOperation.UPDATE: (None, None),
            EntityLogOperation.DELETE: (None, None),
        }

    def _prepare_helper_class(self) -> Type[BaseExportDataFunctionHelper]:
        """
        Возвращает класс помощника функции.
        """
        return BaseExportDataFunctionHelper

    def _prepare_validator_class(self) -> Type[BaseExportDataFunctionValidator]:
        """
        Возвращает класс валидатора функции.
        """
        return BaseExportDataFunctionValidator

    def _prepare_result_class(self) -> Type[BaseExportDataFunctionResult]:
        """
        Возвращает класс результата функции.
        """
        return BaseExportDataFunctionResult

    def _before_prepare(self, *args, **kwargs):
        """
        Выполнение действий функций системы.
        """
        self._sub_stage.status_id = ExportingDataSubStageStatus.IN_PROGRESS.key
        self._sub_stage.save()

        logger.info(f'{LOGS_DELIMITER * 3}change status {repr(self._sub_stage)}')

    def _prepare_record(self, entity_instance) -> List[str]:
        """
        Формирование списка строковых значений полей.
        """
        ordered_fields = self.first_entity.entity.get_ordered_fields()
        primary_key_fields = self.first_entity.entity.get_primary_key_fields()
        foreign_key_fields = self.first_entity.entity.get_foreign_key_fields()
        hashable_fields = self.first_entity.entity.get_hashable_fields()

        field_values = self.helper.prepare_record(
            entity_instance=entity_instance,
            ordered_fields=ordered_fields,
            primary_key_fields=primary_key_fields,
            foreign_key_fields=foreign_key_fields,
            hashable_fields=hashable_fields,
        )

        return field_values

    def _prepare_data(self):
        """
        Преобразование собранных данных в удобный для выгрузки вид.
        """
        logger.info(f'{LOGS_DELIMITER * 3}{self.__class__.__name__} prepare data..')

        for entity_instance in self.helper.cache.entity_instances:
            self._data[entity_instance.operation].append(
                self._prepare_record(
                    entity_instance=entity_instance,
                )
            )

            entity_instance.exporting_sub_stage = self._sub_stage

        for operation in EntityLogOperation.values.keys():
            entities = self._data.get(operation)

            if entities:
                logger.info(
                    f'{LOGS_DELIMITER * 3}prepared {len(entities)} records with status '
                    f'{slugify(EntityLogOperation.values.get(operation))}..'
                )

    def _prepare_files(self):
        """
        Формирование файлов для дальнейшей выгрузки.
        """
        logger.info(f'{LOGS_DELIMITER * 3}{self.__class__.__name__} prepare files..')

        for operation in EntityLogOperation.values.keys():
            records = self._data[operation]
            if records:
                title_record = (
                    f'{DELIMITER}'.join([
                        field.lower()
                        for field in self.first_entity.entity.get_ordered_fields()
                    ])
                )

                joined_records = (
                    '\n'.join([
                        title_record,
                        *[f'{DELIMITER}'.join(record) for record in records]]
                    )
                )

                sub_stage_attachment = ExportingDataSubStageAttachment(
                    exporting_data_sub_stage=self._sub_stage,
                    operation=operation,
                )

                file_path = get_exporting_data_stage_attachment_path(
                    instance=sub_stage_attachment,
                    filename=self._file_name,
                )

                sub_stage_attachment.attachment = default_storage.save(file_path, ContentFile(joined_records))

                self.do_on_save(sub_stage_attachment)

                self._file_contents[operation] = (file_path, sub_stage_attachment)

    def _send_files(self):
        """
        Отправка файлов в "Региональная витрина данных".
        """
        # TODO При старте проекта и инициализации приложения function_tools происходит поиск стратегий. При поиске
        #  возникает ошибка "Не произведена настройка клиента". Настройка производится в конфиге
        #  приложения regional_data_mart_integration. Нужно доработать механизм так, чтобы сборка стратегий запускалась
        #  после готовности всех приложений.

        logger.info(f'{LOGS_DELIMITER * 3}{self.__class__.__name__} send files..')

        requests_result = []

        for operation, (relative_file_path, sub_stage_attachment) in self._file_contents.items():
            if relative_file_path:
                if settings.RDM_UPLOADER_CLIENT_ENABLE_REQUEST_EMULATION:
                    logger.warning(
                        f'{LOGS_DELIMITER * 3}ATTENTION!!! REGIONAL DATA MART INTEGRATION REQUEST EMULATION ENABLED!'
                    )

                method = OPERATIONS_METHODS_MAP.get(operation)
                file_path = Path.joinpath(Path(settings.MEDIA_ROOT), relative_file_path)

                request = RegionalDataMartEntityRequest(
                    datamart_name=settings.RDM_UPLOADER_CLIENT_DATAMART_NAME,
                    table_name=self.first_entity.key.lower(),
                    method=method,
                    operation=OPERATIONS_URLS_MAP.get(operation),
                    parameters={},
                    headers={
                        'Content-Type': 'text/csv',
                    },
                    files=[],
                    data=file_path.open('rb').read(),
                )

                result = adapter.send(request)

                request_id = ''
                if not result.error:
                    if getattr(result.response, 'data', None):
                        request_id = json.loads(result.response.data)
                    elif result.response.headers.get('requestId'):
                        request_id = result.response.headers.get('requestId')

                file_upload_status = FileUploadStatusEnum.IN_PROGRESS if request_id else FileUploadStatusEnum.ERROR

                sub_stage_uploader_client_log = ExportingDataSubStageUploaderClientLog(
                    entry=result.log,
                    sub_stage=self._sub_stage,
                    attachment=sub_stage_attachment,
                    request_id=request_id,
                    file_upload_status=file_upload_status,
                    is_emulation=settings.RDM_UPLOADER_CLIENT_ENABLE_REQUEST_EMULATION,
                )

                self.do_on_save(sub_stage_uploader_client_log)

                if result.error:
                    logger.error(
                        f'{result.error}\nrequest - "{result.log.request}"\nresponse - "{result.log.response}"'
                    )

                    error = BaseExportDataError(
                        message=result.error,
                    )
                    self.result.append_entity(entity=error)

                    break
                else:
                    logger.info(
                        f'Response with {result.response.status_code} code and content {result.response.text}'
                    )

                requests_result.append(result)

    def _prepare(self, *args, **kwargs):
        """
        Выполнение действий функции.
        """
        if self.result.has_not_errors:
            if self.helper.cache.entity_instances:
                self._prepare_data()
                self._prepare_files()
                self._send_files()
            else:
                logger.info(f'{LOGS_DELIMITER * 3} no data for preparing.')

    def run(self, *args, **kwargs):
        """
        Выполнение действий функции с дальнейшим сохранением объектов в базу при отсутствии ошибок.
        """
        super().run(*args, **kwargs)

        if self.result.has_not_errors:
            self._sub_stage.status_id = ExportingDataSubStageStatus.FINISHED.key
        else:
            self._sub_stage.status_id = ExportingDataSubStageStatus.FAILED.key

        self._sub_stage.save()

        logger.info(f'{LOGS_DELIMITER * 3}change status {repr(self._sub_stage)}')
