# Ссылка на каталог с файлами для загрузки
UPLOADS = 'uploads'

# Префикс идентификаторов записей сущностей специфический для продукта. Должен быть заполнен в продуктах в settings.py
# или в конфигурационном файле
RDM_EXPORT_ENTITY_ID_PREFIX = ''

# Количество записей моделей ЭШ обрабатываемых за одну итерацию сбора данных
RDM_COLLECT_CHUNK_SIZE = 500

# Количество записей моделей обрабатываемых за одну итерацию экспорта
RDM_EXPORT_CHUNK_SIZE = 500


# Загрузка данных в Региональную витрину данных (РВД)
# Адрес витрины (schema://host:port)
RDM_UPLOADER_CLIENT_URL = 'http://localhost:8090'

# Мнемоника Витрины
RDM_UPLOADER_CLIENT_DATAMART_NAME = 'test'

# Количество повторных попыток запроса
RDM_UPLOADER_CLIENT_REQUEST_RETRIES = 10

# Таймаут запроса, сек
RDM_UPLOADER_CLIENT_REQUEST_TIMEOUT = 10

# Включить эмуляцию отправки запросов
RDM_UPLOADER_CLIENT_ENABLE_REQUEST_EMULATION = True


# Настройка запуска периодической задачи выгрузки данных:
RDM_TRANSFER_TASK_MINUTE = '0'
RDM_TRANSFER_TASK_HOUR = '*/4'
RDM_TRANSFER_TASK_DAY_OF_WEEK = '*'
RDM_TRANSFER_TASK_TIMEDELTA = 3600

# Настройка запуска периодической задачи статуса загрузки данных в витрину:
RDM_UPLOAD_STATUS_TASK_MINUTE = '*/30'
RDM_UPLOAD_STATUS_TASK_HOUR = '*'
RDM_UPLOAD_STATUS_TASK_DAY_OF_WEEK = '*'
