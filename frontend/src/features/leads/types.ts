import type { SoftDeletable } from "@/types/common"

export type FieldType =
  | "text"
  | "number"
  | "date"
  | "time"
  | "select_one"
  | "select_many"
  | "boolean"

export type StageType = "initial" | "intermediate" | "won" | "lost"

export interface LeadCustomFieldValue {
  id: string
  custom_field_id: string
  value_text?: string
  value_number?: number
  value_date?: string
  value_time?: string
  value_boolean?: boolean
  enum_value?: string
  enum_values?: string[]
}

export interface Lead extends SoftDeletable {
  name: string
  phone?: string
  email?: string
  comment?: string
  tags: string[]
  source_id: string
  funnel_id: string
  stage_id: string
  assign_to?: string
  custom_values: LeadCustomFieldValue[]
  closed_at?: string
}

export interface LeadFilters {
  funnel_id?: string
  stage_id?: string
  source_id?: string
  assign_to?: string
  tags?: string[]
  created_from?: string
  created_to?: string
  page?: number
  limit?: number
}
