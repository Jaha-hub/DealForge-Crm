export interface BaseEntity {
  id: string
  created_at: string
  updated_at: string
}

export interface SoftDeletable extends BaseEntity {
  is_deleted: boolean
}
