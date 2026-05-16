export type NotificationEventType =
  | "lead_assigned"
  | "lead_stage_changed"
  | "lead_created_webhook"
  | "lead_created_form"
  | "lead_returned"

export interface Notification {
  id: string
  user_id: string
  title: string
  body: string
  is_read: boolean
  event_type: NotificationEventType
  payload?: Record<string, unknown>
  created_at: string
}
