import { apiClient } from "@/lib/axios"
import type { AuthUser } from "@/store/auth.store"

export interface LoginPayload {
  email: string
  password: string
}

export interface LoginResponse {
  access_token: string
  user: AuthUser
}

export const authApi = {
  login: (data: LoginPayload) =>
    apiClient.post<LoginResponse>("/auth/login", data),

  // refresh is handled transparently by the axios interceptor in lib/axios.ts
  // and should not be called directly from feature code.

  logout: () =>
    apiClient.post("/auth/logout"),

  me: () =>
    apiClient.get<AuthUser>("/auth/me"),
}
