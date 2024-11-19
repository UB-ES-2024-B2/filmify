<template>
  <div class="flex items-center">
    <img :src="movie.poster_url" alt="Poster" class="w-24 h-36 object-cover mr-4 rounded-lg" />
    <div class="flex-1">
      <h3 class="text-lg font-bold">{{ movie.title }}</h3>
      <p class="text-sm text-gray-500">{{ movie.release_date }}</p>
      <p class="mt-2">{{ movie.overview }}</p>
      
      <!-- Componente de valoración -->
      <div class="mt-2">
        <NuxtRating
          :read-only="true"
          :ratingValue="(movie.vote_average / 10) * 5"
          :activeColor="'#800080'"
          class="flex justify-start"
        />
      </div>
      
      <button @click="goToMovieDetail" class="text-blue-500 hover:underline mt-3">
        Ver detalles
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  movie: {
    type: Object,
    required: true,
  },
});

const router = useRouter();

const goToMovieDetail = () => {
  router.push(`/movies/${props.movie.id}`);
};
</script>

<style scoped>
.search-result-card {
  max-width: 100%;
}
</style>
