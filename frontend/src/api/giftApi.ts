import type { Brand, CheckoutPayload, CheckoutResult } from '@/types/gift'

function getApiBaseUrl(): string {
  const fromEnv = import.meta.env.VITE_API_BASE_URL as string | undefined
  if (fromEnv?.trim()) {
    return fromEnv.trim().replace(/\/$/, '')
  }
  
  // Force it to point to your FastAPI backend port 8000
  return 'http://localhost:8080'
}

const baseUrl = getApiBaseUrl()

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const hasBody = init?.body != null
  const response = await fetch(`${baseUrl}${path}`, {
    ...init,
    headers: {
      ...(hasBody ? { 'Content-Type': 'application/json' } : {}),
      ...init?.headers,
    },
  })

  if (!response.ok) {
    const detail = await response.text()
    throw new Error(detail || `Request failed (${response.status})`)
  }

  return response.json() as Promise<T>
}

export function fetchBrands(): Promise<Brand[]> {
  return request<Brand[]>('/api/brands')
}

export function submitCheckout(payload: CheckoutPayload): Promise<CheckoutResult> {
  return request<CheckoutResult>('/api/checkout', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}
