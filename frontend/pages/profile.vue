<template>
  <main class="px-10 overflow-y-auto dark:bg-slate-800 page xl:px-12">
    <section class="container mx-auto flex flex-col gap-5 items-center justify-center mt-6 scroll-mt-[120px] min-h-screen">
      <Profile />

      <h2 class="text-2xl font-display">Favoritas</h2>
      <template v-if="fav_list.length > 0">
        <UCarousel 
          class="px-10"
          v-slot="{ item, index }"
          :items="fav_list"
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

      <h2 class="text-2xl font-display">Wishlist</h2>
      <template v-if="wish_list.length > 0">
        <UCarousel 
          class="px-10"
          v-slot="{ item, index }"
          :items="wish_list"
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

const fav_list = ref([]);

const fetchFavList = async () => {

    const { data, error } = await client.rpc('get_favorites',{user_id: 2});

    if (error) {
      console.error('Error al obtener películas:', error);
    } else {
      fav_list.value = data;
    }
};

const wish_list = ref([]);

const fetchWishList = async () => {

  const { data, error } = await client.rpc('get_wishlist',{user_id: 4});

  if (error) {
    console.error('Error al obtener películas:', error);
  } else {
    wish_list.value = data;
  }
};

onMounted(fetchFavList);
onMounted(fetchWishList);  
</script>