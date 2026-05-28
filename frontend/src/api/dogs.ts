import type { Dog, DogCreatePayload, DogUpdatePayload } from "../types/dog";

const API_BASE = "/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    const detail = await response.text();
    let message = `Request failed (${response.status})`;
    try {
      const body = JSON.parse(detail) as { detail?: string };
      if (typeof body.detail === "string" && body.detail !== "Not Found") {
        message = body.detail;
      } else if (response.status === 404) {
        message = "Could not reach the diary API. Check that the backend is running.";
      }
    } catch {
      if (detail) {
        message = detail;
      }
    }
    throw new Error(message);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export function listDogs(): Promise<Dog[]> {
  return request<Dog[]>("/dogs");
}

export function getDog(id: string): Promise<Dog> {
  return request<Dog>(`/dogs/${id}`);
}

export function createDog(payload: DogCreatePayload): Promise<Dog> {
  return request<Dog>("/dogs", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updateDog(id: string, payload: DogUpdatePayload): Promise<Dog> {
  return request<Dog>(`/dogs/${id}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export function deleteDog(id: string): Promise<void> {
  return request<void>(`/dogs/${id}`, { method: "DELETE" });
}
