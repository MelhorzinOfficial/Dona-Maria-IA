'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState, ComponentType } from 'react';
import { useAuth } from '@/hooks/useAuth';

/**
 * HOC para proteger rotas que requerem autenticação.
 *
 * Redireciona para /login se o usuário não estiver autenticado.
 *
 * @param WrappedComponent - Componente a ser protegido.
 * @returns Componente protegido.
 */
export function withAuth<P extends object>(WrappedComponent: ComponentType<P>) {
  return function WithAuthComponent(props: P) {
    const router = useRouter();
    const { isAuthenticated } = useAuth();
    const [isChecking, setIsChecking] = useState(true);

    useEffect(() => {
      // Verificar autenticação no cliente
      if (!isAuthenticated()) {
        router.replace('/login');
      } else {
        setIsChecking(false);
      }
    }, [isAuthenticated, router]);

    // Mostrar loading enquanto verifica
    if (isChecking) {
      return (
        <div className="flex min-h-screen items-center justify-center bg-[#333333]">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-[#aeffde] border-t-transparent"></div>
        </div>
      );
    }

    return <WrappedComponent {...props} />;
  };
}
