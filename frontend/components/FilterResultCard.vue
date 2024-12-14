<template>
  <div @click='goToDetails' class="flex items-start gap-4">
    <img :src="movie.poster_url" alt="Poster" class="w-24 h-36 object-cover rounded-md" />
    <div>
      <h3 class="text-lg font-semibold">{{ movie.title }}</h3>
      <p class="text-sm text-gray-500">Género: {{ movie.genre }}</p>
      <p class="text-sm text-gray-500">Fecha: {{ movie.release_date }}</p>
      <NuxtRating :ratingValue="(movie.vote_average / 10) * 5" :read-only="true" :activeColor="'#800080'" />
    </div>
  </div>
</template>

<script setup lang="ts">

const props = defineProps({
  movie: {
    type: Object,
    required: true,
  },
});

const goToDetails = () => {
  navigateTo({
    path: `/movies/${props.movie.title.replace(/\s+/g, '-').toLowerCase()}`,
    query: { id: props.movie.id },
  });
};
</script>
