"use client"

import Link from "next/link"
import { useRouter } from "next/navigation"
import { Menu, Bell, LogOut, User } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { RoleBadge } from "@/components/shared/RoleBadge"
import { useCurrentUser } from "@/store/auth.store"
import { useUIStore } from "@/store/ui.store"
import { useLogout } from "@/features/auth/hooks"

function getInitials(name: string): string {
  return name
    .split(" ")
    .slice(0, 2)
    .map((w) => w[0]?.toUpperCase() ?? "")
    .join("")
}

export function Header() {
  const user = useCurrentUser()
  const { toggleSidebar } = useUIStore()
  const { mutate: logout, isPending } = useLogout()
  const router = useRouter()

  return (
    <header className="flex h-16 items-center border-b bg-card px-4 gap-4">
      {/* Burger — mobile only */}
      <Button
        variant="ghost"
        size="icon"
        className="lg:hidden"
        onClick={toggleSidebar}
      >
        <Menu className="h-5 w-5" />
      </Button>

      {/* Spacer */}
      <div className="flex-1" />

      {/* Notifications (placeholder — Phase 8) */}
      <Link
        href="/dashboard"
        aria-label="Уведомления"
        className="inline-flex items-center justify-center size-8 rounded-lg text-muted-foreground hover:bg-muted hover:text-foreground transition-colors"
      >
        <Bell className="h-5 w-5" />
      </Link>

      {/* User menu */}
      <DropdownMenu>
        <DropdownMenuTrigger>
          <Button variant="ghost" className="flex items-center gap-2 px-2 h-auto py-1">
            <Avatar className="h-8 w-8">
              <AvatarFallback className="text-xs">
                {user ? getInitials(user.name) : "?"}
              </AvatarFallback>
            </Avatar>
            <div className="hidden sm:flex flex-col items-start">
              <span className="text-sm font-medium leading-none">
                {user?.name ?? ""}
              </span>
              {user?.role && (
                <span className="mt-1">
                  <RoleBadge role={user.role} />
                </span>
              )}
            </div>
          </Button>
        </DropdownMenuTrigger>

        <DropdownMenuContent align="end" className="w-48">
          <DropdownMenuItem onClick={() => router.push("/profile")}>
            <User className="h-4 w-4" />
            Профиль
          </DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem
            variant="destructive"
            disabled={isPending}
            onClick={() => logout()}
          >
            <LogOut className="h-4 w-4" />
            Выйти
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </header>
  )
}
