<template>
  <nav id="header-nav" class="fixed top-0 z-50 flex w-full h-20 px-5 bg-white dark:bg-gray-800 border-b-slate-400 backdrop-blur-lg">
    <div id="header-container" class="container flex items-center justify-between h-full mx-auto flex-wrap">
      <NuxtLink
        id="header-logo-link"
        :to="{ path: '/'}"
        class="text-3xl font-bold dark:text-white text-purple-800 font-display"
      >
        <span id="header-logo-text" class="hidden md:inline">Filmify 🎞️</span>
        <span id="header-logo-icon" class="inline md:hidden">🎞️</span>
      </NuxtLink>

      <div id="header-search" class="flex-1 mx-4">
        <SearchDropdown />
      </div>

      <div id="header-actions" class="flex items-center gap-2">
        <FilterDropdown id="filter-dropdown" class="hidden sm:inline" />
        <UButton v-if="!user" id="login-button" :size="'md'" to="/login" color="purple">Login</UButton>
        <UButton v-if="!user" id="signup-button" :size="'md'" to="/register" color="gray" class="hidden sm:inline">Sign Up</UButton>
        <ProfileNav id="profile-nav" v-if="user" />
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
