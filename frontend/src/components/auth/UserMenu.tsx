'use client';

import { useState, useRef, useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';

/**
 * Menu de usuário com opção de logout.
 */
export function UserMenu() {
  const { logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  // Fechar menu ao clicar fora
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogout = async () => {
    setIsOpen(false);
    await logout();
  };

  return (
    <div className="relative" ref={menuRef}>
      {/* Botão do Menu */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 rounded-full bg-[#e4f1ff]/10 px-4 py-2 text-[#e4f1ff] transition-colors hover:bg-[#e4f1ff]/20 focus:ring-2 focus:ring-[#aeffde] focus:outline-none"
        aria-haspopup="true"
        aria-expanded={isOpen}
      >
        {/* Ícone de usuário */}
        <svg
          className="h-5 w-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
          />
        </svg>
        {/* Seta dropdown */}
        <svg
          className={`h-4 w-4 transition-transform ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Menu Dropdown */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 rounded-md border border-[#e4f1ff]/10 bg-[#333333] py-1 shadow-lg">
          <button
            onClick={handleLogout}
            className="flex w-full items-center gap-2 px-4 py-2 text-left text-[#e4f1ff] transition-colors hover:bg-[#e4f1ff]/10"
          >
            {/* Ícone de logout */}
            <svg
              className="h-5 w-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
              />
            </svg>
            Sair
          </button>
        </div>
      )}
    </div>
  );
}
