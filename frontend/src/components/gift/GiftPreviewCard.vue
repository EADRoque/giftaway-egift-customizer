<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { computed } from 'vue'
import { useGiftStore } from '@/stores/gift'

const store = useGiftStore()
const {
  selectedBrand,
  personalMessage,
  recipientName,
  senderName,
  themeColor,
  formattedAmount,
} = storeToRefs(store)

const cardStyle = computed(() => ({
  background: `linear-gradient(135deg, ${themeColor.value} 0%, color-mix(in srgb, ${themeColor.value} 70%, #000) 100%)`,
}))

const displayMessage = computed(
  () => personalMessage.value.trim() || 'Your personal message appears here…',
)
</script>

<template>
  <div class="w-full max-w-sm">
    <p class="mb-3 text-center text-xs font-medium uppercase tracking-widest text-muted sm:text-left">
      Live preview
    </p>
    <div
      class="relative aspect-[1.6/1] overflow-hidden rounded-2xl p-6 text-white shadow-2xl shadow-stone-900/20 ring-1 ring-white/20 transition-all duration-500"
      :style="cardStyle"
    >
      <div
        class="pointer-events-none absolute -right-8 -top-8 h-32 w-32 rounded-full bg-white/10 blur-2xl"
      />
      <div
        class="pointer-events-none absolute -bottom-10 -left-6 h-28 w-28 rounded-full bg-black/10 blur-xl"
      />

      <div class="relative flex h-full flex-col justify-between">
        <div class="flex items-start justify-between gap-3">
          <div>
            <p class="text-[10px] font-medium uppercase tracking-[0.2em] text-white/70">
              E-Gift Card
            </p>
            <p v-if="selectedBrand" class="mt-1 text-lg font-semibold">
              {{ selectedBrand.name }}
            </p>
            <p v-else class="mt-1 text-lg font-semibold text-white/80">Select a brand</p>
          </div>
          <img
            v-if="selectedBrand"
            :src="selectedBrand.logoUrl"
            :alt="selectedBrand.name"
            class="h-8 w-auto rounded bg-white/95 px-2 py-1 object-contain"
          />
        </div>

        <div>
          <p class="text-4xl font-bold tracking-tight">{{ formattedAmount }}</p>
          <p
            class="mt-3 line-clamp-3 text-sm leading-relaxed text-white/90 transition-opacity duration-300"
            :class="{ 'italic text-white/60': !personalMessage.trim() }"
          >
            {{ displayMessage }}
          </p>
        </div>

        <div class="border-t border-white/20 pt-3">
          <p class="text-[10px] uppercase tracking-wider text-white/60">From</p>
          <p class="text-sm font-medium">
            {{ senderName.trim() || 'Your name' }}
          </p>
          <p class="mt-2 text-[10px] uppercase tracking-wider text-white/60">To</p>
          <p class="font-medium">
            {{ recipientName.trim() || 'Recipient name' }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
