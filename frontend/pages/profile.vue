<template>
  <main class="px-10 overflow-y-auto dark:bg-slate-800 page xl:px-12">
    <section class="container mx-auto flex flex-col gap-5 items-center justify-center mt-6 scroll-mt-[120px] min-h-screen">
      <Profile :userData="userData"/>

      <h2 class="text-2xl font-display">Favoritas</h2>
      <template v-if="newest_movies.length > 0">
        <UCarousel 
          class="px-10"
          v-slot="{ item, index }"
          :items="newest_movies"
          :ui="{
            wrapper: 'w-full',
            container: 'gap-5',
            item: 'h-[350px] w-[150px]',
          }"
          arrows
        >
          <CarouselCard :item="item" :index="index" />
        </UCarousel>
      </template>
      <template v-else>
        <EmptyCarouselCard />
      </template>

      <h2 class="text-2xl font-display">Wishlist</h2>
      <template v-if="popular_movies.length > 0">
        <UCarousel 
          class="px-10"
          v-slot="{ item, index }"
          :items="popular_movies"
          :ui="{
            wrapper: 'w-full flex justify-center',
            container: 'flex justify-center gap-5',
            item: 'h-[350px] w-[150px]',
          }"
          arrows
        >
          <CarouselCard :item="item" :index="index" />
        </UCarousel>
      </template>
      <template v-else>
        <EmptyCarouselCard />
      </template>

    </section>
  </main>
</template>
  
<script setup lang="ts">

const client = useSupabaseAuthClient()
const user = useSupabaseUser()
const userData = user.value?.user_metadata

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