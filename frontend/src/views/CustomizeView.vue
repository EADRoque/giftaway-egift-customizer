<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { fetchBrands, submitCheckout } from '@/api/giftApi'
import GiftPreviewCard from '@/components/gift/GiftPreviewCard.vue'
import FormWizard from '@/components/wizard/FormWizard.vue'
import { useGiftStore } from '@/stores/gift'

const route = useRoute()
const router = useRouter()
const store = useGiftStore()

const isLoading = ref(true)
const error = ref<string | null>(null)
const checkoutError = ref<string | null>(null)

function formatCheckoutError(err: unknown): string {
  if (!(err instanceof Error)) return 'Checkout failed'
  try {
    const body = JSON.parse(err.message) as { detail?: unknown }
    if (Array.isArray(body.detail)) {
      return body.detail
        .map((item: { msg?: string; loc?: string[] }) => {
          const field = item.loc?.slice(-1)[0] ?? 'field'
          return `${field}: ${item.msg ?? 'invalid'}`
        })
        .join('; ')
    }
  } catch {
    /* plain text error */
  }
  return err.message
}

async function loadBrand(id: string) {
  isLoading.value = true
  error.value = null
  try {
    const brands = await fetchBrands()
    const brand = brands.find((b) => b.id === id)
    if (!brand) {
      error.value = 'Brand not found'
      return
    }
    store.setBrand(brand)
    store.resetFlow()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to load brand'
  } finally {
    isLoading.value = false
  }
}

async function handleCheckout() {
  if (!store.selectedBrand) return
  checkoutError.value = null
  store.isSubmitting = true
  try {
    store.checkoutResult = await submitCheckout({
      brand: { id: store.selectedBrand.id, name: store.selectedBrand.name },
      giftAmount: store.giftAmount,
      recipientName: store.recipientName.trim(),
      recipientEmail: store.recipientEmail.trim(),
      senderName: store.senderName.trim(),
      personalMessage: store.personalMessage.trim(),
      themeColor: store.themeColor,
    })
  } catch (e) {
    checkoutError.value = formatCheckoutError(e)
  } finally {
    store.isSubmitting = false
  }
}

onMounted(() => {
  const id = route.params.id as string
  if (id) loadBrand(id)
})

watch(
  () => route.params.id,
  (id) => {
    if (typeof id === 'string' && id) loadBrand(id)
  },
)
</script>

<template>
  <section class="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8 lg:py-12">
    <button
      type="button"
      class="mb-6 inline-flex items-center gap-1 text-sm font-medium text-muted transition hover:text-ink"
      @click="router.push('/')"
    >
      ← Back to brands
    </button>

    <div v-if="isLoading" class="py-20 text-center text-muted">Loading…</div>

    <div
      v-else-if="error"
      class="rounded-2xl border border-red-200 bg-red-50 p-6 text-red-800"
    >
      {{ error }}
      <button
        type="button"
        class="mt-4 block text-sm font-semibold underline"
        @click="router.push('/')"
      >
        Return home
      </button>
    </div>

    <template v-else-if="store.selectedBrand">
      <div class="mb-8">
        <h1 class="text-2xl font-bold tracking-tight text-ink sm:text-3xl">
          Customize your {{ store.selectedBrand.name }} gift
        </h1>
        <p class="mt-2 text-muted">Design your card—the preview updates as you type.</p>
      </div>

      <div class="lg:grid lg:grid-cols-[1fr_320px] lg:items-start lg:gap-10 xl:gap-14">
        <div class="min-w-0">
          <div
            v-if="checkoutError"
            class="mb-4 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800"
          >
            {{ checkoutError }}
          </div>
          <FormWizard @checkout="handleCheckout" />
        </div>

        <aside class="mt-8 lg:sticky lg:top-8 lg:mt-0">
          <GiftPreviewCard />
        </aside>
      </div>
    </template>
  </section>
</template>
