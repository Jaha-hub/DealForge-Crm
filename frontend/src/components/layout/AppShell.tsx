"use client"

import { useInitAuth } from "@/features/auth/hooks"
import { Sidebar } from "./Sidebar"
import { Header } from "./Header"

export function AppShell({ children }: { children: React.ReactNode }) {
  // Восстанавливает сессию после F5 без блокирующего спиннера.
  // Middleware уже проверил refresh cookie, поэтому пользователь аутентифицирован —
  // просто ждём пока store заполнится данными из /auth/me.
  useInitAuth()

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <Sidebar />
      <div className="flex flex-1 flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-6">{children}</main>
      </div>
    </div>
  )
}
