<template>
  <main class="px-10 overflow-y-auto dark:bg-slate-800 page xl:px-12">
    <section class="container mx-auto flex flex-col gap-5 items-center justify-center mt-6 scroll-mt-[120px] min-h-screen">
      <Profile />
    </section>
  </main>
</template>
  
<script setup lang="ts">
const client = useSupabaseAuthClient()
import { ref, onMounted } from 'vue';

useHead({
title: 'User profile',
meta: [
    { name: 'description', content: 'Profile view.' }
]
})

definePageMeta({
layout: "home"
  })

const newest_movies = ref([]);

const fetchNewestMovies = async () => {

    const { data, error } = await client.rpc('get_newest_movies',{length_movies: 0});

    if (error) {
        console.error('Error al obtener películas:', error);
    } else {
        newest_movies.value = data;
    }
};

const popular_movies = ref([]);

const fetchPopularMovies = async () => {

  const { data, error } = await client.rpc('get_popular_movies',{length_movies: 4});

  if (error) {
    console.error('Error al obtener películas:', error);
  } else {
    popular_movies.value = data;
  }
};

onMounted(fetchNewestMovies);
onMounted(fetchPopularMovies);
  
</script>