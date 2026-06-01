export interface Brand {
  id: string
  name: string
  logoUrl: string
}

export interface CheckoutPayload {
  brand: Pick<Brand, 'id' | 'name'>
  giftAmount: number
  recipientName: string
  recipientEmail: string
  senderName: string
  personalMessage: string
  themeColor: string
}

export interface CheckoutResult {
  success: boolean
  orderId: string
  giftCode: string
  message: string
  emailQueued: boolean
}

export const THEME_COLORS = [
  { id: 'midnight', label: 'Midnight', value: '#1e3a5f' },
  { id: 'violet', label: 'Violet', value: '#6d28d9' },
  { id: 'rose', label: 'Rose', value: '#be185d' },
  { id: 'teal', label: 'Teal', value: '#0f766e' },
  { id: 'gold', label: 'Gold', value: '#b45309' },
] as const

export const PRESET_AMOUNTS = [25, 50, 75, 100, 150] as const

export const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
