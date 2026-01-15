'use client';

import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { LoginForm } from '@/components/auth/LoginForm';
import { OAuthButtons } from '@/components/auth/OAuthButtons';

/**
 * Página de login de usuário.
 */
export default function LoginPage() {
  const searchParams = useSearchParams();
  const error = searchParams.get('error');

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#333333] px-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-[#aeffde]">Dona Maria</h1>
          <p className="mt-2 text-[#e4f1ff]">Entre na sua conta</p>
        </div>

        {/* Card do Formulário */}
        <div className="rounded-lg border border-[#e4f1ff]/10 bg-[#333333]/80 p-8 shadow-lg backdrop-blur-sm">
          {/* Mensagem de erro OAuth */}
          {error && (
            <div className="mb-6 rounded-md border border-[#ff8080] bg-[#ff8080]/10 p-3 text-sm text-[#ff8080]">
              {getErrorMessage(error)}
            </div>
          )}

          {/* Formulário de login com email */}
          <LoginForm />

          {/* Separador */}
          <div className="my-6 flex items-center">
            <div className="flex-1 border-t border-[#e4f1ff]/20"></div>
            <span className="px-4 text-sm text-[#e4f1ff]/50">ou</span>
            <div className="flex-1 border-t border-[#e4f1ff]/20"></div>
          </div>

          {/* Botões OAuth */}
          <OAuthButtons />

          {/* Link para Registro */}
          <p className="mt-6 text-center text-sm text-[#e4f1ff]/70">
            Não tem uma conta?{' '}
            <Link href="/register" className="text-[#aeffde] hover:underline">
              Criar conta
            </Link>
          </p>
        </div>
      </div>
    </div>
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
      return `Erro: ${error}`;
  }
}
