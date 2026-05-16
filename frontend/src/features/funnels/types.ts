import type { BaseEntity, SoftDeletable } from "@/types/common"
import type { StageType } from "@/features/leads/types"

export interface FunnelStage extends BaseEntity {
  name: string
  color: string
  order: number
  probability: number
  stage_type: StageType
  funnel_id: string
}

export interface Funnel extends SoftDeletable {
  name: string
  stages: FunnelStage[]
}
