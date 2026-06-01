import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import type { Brand, CheckoutResult } from '@/types/gift'
import { EMAIL_PATTERN, THEME_COLORS } from '@/types/gift'

export const useGiftStore = defineStore('gift', () => {
  const selectedBrand = ref<Brand | null>(null)
  const giftAmount = ref(50)
  const recipientName = ref('')
  const recipientEmail = ref('')
  const senderName = ref('')
  const personalMessage = ref('')
  const themeColor = ref<string>(THEME_COLORS[0].value)
  const currentStep = ref(1)
  const checkoutResult = ref<CheckoutResult | null>(null)
  const isSubmitting = ref(false)

  const formattedAmount = computed(() =>
    new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0,
    }).format(giftAmount.value),
  )

  const isRecipientEmailValid = computed(() =>
    EMAIL_PATTERN.test(recipientEmail.value.trim()),
  )

  const isStep1Valid = computed(() => giftAmount.value > 0)

  const isStep2Valid = computed(
    () =>
      recipientName.value.trim().length > 0 &&
      senderName.value.trim().length > 0 &&
      isRecipientEmailValid.value,
  )

  function setBrand(brand: Brand) {
    selectedBrand.value = brand
    checkoutResult.value = null
  }

  function setStep(step: number) {
    currentStep.value = Math.min(3, Math.max(1, step))
  }

  function nextStep() {
    setStep(currentStep.value + 1)
  }

  function prevStep() {
    setStep(currentStep.value - 1)
  }

  function resetFlow() {
    giftAmount.value = 50
    recipientName.value = ''
    recipientEmail.value = ''
    senderName.value = ''
    personalMessage.value = ''
    themeColor.value = THEME_COLORS[0].value
    currentStep.value = 1
    checkoutResult.value = null
    isSubmitting.value = false
  }

  function resetAll() {
    selectedBrand.value = null
    resetFlow()
  }

  return {
    selectedBrand,
    giftAmount,
    recipientName,
    recipientEmail,
    senderName,
    personalMessage,
    themeColor,
    currentStep,
    checkoutResult,
    isSubmitting,
    formattedAmount,
    isRecipientEmailValid,
    isStep1Valid,
    isStep2Valid,
    setBrand,
    setStep,
    nextStep,
    prevStep,
    resetFlow,
    resetAll,
  }
})
