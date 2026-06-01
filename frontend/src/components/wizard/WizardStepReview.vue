<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { RouterLink } from 'vue-router'
import { useGiftStore } from '@/stores/gift'

const emit = defineEmits<{
  checkout: []
}>()

const store = useGiftStore()
const {
  selectedBrand,
  recipientName,
  recipientEmail,
  senderName,
  personalMessage,
  themeColor,
  formattedAmount,
  checkoutResult,
  isSubmitting,
} = storeToRefs(store)
</script>

<template>
  <div>
    <template v-if="checkoutResult">
      <div
        class="rounded-2xl border border-emerald-200 bg-emerald-50/80 p-6 text-center"
      >
        <div
          class="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-emerald-500 text-2xl text-white shadow-lg shadow-emerald-500/30"
        >
          ✓
        </div>
        <h2 class="text-xl font-semibold text-emerald-900">Gift sent!</h2>
        <p class="mt-2 text-sm text-emerald-800">{{ checkoutResult.message }}</p>
        <p class="mt-4 font-mono text-lg font-bold tracking-widest text-emerald-900">
          {{ checkoutResult.giftCode }}
        </p>
        <p class="mt-1 text-xs text-emerald-700">Gift code</p>
        <p class="mt-3 font-mono text-sm text-emerald-800">
          Order ID: {{ checkoutResult.orderId }}
        </p>
        <p v-if="checkoutResult.emailQueued" class="mt-3 text-sm text-emerald-700">
          A voucher email is on its way to {{ recipientEmail }}.
        </p>
        <p v-else class="mt-3 text-sm text-amber-700">
          Email delivery was skipped (SMTP not configured on the server).
        </p>
        <RouterLink
          to="/"
          class="mt-6 inline-flex rounded-xl bg-emerald-600 px-6 py-2.5 text-sm font-semibold text-white transition hover:bg-emerald-700"
        >
          Send another gift
        </RouterLink>
      </div>
    </template>

    <template v-else>
      <h2 class="text-xl font-semibold text-ink">Review & checkout</h2>
      <p class="mt-1 text-sm text-muted">Confirm the details before sending.</p>

      <dl class="mt-6 space-y-4 rounded-xl bg-stone-50 p-5 text-sm">
        <div class="flex justify-between gap-4 border-b border-stone-200/80 pb-3">
          <dt class="text-muted">Brand</dt>
          <dd class="font-medium text-ink">{{ selectedBrand?.name }}</dd>
        </div>
        <div class="flex justify-between gap-4 border-b border-stone-200/80 pb-3">
          <dt class="text-muted">Amount</dt>
          <dd class="font-medium text-ink">{{ formattedAmount }}</dd>
        </div>
        <div class="flex justify-between gap-4 border-b border-stone-200/80 pb-3">
          <dt class="text-muted">From</dt>
          <dd class="font-medium text-ink">{{ senderName }}</dd>
        </div>
        <div class="flex justify-between gap-4 border-b border-stone-200/80 pb-3">
          <dt class="text-muted">Recipient</dt>
          <dd class="text-right font-medium text-ink">
            {{ recipientName }}<br />
            <span class="text-xs font-normal text-muted">{{ recipientEmail }}</span>
          </dd>
        </div>
        <div class="flex justify-between gap-4 border-b border-stone-200/80 pb-3">
          <dt class="text-muted">Theme</dt>
          <dd class="flex items-center gap-2 font-medium text-ink">
            <span
              class="h-4 w-4 rounded-full ring-1 ring-black/10"
              :style="{ backgroundColor: themeColor }"
            />
            Custom
          </dd>
        </div>
        <div>
          <dt class="text-muted">Message</dt>
          <dd class="mt-1 font-medium text-ink">
            {{ personalMessage || '—' }}
          </dd>
        </div>
      </dl>

      <button
        type="button"
        class="mt-6 w-full rounded-xl bg-gradient-to-r from-violet-600 to-fuchsia-500 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-violet-500/25 transition hover:shadow-xl hover:shadow-violet-500/30 disabled:cursor-not-allowed disabled:opacity-60"
        :disabled="isSubmitting"
        @click="emit('checkout')"
      >
        {{ isSubmitting ? 'Processing…' : 'Complete checkout' }}
      </button>

      <button
        type="button"
        class="mt-3 w-full rounded-xl py-2.5 text-sm font-medium text-muted transition hover:bg-stone-100"
        :disabled="isSubmitting"
        @click="store.prevStep()"
      >
        Back
      </button>
    </template>
  </div>
</template>
