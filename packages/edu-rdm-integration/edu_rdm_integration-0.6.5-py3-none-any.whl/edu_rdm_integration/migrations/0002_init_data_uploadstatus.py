# flake8: noqa
from django.db import (
    migrations,
)

from edu_rdm_integration.enums import (
    UploadStatusEnum,
)


def load_initial_data(apps, schema_editor):
    UploadStatus = apps.get_model('edu_rdm_integration', 'UploadStatus')

    statuses = []

    for code, description in UploadStatusEnum.values.items():
        status = UploadStatus(code=code, description=description)
        statuses.append(status)

    UploadStatus.objects.bulk_create(statuses)


def delete_all_data(apps, schema_editor):
    """Удаление всех данных из модели UploadStatus при откате миграции."""
    apps.get_model('regional_data_mart_integration', 'UploadStatus').objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('edu_rdm_integration', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_data, reverse_code=delete_all_data)
    ]
