'use client';

import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { useAuth } from '@/hooks/useAuth';

/**
 * Schema de validação para o formulário de registro.
 */
const registerSchema = z
  .object({
    email: z.string().email('Email inválido'),
    password: z.string().min(8, 'Senha deve ter no mínimo 8 caracteres'),
    confirmPassword: z.string(),
  })
  .refine(data => data.password === data.confirmPassword, {
    message: 'Senhas não conferem',
    path: ['confirmPassword'],
  });

type RegisterFormData = z.infer<typeof registerSchema>;

/**
 * Componente de formulário de registro de usuário.
 *
 * Inclui validação client-side e feedback visual de loading/erros.
 */
export function RegisterForm() {
  const { register: registerUser, isLoading, error, clearError } = useAuth();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterFormData) => {
    clearError();
    await registerUser({
      email: data.email,
      password: data.password,
    });
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
          placeholder="Mínimo 8 caracteres"
          disabled={isLoading}
        />
        {errors.password && (
          <p className="mt-1 text-sm text-[#ff8080]">{errors.password.message}</p>
        )}
      </div>

      {/* Campo Confirmar Senha */}
      <div>
        <label htmlFor="confirmPassword" className="mb-2 block text-sm font-medium text-[#e4f1ff]">
          Confirmar Senha
        </label>
        <input
          id="confirmPassword"
          type="password"
          {...register('confirmPassword')}
          className="w-full rounded-md border border-[#e4f1ff]/20 bg-[#333333] px-4 py-2 text-white placeholder-[#e4f1ff]/50 focus:border-[#aeffde] focus:ring-1 focus:ring-[#aeffde] focus:outline-none"
          placeholder="Repita a senha"
          disabled={isLoading}
        />
        {errors.confirmPassword && (
          <p className="mt-1 text-sm text-[#ff8080]">{errors.confirmPassword.message}</p>
        )}
      </div>

      {/* Botão Submit */}
      <button
        type="submit"
        disabled={isLoading}
        className="w-full rounded-md bg-[#aeffde] px-4 py-2 font-medium text-[#333333] transition-colors hover:bg-[#aeffde]/90 focus:ring-2 focus:ring-[#aeffde] focus:ring-offset-2 focus:ring-offset-[#333333] focus:outline-none disabled:cursor-not-allowed disabled:opacity-50"
      >
        {isLoading ? 'Criando conta...' : 'Criar conta'}
      </button>
    </form>
  );
}
