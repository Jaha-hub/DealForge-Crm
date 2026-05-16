import { QueryClient } from "@tanstack/react-query"

export const queryClientConfig = {
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60,
      retry: 1,
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 0,
    },
  },
} as const

export function makeQueryClient() {
  return new QueryClient(queryClientConfig)
}
