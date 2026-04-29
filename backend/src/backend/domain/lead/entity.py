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
    custom_field_id: UUID
    value: str

    @classmethod
    def create(
            cls,
            custom_field_id: UUID,
            value: str,
    ):
        return cls(
            custom_field_id=custom_field_id,
            value=value,
        )

@dataclass
class LeadCustomField(BaseEntity,TimeActionMixin, LeadCustomFieldEnum):
    name: LeadName
    type: FieldType
    enums: list[LeadCustomFieldEnum] = field(default_factory=list)

    @classmethod
    def create(
            cls,
            name:str,
            type:FieldType,
    ):
        return cls(
            name=LeadName(name),
            type=type,
        )

    def add_enum(
            self,
            value: str
    ):
        if not self.type in [FieldType.select_many, FieldType.select_one]:
            raise
        new_enum = LeadCustomFieldEnum.create(self.id, value)
        self.enums.append(new_enum)
        self.touch()

    def remove_enum(
            self,
            enum_id: UUID
    ):
        self.enums = [e for e in self.enums if e.id == enum_id]
        self.touch()

    def rename(
            self,
            name: str
    ):
        self.name = LeadName(name)
        self.touch()


@dataclass
class LeadCustomFieldValue(BaseEntity):
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
        return cls(
            custom_field_id=custom_field_id,
            lead_id=lead_id,
            value=value
        )


@dataclass
class Lead(BaseEntity,TimeActionMixin, LeadCustomFieldValue):
    name: LeadName
    contact: Contact
    is_delete: bool = field(default=False)
    assign_to: UUID | None = None
    custom_values: list[LeadCustomFieldValue] = field(default_factory=list)

    def set_custom_value(
            self,
            custom_field: LeadCustomField,
            value: FieldValue,
    ):
        if custom_field.type.select_many:
            if value.enum_id is not None:
                if not value.enum_id in [e.id for e in custom_field.enums]:
                    raise
                existing = self._find_value(custom_field.id)
                if not value.enum_id in [e.id for e in custom_field.enums]:
                    raise
                if not existing:
                    existing.value = value
                    self.custom_values.append(
                        LeadCustomFieldValue.create(
                            custom_field_id=custom_field.id,
                            value=value,
                            lead_id=self.id
                        )
                    )
                else:
                    raise


            elif custom_field.type.text and value.value_text is not None:
                existing = self._find_value(custom_field.id)
                if not value.enum_id in [e.id for e in custom_field.enums]:
                    raise
                if existing:
                    existing.value = value
                else:
                    self.custom_values.append(
                        LeadCustomFieldValue.create(
                            custom_field_id=custom_field.id,
                            value=value,
                            lead_id=self.id
                        )
                    )

            elif custom_field.type.boolean and value.value_boolean is not None:
                existing = self._find_value(custom_field.id)
                if not value.enum_id in [e.id for e in custom_field.enums]:
                    raise
                if existing:
                    existing.value = value
                else:
                    self.custom_values.append(
                        LeadCustomFieldValue.create(
                            custom_field_id=custom_field.id,
                            value=value,
                            lead_id=self.id
                        )
                    )

            elif custom_field.type.datetime and value.value_date is not None:
                existing = self._find_value(custom_field.id)
                if not value.enum_id in [e.id for e in custom_field.enums]:
                    raise
                if existing:
                    existing.value = value
                else:
                    self.custom_values.append(
                        LeadCustomFieldValue.create(
                            custom_field_id=custom_field.id,
                            value=value,
                            lead_id=self.id
                        )
                    )

            elif custom_field.type.number and value.value_number is not None:
                existing = self._find_value(custom_field.id)
                if not value.enum_id in [e.id for e in custom_field.enums]:
                    raise
                if existing:
                    existing.value = value
                else:
                    self.custom_values.append(
                        LeadCustomFieldValue.create(
                            custom_field_id=custom_field.id,
                            value=value,
                            lead_id=self.id
                        )
                    )
        self.touch()

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