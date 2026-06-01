<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { computed } from 'vue'
import { useGiftStore } from '@/stores/gift'
import WizardStepAmount from './WizardStepAmount.vue'
import WizardStepMessage from './WizardStepMessage.vue'
import WizardStepReview from './WizardStepReview.vue'

const emit = defineEmits<{
  checkout: []
}>()

const store = useGiftStore()
const { currentStep, isStep1Valid, isStep2Valid } = storeToRefs(store)

const steps = [
  { number: 1, title: 'Amount & theme' },
  { number: 2, title: 'Details & message' },
  { number: 3, title: 'Review & send' },
]

const canGoNext = computed(() => {
  if (currentStep.value === 1) return isStep1Valid.value
  if (currentStep.value === 2) return isStep2Valid.value
  return false
})
</script>

<template>
  <div class="rounded-2xl border border-stone-200/80 bg-white p-6 shadow-sm sm:p-8">
    <nav aria-label="Checkout progress" class="mb-8">
      <ol class="flex gap-2 sm:gap-4">
        <li
          v-for="step in steps"
          :key="step.number"
          class="flex flex-1 flex-col items-center gap-2"
        >
          <span
            class="flex h-8 w-8 items-center justify-center rounded-full text-sm font-semibold transition-all duration-300"
            :class="
              currentStep >= step.number
                ? 'bg-violet-600 text-white shadow-md shadow-violet-500/30'
                : 'bg-stone-100 text-stone-400'
            "
          >
            {{ step.number }}
          </span>
          <span
            class="hidden text-center text-xs font-medium sm:block"
            :class="currentStep >= step.number ? 'text-ink' : 'text-stone-400'"
          >
            {{ step.title }}
          </span>
        </li>
      </ol>
      <div class="mt-4 h-1 overflow-hidden rounded-full bg-stone-100">
        <div
          class="h-full rounded-full bg-gradient-to-r from-violet-600 to-fuchsia-500 transition-all duration-500 ease-out"
          :style="{ width: `${((currentStep - 1) / 2) * 100}%` }"
        />
      </div>
    </nav>

    <Transition name="wizard-fade" mode="out-in">
      <WizardStepAmount v-if="currentStep === 1" key="step-1" />
      <WizardStepMessage v-else-if="currentStep === 2" key="step-2" />
      <WizardStepReview v-else key="step-3" @checkout="emit('checkout')" />
    </Transition>

    <div
      v-if="currentStep < 3"
      class="mt-8 flex flex-col-reverse gap-3 border-t border-stone-100 pt-6 sm:flex-row sm:justify-between"
    >
      <button
        type="button"
        class="rounded-xl px-5 py-2.5 text-sm font-medium text-muted transition hover:bg-stone-100 hover:text-ink disabled:invisible"
        :disabled="currentStep === 1"
        @click="store.prevStep()"
      >
        Back
      </button>
      <button
        type="button"
        class="rounded-xl bg-ink px-6 py-2.5 text-sm font-semibold text-white shadow-md transition hover:bg-stone-800 disabled:cursor-not-allowed disabled:opacity-40"
        :disabled="!canGoNext"
        @click="store.nextStep()"
      >
        Continue
      </button>
    </div>
  </div>
</template>

<style scoped>
.wizard-fade-enter-active,
.wizard-fade-leave-active {
  transition:
    opacity 0.25s ease,
    transform 0.25s ease;
}

.wizard-fade-enter-from,
.wizard-fade-leave-to {
  opacity: 0;
  transform: translateY(8px);
}
</style>
