import React from 'react';
import { useQuery } from '@tanstack/react-query';
import apiClient from '../api/client';
import type { DatabaseStatus as DBStatus } from '../types/api';

export function DatabaseStatus() {
  const { data, error, isLoading } = useQuery<DBStatus>({
    queryKey: ['dbStatus'],
    queryFn: async () => {
      const response = await apiClient.get('/api/health/db');
      return response.data;
    },
    retry: 1,
    refetchOnWindowFocus: false
  });

  if (isLoading) {
    return <div className="animate-pulse">Checking database connection...</div>;
  }

  if (error || !data?.success) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
        <strong className="font-bold">Connection Error: </strong>
        <span className="block sm:inline">
          {data?.message || (error as Error)?.message || 'Failed to connect to database'}
        </span>
        {data?.config && (
          <pre className="mt-2 text-sm overflow-x-auto">
            {JSON.stringify(data.config, null, 2)}
          </pre>
        )}
      </div>
    );
  }

  return (
    <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
      <div className="flex items-center">
        <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
        </svg>
        <div>
          <p className="font-bold">Connected to MySQL {data.version}</p>
          <p>Database: {data.config?.database}</p>
          <p>User: {data.config?.user}</p>
        </div>
      </div>
    </div>
  );
}