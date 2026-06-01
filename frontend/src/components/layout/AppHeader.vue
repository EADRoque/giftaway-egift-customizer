<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <header class="border-b border-stone-200/80 bg-white/80 backdrop-blur-md">
    <div
      class="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8"
    >
      <RouterLink to="/" class="group flex items-center gap-2.5">
        <span
          class="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-violet-600 to-fuchsia-500 text-sm font-bold text-white shadow-md shadow-violet-500/25 transition group-hover:shadow-lg group-hover:shadow-violet-500/30"
        >
          G
        </span>
        <span class="text-lg font-semibold tracking-tight text-ink">Giftaway</span>
      </RouterLink>
      <p class="hidden text-sm text-muted sm:block">Premium digital gifting</p>
    </div>
  </header>
</template>
