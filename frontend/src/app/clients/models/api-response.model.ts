import { Client } from './client.model';

export interface ApiResponse {
  response_id: string;
  path: string;
  method: string;
  request: number;
  msg: string;
  'api-version': string;
  status: string;
  service: string;
  data: {
    items: Client[];
  };
}
