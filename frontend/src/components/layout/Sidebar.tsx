"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  LayoutDashboard,
  Users,
  Kanban,
  List,
  GitBranch,
  Radio,
  SlidersHorizontal,
  BarChart3,
  User,
  X,
} from "lucide-react"
import { cn } from "@/lib/utils"
import { useCurrentRole } from "@/store/auth.store"
import { useUIStore } from "@/store/ui.store"
import type { UserRole } from "@/store/auth.store"
import { Button } from "@/components/ui/button"

interface NavItem {
  href: string
  label: string
  icon: React.ElementType
  roles?: UserRole[]
}

const NAV_ITEMS: NavItem[] = [
  {
    href: "/dashboard",
    label: "Дашборд",
    icon: LayoutDashboard,
  },
  {
    href: "/funnels",
    label: "Воронки",
    icon: Kanban,
  },
  {
    href: "/leads",
    label: "Лиды",
    icon: List,
  },
  {
    href: "/sources",
    label: "Источники",
    icon: Radio,
    roles: ["admin", "director"],
  },
  {
    href: "/custom-fields",
    label: "Кастомные поля",
    icon: SlidersHorizontal,
    roles: ["admin", "director"],
  },
  {
    href: "/analytics",
    label: "Аналитика",
    icon: BarChart3,
    roles: ["admin", "director", "sales_manager"],
  },
  {
    href: "/users",
    label: "Пользователи",
    icon: Users,
    roles: ["admin"],
  },
  {
    href: "/profile",
    label: "Профиль",
    icon: User,
  },
]

export function Sidebar() {
  const pathname = usePathname()
  const role = useCurrentRole()
  const { sidebarOpen, setSidebarOpen } = useUIStore()

  const visibleItems = NAV_ITEMS.filter(
    (item) => !item.roles || (role && item.roles.includes(role))
  )

  return (
    <>
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-20 bg-black/40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-30 flex w-64 flex-col bg-card border-r transition-transform duration-200",
          "lg:relative lg:translate-x-0 lg:z-auto",
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        {/* Logo */}
        <div className="flex h-16 items-center justify-between px-6 border-b">
          <Link href="/dashboard" className="flex items-center gap-2">
            <GitBranch className="h-5 w-5 text-primary" />
            <span className="font-bold text-lg">DealForge</span>
          </Link>
          <Button
            variant="ghost"
            size="icon"
            className="lg:hidden"
            onClick={() => setSidebarOpen(false)}
          >
            <X className="h-4 w-4" />
          </Button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto py-4 px-3">
          <ul className="space-y-1">
            {visibleItems.map((item) => {
              const isActive =
                item.href === "/dashboard"
                  ? pathname === "/dashboard"
                  : pathname.startsWith(item.href)
              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    onClick={() => setSidebarOpen(false)}
                    className={cn(
                      "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                      isActive
                        ? "bg-primary text-primary-foreground"
                        : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                    )}
                  >
                    <item.icon className="h-4 w-4 shrink-0" />
                    {item.label}
                  </Link>
                </li>
              )
            })}
          </ul>
        </nav>
      </aside>
    </>
  )
}
