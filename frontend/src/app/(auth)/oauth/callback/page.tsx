'use client';

import { useEffect, useMemo } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Suspense } from 'react';

/**
 * Componente interno que processa o callback OAuth.
 */
function OAuthCallbackContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  // Computar estado a partir dos parâmetros de URL (sem useState)
  const { error, hasTokens, accessToken, refreshToken } = useMemo(() => {
    const errorParam = searchParams.get('error');
    const access = searchParams.get('access_token');
    const refresh = searchParams.get('refresh_token');

    if (errorParam) {
      return {
        error: getErrorMessage(errorParam),
        hasTokens: false,
        accessToken: null,
        refreshToken: null,
      };
    }

    if (access && refresh) {
      return {
        error: null,
        hasTokens: true,
        accessToken: access,
        refreshToken: refresh,
      };
    }

    return {
      error: 'Tokens não recebidos. Tente novamente.',
      hasTokens: false,
      accessToken: null,
      refreshToken: null,
    };
  }, [searchParams]);

  useEffect(() => {
    // Somente processar se temos tokens válidos
    if (hasTokens && accessToken && refreshToken) {
      // Armazenar tokens no localStorage
      localStorage.setItem('access_token', accessToken);
      localStorage.setItem('refresh_token', refreshToken);

      // Redirecionar para o chat
      router.push('/chat');
    }
  }, [hasTokens, accessToken, refreshToken, router]);

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#333333] px-4">
        <div className="w-full max-w-md text-center">
          {/* Ícone de erro */}
          <div className="mb-6 inline-flex h-16 w-16 items-center justify-center rounded-full bg-[#ff8080]/10">
            <svg
              className="h-8 w-8 text-[#ff8080]"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </div>

          <h1 className="mb-4 text-2xl font-bold text-[#ff8080]">Erro na autenticação</h1>
          <p className="mb-8 text-[#e4f1ff]/70">{error}</p>

          <a
            href="/login"
            className="inline-block rounded-md bg-[#aeffde] px-6 py-3 font-medium text-[#333333] transition-colors hover:bg-[#aeffde]/90"
          >
            Voltar para Login
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#333333] px-4">
      <div className="text-center">
        {/* Loading spinner */}
        <div className="mb-6 inline-flex h-16 w-16 items-center justify-center">
          <svg className="h-12 w-12 animate-spin text-[#aeffde]" fill="none" viewBox="0 0 24 24">
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        </div>

        <h1 className="mb-2 text-xl font-medium text-[#e4f1ff]">Autenticando...</h1>
        <p className="text-[#e4f1ff]/50">Aguarde enquanto finalizamos seu login.</p>
      </div>
    </div>
  );
}

/**
 * Página de callback OAuth.
 *
 * Processa tokens recebidos do backend e redireciona para o chat.
 */
export default function OAuthCallbackPage() {
  return (
    <Suspense
      fallback={
        <div className="flex min-h-screen items-center justify-center bg-[#333333]">
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-[#aeffde] border-t-transparent" />
        </div>
      }
    >
      <OAuthCallbackContent />
    </Suspense>
  );
}

/**
 * Converter código de erro em mensagem amigável.
 */
function getErrorMessage(error: string): string {
  switch (error) {
    case 'access_denied':
      return 'Acesso negado. Você cancelou a autorização.';
    case 'invalid_state':
      return 'Sessão expirada. Por favor, tente novamente.';
    case 'oauth_failed':
      return 'Falha na autenticação. Por favor, tente novamente.';
    case 'missing_params':
      return 'Parâmetros inválidos. Por favor, tente novamente.';
    default:
      return `Erro desconhecido: ${error}`;
  }
}
