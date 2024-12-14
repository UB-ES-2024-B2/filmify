<template>
  <main id="main-page" class="overflow-y-auto overflow-x-auto">
    <!-- Newest Movies -->
    <section id="newest-section" class="py-12">
      <h2 class="text-3xl font-bold mb-6 text-center">Nuevas</h2>
      <UCarousel
        id="newest-carousel"
        class="relative px-8"
        v-slot="{ item, index }"
        :items="newest_movies"
        :ui="{
          wrapper: 'w-full',
          container: 'gap-5',
          item: 'w-[200px]',
        }"
        arrows
      >
        <CarouselCard id="newest-carousel-card" :item="item" :index="index" />
      </UCarousel>
    </section>

    <!-- Popular Movies -->
    <section id="popular-section" class="py-12">
      <h2 class="text-3xl font-bold mb-6 text-center">Populares</h2>
      <UCarousel
        id="popular-carousel"
        class="relative px-8"
        v-slot="{ item, index }"
        :items="popular_movies"
        :ui="{
          wrapper: 'w-full',
          container: 'gap-5',
          item: 'w-[200px]',
        }"
        arrows
      >
        <CarouselCard id="popular-carousel-card" :item="item" :index="index" />
      </UCarousel>
    </section>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
const client = useSupabaseAuthClient()
const user = useSupabaseUser()
const loading = ref(false)

const logout = async () => {
  loading.value = true
  const { error } = await client.auth.signOut()
  if (error) {
    loading.value = false
    return alert('Something went wrong !')
  }
}

useHead({
  title: 'Filmify',
  meta: [
    { name: 'description', content: 'Your web for movies.' }
  ]
})

definePageMeta({
  layout: "home"
})

const newest_movies = ref([]);

const fetchNewestMovies = async () => {

  const { data, error } = await client.rpc('get_newest_movies',{length_movies: 15});


  if (error) {
    console.error('Error al obtener películas:', error);
  } else {
    newest_movies.value = data;
  }
};

const popular_movies = ref([]);

const fetchPopularMovies = async () => {

  const { data, error } = await client.rpc('get_popular_movies',{length_movies: 15});

  if (error) {
    console.error('Error al obtener películas:', error);
  } else {
    popular_movies.value = data;
  }
};

onMounted(fetchNewestMovies);
onMounted(fetchPopularMovies);
</script>