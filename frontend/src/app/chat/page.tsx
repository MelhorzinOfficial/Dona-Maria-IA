'use client';

import { UserMenu } from '@/components/auth/UserMenu';
import { withAuth } from '@/components/auth/withAuth';

/**
 * Página principal do chat.
 *
 * Protegida - requer autenticação.
 */
function ChatPage() {
  return (
    <div className="flex min-h-screen flex-col bg-[#333333]">
      {/* Header */}
      <header className="border-b border-[#e4f1ff]/10 px-6 py-4">
        <div className="mx-auto flex max-w-4xl items-center justify-between">
          <h1 className="text-xl font-bold text-[#aeffde]">Dona Maria</h1>
          <UserMenu />
        </div>
      </header>

      {/* Main Content */}
      <main className="flex flex-1 items-center justify-center">
        <div className="text-center">
          <p className="text-lg text-[#e4f1ff]">Bem-vindo ao chat!</p>
          <p className="mt-2 text-sm text-[#e4f1ff]/50">
            O chat será implementado na próxima sprint.
          </p>
        </div>
      </main>
    </div>
  );
}

export default withAuth(ChatPage);
