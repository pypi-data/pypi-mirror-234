from datetime import (
    date,
    datetime,
    time,
)
from typing import (
    TYPE_CHECKING,
)

from django.core.management.base import (
    BaseCommand,
)

from edu_rdm_integration.collect_data.collect import (
    BaseCollectModelsData,
)
from edu_rdm_integration.consts import (
    DATETIME_FORMAT,
)
from edu_rdm_integration.export_data.export import (
    BaseExportEntitiesData,
)
from edu_rdm_integration.models import (
    RegionalDataMartEntityEnum,
    RegionalDataMartModelEnum,
)


if TYPE_CHECKING:
    from django.core.management.base import (
        CommandParser,
    )


class BaseCollectModelDataCommand(BaseCommand):
    """
    Базовая команда для выполнения сбора данных моделей РВД.
    """

    def add_arguments(self, parser: 'CommandParser'):
        """
        Добавление параметров.
        """
        models = ', '.join([
            f'{key} - {value.title}'
            for key, value in RegionalDataMartModelEnum.get_enum_data().items()
        ])
        models_help_text = (
            f'Значением параметра является перечисление моделей РВД, для которых должен быть произведен сбор данных. '
            f'Перечисление моделей:\n{models}. Если модели не указываются, то сбор данных производится для всех '
            f'моделей. Модели перечисляются через запятую без пробелов.'
        )
        parser.add_argument(
            '--models',
            action='store',
            dest='models',
            type=lambda e: e.split(','),
            help=models_help_text,
        )

        parser.add_argument(
            '--logs_period_started_at',
            action='store',
            dest='logs_period_started_at',
            type=lambda started_at: datetime.strptime(started_at, DATETIME_FORMAT),
            default=datetime.combine(date.today(), time.min),
            help=(
                'Дата и время начала периода обрабатываемых логов. Значение предоставляется в формате '
                '"дд.мм.гггг чч:мм:сс". По умолчанию, сегодняшний день, время 00:00:00.'
            ),
        )

        parser.add_argument(
            '--logs_period_ended_at',
            action='store',
            dest='logs_period_ended_at',
            type=lambda ended_at: datetime.strptime(ended_at, DATETIME_FORMAT),
            default=datetime.combine(date.today(), time.max),
            help=(
                'Дата и время конца периода обрабатываемых логов. Значение предоставляется в формате '
                '"дд.мм.гггг чч:мм:сс". По умолчанию, сегодняшний день, время 23:59:59.'
            ),
        )

    def _prepare_collect_models_data_class(self, *args, **kwargs) -> BaseCollectModelsData:
        """Возвращает объект класса сбора данных моделей РВД."""
        raise NotImplementedError

    def handle(self, *args, **kwargs):
        """
        Выполнение действий команды.
        """
        collect_models_data = self._prepare_collect_models_data_class(*args, **kwargs)
        collect_models_data.collect()


class BaseExportEntityDataCommand(BaseCommand):
    """
    Базовая команда для выполнения выгрузки данных сущностей РВД за указанный период.
    """

    def add_arguments(self, parser: 'CommandParser'):
        """
        Добавление параметров.
        """
        entities = ', '.join([
            f'{key} - {value.title}'
            for key, value in RegionalDataMartEntityEnum.get_enum_data().items()
        ])
        entities_help_text = (
            f'Значением параметра является перечисление сущностей РВД, для которых должена быть произведена выгрузка '
            f'данных. Перечисление сущностей:\n{entities}. Если сущности не указываются, то выгрузка данных '
            f'производится для всех сущностей. Сущности перечисляются через запятую без пробелов.'
        )
        parser.add_argument(
            '--entities',
            action='store',
            dest='entities',
            type=lambda e: e.split(','),
            help=entities_help_text,
        )

        parser.add_argument(
            '--period_started_at',
            action='store',
            dest='period_started_at',
            type=lambda started_at: datetime.strptime(started_at, DATETIME_FORMAT),
            default=datetime.combine(date.today(), time.min),
            help=(
                'Дата и время начала периода сбора записей моделей РВД. Значение предоставляется в формате '
                '"дд.мм.гггг чч:мм:сс". По умолчанию, сегодняшний день, время 00:00:00.'
            ),
        )

        parser.add_argument(
            '--period_ended_at',
            action='store',
            dest='period_ended_at',
            type=(
                lambda ended_at: datetime.strptime(ended_at, DATETIME_FORMAT).replace(microsecond=time.max.microsecond)
            ),
            default=datetime.combine(date.today(), time.max),
            help=(
                'Дата и время конца периода сбора записей моделей РВД. Значение предоставляется в формате '
                '"дд.мм.гггг чч:мм:сс". По умолчанию, сегодняшний день, время 23:59:59.'
            ),
        )
        parser.add_argument(
            '--task_id',
            action='store',
            dest='task_id',
            type=str,
            default=None,
            help='task_id для поиска асинхронной задачи',
        )
        parser.add_argument(
            '--no-update-modified',
            dest='update_modified',
            action='store_false',
            default=True,
            help='Не обновлять поле modified моделей',
        )

    def _prepare_export_entities_data_class(self, *args, **kwargs) -> BaseExportEntitiesData:
        """Возвращает объект класса экспорта данных сущностей РВД."""
        raise NotImplementedError

    def handle(self, *args, **kwargs):
        """
        Выполнение действий команды.
        """
        export_entities_data = self._prepare_export_entities_data_class(*args, **kwargs)
        export_entities_data.export()


class BaseCollectModelsDataByGeneratingLogsCommand(BaseCollectModelDataCommand):
    """
    Команда сбора данных моделей РВД на основе существующих в БД данных моделей ЭШ.

    Можно регулировать, для каких моделей должен быть произведен сбор данных, и период, за который должны
    быть собраны логи. Логи формируются в процессе выполнения команды при помощи генератора логов LogGenerator для
    указанной модели.
    """

    # flake8: noqa: A003
    help = 'Команда сбора данных моделей РВД на основе существующих в БД данных моделей продукта'

    def add_arguments(self, parser: 'CommandParser'):
        """
        Добавление параметров.
        """
        super().add_arguments(parser=parser)

        parser.add_argument(
            '--logs_sub_period_days',
            action='store',
            dest='logs_sub_period_days',
            type=int,
            default=0,
            help=(
                'Размер подпериодов, на которые будет разбит основной период, в днях. По умолчанию, '
                '0 - разбиение на подпериоды отключено.'
            ),
        )

        parser.add_argument(
            '--school_ids',
            action='store',
            dest='school_ids',
            type=lambda v: tuple(map(int, v.split(','))),
            default=(),
            help='Школы, для которых производится выгрузка.',
        )
