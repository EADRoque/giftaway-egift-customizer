<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { fetchBrands } from '@/api/giftApi'
import BrandCard from '@/components/brand/BrandCard.vue'
import { useGiftStore } from '@/stores/gift'
import type { Brand } from '@/types/gift'

const store = useGiftStore()
const brands = ref<Brand[]>([])
const isLoading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  store.resetAll()
  try {
    brands.value = await fetchBrands()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to load brands'
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <section class="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8 lg:py-14">
    <div class="max-w-2xl">
      <p class="text-sm font-medium uppercase tracking-widest text-violet-600">
        Digital gifting
      </p>
      <h1 class="mt-2 text-3xl font-bold tracking-tight text-ink sm:text-4xl lg:text-5xl">
        Send a premium e-gift in minutes
      </h1>
      <p class="mt-4 text-lg text-muted">
        Choose a brand, customize the card, and deliver a thoughtful gift—no plastic required.
      </p>
    </div>

    <div v-if="isLoading" class="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="n in 5"
        :key="n"
        class="h-44 animate-pulse rounded-2xl bg-stone-200/60"
      />
    </div>

    <div
      v-else-if="error"
      class="mt-12 rounded-2xl border border-red-200 bg-red-50 p-6 text-red-800"
    >
      <p class="font-medium">Could not load brands</p>
      <p class="mt-1 text-sm">{{ error }}</p>
      <p class="mt-2 text-sm text-red-700">
        Start the API with
        <code class="rounded bg-red-100 px-1">uvicorn main:app --reload --port 8000</code>
        in the <code class="rounded bg-red-100 px-1">backend</code> folder, then restart
        <code class="rounded bg-red-100 px-1">npm run dev</code>.
      </p>
    </div>

    <div
      v-else
      class="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-3"
    >
      <BrandCard v-for="brand in brands" :key="brand.id" :brand="brand" />
    </div>
  </section>
</template>
