import { Suspense } from "react"
import { LoginForm } from "@/features/auth/components/LoginForm"

export default function LoginPage() {
  return (
    <div className="w-full max-w-md">
      <div className="text-center mb-8">
        <h1 className="text-2xl font-bold">DealForge CRM</h1>
        <p className="text-muted-foreground mt-1">Войдите в свой аккаунт</p>
      </div>
      {/* Suspense нужен из-за useSearchParams внутри LoginForm → useLogin */}
      <Suspense>
        <LoginForm />
      </Suspense>
    </div>
  )
}
