import { create } from "zustand"

interface UIStore {
  sidebarOpen: boolean
  activeFunnelId: string | null
  toggleSidebar: () => void
  setSidebarOpen: (open: boolean) => void
  setActiveFunnel: (id: string | null) => void
}

export const useUIStore = create<UIStore>((set) => ({
  sidebarOpen: true,
  activeFunnelId: null,

  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  setActiveFunnel: (id) => set({ activeFunnelId: id }),
}))
