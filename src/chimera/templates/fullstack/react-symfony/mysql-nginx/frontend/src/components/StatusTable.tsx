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