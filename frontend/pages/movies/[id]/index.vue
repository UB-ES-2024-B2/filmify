<template>
  <div>
    <MovieDetails></MovieDetails>
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
</script>
