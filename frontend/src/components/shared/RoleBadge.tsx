import { Badge } from "@/components/ui/badge"
import type { UserRole } from "@/store/auth.store"

type BadgeVariant = "default" | "secondary" | "outline"

const ROLE_CONFIG: Record<UserRole, { label: string; variant: BadgeVariant }> = {
  admin:         { label: "Администратор", variant: "default" },
  director:      { label: "Руководитель",  variant: "default" },
  sales_manager: { label: "Менеджер",      variant: "secondary" },
  consultant:    { label: "Консультант",   variant: "outline" },
}

export function RoleBadge({ role }: { role: UserRole }) {
  const { label, variant } = ROLE_CONFIG[role]
  return <Badge variant={variant}>{label}</Badge>
}
