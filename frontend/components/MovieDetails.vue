<template>
  <main class="px-10 overflow-y-auto page xl:px-12">
    <section
      class="container mx-auto flex flex-col gap-5 items-center justify-center mt-6 scroll-mt-[120px] min-h-screen"
    >
      <div v-if="!movie" class="text-center">
        <p class="text-gray-500 text-lg">Loading movie details...</p>
      </div>

      <div v-else>
        <div class="text-center">
          <h1 class="text-4xl font-bold mb-2">{{ movie.title }}</h1>
          <p class="text-gray-500">
            {{ movie.release_date }} | Rating: {{ movie.vote_average }}
          </p>
        </div>

        <div class="flex flex-col md:flex-row gap-8 mt-8 w-full">
          <NuxtImg
            :src="movie.poster_url"
            :alt="movie.title"
            class="md:w-1/3 w-full aspect-[2/3] object-cover rounded-lg"
          />
          <div class="flex flex-col mt-8 md:w-2/3">
            <NuxtRating
              class="flex w-full justify-center mb-4"
              :read-only="true"
              :ratingValue="(movie.vote_average / 10) * 5"
              :rating-size="30"
              :activeColor="'#800080'"
            />
            <p class="text-gray-500 text-lg md:text-xl my-4">{{ movie.overview }}</p>
            <UButton
              @click="goToForum"
              class="mx-auto px-8"
              color="purple"
              size="xl"
            >
              Foro
            </UButton>
          </div>
        </div>

        <div class="mt-8 bg-gray-200 p-4 rounded-lg w-full">
          <h2 class="text-3xl text-center font-bold mb-6">Info</h2>
          <div class="grid grid-cols-5 gap-4 text-gray-700">
            <div class="font-bold col-span-1">Director:</div>
            <div class="col-span-4">{{ director[0].director_name }}</div>

            <div class="font-bold col-span-1">Actores:</div>
            <div class="col-span-4">
              <ul class="flex flex-wrap gap-2">
                <li v-for="(actor, index) in cast" :key="index" class="text-gray-700">
                  <span>{{ actor }}</span><span v-if="index < cast.length - 1">,</span>
                </li>
              </ul>
            </div>

            <div class="font-bold col-span-1">Idioma:</div>
            <div class="col-span-4">{{ language[0].language_name }}</div>

            <div class="font-bold col-span-1">Género:</div>
            <div class="col-span-4">
              <ul class="flex flex-wrap gap-2">
                <li v-for="(genre, index) in genres" :key="index" class="text-gray-700">
                  <span>{{ genre }}</span><span v-if="index < genres.length - 1">,</span>
                </li>
              </ul>
            </div>

            <div class="font-bold col-span-1">Fecha de estreno:</div>
            <div class="col-span-4">{{ movie.release_date }}</div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>


  
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const client = useSupabaseClient();
const movieID = route.query.id;
const movieTitle = route.params.id;
const forumLink = `/movies/${movieTitle}/forum?id=${movieID}`;

const goToForum = () => {
  navigateTo({
    path: forumLink,
    query: { id: route.query.id },
  });
};

const movie = ref(null); // Start with null to indicate loading
const genres = ref(null);
const cast = ref(null);
const director = ref(null);
const language = ref(null);

const fetchMovieDetails = async () => {
  try {
    const { data, error } = await client.rpc('get_movie_details', { movie_id: movieID });

    if (error) {
      console.error('Error fetching movie details:', error);
    } else if (data && data.length > 0) {
      movie.value = data[0];
    } else {
      console.warn('No data returned for the given movie ID');
    }
  } catch (err) {
    console.error('Unexpected error:', err);
  }
};

const fetchGenres = async () => {
  try {
    const { data, error } = await client.rpc('get_movie_genres', { movie_id: movieID })

    if (error) {
      console.error('Error fetching movie details:', error);
    } else if (data && data.length > 0) {
      genres.value = data.map((genre) => genre.genre_name);
    } else {
      console.warn('No data returned for the given movie ID');
    }
  } catch (err) {
    console.error('Unexpected error:', err);
  }
};

const fetchCast = async () => {
  try {
    const { data, error } = await client.rpc('get_movie_cast', { movie_id: movieID })

    if (error) {
      console.error('Error fetching movie details:', error);
    } else if (data && data.length > 0) {
      cast.value = data.map((actor) => actor.actor_name);
    } else {
      console.warn('No data returned for the given movie ID');
    }
  } catch (err) {
    console.error('Unexpected error:', err);
  }
};

const fetchDirector = async () => {
  try {
    const { data, error } = await client.rpc('get_movie_director', { movie_id: movieID })

    if (error) {
      console.error('Error fetching movie details:', error);
    } else if (data && data.length > 0) {
      director.value = data
    } else {
      console.warn('No data returned for the given movie ID');
    }
  } catch (err) {
    console.error('Unexpected error:', err);
  }
};

const fetchLanguage = async () => {
  try {
    const { data, error } = await client.rpc('get_movie_language', { movie_id: movieID })

    if (error) {
      console.error('Error fetching movie details:', error);
    } else if (data && data.length > 0) {
      language.value = data
    } else {
      console.warn('No data returned for the given movie ID');
    }
  } catch (err) {
    console.error('Unexpected error:', err);
  }
};

onMounted(fetchMovieDetails);
onMounted(fetchGenres);
onMounted(fetchCast);
onMounted(fetchDirector)
onMounted(fetchLanguage)
</script>