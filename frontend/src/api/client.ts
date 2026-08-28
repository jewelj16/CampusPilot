import type { ApiError, DayMenu, Registration } from "../types/mess";

const BASE = "/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const token = localStorage.getItem("token");
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${BASE}${path}`, {
    headers: { ...headers, ...(init?.headers || {}) },
    ...init,
  });

  if (!res.ok) {
    const body = (await res.json().catch(() => ({ detail: res.statusText }))) as ApiError;
    throw new Error(body.detail || `Request failed with ${res.status}`);
  }

  return res.status === 204 ? (undefined as T) : ((await res.json()) as T);
}

export const messApi = {
  getMenu: (days = 7) => request<DayMenu[]>(`/mess/menu?days=${days}`),
  myRegistrations: () => request<Registration[]>(`/mess/registrations/me`),
  register: (mealId: string) =>
    request<Registration>(`/mess/registrations`, {
      method: "POST",
      body: JSON.stringify({ meal_id: mealId }),
    }),
  cancel: (registrationId: string) =>
    request<Registration>(`/mess/registrations/${registrationId}`, {
      method: "DELETE",
    }),
};

export const authApi = {
  login: (data: any) =>
    request<{ access_token: string; token_type: string }>(`/auth/login`, {
      method: "POST",
      body: JSON.stringify(data),
    }),
  signup: (data: any) =>
    request<{ access_token: string; token_type: string }>(`/auth/signup`, {
      method: "POST",
      body: JSON.stringify(data),
    }),
  me: () => request<any>(`/auth/me`),
};
