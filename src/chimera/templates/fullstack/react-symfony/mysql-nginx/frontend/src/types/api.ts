export interface DatabaseStatus {
  success: boolean;
  version?: string;
  message?: string;
  config?: {
    host: string;
    port: number;
    database: string;
    user: string;
  };
}