<template>
  <main class="px-10 overflow-y-auto dark:bg-slate-800 page xl:px-0">
    <section
      class="container mx-auto flex flex-col gap-5 items-center justify-center mt-6 scroll-mt-[120px] min-h-screen"
    >
      <h2 class="text-2xl font-display">Nuevas</h2>
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

      <h2 class="text-2xl font-display">Populares</h2>
      <UCarousel 
        class="px-10"
        v-slot="{ item, index }"
        :items="popular_movies"
        :ui="{
          wrapper: 'w-full',
          container: 'gap-5',
          item: 'h-[350px] w-[150px]',
        }"
        arrows
      >
        <CarouselCard :item="item" :index="index" />
      </UCarousel>
    </section>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
const client = useSupabaseAuthClient()
const user = useSupabaseUser()
const loading = ref(false)

// En un componente o página de Nuxt, usa 'useRuntimeConfig'
const config = useRuntimeConfig();

console.log('Supabase URL:', config.public.SUPABASE_URL);
console.log('Supabase Key:', config.public.SUPABASE_KEY);

const logout = async () => {
  loading.value = true
  const { error } = await client.auth.signOut()
  if (error) {
    loading.value = false
    return alert('Something went wrong !')
  }
}

useHead({
  title: 'supaAuth',
  meta: [
    { name: 'description', content: 'Authentication template with email and password, using Supabase. If you want to a quick start to your next Nuxt3 app, please feel free to use this template.' }
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