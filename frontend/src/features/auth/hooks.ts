"use client"

import { useEffect } from "react"
import { useMutation, useQuery } from "@tanstack/react-query"
import { useRouter, useSearchParams } from "next/navigation"
import { toast } from "sonner"
import { authApi } from "./api"
import { useAuthStore } from "@/store/auth.store"
import { getAccessToken } from "@/lib/axios"

export function useLogin() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const setAuth = useAuthStore((s) => s.setAuth)

  return useMutation({
    mutationFn: authApi.login,
    onSuccess: ({ data }) => {
      setAuth(data.user, data.access_token)
      const from = searchParams.get("from") ?? "/dashboard"
      router.replace(from)
    },
    onError: () => {
      toast.error("Неверный email или пароль")
    },
  })
}

export function useLogout() {
  const router = useRouter()
  const logout = useAuthStore((s) => s.logout)

  return useMutation({
    mutationFn: authApi.logout,
    onSettled: () => {
      logout()
      router.replace("/login")
    },
  })
}

// Восстанавливает сессию после F5. Если refresh cookie есть, axios interceptor
// при 401 автоматически обновит access token, затем запрос /auth/me успешно вернёт user.
export function useInitAuth() {
  const setAuth = useAuthStore((s) => s.setAuth)
  const user = useAuthStore((s) => s.user)

  const query = useQuery({
    queryKey: ["auth", "me"],
    queryFn: () => authApi.me().then((r) => r.data),
    enabled: user === null,
    retry: false,
    staleTime: Infinity,
  })

  useEffect(() => {
    if (query.data) {
      // После успешного /auth/me axios interceptor уже обновил access token
      const token = getAccessToken() ?? ""
      setAuth(query.data, token)
    }
  }, [query.data, setAuth])

  return query
}
