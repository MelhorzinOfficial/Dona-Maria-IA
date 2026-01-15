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

type OAuthProvider = 'google' | 'github';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Hook para autenticação de usuários.
 *
 * Fornece funções para registro, login, OAuth e gerenciamento de estado de autenticação.
 */
export function useAuth() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Fazer login com email e senha.
   *
   * @param email - Email do usuário.
   * @param password - Senha do usuário.
   * @returns Promise com tokens em caso de sucesso.
   */
  const login = useCallback(
    async (email: string, password: string): Promise<AuthTokens | null> => {
      setIsLoading(true);
      setError(null);

      try {
        // OAuth2PasswordRequestForm espera form data, não JSON
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: formData,
        });

        if (!response.ok) {
          try {
            const errorData: ApiError = await response.json();
            setError(errorData.detail || 'Email ou senha incorretos');
          } catch {
            setError('Erro ao fazer login. Tente novamente.');
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
   * Iniciar login via OAuth.
   *
   * Redireciona para o provedor OAuth.
   *
   * @param provider - Provedor OAuth ('google' ou 'github').
   */
  const loginWithOAuth = useCallback((provider: OAuthProvider) => {
    // Redirecionar para endpoint OAuth do backend
    window.location.href = `${API_BASE_URL}/api/v1/auth/oauth/${provider}`;
  }, []);

  /**
   * Armazenar tokens de autenticação.
   *
   * @param accessToken - Token de acesso JWT.
   * @param refreshToken - Token de refresh JWT.
   */
  const setTokens = useCallback((accessToken: string, refreshToken: string) => {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
  }, []);

  /**
   * Obter token de acesso armazenado.
   *
   * @returns Token de acesso ou null se não existir.
   */
  const getAccessToken = useCallback((): string | null => {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('access_token');
  }, []);

  /**
   * Verificar se usuário está autenticado.
   *
   * @returns True se há token de acesso armazenado.
   */
  const isAuthenticated = useCallback((): boolean => {
    return getAccessToken() !== null;
  }, [getAccessToken]);

  /**
   * Fazer logout do usuário.
   *
   * Chama endpoint de logout, remove tokens e redireciona para landing page.
   */
  const logout = useCallback(async () => {
    const accessToken = getAccessToken();

    // Chamar endpoint de logout se tiver token
    if (accessToken) {
      try {
        await fetch(`${API_BASE_URL}/api/v1/auth/logout`, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
      } catch {
        // Ignorar erros - vamos limpar tokens de qualquer forma
      }
    }

    // Limpar tokens locais
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    router.push('/');
  }, [router, getAccessToken]);

  /**
   * Renovar access token usando refresh token.
   *
   * @returns Novos tokens ou null se falhar.
   */
  const refreshAccessToken = useCallback(async (): Promise<AuthTokens | null> => {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) return null;

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });

      if (!response.ok) {
        // Refresh token inválido - fazer logout
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        return null;
      }

      const tokens: AuthTokens = await response.json();
      localStorage.setItem('access_token', tokens.access_token);
      localStorage.setItem('refresh_token', tokens.refresh_token);
      return tokens;
    } catch {
      return null;
    }
  }, []);

  /**
   * Limpar erro atual.
   */
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    login,
    register,
    loginWithOAuth,
    setTokens,
    getAccessToken,
    isAuthenticated,
    logout,
    refreshAccessToken,
    isLoading,
    error,
    clearError,
  };
}
