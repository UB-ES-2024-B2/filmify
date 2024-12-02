<template>
  <div class="bg-white shadow-md rounded-md p-4 mb-6 w-full">
    <!-- Titulo del post -->
    <h2 class="text-xl font-semibold mb-2">{{ post.title }}</h2>

    <!-- Contenido del post -->
    <p class="text-gray-600 mb-4">{{ post.content }}</p>

    <!-- Autor del post -->
    <p class="text-sm text-gray-500 mb-4">Posted by: <span class="font-semibold">{{ post.username }}</span></p>

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
  </div>
</template>

<script setup lang="ts">
import { defineProps, ref } from 'vue';
import { useSupabaseUser } from '#imports';

const user = useSupabaseUser();

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(['change-vote'])


const changeVote = (vote_type: boolean) => {
  emit('change-vote', props.post, vote_type)
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