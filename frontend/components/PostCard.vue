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
        @click="changeVote(1)"
        :disabled="hasVoted === 'upvote' ||!user"
        class="text-purple-500 hover:text-purple-800 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
          <path fill-rule="evenodd" d="M10 16.75a.75.75 0 01-.75-.75V5.656L5.603 9.303a.75.75 0 01-1.061-1.057l5-5a.75.75 0 011.061 0l5 5a.75.75 0 01-1.061 1.057L10.75 5.656V16a.75.75 0 01-.75.75z" clip-rule="evenodd" />
        </svg>
      </button>
      
      <!-- Score de post base -->
      <span class="text-lg mx-2">{{ voteCount }}</span>
      
      <button 
        @click="changeVote(-1)"
        :disabled="hasVoted === 'downvote' ||!user "
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

// Estados para rastrear la votacion
const voteCount = ref(props.post.votes || 0);  // La base de votos de cada post
const hasVoted = ref<string | null>(null);  // Flag para rastrear si el usuario ha votado, 'upvote' or 'downvote'

// Methods to handle upvote and downvote actions
const changeVote = (delta: number) => {
  if (hasVoted.value === null) {
    // Si no ha votado, se incrementa o decrementa la base por 1
    voteCount.value += delta;
    hasVoted.value = delta > 0 ? 'upvote' : 'downvote';
  } else if ((delta > 0 && hasVoted.value === 'downvote') || (delta < 0 && hasVoted.value === 'upvote')) {
    // Si ha cambiado su voto, se incrementa o decrementa la base por 2
    voteCount.value += 2 * delta;
    hasVoted.value = delta > 0 ? 'upvote' : 'downvote';
  }
};
</script>

<style scoped>
.w-full {
  width: 100%;
}
</style>

