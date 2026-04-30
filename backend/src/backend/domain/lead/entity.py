from dataclasses import dataclass, field
from uuid import UUID

from src.backend.domain.lead.value_objects.contact.value_object import Contact
from src.backend.domain.lead.value_objects.field_type.value_object import FieldType
from src.backend.domain.lead.value_objects.field_value.value_objects import FieldValue
from src.backend.domain.lead.value_objects.lead_name.value_object import LeadName
from src.backend.domain.shared.entity import BaseEntity
from src.backend.domain.shared.mixins import TimeActionMixin

@dataclass
class LeadCustomFieldEnum(BaseEntity):
    """
    Представляет одно значение перечисления для кастомного поля.

    Attributes:
        custom_field_id: Идентификатор связанного кастомного поля
        value: Значение опции
    """
    custom_field_id: UUID
    value: str

    @classmethod
    def create(
            cls,
            custom_field_id: UUID,
            value: str,
    ):
        """
        Создает новую опцию перечисления.

        Args:
            custom_field_id: кастомного поля
            value: Значение опции

        Returns:
            Созданный объект опции
        """
        return cls(
            custom_field_id=custom_field_id,
            value=value,
        )

@dataclass
class LeadCustomField(BaseEntity,TimeActionMixin, LeadCustomFieldEnum):
    """
    Представляет кастомное поле лида.

    Attributes:
        name: название поля
        type: тип поля
        enums: список возможных значений для select-полей
    """
    name: LeadName
    type: FieldType
    enums: list[LeadCustomFieldEnum] = field(default_factory=list)
    is_deleted: bool = field(default=False)


    @classmethod
    def create(
            cls,
            name:str,
            type:FieldType,
    ):
        """
        Создает новое кастомное поле.

        Args:
            name: название поля
            type: тип поля

        Returns:
            LeadCustomField: созданный объект
        """
        return cls(
            name=LeadName(name),
            type=type,
        )

    def delete(self):
        self.is_deleted = True
        self.touch()

    def add_enum(
            self,
            value: str
    ) -> None:
        if not self.type.is_select:
            raise
        if any(e.value == value for e in self.enums):
            raise
            # if not self.type in [FieldType.select_many, FieldType.select_one]:
        #     raise
        new_enum = LeadCustomFieldEnum.create(self.id, value)
        self.enums.append(new_enum)
        self.touch()

    def remove_enum(
            self,
            enum_id: UUID
    ):
        """
        Удаляет значение перечисления.

        Args:
            enum_id: идентификатор опции
        """
        self.enums = [e for e in self.enums if e.id == enum_id]
        self.touch()

    def rename(
            self,
            name: str
    ):
        """
        Переименовывает поле.

        Args:
            name: новое название
        """
        self.name = LeadName(name)
        self.touch()


@dataclass
class LeadCustomFieldValue(BaseEntity):
    """
    Значение кастомного поля для конкретного лида.

    Attributes:
        custom_field_id: кастомного поля
        lead_id: ID лида
        value: значение поля
    """
    custom_field_id: UUID
    lead_id: UUID
    value: FieldValue

    @classmethod
    def create(
            cls,
            custom_field_id: UUID,
            lead_id: UUID,
            value: FieldValue,
    ):
        """
        Создает значение кастомного поля.

        Args:
            custom_field_id: ID поля
            lead_id: ID лида
            value: значение

        Returns:
            LeadCustomFieldValue — созданный объект
        """
        return cls(
            custom_field_id=custom_field_id,
            lead_id=lead_id,
            value=value
        )


@dataclass
class Lead(BaseEntity,TimeActionMixin, LeadCustomFieldValue):
    """
    Представляет лида.

    Attributes:
        name: имя лида
        contact: контактная информация
        is_delete: флаг удаления
        assign_to: назначенный пользователь
        custom_values: LeadCustomFieldValue — список кастомных значений
    """
    name: LeadName
    contact: Contact
    is_delete: bool = field(default=False)
    assign_to: UUID | None = None
    funnel_id: UUID | None = None
    custom_values: list[LeadCustomFieldValue] = field(default_factory=list)

    def set_custom_value(
            self,
            custom_field: LeadCustomField,
            value: FieldValue
    ):
        custom_field.type.validate_value(value)

        if value.enum_id is not None:
            valid_enum_ids = {e.id for e in custom_field.enums}
            if value.enum_id not in valid_enum_ids:
                raise

        if custom_field.type.is_multi:
            pass
        else:
            pass

        self.touch()

    def _add_multi_value(
            self,
            custom_field_id: UUID,
            value: FieldValue
    ):
        existing = self._find_value(custom_field_id, value.enum_id)
        if existing is not None:
            return
        self.custom_values.append(
            LeadCustomFieldValue.create(
                custom_field_id=custom_field_id,
                value=value,
                lead_id=self.id
            )
        )

    def _add_single_value(
            self,
            custom_field_id: UUID,
            value: FieldValue
    ):
        existing = self._find_value(custom_field_id)
        if existing is not None:
            existing.value = value
            return
        self.custom_values.append(
            LeadCustomFieldValue.create(
                custom_field_id=custom_field_id,
                value=value,
                lead_id=self.id
            )
        )


    # def set_custom_value(
    #         self,
    #         custom_field: LeadCustomField,
    #         value: FieldValue,
    # ):
    #     """
    #     Устанавливает значение кастомного поля.
    #
    #     Args:
    #         custom_field: Поле
    #         value: Значение
    #
    #     Raises:
    #         Exception: Если значение не подходит для поля
    #     """
    #     if custom_field.type.select_many:
    #         if value.enum_id is not None:
    #             if not value.enum_id in [e.id for e in custom_field.enums]:
    #                 raise
    #             existing = self._find_value(custom_field.id)
    #             if not value.enum_id in [e.id for e in custom_field.enums]:
    #                 raise
    #             if not existing:
    #                 existing.value = value
    #                 self.custom_values.append(
    #                     LeadCustomFieldValue.create(
    #                         custom_field_id=custom_field.id,
    #                         value=value,
    #                         lead_id=self.id
    #                     )
    #                 )
    #             else:
    #                 raise
    #
    #
    #         elif custom_field.type.text and value.value_text is not None:
    #             existing = self._find_value(custom_field.id)
    #             if not value.enum_id in [e.id for e in custom_field.enums]:
    #                 raise
    #             if existing:
    #                 existing.value = value
    #             else:
    #                 self.custom_values.append(
    #                     LeadCustomFieldValue.create(
    #                         custom_field_id=custom_field.id,
    #                         value=value,
    #                         lead_id=self.id
    #                     )
    #                 )
    #
    #         elif custom_field.type.boolean and value.value_boolean is not None:
    #             existing = self._find_value(custom_field.id)
    #             if not value.enum_id in [e.id for e in custom_field.enums]:
    #                 raise
    #             if existing:
    #                 existing.value = value
    #             else:
    #                 self.custom_values.append(
    #                     LeadCustomFieldValue.create(
    #                         custom_field_id=custom_field.id,
    #                         value=value,
    #                         lead_id=self.id
    #                     )
    #                 )
    #
    #         elif custom_field.type.datetime and value.value_date is not None:
    #             existing = self._find_value(custom_field.id)
    #             if not value.enum_id in [e.id for e in custom_field.enums]:
    #                 raise
    #             if existing:
    #                 existing.value = value
    #             else:
    #                 self.custom_values.append(
    #                     LeadCustomFieldValue.create(
    #                         custom_field_id=custom_field.id,
    #                         value=value,
    #                         lead_id=self.id
    #                     )
    #                 )
    #
    #         elif custom_field.type.number and value.value_number is not None:
    #             existing = self._find_value(custom_field.id)
    #             if not value.enum_id in [e.id for e in custom_field.enums]:
    #                 raise
    #             if existing:
    #                 existing.value = value
    #             else:
    #                 self.custom_values.append(
    #                     LeadCustomFieldValue.create(
    #                         custom_field_id=custom_field.id,
    #                         value=value,
    #                         lead_id=self.id
    #                     )
    #                 )
    #     self.touch()

    def remove_custom_value(
        self,
        custom_field_value_id: UUID
    ):
        self.custom_values = [
            v for v in self.custom_values if v.id != custom_field_value_id
        ]
        self.touch()


    def _find_value(
            self,
            custom_field_id: UUID,
            enum_id: UUID | None = None
    )-> LeadCustomFieldValue | None:
        option = lambda v :(
            v for v in self.custom_values if v.custom_field_id == custom_field_id and v.value.enum_id == enum_id
        ) if enum_id is not None else(
            v.custom_field_id == custom_field_id
        )
        return next(
            (v for v in self.custom_values if option(v)),
            None
        )

    def delete(self):
        self.is_delete = True
        self.touch()