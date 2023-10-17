import os
from datetime import (
    datetime,
    time,
    timedelta,
)
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    NamedTuple,
    Union,
)

from django.conf import (
    settings,
)
from django.db.models import (
    Model,
)

from edu_rdm_integration.apps import (
    EduRDMIntegrationConfig,
)
from edu_rdm_integration.consts import (
    ACADEMIC_YEAR,
)


if TYPE_CHECKING:
    from edu_rdm_integration.models import (
        BaseEntityModel,
    )


def get_exporting_data_stage_attachment_path(instance, filename):
    """Возвращает путь до файла-вложения в этап выгрузки данных сущности.

    Args:
        instance: объект ExportingDataStage
        filename: имя загружаемого файла

    Returns:
        Строковое представление пути
    """
    datetime_now = datetime.now()

    return os.path.join(
        settings.UPLOADS,
        EduRDMIntegrationConfig.label,
        datetime_now.strftime('%Y/%m/%d'),
        instance.exporting_data_sub_stage.__class__.__name__.lower(),
        str(instance.exporting_data_sub_stage_id),
        str(instance.operation),
        filename,
    )


def update_fields(
    entity: 'BaseEntityModel',
    field_values: Dict[str, Any],
    mapping: Dict[str, str]
) -> None:
    """Обновление значений полей сущности по измененным полям модели.

    :param entity: Выгружаемая сущность
    :param field_values: Словарь с измененными данными модели
    :param mapping: Словарь маппинга полей модели к полям сущности
    """
    for model_field, entity_field in mapping.items():
        if model_field in field_values:
            setattr(entity, entity_field, field_values[model_field])


def set_entity_field_by_model_object(
    entity: 'BaseEntityModel',
    model_object: Union[Model, NamedTuple],
    mapping: Dict[str, str]
) -> None:
    """Обновление значений полей сущности по измененным полям модели.

    Args:
        entity: Выгружаемая сущность;
        model_object: Объект модели с измененными полями;
        mapping: Словарь маппинга полей модели к полям сущности
    """
    for model_field, entity_field in mapping.items():
        if hasattr(model_object, model_field):
            setattr(entity, entity_field, getattr(model_object, model_field))


def get_isoformat_timezone():
    """Возвращает временную зонну в ISO представлении."""
    return datetime.now().astimezone().isoformat()[-6:]


def split_by_academic_years(start_date: datetime, end_date: datetime) -> List[tuple]:
    """Разбивает исходный интервал из команды по учебным годам."""
    academic_year_end_date = datetime(
        start_date.year, ACADEMIC_YEAR['end_month'], ACADEMIC_YEAR['end_day'],

    )
    if academic_year_end_date <= start_date:
        academic_year_end_date = datetime(
            academic_year_end_date.year + 1,
            ACADEMIC_YEAR['end_month'],
            ACADEMIC_YEAR['end_day'],
            time.max.hour,
            time.max.minute,
            time.max.second,
        )

    splitted_interval = []
    splitted_interval.append(start_date)

    while start_date < academic_year_end_date < end_date:
        splitted_interval.append(academic_year_end_date)

        academic_year_end_date = datetime(
            academic_year_end_date.year + 1,
            ACADEMIC_YEAR['end_month'],
            ACADEMIC_YEAR['end_day'],
            time.max.hour,
            time.max.minute,
            time.max.second,
        )
        academic_year_start_date = datetime(
            academic_year_end_date.year - 1,
            ACADEMIC_YEAR['start_month'],
            ACADEMIC_YEAR['start_day'],
            time.min.hour,
            time.min.minute,
            time.min.second,
        )

        splitted_interval.append(academic_year_start_date)

    splitted_interval.append(end_date)

    iter_interval = iter(splitted_interval)
    intervals = [*zip(iter_interval, iter_interval)]

    return intervals


def split_interval_by_delta(start_date: datetime, end_date: datetime, days_delta: int) -> List[tuple]:
    """Разбивает учебный год на интервалы по дельте."""
    subinterval_end = start_date + timedelta(days=days_delta)

    splitted_interval = []
    splitted_interval.append(start_date)

    # В данном цикле проверять нужно именно даты чтобы не получилась ситуация что две одинаковые даты
    # попадут в интервалы и различаться будут лишь временем (минимальная дельта 1 день т.е. 24 часа)
    while start_date.date() < subinterval_end.date() < end_date.date():
        splitted_interval.append(subinterval_end)
        subinterval_start = subinterval_end + timedelta(days=1)
        splitted_interval.append(subinterval_start)
        subinterval_end = subinterval_end + timedelta(days=days_delta + 1)

    splitted_interval.append(end_date)

    iter_interval = iter(splitted_interval)
    intervals = [*zip(iter_interval, iter_interval)]

    return intervals
