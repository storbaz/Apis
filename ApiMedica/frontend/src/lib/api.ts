const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001";

interface FetchOptions extends RequestInit {
  apiKey?: string;
  token?: string;
}

async function apiFetch<T>(path: string, options: FetchOptions = {}): Promise<T> {
  const { apiKey, token, ...fetchOptions } = options;
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  if (apiKey) headers["X-API-Key"] = apiKey;
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, {
    ...fetchOptions,
    headers,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || `API error: ${res.status}`);
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}

export interface User {
  id: number;
  email: string;
  full_name: string | null;
  company: string | null;
  plan: string;
  is_active: boolean;
  created_at: string;
}

export interface ApiKeyItem {
  id: number;
  key: string;
  name: string;
  rate_limit: number;
  is_active: boolean;
  created_at: string;
  last_used_at: string | null;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface ProductionRecord {
  country: string;
  country_code: string;
  year: number;
  variety: string;
  bags_60kg: number | null;
  tonnes: number | null;
  source: string | null;
}

export interface PriceRecord {
  date: string;
  variety: string;
  price_usd_cents_per_lb: number;
  source: string | null;
}

export interface Overview {
  total_countries: number;
  latest_year: number;
  total_production_bags: number;
  top_producer: string;
  top_producer_bags: number;
}

export const api = {
  auth: {
    register: (data: { email: string; password: string; full_name?: string; company?: string }) =>
      apiFetch<User>("/v1/auth/register", { method: "POST", body: JSON.stringify(data) }),
    login: (data: { email: string; password: string }) =>
      apiFetch<{ access_token: string; token_type: string; user_id: number; plan: string }>(
        "/v1/auth/login",
        { method: "POST", body: JSON.stringify(data) }
      ),
    me: (token: string) => apiFetch<User>("/v1/auth/me", { token }),
  },
  apiKeys: {
    list: (token: string) =>
      apiFetch<{ keys: ApiKeyItem[]; total: number }>("/v1/api-keys", { token }),
    create: (token: string, name: string) =>
      apiFetch<ApiKeyItem>("/v1/api-keys", {
        method: "POST",
        body: JSON.stringify({ name }),
        token,
      }),
    revoke: (token: string, id: number) =>
      apiFetch<void>(`/v1/api-keys/${id}`, { method: "DELETE", token }),
  },
  production: {
    list: (apiKey: string, params?: Record<string, string>) => {
      const qs = params ? "?" + new URLSearchParams(params).toString() : "";
      return apiFetch<PaginatedResponse<ProductionRecord>>(`/v1/production${qs}`, { apiKey });
    },
    overview: (apiKey: string) =>
      apiFetch<Overview>("/v1/overview", { apiKey }),
  },
  prices: {
    list: (apiKey: string, params?: Record<string, string>) => {
      const qs = params ? "?" + new URLSearchParams(params).toString() : "";
      return apiFetch<PaginatedResponse<PriceRecord>>(`/v1/prices${qs}`, { apiKey });
    },
    latest: (apiKey: string, variety = "arabica") =>
      apiFetch<{ data: PriceRecord | null }>(`/v1/prices/latest?variety=${variety}`, { apiKey }),
  },
};
