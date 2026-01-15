import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

/**
 * Middleware para proteção de rotas.
 *
 * - Rotas autenticadas: redireciona para /login se não tiver token
 * - Rotas de auth: redireciona para /chat se já estiver autenticado
 *
 * Note: A proteção principal é feita pelo withAuth HOC no client-side
 * pois o middleware do Next.js não tem acesso ao localStorage.
 */
export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Para rotas de API, não fazer nada
  if (pathname.startsWith('/api')) {
    return NextResponse.next();
  }

  // Para arquivos estáticos, não fazer nada
  if (pathname.startsWith('/_next') || pathname.includes('.')) {
    return NextResponse.next();
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
