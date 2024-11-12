<script setup lang="ts">

const client = useSupabaseClient()
const user = useSupabaseUser()
const userData = user.value?.user_metadata
const userName = userData?.username

const logout = async () => {
  const { error } = await client.auth.signOut()
  if (error) {
    return alert('Algo ha salido mal!')
  }
}

const itemsProfile = [
  [
    {
      label: userName,
      slot: "account",
      disabled: true,
    },
  ],
  [
    {
      label: "Perfil",
      icon: "i-heroicons-user-circle",
      click: () => {
        navigateTo('/profile')
      }
    },
  ],
  [
    {
      label: "Cerrar sesión",
      icon: "i-heroicons-arrow-left-on-rectangle",
      click: () => {
        isOpenModal.value = true
      }
    },
  ],
];

const isOpenModal = ref(false)

</script>

<template>
  <UModal v-model="isOpenModal" :ui="{ width: 'w-max' }">
    <div class="flex flex-col items-center w-max px-6 py-5">
      <div>
        <h2 class="text-center text-lg font-bold mb-1">¿Cerrar sesión?</h2>
        <p class="text-sm mb-4">¿Estás seguro de que quieres cerrar sesión?</p>
      </div>
      <div class="flex justify-center gap-3">
        <UButton color="purple" size="xs" @click="isOpenModal = false">Cancelar</UButton>
        <UButton color="purple" size="xs" @click="logout" to="/">Cerrar sesión</UButton>
      </div>
    </div>
  </UModal>
  
  <div class="flex items-center gap-3">
    <UDropdown mode="click" :items="itemsProfile">
      <UAvatar
        size="sm"
        src="https://avatars.githubusercontent.com/u/113581734?v=4"
        class="cursor-pointer"
      />
      <template #account="{ item }">
        <div class="text-left">
          <p class="text-xs">Bienvenido</p>
          <p class="font-medium text-gray-900 truncate dark:text-white text-sm">{{ item.label }}</p>
        </div>
      </template>
    </UDropdown>
  </div>
</template>