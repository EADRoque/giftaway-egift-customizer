<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { computed, ref } from 'vue'
import { useGiftStore } from '@/stores/gift'

const store = useGiftStore()
const { recipientName, recipientEmail, senderName, personalMessage, isRecipientEmailValid } =
  storeToRefs(store)

const maxMessageLength = 500
const emailTouched = ref(false)

const showEmailError = computed(
  () => emailTouched.value && recipientEmail.value.trim() && !isRecipientEmailValid.value,
)
</script>

<template>
  <div>
    <h2 class="text-xl font-semibold text-ink">Personalize your gift</h2>
    <p class="mt-1 text-sm text-muted">
      Who is it from, who receives it, and what would you like to say?
    </p>

    <div class="mt-6 space-y-5">
      <div>
        <label for="sender" class="text-sm font-medium text-ink">Your name (sender)</label>
        <input
          id="sender"
          v-model="senderName"
          type="text"
          maxlength="100"
          autocomplete="name"
          placeholder="e.g. Jordan Lee"
          class="mt-2 w-full rounded-xl border border-stone-200 px-4 py-2.5 text-ink outline-none transition focus:border-violet-400 focus:ring-2 focus:ring-violet-100"
        />
      </div>

      <div>
        <label for="recipient" class="text-sm font-medium text-ink">Recipient name</label>
        <input
          id="recipient"
          v-model="recipientName"
          type="text"
          maxlength="100"
          autocomplete="name"
          placeholder="e.g. Alex Johnson"
          class="mt-2 w-full rounded-xl border border-stone-200 px-4 py-2.5 text-ink outline-none transition focus:border-violet-400 focus:ring-2 focus:ring-violet-100"
        />
      </div>

      <div>
        <label for="recipient-email" class="text-sm font-medium text-ink">
          Recipient email
        </label>
        <input
          id="recipient-email"
          v-model="recipientEmail"
          type="email"
          autocomplete="email"
          placeholder="e.g. alex@example.com"
          class="mt-2 w-full rounded-xl border px-4 py-2.5 text-ink outline-none transition focus:ring-2"
          :class="
            showEmailError
              ? 'border-red-300 focus:border-red-400 focus:ring-red-100'
              : 'border-stone-200 focus:border-violet-400 focus:ring-violet-100'
          "
          @blur="emailTouched = true"
        />
        <p v-if="showEmailError" class="mt-1.5 text-sm text-red-600">
          Please enter a valid email address.
        </p>
        <p v-else class="mt-1.5 text-xs text-muted">
          We&rsquo;ll email their digital voucher and gift code to this address.
        </p>
      </div>

      <div>
        <div class="flex items-baseline justify-between">
          <label for="message" class="text-sm font-medium text-ink">Personal message</label>
          <span class="text-xs text-muted">
            {{ personalMessage.length }} / {{ maxMessageLength }}
          </span>
        </div>
        <textarea
          id="message"
          v-model="personalMessage"
          rows="5"
          :maxlength="maxMessageLength"
          placeholder="Write something they'll remember…"
          class="mt-2 w-full resize-none rounded-xl border border-stone-200 px-4 py-3 text-ink outline-none transition focus:border-violet-400 focus:ring-2 focus:ring-violet-100"
        />
      </div>
    </div>
  </div>
</template>
