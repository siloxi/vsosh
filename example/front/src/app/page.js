'use client';

import Link from 'next/link';

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-100 via-purple-100 to-blue-100 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">My Notes</h1>
          <p className="text-gray-600">Organize your thoughts and ideas</p>
        </header>

        {/* Center Card */}
        <div className="bg-white rounded-3xl shadow-2xl p-12 text-center backdrop-blur-sm bg-opacity-95">
          <div className="mb-6">
            <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-10 h-10 text-blue-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15V5a2 2 0 0 0-2-2H7l-4 4v8a2 2 0 0 0 2 2h12" />
                <path d="M17 21v-4a2 2 0 0 0-2-2H7" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Welcome</h2>
            <p className="text-gray-600 mb-6">Quickly access your notes and stay organized.</p>
          </div>

          <Link href="/notes" className="inline-block bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white font-bold py-3 px-8 rounded-xl transition-all duration-200 transform hover:scale-105 active:scale-95 shadow-lg">
              To notes
          </Link>
        </div>
      </div>
    </main>
  );
}
