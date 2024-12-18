<template>
  <main class="px-10 overflow-y-auto page xl:px-12">
    <link
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"
      rel="stylesheet"
    />
    <section
      class="container mx-auto flex flex-col gap-5 items-center justify-center mt-6 scroll-mt-[120px] min-h-screen"
    >

      <!-- Contingut principal -->
      <div v-if="!movie" class="text-center">
        <p class="text-gray-500 text-lg" id="loading-message">Loading movie details...</p>
      </div>

      <div v-else>
        <div class="text-center">
          <h1 class="text-4xl font-bold mb-2" id="movie-title">{{ movie?.title || 'Loading' }}</h1>
          <p class="text-gray-500" id="movie-release-rating">
            {{ movie?.release_date || 'N/A' }} | Rating: {{ movie?.vote_average || 'N/A' }} / 5
          </p>
        </div>

        <div class="flex flex-col md:flex-row gap-8 mt-8 w-full">
          <NuxtImg
            :src="movie?.poster_url"
            :alt="movie?.title"
            class="md:w-1/3 w-full aspect-[2/3] object-cover rounded-lg"
            id="movie-poster"
          />
          <div class="flex flex-col md:w-2/3">
            <div class="flex items-center justify-center gap-4">
              <NuxtRating
                class="flex"
                :read-only="true"
                :ratingValue="movie.vote_average"
                :rating-size="30"
                :activeColor="'#800080'"
              />
              <!-- Botón para valorar o eliminar valoración -->
              <div>
                <button
                  v-if="!hasRated"
                  @click="openRatingModal"
                  class="bg-purple-600 text-white font-bold py-2 px-4 rounded flex items-center space-x-2"
                >
                  <i class="fas fa-star"></i>
                  <span>Valorar</span>
                </button>
                <div v-else>
                  <p class="text-gray-700">Tu valoración: {{ userRating }}</p>
                  <button
                    @click="openDeleteModal"
                    class="bg-red-600 text-white font-bold py-2 px-4 rounded rounded flex items-center space-x-2"
                  >
                    <i class="far fa-star"></i>
                    <span>Eliminar valoración</span> 
                  </button>
                </div>
              </div>
            </div>
            <p class="text-gray-500 text-lg md:text-xl my-4" id="movie-overview">{{ movie?.overview || 'No overview available.' }}</p>
            <!-- Botó per anar al fòrum -->
            <UButton
              @click="goToForum"
              class="mx-auto px-8 mt-6"
              color="purple"
              size="xl"
              id="forum-button"
            >
              <i class="fas fa-comments"></i>
              <span>Foro</span>
            </UButton>
          </div>
        </div>

        <!-- Modal para valoración -->

        <div
          v-if="isRatingModalOpen"
          class="fixed inset-0 flex justify-center items-center bg-black bg-opacity-50"
        >
          <div class="bg-white p-6 rounded-md w-96">
            <h2 class="text-xl font-semibold mb-4 text-center">Valora esta película</h2>

            <div class="flex justify-center">
              <NuxtRating
                :read-only="false"
                :rating-size="30"
                :activeColor="'#ffb400'"
                @rating-selected="updateRating"
                :ratingValue="userRating"
              />
            </div>

            <div class="flex justify-end gap-4 mt-4">
              <button
                @click="closeRatingModal"
                class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-700"
              >
                Cancelar
              </button>
              <button
                @click="submitRating"
                class="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-800"
              >
                Guardar
              </button>
            </div>
          </div>
        </div>
        <!-- Modal para confirmar eliminación de valoración -->
        <div
          v-if="isDeleteModalOpen"
          class="fixed inset-0 flex justify-center items-center bg-black bg-opacity-50"
        >
          <div class="bg-white p-6 rounded-md w-96 text-center">
            <h2 class="text-xl font-semibold mb-4 text-red-600">Confirmar eliminación</h2>
            <p class="text-gray-700 mb-4">
              ¿Estás seguro de que quieres quitar tu valoración?
            </p>
            <div class="flex justify-center gap-4">
              <button
                @click="closeDeleteModal"
                class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-700"
              >
                Cancelar
              </button>
              <button
                @click="deleteRating"
                class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-800"
              >
                Eliminar
              </button>
            </div>
          </div>
        </div>

        <!-- Modal para error de login -->
        <div
          v-if="loginError"
          class="fixed inset-0 flex justify-center items-center bg-black bg-opacity-50"
        >
          <div class="bg-white p-6 rounded-md w-96 text-center">
            <h2 class="text-xl font-semibold mb-4 text-red-600">¡Error!</h2>
            <p class="text-gray-700 mb-4">Necesitas iniciar sesión para valorar esta película.</p>
            <div class="flex justify-center gap-4">
              <button
                @click="closeRatingModal"
                class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-700"
              >
                Cerrar
              </button>
              <button
                @click="goToLogin"
                class="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-800"
              >
                Ir a Login
              </button>
            </div>
          </div>
        </div>

        <!-- Botón de favoritos -->
        <div class="mt-4 flex justify-center gap-4">
          <!-- Botón de favoritos -->
          <button
            v-if="userID"
            @click="toggleFavorite"
            :class="isFavorited ? 'bg-red-500' : 'bg-green-500'"
            class="flex items-center text-white font-bold py-2 px-4 rounded space-x-2"
          >
            <i :class="isFavorited ? 'fas fa-heart' : 'far fa-heart'"></i>
            <span>{{ isFavorited ? 'Eliminar de favoritos' : 'Añadir a favoritos' }}</span>
          </button>

          <!-- Botón de wishlist -->
          <button
            v-if="userID"
            @click="toggleWish"
            :class="isWished ? 'bg-blue-500' : 'bg-yellow-500'"
            class="flex items-center text-white font-bold py-2 px-4 rounded space-x-2"
          >
            <i :class="isWished ? 'fas fa-list' : 'far fa-list-alt'"></i>
            <span>{{ isWished ? 'Eliminar de wishlist' : 'Añadir a wishlist' }}</span>
          </button>
        </div>


        <!-- Informació de la pel·lícula -->
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
const isWished = ref(false); // Estado inicial
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
      movie.value.vote_average = Math.round(movie.value.vote_average * 10) / 10;
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


const isRatingModalOpen = ref(false); // Controla el estado del modal
const userRating = ref(0); // Valoración seleccionada por el usuario
const loginError = ref(false); // Controla si el mensaje de error está visible
const isDeleteModalOpen = ref(false);
const hasRated = ref(false); // Controla si el usuario ha valorado la película

const fetchUserRating = async () => {
  try {
    const { data, error } = await client.rpc('get_rating', {
      user_id: userID.value,
      movie_id: movieID,
    });

    if (error) {
      console.error('Error al obtener la valoración del usuario:', error);
    } else if (data !== null) {
      userRating.value = data;
      hasRated.value = true;
    } else {
      hasRated.value = false;
    }
  } catch (err) {
    console.error('Error inesperado al obtener la valoración:', err);
  }
};

const goToLogin = () => {
  // Usa el enrutador para redirigir al usuario a la página de inicio de sesión
  const router = useRouter();
  router.push('/login');
};

const updateRating = (rating) => {
  console.log('Valor seleccionado:', rating); // Verifica el valor seleccionado
  userRating.value = rating; // Actualiza userRating
};


// Abre el modal de valoración
const openRatingModal = () => {
  if (!userID.value) {
    loginError.value = true; // Muestra el mensaje de error
    return;
  }
  isRatingModalOpen.value = true;
};


// Cierra el modal de valoración
const closeRatingModal = () => {
  isRatingModalOpen.value = false;
};

// Envía la valoración al backend
const submitRating = async () => {
  if (!userID.value) {
    alert('Necesitas iniciar sesión para valorar.');
    return;
  }

  try {
    // Redondeamos la valoración al entero más cercano antes de enviarla
    const roundedRating = Math.round(userRating.value);
    console.log('Valoración :', userRating.value);
    console.log('Valoración redondeada:', roundedRating);

    const { data, error } = await client.rpc('ratemovie', {
      user_id: userID.value,
      movie_id: movieID,
      new_rating: roundedRating
    });
    console.log('DATAA:',data)
    if (error) {
      console.error('Error enviando la valoración:', error);
      alert('Hubo un problema al enviar tu valoración.');
    } else if (data) {

      hasRated.value = true;
      //alert(data.message); // Mensaje de éxito del backend

      closeRatingModal(); // Cierra el modal tras guardar
    }
  } catch (err) {
    console.error('Error inesperado:', err);
    alert('Hubo un error inesperado al enviar tu valoración.');
  }
};

const openDeleteModal = () => {
  isDeleteModalOpen.value = true;
};

const closeDeleteModal = () => {
  isDeleteModalOpen.value = false;
};

const deleteRating = async () => {
  try {
    const { data, error } = await client.rpc('removemovierating', {
      user_id: userID.value,
      movie_id: movieID,
    });

    if (error) {
      console.error('Error al eliminar la valoración:', error);
    } else {
      hasRated.value = false;
      userRating.value = 0;
      closeDeleteModal();
    }
  } catch (err) {
    console.error('Error inesperado:', err);
  }
};


const checkIfWished = async () => {
  try {
    const { data, error } = await client.rpc('is_wished', {
      user_id: userID.value,
      movie_id: movieID,
    });

    if (error) {
      console.error('Error verificando si esta en la wishlist:', error);
      return false;
    }
    isWished.value = data
    return data; // Devuelve true si es favorita, false si no
  } catch (err) {
    console.error('Error al comprobar si esta en la wishlist:', err);
    return false;
  }
};


// Toggle wishlist status
const toggleWish = async () => {
  try {
    if (!movie.value) return; // Asegúrate de que haya una película cargada antes de continuar

    if (isWished.value) {
      // Lógica para eliminar de favoritos
      const { data, error } = await client.rpc('remove_from_wishlist', {
        user_id: userID.value, // userID debe estar definido
        movie_id: movieID, // movieID es la ID de la película actual
      });

      if (error) {
        console.error('Error eliminando de wishlist:', error);
      } else if (data) {
        isWished.value = false;
        console.log(`${movie.value.title} eliminado de wishlist.`);
      } else {
        console.warn('No se pudo eliminar de wishlist. Verifica las restricciones.');
      }
    } else {
      // Lógica para añadir a favoritos
      const { data, error } = await client.rpc('add_to_wishlist', {
        user_id: userID.value, // userID debe estar definido
        movie_id: movieID, // movieID es la ID de la película actual
      });

      if (error) {
        console.error('Error añadiendo a wishlist:', error);
      } else if (data) {
        isWished.value = true;
        console.log(`${movie.value.title} añadido a wishlist.`);
      } else {
        console.warn('No se pudo añadir a wishlist. Verifica las restricciones.');
      }
    }
  } catch (err) {
    console.error('Error al alternar estado de wishlist:', err);
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
  await checkIfWished();
  await fetchUserRating();

});

</script>
