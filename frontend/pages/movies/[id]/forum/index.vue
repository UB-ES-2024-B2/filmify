<template>
    <div>
      <h1>Forum for Movie ID: {{ movieId }}</h1>
      <p>Welcome to the forum for {{ movieTitle }}.</p>
    </div>
  </template>
  
<script setup>
import { useRoute } from 'vue-router';

useHead({
    title: 'Forum',
    meta: [{ name: 'description', content: 'Forum' }],
});

definePageMeta({
    layout: 'home',
});

const route = useRoute();
const movieId = route.query.id; // Access movie ID from query params
const movieTitle = route.params.id; // Access movie title from route params
</script>
  