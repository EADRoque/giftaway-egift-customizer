<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useGiftStore } from '@/stores/gift'
import type { Brand } from '@/types/gift'

const props = defineProps<{
  brand: Brand
}>()

const store = useGiftStore()

function onSelect() {
  store.setBrand(props.brand)
}
</script>

<template>
  <RouterLink
    :to="{ name: 'customize', params: { id: brand.id } }"
    @click="onSelect"
    class="group flex flex-col overflow-hidden rounded-2xl border border-stone-200/80 bg-white shadow-sm transition duration-300 hover:-translate-y-1 hover:border-violet-200 hover:shadow-xl hover:shadow-violet-500/10"
  >
    <div
      class="flex h-28 items-center justify-center bg-gradient-to-b from-stone-50 to-white p-6"
    >
      <img
        :src="brand.logoUrl"
        :alt="`${brand.name} logo`"
        class="max-h-12 w-auto object-contain opacity-90 transition group-hover:opacity-100"
      />
    </div>
    <div class="border-t border-stone-100 px-5 py-4 text-left">
      <h3 class="font-semibold text-ink">{{ brand.name }}</h3>
      <p class="mt-1 text-sm text-muted">Customize & send →</p>
    </div>
  </RouterLink>
</template>
