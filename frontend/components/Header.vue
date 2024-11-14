<template>
  <nav class="fixed top-0 z-50 flex w-full h-20 px-5 bg-white dark:bg-gray-800 border-b-slate-400 backdrop-blur-lg">
    <div class="container flex items-center justify-between h-full mx-auto flex-wrap">
      <NuxtLink
        :to="{ path: '/', hash: '#hero' }"
        class="text-3xl font-bold dark:text-white text-purple-800 font-display"
      >
        <span class="hidden md:inline">Filmify 🎞️</span> <!-- Hidden on small screens -->
        <span class="inline md:hidden">🎞️</span> <!-- Visible on small screens -->
      </NuxtLink>
      <div class="mx-2 flex-grow">
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
      <div class="flex items-center gap-2">
        <div class="flex items-center gap-2">
          <UButton v-if="!user" :size="'md'" to="/login" color="purple" class="inline">Login</UButton>
          <UButton v-if="!user" :size="'md'" to="/register" color="gray" class="inline">Sign Up</UButton>
          <ProfileNav v-if="user" />
        </div>
      </div>
    </div>
  </nav>
</template>
  
  
<script setup lang="ts">
const q = ref('')
const supabase = useSupabaseClient()
const user = useSupabaseUser()

const logout = async () => {
  await supabase.auth.signOut()
}
</script>