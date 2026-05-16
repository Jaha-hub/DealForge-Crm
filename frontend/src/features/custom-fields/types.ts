import type { BaseEntity, SoftDeletable } from "@/types/common"
import type { FieldType } from "@/features/leads/types"

export interface CustomFieldEnum extends BaseEntity {
  value: string
  order: number
}

export interface CustomField extends SoftDeletable {
  name: string
  field_type: FieldType
  is_required: boolean
  enums: CustomFieldEnum[]
}
