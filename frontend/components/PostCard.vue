<template>
  <div class="bg-white shadow-md rounded-md p-4 mb-6 w-full">
    <!-- Titulo del post -->
    <div class="flex justify-between items-center mb-4">
      <!-- Titulo del post -->
      <h2 class="text-xl font-semibold">{{ post.title }}</h2>

      <!-- Botón de eliminar post -->
      <UButton
        v-if="post.owner"
        variant="ghost"
        color="red"
        hoverColor="red.800"
        class="flex items-center gap-0"
        @click="openModal"
      >
        <Icon name="ph:x-bold" class="w-6 h-6" />
      </UButton>
    </div>

    <!-- Contenido del post -->
    <p class="text-gray-600 mb-4">{{ post.content }}</p>

    <!-- Autor del post -->
    <p class="text-sm text-gray-500 mb-4">Publicado por: <span class="font-semibold">{{ post.username }}</span></p>

    <!-- Botones de upvote y downvote -->
    <div class="flex items-center justify-center">
      <button 
        @click="changeVote(true)"
        :disabled="post.vote == true || !user"
        class="text-gray-500 hover:text-gray-800 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
          <path fill-rule="evenodd" d="M10 16.75a.75.75 0 01-.75-.75V5.656L5.603 9.303a.75.75 0 01-1.061-1.057l5-5a.75.75 0 011.061 0l5 5a.75.75 0 01-1.061 1.057L10.75 5.656V16a.75.75 0 01-.75.75z" clip-rule="evenodd" />
        </svg>
      </button>
      
      <!-- Score de post base -->
      <span class="text-lg mx-2">{{ post.votes }}</span>
      
      <button 
        @click="changeVote(false)"
        :disabled="post.vote == false ||!user "
        class="text-gray-500 hover:text-gray-800 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
          <path fill-rule="evenodd" d="M10 3.25a.75.75 0 01.75.75v10.344l3.647-3.647a.75.75 0 111.061 1.057l-5 5a.75.75 0 01-1.061 0l-5-5a.75.75 0 111.061-1.057L9.25 14V4a.75.75 0 01.75-.75z" clip-rule="evenodd" />
        </svg>
      </button>
    </div>

    <!-- Modal -->
    <div 
      v-if="isModalOpen" 
      class="fixed inset-0 flex justify-center items-center bg-black bg-opacity-50"
    >
      <div class="bg-white p-6 rounded-md w-110">
        <h2 class="text-md font-semibold mb-4">¿Estás seguro de eliminar este post?</h2>

        <!-- Botones -->
        <div class="flex justify-center gap-4">
          <UButton @click="closeModal" class="px-4" color="gray" size="md">Cancelar</UButton>
          <UButton @click="deletePost" class="px-4" color="red" size="md">Eliminar</UButton>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { defineProps, ref } from 'vue';
import { useSupabaseUser } from '#imports';

// Estado de modal
const isModalOpen = ref(false);

// Abre modal
const openModal = () => {
  isModalOpen.value = true;
};

// Cierra modal
const closeModal = () => {
  isModalOpen.value = false;

};

const user = useSupabaseUser();

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(['change-vote','delete-post'])

const changeVote = (vote_type: boolean) => {
  emit('change-vote', props.post, vote_type)
};

const deletePost = () => {
  emit('delete-post', props.post)
  closeModal();
};

</script>

<style scoped>
.w-full {
  width: 100%;
}
button:disabled {
  pointer-events: none; /* Sin interacción */
  animation: none; /* Sin animaciones */
  transition: none; /* Sin transiciones */
  background-color: transparent;
  color: #a855f7;
  cursor: not-allowed;
  transform: none; /* Elimina efectos de escala */
}
</style>