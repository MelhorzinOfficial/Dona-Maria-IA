'use client';

import { useRouter } from 'next/navigation';
import { useCallback, useState } from 'react';

interface RegisterData {
  email: string;
  password: string;
}

interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

interface ApiError {
  detail: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Hook para autenticação de usuários.
 *
 * Fornece funções para registro, login e gerenciamento de estado de autenticação.
 */
export function useAuth() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Registrar novo usuário.
   *
   * @param data - Email e senha do novo usuário.
   * @returns Promise com tokens em caso de sucesso.
   */
  const register = useCallback(
    async (data: RegisterData): Promise<AuthTokens | null> => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await fetch(`${API_BASE_URL}/api/v1/auth/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        });

        if (!response.ok) {
          try {
            const errorData: ApiError = await response.json();
            setError(errorData.detail || 'Erro ao registrar');
          } catch {
            setError('Erro ao registrar. Tente novamente.');
          }
          return null;
        }

        const tokens: AuthTokens = await response.json();

        // Armazenar tokens
        localStorage.setItem('access_token', tokens.access_token);
        localStorage.setItem('refresh_token', tokens.refresh_token);

        // Redirecionar para o chat
        router.push('/chat');

        return tokens;
      } catch {
        setError('Erro de conexão. Tente novamente.');
        return null;
      } finally {
        setIsLoading(false);
      }
    },
    [router]
  );

  /**
   * Limpar erro atual.
   */
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    register,
    isLoading,
    error,
    clearError,
  };
}
