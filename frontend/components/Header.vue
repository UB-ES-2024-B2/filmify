<template>
  <nav class="fixed top-0 z-50 flex w-full h-20 px-5 bg-white dark:bg-gray-800 border-b-slate-400 backdrop-blur-lg">
    <div class="container flex items-center justify-between h-full mx-auto flex-wrap">
      <NuxtLink
        :to="{ path: '/', hash: '#hero' }"
        class="text-3xl font-bold dark:text-white text-purple-800 font-display"
      >
        <span class="hidden md:inline">Filmify 🎞️</span>
        <span class="inline md:hidden">🎞️</span>
      </NuxtLink>

      <!-- Componente de búsqueda -->
      <div class="flex-1 mx-4">
        <SearchDropdown />
      </div>

      <div class="flex items-center gap-2">
        <FilterDropdown class="hidden sm:inline"/>
        <UButton v-if="!user" :size="'md'" to="/login" color="purple">Login</UButton>
        <UButton v-if="!user" :size="'md'" to="/register" color="gray" class="hidden sm:inline">Sign Up</UButton>
        <ProfileNav v-if="user" />
      </div>
    </div>
  </nav>
</template>


<script setup lang="ts">
import FilterDropdown from './components/FilterDropdown.vue';
import SearchDropdown from './components/SearchDropdown.vue';
import { useSupabaseUser } from '#imports';

const user = useSupabaseUser();
</script>
