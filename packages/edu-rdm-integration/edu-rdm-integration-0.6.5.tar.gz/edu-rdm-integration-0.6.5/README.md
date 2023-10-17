# Проект "Интеграция с Региональной витриной данных (РВД)"

Для интеграции с Региональной витриной данных был выделен отдельный пакет для использования его компонентов в различных 
продуктах. 

На текущий момент интеграция реализуется в рамках проектов Электронная школа (ЭШ) и Электронный колледж (ЭК).

## Описание концепции

Со стороны Минцифры предоставляется спецификация (ЕФТТ) с требованиями по формату и механизму выгрузки данных. 

Выбрана модель промежуточного хранения данных на стороне продукта, которые подлежат выгрузке. При помощи такого подхода,
можно обеспечить формирование не хранящихся в продукте данных и дальнейшее их обновление и удаление. Упрощается процесс 
поиска ошибок в данных, т.к. можно явно определить, в каких записях находятся ошибки и далее анализировать существующие 
данные в продуктах или функционал по формированию данных.

## Принцип работы

Весь процесс разделен на сбор и выгрузку данных. Выделяются следующие понятия:

Модель продукта
: Django-модель находящаяся в самом продукте. При помощи нее производится накапливание пользовательских данных;

Модель РВД
: Django-модель находящаяся в пакете РВД продукта. Из моделей РВД формируется схема БД, позволяющая хранить данные для 
дальнейшей выгрузки в нормализованном виде;

Сущность РВД
: Описание формата выгрузки данных в РВД в виде dataclass-а. Хранит в себе описание первичных, внешних ключей, 
обязательность и порядок полей.

На этапе сбора данных производится формирование данных моделей РВД на основе данных моделей продуктов. Существуют так 
называемые расчетные модели, для которых данные рассчитываются в процессе сбора.

Стоит обратить внимание, что сущности РВД могут содержать в себе данные из нескольких моделей РВД.

## Требования к окружению

Для работы требуется Python >=3.7. Так же в зависимостях есть внутренние пакеты:

- educommon;
- function-tools;
- m3-db-utils;
- uploader-client.

Версии всех пакетов уточнены в файлах с зависимостями.

## Разворачивание

Перед внедрением пакета в проект, необходимо убедиться, что:

- В проекте используется логирование из educommon;
- В проект внедрен function-tools;
- В проект внедрен m3-db-utils;
- В проект внедрен uploader-client. 

## Параметры конфигурационного файла

В разных проектах существуют различные способы добавления настроек, где-то через плагины, где-то напрямую в settings.py.
Будет рассмотрен подход указания настроек в settings.py и указания параметров в конфигурационном файле.

Для возможности конфигурирования необходимо проделать ряд действий:

- Определение значений по умолчанию настроек в settings.py:
    ```
    PROJECT_DEFAULT_CONFIG.update({
        # Настройки РВД
        ('rdm_general', 'EXPORT_ENTITY_ID_PREFIX'): '', # Дефолтное значение нужно изменить на специфическое системе
        ('rdm_general', 'COLLECT_CHUNK_SIZE'): 500,
        ('rdm_general', 'EXPORT_CHUNK_SIZE'): 500,
        ('rdm_transfer_task', 'MINUTE'): '0',
        ('rdm_transfer_task', 'HOUR'): '*/4',
        ('rdm_transfer_task', 'TRANSFER_TASK_DAY_OF_WEEK'): '*',
        ('rdm_transfer_task', 'TIMEDELTA'): 3600,
        ('rdm_transfer_task', 'ENTITIES'): '',
        ('rdm_upload_status_task', 'MINUTE'): '*/30',
        ('rdm_upload_status_task', 'HOUR'): '*',
        ('rdm_upload_status_task', 'DAY_OF_WEEK'): '*',
        ('uploader_client', 'URL'): 'http://localhost:8090',
        ('uploader_client', 'DATAMART_NAME'): '',
        ('uploader_client', 'REQUEST_RETRIES'): 10,
        ('uploader_client', 'REQUEST_TIMEOUT'): 10,
        ('uploader_client', 'ENABLE_REQUEST_EMULATION'): False,
    })
    ```
- Получение значений настроек из конфигурационного файла в settings.py:

    ```
    # Ссылка на каталог с файлами для загрузки
    UPLOADS = 'uploads'
  
    # =============================================================================
    # Интеграция с Региональной витриной данных (РВД)
    # =============================================================================
    
    # Префикс идентификаторов записей сущностей специфический для продукта
    RDM_EXPORT_ENTITY_ID_PREFIX = conf.get('rdm_general', 'EXPORT_ENTITY_ID_PREFIX') 
  
    # Количество записей моделей ЭШ обрабатываемых за одну итерацию сбора данных
    RDM_COLLECT_CHUNK_SIZE = conf.get_int('rdm_general', 'COLLECT_CHUNK_SIZE')
    
    # Количество записей моделей обрабатываемых за одну итерацию экспорта данных
    RDM_EXPORT_CHUNK_SIZE = conf.get_int('rdm_general', 'EXPORT_CHUNK_SIZE')
    
    # Настройка запуска периодической задачи выгрузки данных:
    RDM_TRANSFER_TASK_MINUTE = conf.get('rdm_transfer_task', 'MINUTE')
    RDM_TRANSFER_TASK_HOUR = conf.get('rdm_transfer_task', 'HOUR')
    RDM_TRANSFER_TASK_DAY_OF_WEEK = conf.get('rdm_transfer_task', 'DAY_OF_WEEK')
    RDM_TRANSFER_TASK_TIMEDELTA = conf.get_int('rdm_transfer_task', 'TIMEDELTA')
    # Сущности, по которым должен производиться сбор и выгрузка данных
    RDM_TRANSFER_TASK_ENTITIES = conf.get_tuple('rdm_transfer_task', 'ENTITIES') or ()
    
    # Настройка запуска периодической задачи статуса загрузки данных в витрину:
    RDM_UPLOAD_STATUS_TASK_MINUTE = conf.get('rdm_upload_status_task', 'MINUTE')
    RDM_UPLOAD_STATUS_TASK_HOUR = conf.get('rdm_upload_status_task', 'HOUR')
    RDM_UPLOAD_STATUS_TASK_DAY_OF_WEEK = conf.get('rdm_upload_status_task', 'DAY_OF_WEEK')
  
    # Настройка запуска периодической задачи поиска зависших этапов экспорта:
    RDM_CHECK_SUSPEND_TASK_MINUTE = conf.get('rdm_check_suspend_task', 'MINUTE')
    RDM_CHECK_SUSPEND_TASK_HOUR = conf.get('rdm_check_suspend_task', 'HOUR')
    RDM_CHECK_SUSPEND_TASK_DAY_OF_WEEK = conf.get('rdm_check_suspend_task', 'DAY_OF_WEEK')
    RDM_CHECK_SUSPEND_TASK_TIMEDELTA = conf.get_int('rdm_check_suspend_task', 'TIMEDELTA')
    
    # Загрузка данных в Региональную витрину данных (РВД)
    # Адрес витрины (schema://host:port)
    RDM_UPLOADER_CLIENT_URL = conf.get('uploader_client', 'URL')
    
    # Мнемоника Витрины
    RDM_UPLOADER_CLIENT_DATAMART_NAME = conf.get('uploader_client', 'DATAMART_NAME')
    
    # Количество повторных попыток запроса
    RDM_UPLOADER_CLIENT_REQUEST_RETRIES = conf.get_int('uploader_client', 'REQUEST_RETRIES')
    
    # Таймаут запроса, сек
    RDM_UPLOADER_CLIENT_REQUEST_TIMEOUT = conf.get_int('uploader_client', 'REQUEST_TIMEOUT')
    
    # Включить эмуляцию отправки запросов
    RDM_UPLOADER_CLIENT_ENABLE_REQUEST_EMULATION = conf.get_bool('uploader_client', 'ENABLE_REQUEST_EMULATION')
    
    ```
  
    Перечень настроек в settings.py указан в таблице ниже.
    
    | Название настройки в settings                | Описание                                                                                                                           | Значение по умолчанию   |
    |----------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|-------------------------|
    | UPLOADS                                      | Основная директория в MEDIA, в которой будет создана директория edu_rdm_integration  для сохранения файлов для дальнейшей выгрузки | 500                     |
    | RDM_COLLECT_CHUNK_SIZE                       | Количество записей моделей обрабатываемых за одну итерацию сбора данных                                                            | 500                     |
    | RDM_EXPORT_CHUNK_SIZE                        | Количество записей моделей обрабатываемых за одну итерацию экспорта                                                                | 500                     |
    | RDM_UPLOADER_CLIENT_URL                      | Адрес витрины (schema://host:port)                                                                                                 | 'http://localhost:8090' |
    | RDM_UPLOADER_CLIENT_DATAMART_NAME            | Мнемоника Витрины                                                                                                                  | 'test'                  |
    | RDM_UPLOADER_CLIENT_REQUEST_RETRIES          | Количество повторных попыток запроса                                                                                               | 10                      |
    | RDM_UPLOADER_CLIENT_REQUEST_TIMEOUT          | Таймаут запроса, сек                                                                                                               | 10                      |
    | RDM_UPLOADER_CLIENT_ENABLE_REQUEST_EMULATION | Включить эмуляцию отправки запросов                                                                                                | True                    |
    | RDM_TRANSFER_TASK_MINUTE                     | Настройка запуска периодической задачи выгрузки данных. Минута                                                                     | '0'                     |
    | RDM_TRANSFER_TASK_HOUR                       | Настройка запуска периодической задачи выгрузки данных. Час                                                                        | '*/4'                   |
    | RDM_TRANSFER_TASK_DAY_OF_WEEK                | Настройка запуска периодической задачи выгрузки данных. День недели                                                                | '*'                     |
    | RDM_TRANSFER_TASK_TIMEDELTA                  | Дельта между предыдущим и следующим запуском периодической задачи в секундах                                                       | 3600                    |
    | RDM_TRANSFER_TASK_ENTITIES                   | Сущности, по которым должен производиться сбор и выгрузка данных                                                                   | ''                      |
    | RDM_UPLOAD_STATUS_TASK_MINUTE                | Настройка запуска периодической задачи статуса загрузки данных в витрину. Минута                                                   | '*/30'                  |
    | RDM_UPLOAD_STATUS_TASK_HOUR                  | Настройка запуска периодической задачи статуса загрузки данных в витрину. Час                                                      | '*'                     |
    | RDM_UPLOAD_STATUS_TASK_DAY_OF_WEEK           | Настройка запуска периодической задачи статуса загрузки данных в витрину. День недели                                              | '*'                     |
    | RDM_CHECK_SUSPEND_TASK_STAGE_TIMEOUT         | Дельта для определения зависшего подэтапа. Минута                                                                                  | 120                     |
    


- В дефолтный конфиг проекта необходимо добавить:

    ```
    # Общие настройки интеграции с РВД
    [rmd_general]
    # Префикс идентификаторов записей сущностей специфический для продукта. Указывается в settings.py и не должен 
    # изменяться. Возможность изменения через конфигурационный файл оставлена для экстренных случаев.
    # EXPORT_ENTITY_ID_PREFIX = 
    # Количество записей моделей обрабатываемых за одну итерацию экспорта данных
    EXPORT_CHUNK_SIZE = 500
    # Количество записей моделей ЭШ обрабатываемых за одну итерацию сбора данных
    COLLECT_CHUNK_SIZE = 500
    
    # Настройка запуска периодической задачи выгрузки данных
    [rdm_transfer_task]
    MINUTE=*/2
    HOUR=*
    DAY_OF_WEEK=*
    # Дельта между прошлым и текущим запуском, сек
    TIMEDELTA=120
    # Сущности, по которым должен производиться сбор и выгрузка данных. Перечисляются через запятую без пробелов.
    ENTITIES =
    
    # Настройка запуска периодической задачи статуса загрузки данных в витрину
    [rdm_upload_status_task]
    MINUTE=*/2
    HOUR=*
    DAY_OF_WEEK=*
  
    # Настройка запуска периодической задачи поиска зависших этапов экспорта
    [rdm_check_suspend_task]
    MINUTE=*/10
    HOUR=*
    DAY_OF_WEEK=*
    # Дельта для определения зависшего подэтапа, мин
    STAGE_TIMEOUT=120
    
    [uploader_client]
    # Адрес витрины
    URL = http://localhost:8090
    # Мнемоника Витрины
    DATAMART_NAME = test
    # Количество повторных попыток запроса
    REQUEST_RETRIES = 10
    # Таймаут запроса, сек
    REQUEST_TIMEOUT = 10
    # Включить эмуляцию отправки запросов
    ENABLE_REQUEST_EMULATION = True
    ```

На основе дефолтного конфига произвести конфигурирование приложений.

## Сборка и распространение

Сборка пакета производится при помощи [Job-а в Jenkins M3.build_dist](http://jenkins.py.bars.group/view/PY/job/M3.packages/job/M3.build_dist/).

Пакет выкладывается в глобальный [PYPI](https://pypi.org/project/edu-rdm-integration/) и во внутренний [Nexus](http://nexus.py.bars.group/#browse/browse:pypi-edu-private:edu-rdm-integration) 

## Документация

С документацией можно ознакомиться по ссылке http://docs.py.bars.group/edu-rdm-integration/
