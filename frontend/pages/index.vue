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
    <!-- Trending POSTS -->
    <section id="trending-tops" class="py-12">
      <h2 class="text-3xl font-bold mb-6 text-center">Trending Posts</h2>
      <div class="grid grid-cols-2 gap-4 px-8">
        <!-- Posts recientes -->
        <div>
          <h3 class="text-xl font-semibold mb-4 text-center">Posts recientes</h3>
          <ul class="space-y-4">
            <li
              v-for="post in recent_posts"
              :key="post.post_id"
              class="bg-gray-100 p-4 rounded shadow overflow-hidden h-[150px] w-full"
            >
              <h4 class="font-bold truncate">{{ post.title }}</h4>
              <p class="text-gray-600 text-sm truncate">{{ post.username }} - {{ post.creation_date }}</p>
              <p class="mt-2 whitespace-normal break-words text-sm overflow-hidden">
                {{ post.content }}
              </p>
            </li>
          </ul>
        </div>
        <!-- Lugar vacío para la US 25 -->
        <div>
          <h3 class="text-xl font-semibold mb-4 text-center">Posts más valorados</h3>
          <p class="text-gray-500 text-center">Próximamente...</p>
        </div>
      </div>
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

// Posts más recientes
const recent_posts = ref([]);
const fetchRecentPosts = async () => {
  const { data, error } = await client.rpc('get_latest_posts', { length: 5 });
  if (error) console.error('Error al obtener posts recientes:', error);
  else recent_posts.value = data;
};

onMounted(fetchNewestMovies);
onMounted(fetchPopularMovies);
fetchRecentPosts();
</script>