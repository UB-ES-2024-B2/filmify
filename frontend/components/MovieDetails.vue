<template>
  <main class="px-10 overflow-y-auto page xl:px-12">
    <section
      class="container mx-auto flex flex-col gap-5 items-center justify-center mt-6 scroll-mt-[120px] min-h-screen"
    >
      <div v-if="!movie" class="text-center">

        <p class="text-gray-500 text-lg" id="loading-message">Loading movie details...</p>
      </div>

      <div v-else>
        <div class="text-center">
          <h1 class="text-4xl font-bold mb-2" id="movie-title">{{ movie?.title || 'Loading' }}</h1>
          <p class="text-gray-500" id="movie-release-rating">
            {{ movie?.release_date || 'N/A' }} | Rating: {{ movie?.vote_average || 'N/A' }}
          </p>
        </div>

        <div class="flex flex-col md:flex-row gap-8 mt-8 w-full">
          <NuxtImg
            :src="movie?.poster_url"
            :alt="movie?.title"
            class="md:w-1/3 w-full aspect-[2/3] object-cover rounded-lg"
            id="movie-poster"
          />
          <div class="flex flex-col mt-8 md:w-2/3">
            <NuxtRating
              class="flex w-full justify-center mb-4"
              :read-only="true"
              :ratingValue="(movie?.vote_average / 10) * 5"
              :rating-size="30"
              :activeColor="'#800080'"
              id="movie-rating"
            />
            <p class="text-gray-500 text-lg md:text-xl my-4" id="movie-overview">{{ movie?.overview || 'No overview available.' }}</p>
            <UButton
              @click="goToForum"
              class="mx-auto px-8"
              color="purple"
              size="xl"
              id="forum-button"
            >
              Foro
            </UButton>
          </div>
        </div>

        <!-- Botón de favoritos -->
        <div class="mt-4 flex justify-center">
          <button
            @click="toggleFavorite"
            :class="isFavorited ? 'bg-red-500' : 'bg-green-500'"
            class="text-white font-bold py-2 px-4 rounded"
          >
            {{ isFavorited ? 'Eliminar de favoritos' : 'Añadir a favoritos' }}
          </button>
        </div>
        <div class="mt-8 bg-gray-200 p-4 rounded-lg w-full" id="movie-info">
          <h2 class="text-3xl text-center font-bold mb-6" id="info-heading">Info</h2>

          <div class="grid grid-cols-5 gap-4 text-gray-700">
            <div class="font-bold col-span-1" id="director-heading">Director:</div>
            <div class="col-span-4" id="director-name">{{ director[0]?.director_name || 'N/A' }}</div>

            <div class="font-bold col-span-1" id="cast-heading">Actores:</div>
            <div class="col-span-4">
              <ul class="flex flex-wrap gap-2" id="cast-list">
                <li v-for="(actor, index) in cast" :key="index" class="text-gray-700" id="actor-name">
                  <span>{{ actor }}</span><span v-if="index < cast.length - 1">,</span>
                </li>
              </ul>
            </div>

            <div class="font-bold col-span-1" id="language-heading">Idioma:</div>
            <div class="col-span-4" id="language-name">{{ language[0]?.language_name || 'N/A' }}</div>

            <div class="font-bold col-span-1" id="genre-heading">Género:</div>
            <div class="col-span-4">
              <ul class="flex flex-wrap gap-2" id="genre-list">
                <li v-for="(genre, index) in genres" :key="index" class="text-gray-700" id="genre-name">
                  <span>{{ genre }}</span><span v-if="index < genres.length - 1">,</span>
                </li>
              </ul>
            </div>

            <div class="font-bold col-span-1" id="release-date-heading">Fecha de estreno:</div>
            <div class="col-span-4" id="release-date">{{ movie?.release_date || 'N/A' }}</div>
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
const clientauth = useSupabaseAuthClient();
const movieID = route.query.id;
const movieTitle = route.params.id;
const forumLink = `/movies/${movieTitle}/forum?id=${movieID}`;

const goToForum = () => {
  navigateTo({
    path: forumLink,
    query: { id: route.query.id },
  });
};


const isFavorited = ref(false); // Estado inicial
const userID = ref(null);

const movie = ref(null);
const genres = ref([]);
const cast = ref([]);
const director = ref([]);
const language = ref([]);

// Fetch movie details
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

// Fetch other movie-related data
const fetchGenres = async () => {
  try {
    const { data, error } = await client.rpc('get_movie_genres', { movie_id: movieID });

    if (error) {
      console.error('Error fetching movie genres:', error);

    } else if (data && data.length > 0) {
      genres.value = data.map((genre) => genre.genre_name);
    }
  } catch (err) {
    console.error('Unexpected error:', err);
  }
};

const fetchCast = async () => {
  try {
    const { data, error } = await client.rpc('get_movie_cast', { movie_id: movieID });

    if (error) {
      console.error('Error fetching movie cast:', error);

    } else if (data && data.length > 0) {
      cast.value = data.map((actor) => actor.actor_name);
    }
  } catch (err) {
    console.error('Unexpected error:', err);
  }
};

const fetchDirector = async () => {
  try {
    const { data, error } = await client.rpc('get_movie_director', { movie_id: movieID });

    if (error) {
      console.error('Error fetching movie director:', error);
    } else if (data && data.length > 0) {
      director.value = data;
    } else {
      console.warn('No data returned for the given movie ID');

    }
  } catch (err) {
    console.error('Unexpected error:', err);
  }
};

const fetchLanguage = async () => {
  try {
    const { data, error } = await client.rpc('get_movie_language', { movie_id: movieID });


    if (error) {
      console.error('Error fetching movie language:', error);
    } else if (data && data.length > 0) {
      language.value = data;
    } else {
      console.warn('No data returned for the given movie ID');

    }
  } catch (err) {
    console.error('Unexpected error:', err);
  }
};

// Reactive user ID


const fetchUserId = async () => {
  const { data: sessionData, error: sessionError } = await clientauth.auth.getSession();

  if (sessionError || !sessionData.session) {
    console.error('User is not authenticated:', sessionError);
    return;
  }

  const { data: user, error: userError } = await clientauth.auth.getUser();


  if (userError) {
    console.error('Error fetching user:', userError);
  } else {
    userID.value = user.user.id || null;
  }
};

const checkIfFavorited = async () => {
  try {
    const { data, error } = await client.rpc('is_favorited', {
      user_id: userID.value,
      movie_id: movieID,
    });

    if (error) {
      console.error('Error verificando si es favorita:', error);
      return false;
    }
    isFavorited.value = data
    return data; // Devuelve true si es favorita, false si no
  } catch (err) {
    console.error('Error al comprobar si es favorita:', err);
    return false;
  }
};


// Toggle favorite status
const toggleFavorite = async () => {
  try {
    if (!movie.value) return; // Asegúrate de que haya una película cargada antes de continuar

    if (isFavorited.value) {
      // Lógica para eliminar de favoritos
      const { data, error } = await client.rpc('remove_from_favorites', {
        user_id: userID.value, // userID debe estar definido
        movie_id: movieID, // movieID es la ID de la película actual
      });

      if (error) {
        console.error('Error eliminando de favoritos:', error);
      } else if (data) {
        isFavorited.value = false;
        console.log(`${movie.value.title} eliminado de favoritos.`);
      } else {
        console.warn('No se pudo eliminar de favoritos. Verifica las restricciones.');
      }
    } else {
      // Lógica para añadir a favoritos
      const { data, error } = await client.rpc('add_to_favorites', {
        user_id: userID.value, // userID debe estar definido
        movie_id: movieID, // movieID es la ID de la película actual
      });

      if (error) {
        console.error('Error añadiendo a favoritos:', error);
      } else if (data) {
        isFavorited.value = true;
        console.log(`${movie.value.title} añadido a favoritos.`);
      } else {
        console.warn('No se pudo añadir a favoritos. Verifica las restricciones.');
      }
    }
  } catch (err) {
    console.error('Error al alternar estado de favorito:', err);
  }
};

onMounted(async () => {
  await fetchMovieDetails();
  await fetchGenres();
  await fetchCast();
  await fetchDirector();
  await fetchLanguage();
  await fetchUserId(); // Esperar que fetchUserId termine antes de llamar a checkIfFavorited
  await checkIfFavorited(); // Llamar a checkIfFavorited después de que userID esté disponible
});

</script>
