from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from typing import (
    Tuple,
)

from educommon.integration_entities.entities import (
    BaseEntity,
)


@dataclass
class AddressEntity(BaseEntity):
    """Сущность РВД 'Адреса'."""

    # Имена полей объявляются как константы, чтобы можно было выводить списки полей
    ID = 'id'
    USE_ADDRESS = 'use_address'
    TYPE_ADDRESS = 'type_address'
    TEXT = 'text'
    CITY = 'city'
    STATE = 'state'
    DISTRICT = 'district'
    POSTAL_CODE = 'postal_code'
    COUNTRY = 'country'
    START_DATETIME = 'start_datetime'
    FLAT = 'flat'
    BUILDING = 'building'
    HOUSE = 'house'
    STREET = 'street'
    CREATE_DATETIME = 'create_datetime'
    SEND_DATETIME = 'send_datetime'
    END_DATETIME = 'end_datetime'

    id: str
    use_address: int
    type_address: int
    text: str
    city: str
    state: str
    district: str
    postal_code: str
    country: str
    start_datetime: datetime
    flat: str
    building: str
    house: str
    street: str
    create_datetime: datetime
    send_datetime: datetime
    end_datetime: datetime = None

    @classmethod
    def get_required_fields(cls) -> Tuple[str, ...]:
        """Возвращает кортеж обязательных полей."""
        return cls.ID, cls.TYPE_ADDRESS, cls.TEXT, cls.CREATE_DATETIME, cls.SEND_DATETIME

    @classmethod
    def get_hashable_fields(cls) -> Tuple[str, ...]:
        """Возвращает кортеж полей, которые необходимо деперсонализировать (хэшировать)."""
        return tuple()

    @classmethod
    def get_primary_key_fields(cls) -> Tuple[str, ...]:
        """
        Возвращает кортеж полей первичного ключа.
        """
        return cls.ID,

    @classmethod
    def get_foreign_key_fields(cls) -> Tuple[str, ...]:
        """
        Возвращает кортеж полей внешних ключей.
        """
        return ()

    @classmethod
    def get_ordered_fields(cls) -> Tuple[str, ...]:
        return (
            cls.ID, cls.USE_ADDRESS, cls.TYPE_ADDRESS, cls.TEXT, cls.CITY, cls.DISTRICT, cls.STATE, cls.POSTAL_CODE,
            cls.COUNTRY, cls.START_DATETIME, cls.END_DATETIME, cls.FLAT, cls.BUILDING, cls.HOUSE, cls.STREET,
            cls.CREATE_DATETIME, cls.SEND_DATETIME
        )


@dataclass
class AddressOrganisationEntity(BaseEntity):
    """Сущность РВД 'Адреса'."""

    # Имена полей объявляются как константы, чтобы можно было выводить списки полей
    ADDRESS_ID = 'address_id'
    ORGANISATION_ID = 'organisation_id'
    CREATE_DATETIME = 'create_datetime'
    SEND_DATETIME = 'send_datetime'

    address_id: str
    organisation_id: str
    create_datetime: datetime
    send_datetime: datetime

    @classmethod
    def get_required_fields(cls) -> Tuple[str, ...]:
        """Возвращает кортеж обязательных полей."""
        return cls.ADDRESS_ID, cls.ORGANISATION_ID, cls.CREATE_DATETIME, cls.SEND_DATETIME

    @classmethod
    def get_hashable_fields(cls) -> Tuple[str, ...]:
        """Возвращает кортеж полей, которые необходимо деперсонализировать (хэшировать)."""
        return tuple()

    @classmethod
    def get_primary_key_fields(cls) -> Tuple[str, ...]:
        """
        Возвращает кортеж полей первичного ключа.
        """
        return cls.ADDRESS_ID, cls.ORGANISATION_ID,

    @classmethod
    def get_foreign_key_fields(cls) -> Tuple[str, ...]:
        """
        Возвращает кортеж полей внешних ключей.
        """
        return ()

    @classmethod
    def get_ordered_fields(cls) -> Tuple[str, ...]:
        return cls.ADDRESS_ID, cls.ORGANISATION_ID, cls.CREATE_DATETIME, cls.SEND_DATETIME,


@dataclass
class TelecomEntity(BaseEntity):
    """Сущность РВД "Контактные данные"."""

    # Имена полей объявляются как константы, чтобы можно было выводить списки полей
    ID = 'id'
    TYPE_CONTACT = 'type_contact'
    VALUE_TYPE = 'value_type'
    USE_COD = 'use_cod'
    RANK = 'rank'
    START_DATETIME = 'start_datetime'
    END_DATETIME = 'end_datetime'
    CREATE_DATETIME = 'create_datetime'
    SEND_DATETIME = 'send_datetime'

    id: str
    type_contact: int
    value_type: str
    use_cod: int
    start_datetime: datetime
    create_datetime: datetime
    send_datetime: datetime

    # Данные для полей не собираются
    rank: int = None
    end_datetime: datetime = None

    @classmethod
    def get_ordered_fields(cls) -> Tuple[str, ...]:
        """
        Возвращает кортеж полей в правильном порядке.
        """
        return (cls.ID, cls.TYPE_CONTACT, cls.VALUE_TYPE, cls.USE_COD, cls.RANK,
                cls.START_DATETIME, cls.END_DATETIME, cls.CREATE_DATETIME, cls.SEND_DATETIME,)

    @classmethod
    def get_primary_key_fields(cls) -> Tuple[str, ...]:
        """
        Возвращает кортеж полей первичного ключа.
        """
        return cls.ID,

    @classmethod
    def get_foreign_key_fields(cls) -> Tuple[str, ...]:
        """
        Возвращает кортеж полей внешних ключей.
        """
        return ()

    @classmethod
    def get_required_fields(cls) -> Tuple[str, ...]:
        """
        Возвращает кортеж обязательных полей.
        """
        return cls.ID, cls.CREATE_DATETIME, cls.SEND_DATETIME,

    @classmethod
    def get_hashable_fields(cls) -> Tuple[str, ...]:
        """Возвращает кортеж полей, которые необходимо деперсонализировать (хэшировать)."""
        return tuple()


@dataclass
class OrganisationsEntity(BaseEntity):
    """
    Сущность РВД "Организации".
    """

    ID = 'id'
    ROSOBR_ID = 'rosobr_id'
    OGRN = 'ogrn'
    OKPO = 'okpo'
    INN = 'inn'
    KPP = 'kpp'
    ACTIVE = 'active'
    OKPF = 'okpf'
    OKFS = 'okfs'
    OKOGU = 'okogu'
    OKATO  = 'okato'
    OKTMO = 'oktmo'
    NAME = 'name'
    PARTOF_ID = 'partof_id'
    EXECUTIVE_NAME = 'executive_name'
    EXECUTIVE_POSITION = 'executive_position'
    MODIFIED = 'modified'
    CREATE_DATETIME = 'create_datetime'
    SEND_DATETIME = 'send_datetime'
    PHONE = 'phone'

    id: str
    rosobr_id: str
    ogrn: int
    okpo: str
    inn: str
    kpp: str
    active: bool
    okpf: str
    okfs: int
    okogu: str
    okato: str
    oktmo: str
    name: str
    partof_id: str
    executive_name: str
    executive_position: str
    modified: datetime
    create_datetime: datetime
    send_datetime: datetime
    phone: str

    @classmethod
    def get_ordered_fields(cls) -> Tuple[str, ...]:
        """
        Возвращает кортеж полей в правильном порядке.
        """
        return (
            cls.ID,
            cls.ROSOBR_ID,
            cls.OGRN,
            cls.OKPO,
            cls.INN,
            cls.KPP,
            cls.ACTIVE,
            cls.OKPF,
            cls.OKFS,
            cls.OKOGU,
            cls.OKATO,
            cls.OKTMO,
            cls.NAME,
            cls.PARTOF_ID,
            cls.EXECUTIVE_NAME,
            cls.EXECUTIVE_POSITION,
            cls.PHONE,
            cls.CREATE_DATETIME,
            cls.SEND_DATETIME,
        )

    @classmethod
    def get_required_fields(cls) -> Tuple[str, ...]:
        """
        Возвращает кортеж обязательных полей.
        """
        return (
            cls.ID,
            cls.ROSOBR_ID,
            cls.OGRN,
            cls.INN,
            cls.KPP,
            cls.OKPF,
            cls.OKFS,
            cls.OKOGU,
            cls.OKATO,
            cls.OKTMO,
            cls.NAME,
            cls.EXECUTIVE_NAME,
            cls.EXECUTIVE_POSITION,
            cls.PHONE,
            cls.CREATE_DATETIME,
            cls.SEND_DATETIME,
        )

    @classmethod
    def get_primary_key_fields(cls) -> Tuple[str, ...]:
        """
        Возвращает кортеж полей первичного ключа.
        """
        return cls.ID,

    @classmethod
    def get_foreign_key_fields(cls) -> Tuple[str, ...]:
        """
        Возвращает кортеж полей внешних ключей.
        """
        return cls.PARTOF_ID,

    @classmethod
    def get_hashable_fields(cls) -> Tuple[str, ...]:
        """
        Возвращает кортеж полей, которые необходимо деперсонализировать (хэшировать).
        """
        return ()
