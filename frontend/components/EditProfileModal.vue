<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white p-6 rounded shadow-md w-full max-w-md">
      <h2 class="text-xl font-bold mb-4">Editar Perfil</h2>
      <form @submit.prevent="updateProfile">
        <div class="mb-4">
          <label for="username" class="block text-sm font-medium text-gray-700">Nombre de usuario</label>
          <input 
            id="username" 
            type="text" 
            v-model="username" 
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-purple-500 focus:border-purple-500 sm:text-sm"
          />
        </div>
        <div class="mb-4">
          <label for="bio" class="block text-sm font-medium text-gray-700">Bio</label>
          <textarea 
            id="bio" 
            v-model="bio" 
            rows="4" 
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-purple-500 focus:border-purple-500 sm:text-sm"
          ></textarea>
        </div>
        <div class="flex justify-end gap-2">
          <button 
            @click="$emit('close')"
            type="button" 
            class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-700"
          >
            Cancelar
          </button>
          <button 
            type="submit" 
            class="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-800"
          >
            Guardar
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  userData: Object
});

const emit = defineEmits(['close']);

const username = ref(props.userData.username);
const bio = ref(props.userData.bio);

const updateProfile = async () => {
  console.log("Enviando datos al backend:", {
    userid: props.userData.sub, // Cambiar a 'userid'
    username: username.value,
    userbio: bio.value // Cambiar a 'userbio'
  });

  const client = useSupabaseAuthClient();
  const { data, error } = await client.rpc('edituserinfo', { // Asegúrate de que el nombre de la función sea todo en minúsculas
    userid: props.userData.sub,
    username: username.value,
    userbio: bio.value
  });

  if (error) {
    console.error('Error del backend:', error);
    alert('No se pudo actualizar el perfil. Por favor, inténtalo de nuevo.');
    return;
  }

  if (!data || !data.changeSuccessful) {
    console.error('Respuesta inesperada del backend:', data);
    alert(data?.errorMessage || 'No se pudo actualizar el perfil. Por favor, inténtalo de nuevo.');
    return;
  }

  alert('Perfil actualizado correctamente.');
  emit('close');
};


</script>
