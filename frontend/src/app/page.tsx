export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-3xl flex-col items-center justify-center gap-8 px-8 py-16">
        {/* Logo/Title */}
        <div className="flex flex-col items-center gap-4 text-center">
          <div className="bg-primary flex h-20 w-20 items-center justify-center rounded-2xl text-4xl">
            🤖
          </div>
          <h1 className="text-4xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
            Dona Maria IA
          </h1>
          <p className="max-w-md text-lg text-zinc-600 dark:text-zinc-400">
            Uma assistente de IA que prioriza{' '}
            <span className="font-semibold text-zinc-900 dark:text-zinc-50">honestidade</span> e{' '}
            <span className="font-semibold text-zinc-900 dark:text-zinc-50">transparência</span>
          </p>
        </div>

        {/* Features */}
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="rounded-xl border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-900">
            <div className="mb-2 text-2xl">🎯</div>
            <h3 className="font-semibold text-zinc-900 dark:text-zinc-50">Níveis de Confiança</h3>
            <p className="text-sm text-zinc-600 dark:text-zinc-400">
              Expressa claramente quando tem certeza e quando não tem
            </p>
          </div>
          <div className="rounded-xl border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-900">
            <div className="mb-2 text-2xl">🔍</div>
            <h3 className="font-semibold text-zinc-900 dark:text-zinc-50">Pesquisa Automática</h3>
            <p className="text-sm text-zinc-600 dark:text-zinc-400">
              Busca informações quando detecta incerteza
            </p>
          </div>
          <div className="rounded-xl border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-900">
            <div className="mb-2 text-2xl">📊</div>
            <h3 className="font-semibold text-zinc-900 dark:text-zinc-50">Cita Fontes</h3>
            <p className="text-sm text-zinc-600 dark:text-zinc-400">
              Mostra de onde vêm as informações e o consenso entre elas
            </p>
          </div>
          <div className="rounded-xl border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-900">
            <div className="mb-2 text-2xl">💬</div>
            <h3 className="font-semibold text-zinc-900 dark:text-zinc-50">Admite Limitações</h3>
            <p className="text-sm text-zinc-600 dark:text-zinc-400">
              Reconhece quando não sabe algo de forma natural
            </p>
          </div>
        </div>

        {/* CTA */}
        <div className="flex flex-col items-center gap-4">
          <p className="text-sm text-zinc-500 dark:text-zinc-500">
            Em breve você poderá conversar com a Dona Maria
          </p>
          <a
            href="/docs"
            className="bg-primary rounded-full px-6 py-3 font-medium text-zinc-900 transition-opacity hover:opacity-80"
          >
            Documentação da API
          </a>
        </div>

        {/* Footer */}
        <footer className="mt-8 text-center text-sm text-zinc-400">
          <p>Desenvolvido com ❤️ por Melhorzin Official</p>
        </footer>
      </main>
    </div>
  );
}
