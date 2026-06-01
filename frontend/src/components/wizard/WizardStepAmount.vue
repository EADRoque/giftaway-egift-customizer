<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useGiftStore } from '@/stores/gift'
import { PRESET_AMOUNTS, THEME_COLORS } from '@/types/gift'

const store = useGiftStore()
const { giftAmount, themeColor } = storeToRefs(store)

function selectAmount(amount: number) {
  giftAmount.value = amount
}
</script>

<template>
  <div>
    <h2 class="text-xl font-semibold text-ink">Choose amount & theme</h2>
    <p class="mt-1 text-sm text-muted">Pick a value and a card color for your gift.</p>

    <div class="mt-6">
      <label class="text-sm font-medium text-ink">Gift amount</label>
      <div class="mt-3 flex flex-wrap gap-2">
        <button
          v-for="amount in PRESET_AMOUNTS"
          :key="amount"
          type="button"
          class="rounded-xl border px-4 py-2.5 text-sm font-semibold transition duration-200"
          :class="
            giftAmount === amount
              ? 'border-violet-500 bg-violet-50 text-violet-700 shadow-sm'
              : 'border-stone-200 bg-white text-ink hover:border-violet-200 hover:bg-violet-50/50'
          "
          @click="selectAmount(amount)"
        >
          ${{ amount }}
        </button>
      </div>
      <div class="mt-4">
        <label for="custom-amount" class="text-sm text-muted">Custom amount (USD)</label>
        <div class="relative mt-2 max-w-xs">
          <span class="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-muted"
            >$</span
          >
          <input
            id="custom-amount"
            v-model.number="giftAmount"
            type="number"
            min="1"
            max="500"
            step="1"
            class="w-full rounded-xl border border-stone-200 py-2.5 pl-8 pr-4 text-ink outline-none transition focus:border-violet-400 focus:ring-2 focus:ring-violet-100"
          />
        </div>
      </div>
    </div>

    <div class="mt-8">
      <label class="text-sm font-medium text-ink">Card theme</label>
      <div class="mt-3 flex flex-wrap gap-3">
        <button
          v-for="theme in THEME_COLORS"
          :key="theme.id"
          type="button"
          class="flex items-center gap-2 rounded-xl border px-3 py-2 text-sm transition duration-200"
          :class="
            themeColor === theme.value
              ? 'border-violet-500 bg-violet-50 ring-2 ring-violet-200'
              : 'border-stone-200 hover:border-stone-300'
          "
          :aria-pressed="themeColor === theme.value"
          @click="themeColor = theme.value"
        >
          <span
            class="h-6 w-6 rounded-full shadow-inner ring-1 ring-black/10"
            :style="{ backgroundColor: theme.value }"
          />
          {{ theme.label }}
        </button>
      </div>
    </div>
  </div>
</template>
