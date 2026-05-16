import type { SoftDeletable } from "@/types/common"

export type SourceType = "manual" | "webhook" | "public_form"

export interface Source extends SoftDeletable {
  name: string
  source_type: SourceType
  funnel_id?: string
  is_active: boolean
  webhook_token?: string
  config?: Record<string, unknown>
}
