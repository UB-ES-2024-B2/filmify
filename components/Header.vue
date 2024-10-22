<template>
    <nav class="fixed top-0 z-50 flex w-full h-20 px-5 bg-white dark:bg-gray-800 border-b-slate-400 backdrop-blur-lg">
      <div class="container flex items-center justify-between h-full mx-auto flex-wrap">
        <NuxtLink
          :to="{ path: '/', hash: '#hero' }"
          class="text-4xl font-bold dark:text-white text-purple-800 font-display"
        >
          Filmify 🎞️
        </NuxtLink>
        <div class="mx-5 flex-grow">
          <UInput
            color="purple"
            v-model="q"
            name="q"
            placeholder="Busca..."
            icon="i-heroicons-magnifying-glass-20-solid"
            autocomplete="off"
            :ui="{ icon: { trailing: { pointer: '' } } }"
          >
            <template #trailing>
              <UButton
                v-show="q !== ''"
                color="gray"
                variant="link"
                icon="i-heroicons-x-mark-20-solid"
                :padded="false"
                @click="q = ''"
              />
            </template>
          </UInput>
        </div>
        <div class="flex items-center gap-3">
          <UButton :size="'md'" to="/login" color="purple" class="inline">Login</UButton>
          <UButton :size="'md'" to="/register" color="gray" class="inline">Sign Up</UButton>
        </div>
      </div>
    </nav>
  </template>
  
  
<script setup lang="ts">
const q = ref('')
</script>