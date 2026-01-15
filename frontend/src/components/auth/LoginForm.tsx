'use client';

import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { useAuth } from '@/hooks/useAuth';

/**
 * Schema de validação para o formulário de login.
 */
const loginSchema = z.object({
  email: z.string().email('Email inválido'),
  password: z.string().min(1, 'Senha é obrigatória'),
});

type LoginFormData = z.infer<typeof loginSchema>;

/**
 * Componente de formulário de login de usuário.
 *
 * Inclui validação client-side e feedback visual de loading/erros.
 */
export function LoginForm() {
  const { login, isLoading, error, clearError } = useAuth();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    clearError();
    await login(data.email, data.password);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      {/* Erro da API */}
      {error && (
        <div className="rounded-md border border-[#ff8080] bg-[#ff8080]/10 p-3 text-sm text-[#ff8080]">
          {error}
        </div>
      )}

      {/* Campo Email */}
      <div>
        <label htmlFor="email" className="mb-2 block text-sm font-medium text-[#e4f1ff]">
          Email
        </label>
        <input
          id="email"
          type="email"
          {...register('email')}
          className="w-full rounded-md border border-[#e4f1ff]/20 bg-[#333333] px-4 py-2 text-white placeholder-[#e4f1ff]/50 focus:border-[#aeffde] focus:ring-1 focus:ring-[#aeffde] focus:outline-none"
          placeholder="seu@email.com"
          disabled={isLoading}
        />
        {errors.email && <p className="mt-1 text-sm text-[#ff8080]">{errors.email.message}</p>}
      </div>

      {/* Campo Senha */}
      <div>
        <label htmlFor="password" className="mb-2 block text-sm font-medium text-[#e4f1ff]">
          Senha
        </label>
        <input
          id="password"
          type="password"
          {...register('password')}
          className="w-full rounded-md border border-[#e4f1ff]/20 bg-[#333333] px-4 py-2 text-white placeholder-[#e4f1ff]/50 focus:border-[#aeffde] focus:ring-1 focus:ring-[#aeffde] focus:outline-none"
          placeholder="Sua senha"
          disabled={isLoading}
        />
        {errors.password && (
          <p className="mt-1 text-sm text-[#ff8080]">{errors.password.message}</p>
        )}
      </div>

      {/* Botão Submit */}
      <button
        type="submit"
        disabled={isLoading}
        className="w-full rounded-md bg-[#aeffde] px-4 py-2 font-medium text-[#333333] transition-colors hover:bg-[#aeffde]/90 focus:ring-2 focus:ring-[#aeffde] focus:ring-offset-2 focus:ring-offset-[#333333] focus:outline-none disabled:cursor-not-allowed disabled:opacity-50"
      >
        {isLoading ? 'Entrando...' : 'Entrar'}
      </button>
    </form>
  );
}
