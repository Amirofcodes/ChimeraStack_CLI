import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { StatusTable } from './components/StatusTable';
import { QuickLinks } from './components/QuickLinks';
import { DatabaseStatus } from './components/DatabaseStatus';

const queryClient = new QueryClient();

export default function App() {
  const services = [
    {
      name: 'Frontend',
      details: 'React + TypeScript + Vite',
      port: import.meta.env.VITE_FRONTEND_PORT || '3000',
    },
    {
      name: 'Backend API',
      details: 'Symfony 6.4 + API Platform',
      url: `http://localhost:${import.meta.env.VITE_BACKEND_PORT}/api`,
      port: import.meta.env.VITE_BACKEND_PORT || '8000',
    },
    {
      name: 'Database',
      details: 'MySQL 8.0',
      port: import.meta.env.VITE_MYSQL_PORT || '3306',
    },
    {
      name: 'Database GUI',
      details: 'Adminer',
      url: `http://localhost:${import.meta.env.VITE_ADMINER_PORT}`,
      port: import.meta.env.VITE_ADMINER_PORT || '8080',
    },
  ];

  const quickLinks = [
    {
      name: 'API Documentation',
      url: `http://localhost:${import.meta.env.VITE_BACKEND_PORT}/api/docs`,
    },
    {
      name: 'Adminer',
      url: `http://localhost:${import.meta.env.VITE_ADMINER_PORT}`,
    },
  ];

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gray-100">
        <header className="bg-white shadow">
          <div className="max-w-7xl mx-auto py-6 px-4">
            <h1 className="text-3xl font-bold text-gray-900">
              ChimeraStack React + Symfony Development Environment
            </h1>
          </div>
        </header>

        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0 space-y-6">
            <section>
              <h2 className="text-xl font-bold mb-4">Stack Overview</h2>
              <StatusTable services={services} />
            </section>

            <section>
              <QuickLinks links={quickLinks} />
            </section>

            <section>
              <h2 className="text-xl font-bold mb-4">Database Connection Status</h2>
              <DatabaseStatus />
            </section>
          </div>
        </main>
      </div>
    </QueryClientProvider>
  );
}