import Link from 'next/link';
import { RegisterForm } from '@/components/auth/RegisterForm';
import { OAuthButtons } from '@/components/auth/OAuthButtons';

/**
 * Página de registro de novo usuário.
 */
export default function RegisterPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[#333333] px-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-[#aeffde]">Dona Maria</h1>
          <p className="mt-2 text-[#e4f1ff]">Crie sua conta</p>
        </div>

        {/* Card do Formulário */}
        <div className="rounded-lg border border-[#e4f1ff]/10 bg-[#333333]/80 p-8 shadow-lg backdrop-blur-sm">
          {/* Botões OAuth */}
          <OAuthButtons />

          {/* Separador */}
          <div className="my-6 flex items-center">
            <div className="flex-1 border-t border-[#e4f1ff]/20"></div>
            <span className="px-4 text-sm text-[#e4f1ff]/50">ou</span>
            <div className="flex-1 border-t border-[#e4f1ff]/20"></div>
          </div>

          {/* Formulário tradicional */}
          <RegisterForm />

          {/* Link para Login */}
          <p className="mt-6 text-center text-sm text-[#e4f1ff]/70">
            Já tem uma conta?{' '}
            <Link href="/login" className="text-[#aeffde] hover:underline">
              Entrar
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
