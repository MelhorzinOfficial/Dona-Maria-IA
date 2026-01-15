'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import Link from 'next/link';

const resetPasswordSchema = z
  .object({
    newPassword: z.string().min(8, 'Senha deve ter no mínimo 8 caracteres'),
    confirmPassword: z.string(),
  })
  .refine(data => data.newPassword === data.confirmPassword, {
    message: 'Senhas não conferem',
    path: ['confirmPassword'],
  });

type ResetPasswordData = z.infer<typeof resetPasswordSchema>;

export default function ResetPasswordPage() {
  const params = useParams();
  const router = useRouter();
  const token = params.token as string;

  const [isLoading, setIsLoading] = useState(false);
  const [isValidating, setIsValidating] = useState(true);
  const [isExpired, setIsExpired] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ResetPasswordData>({
    resolver: zodResolver(resetPasswordSchema),
  });

  // Verificar token ao carregar página
  useEffect(() => {
    const verifyToken = async () => {
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/verify-reset-token/${token}`
        );
        if (!response.ok) {
          setIsExpired(true);
        }
      } catch {
        setIsExpired(true);
      } finally {
        setIsValidating(false);
      }
    };

    verifyToken();
  }, [token]);

  const onSubmit = async (data: ResetPasswordData) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/reset-password`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            token,
            new_password: data.newPassword,
          }),
        }
      );

      if (response.ok) {
        setSuccess(true);
        setTimeout(() => router.push('/login'), 3000);
      } else {
        const errorData = await response.json();
        if (response.status === 400) {
          setIsExpired(true);
        } else {
          setError(errorData.detail || 'Erro ao redefinir senha');
        }
      }
    } catch {
      setError('Erro de conexão. Tente novamente.');
    } finally {
      setIsLoading(false);
    }
  };

  if (isValidating) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#333333]">
        <div className="text-white">Verificando link...</div>
      </div>
    );
  }

  if (isExpired) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#333333]">
        <div className="w-full max-w-md rounded-lg bg-white p-8 text-center shadow-lg">
          <div className="mb-4 text-6xl">⏰</div>
          <h1 className="mb-4 text-2xl font-bold text-red-600">Link Expirado</h1>
          <p className="mb-6 text-gray-600">
            Este link de recuperação expirou ou já foi utilizado.
          </p>
          <Link
            href="/forgot-password"
            className="inline-block rounded-lg bg-[#aeffde] px-6 py-3 font-semibold text-[#333333] transition hover:bg-[#9ee8c9]"
          >
            Solicitar Novo Link
          </Link>
          <p className="mt-4">
            <Link href="/login" className="text-sm text-gray-500 hover:underline">
              Voltar para o login
            </Link>
          </p>
        </div>
      </div>
    );
  }

  if (success) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#333333]">
        <div className="w-full max-w-md rounded-lg bg-white p-8 text-center shadow-lg">
          <div className="mb-4 text-6xl">✅</div>
          <h1 className="mb-4 text-2xl font-bold text-green-600">Senha Alterada!</h1>
          <p className="mb-6 text-gray-600">
            Sua senha foi alterada com sucesso. Você será redirecionado para o login...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#333333]">
      <div className="w-full max-w-md rounded-lg bg-white p-8 shadow-lg">
        <h1 className="mb-6 text-center text-2xl font-bold">Redefinir Senha</h1>
        <p className="mb-6 text-center text-gray-600">Digite sua nova senha abaixo.</p>

        {error && (
          <div className="mb-4 rounded-lg bg-red-100 p-3 text-center text-red-600">{error}</div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label htmlFor="newPassword" className="mb-1 block text-sm font-medium text-gray-700">
              Nova Senha
            </label>
            <input
              id="newPassword"
              type="password"
              {...register('newPassword')}
              className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-transparent focus:ring-2 focus:ring-[#aeffde]"
              placeholder="Mínimo 8 caracteres"
            />
            {errors.newPassword && (
              <p className="mt-1 text-sm text-red-500">{errors.newPassword.message}</p>
            )}
          </div>

          <div>
            <label
              htmlFor="confirmPassword"
              className="mb-1 block text-sm font-medium text-gray-700"
            >
              Confirmar Nova Senha
            </label>
            <input
              id="confirmPassword"
              type="password"
              {...register('confirmPassword')}
              className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-transparent focus:ring-2 focus:ring-[#aeffde]"
              placeholder="Digite a senha novamente"
            />
            {errors.confirmPassword && (
              <p className="mt-1 text-sm text-red-500">{errors.confirmPassword.message}</p>
            )}
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full rounded-lg bg-[#aeffde] py-3 font-semibold text-[#333333] transition hover:bg-[#9ee8c9] disabled:opacity-50"
          >
            {isLoading ? 'Salvando...' : 'Salvar Nova Senha'}
          </button>
        </form>
      </div>
    </div>
  );
}
