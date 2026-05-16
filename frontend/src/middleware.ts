import { NextRequest, NextResponse } from "next/server"

const PUBLIC_ROUTES = ["/login", "/forms"]

// Routes to redirect away from when user is already authenticated.
// Distinct from PUBLIC_ROUTES: /forms stays public regardless of auth state.
const REDIRECT_IF_AUTHENTICATED = ["/login"]

function isPublic(pathname: string): boolean {
  return PUBLIC_ROUTES.some((route) => pathname.startsWith(route))
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  const refreshToken = request.cookies.get("refresh_token")?.value

  if (isPublic(pathname)) {
    if (REDIRECT_IF_AUTHENTICATED.includes(pathname) && refreshToken) {
      return NextResponse.redirect(new URL("/dashboard", request.url))
    }
    return NextResponse.next()
  }

  if (!refreshToken) {
    const loginUrl = new URL("/login", request.url)
    loginUrl.searchParams.set("from", pathname)
    return NextResponse.redirect(loginUrl)
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
}
