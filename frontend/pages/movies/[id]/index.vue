<template>
  <div>
    <MovieDetails></MovieDetails>
    <NuxtLink :to="forumLink">Go to Forum</NuxtLink>
  </div>
</template>

<script setup lang="ts">
useHead({
  title: 'Movie',
  meta: [{ name: 'description', content: 'Movie' }],
});

definePageMeta({
  layout: 'home',
});

const route = useRoute();
const movieId = route.query.id; // Movie ID from query
const movieTitle = route.params.id; // Movie title from params
const forumLink = `/movies/${movieTitle}/forum?id=${movieId}`; // Build forum link
</script>
