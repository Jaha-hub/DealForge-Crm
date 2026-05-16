import { create } from "zustand"
import { setAccessToken } from "@/lib/axios"

export type UserRole = "admin" | "director" | "sales_manager" | "consultant"

export interface AuthUser {
  id: string
  name: string
  email: string
  role: UserRole
}

interface AuthStore {
  user: AuthUser | null
  setAuth: (user: AuthUser, token: string) => void
  logout: () => void
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,

  setAuth: (user, token) => {
    setAccessToken(token)
    set({ user })
  },

  logout: () => {
    setAccessToken(null)
    set({ user: null })
  },
}))

export const useIsAuthenticated = () => useAuthStore((s) => s.user !== null)
export const useCurrentUser = () => useAuthStore((s) => s.user)
export const useCurrentRole = () => useAuthStore((s) => s.user?.role)
