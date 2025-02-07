import axios from 'axios';

const baseURL = import.meta.env.VITE_API_URL || `http://localhost:${process.env.BACKEND_PORT}`;

export const apiClient = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

# frontend/src/types/api.ts
export interface DatabaseStatus {
  success: boolean;
  version?: string;
  message?: string;
  config?: {
    host: string;
    port: string;
    database: string;
    user: string;
  };
}

# frontend/src/components/StatusTable.tsx
import React from 'react';

interface Service {
  name: string;
  details: string;
  url?: string;
  port: string;
}

interface StatusTableProps {
  services: Service[];
}

export function StatusTable({ services }: StatusTableProps) {
  return (
    <table className="w-full border-collapse">
      <thead>
        <tr>
          <th className="p-2 border text-left">Component</th>
          <th className="p-2 border text-left">Details</th>
          <th className="p-2 border text-left">Access</th>
        </tr>
      </thead>
      <tbody>
        {services.map((service) => (
          <tr key={service.name}>
            <td className="p-2 border font-medium">{service.name}</td>
            <td className="p-2 border">{service.details}</td>
            <td className="p-2 border">
              {service.url ? (
                <a
                  href={service.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800"
                >
                  localhost:{service.port}
                </a>
              ) : (
                `localhost:${service.port}`
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

# frontend/src/components/QuickLinks.tsx
import React from 'react';

interface QuickLink {
  name: string;
  url: string;
}

interface QuickLinksProps {
  links: QuickLink[];
}

export function QuickLinks({ links }: QuickLinksProps) {
  return (
    <div className="space-y-2">
      <h2 className="text-xl font-bold mb-4">Quick Links</h2>
      <ul className="space-y-2">
        {links.map((link) => (
          <li key={link.name}>
            <a
              href={link.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-800"
            >
              {link.name}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}

# frontend/src/components/DatabaseStatus.tsx
import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import type { DatabaseStatus as DBStatus } from '../types/api';

export function DatabaseStatus() {
  const { data, error, isLoading } = useQuery<DBStatus>({
    queryKey: ['dbStatus'],
    queryFn: async () => {
      const response = await apiClient.get('/api/health/db');
      return response.data;
    },
  });

  if (isLoading) return <div>Checking database connection...</div>;

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        Failed to connect to database
      </div>
    );
  }

  if (!data?.success) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        {data?.message || 'Database connection error'}
        {data?.config && (
          <pre className="mt-2 text-sm">
            {JSON.stringify(data.config, null, 2)}
          </pre>
        )}
      </div>
    );
  }

  return (
    <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
      ✓ Connected to MySQL Server {data.version}
      <br />
      Database: {data.config?.database}
      <br />
      User: {data.config?.user}
    </div>
  );
}

# frontend/src/App.tsx
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
      port: process.env.FRONTEND_PORT || '3000',
    },
    {
      name: 'Backend API',
      details: 'Symfony 6.4 + API Platform',
      url: `http://localhost:${process.env.BACKEND_PORT}/api`,
      port: process.env.BACKEND_PORT || '8000',
    },
    {
      name: 'Database',
      details: 'MySQL 8.0',
      port: process.env.MYSQL_PORT || '3306',
    },
    {
      name: 'Database GUI',
      details: 'Adminer',
      url: `http://localhost:${process.env.ADMINER_PORT}`,
      port: process.env.ADMINER_PORT || '8080',
    },
  ];

  const quickLinks = [
    {
      name: 'API Documentation',
      url: `http://localhost:${process.env.BACKEND_PORT}/api/docs`,
    },
    {
      name: 'Adminer',
      url: `http://localhost:${process.env.ADMINER_PORT}`,
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