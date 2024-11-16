<template>
  <nav class="fixed top-0 z-50 flex w-full h-20 px-5 bg-white dark:bg-gray-800 border-b-slate-400 backdrop-blur-lg">
    <div class="container flex items-center justify-between h-full mx-auto flex-wrap">
      <NuxtLink
        :to="{ path: '/', hash: '#hero' }"
        class="text-3xl font-bold dark:text-white text-purple-800 font-display"
      >
        <span class="hidden md:inline">Filmify 🎞️</span>
        <span class="inline md:hidden">🎞️</span>
      </NuxtLink>

      <!-- Barra de búsqueda -->
      <div class="relative mx-2 flex-grow" ref="dropdownContainer">
        <UInput
          color="purple"
          v-model="q"
          name="q"
          placeholder="Busca..."
          icon="i-heroicons-magnifying-glass-20-solid"
          autocomplete="off"
          @input="fetchDropdownResults" 
          @keyup.enter="handleSearch"
          :ui="{ icon: { trailing: { pointer: '' } } }"
          @focus="showDropdown = true"
        >
          <template #trailing>
            <UButton
              v-show="q !== ''"
              color="gray"
              variant="link"
              icon="i-heroicons-x-mark-20-solid"
              :padded="false"
              @click="q = ''"
            />
          </template>
        </UInput>

        <!-- Dropdown de resultados -->
        <div v-if="showDropdown && dropdownResults.length > 0" class="absolute bg-white shadow-lg border rounded-lg w-full mt-1 z-40">
          <ul>
            <li v-for="movie in dropdownResults" :key="movie.id" class="p-2 hover:bg-gray-100 cursor-pointer" @click="goToMovieDetail(movie.id)">
              <div class="flex items-center">
                <img :src="movie.poster_url" alt="Poster" class="w-10 h-14 object-cover rounded mr-2" />
                <div>
                  <h3 class="font-semibold">{{ movie.title }}</h3>
                  <p class="text-sm text-gray-500">{{ movie.release_date }}</p>
                  <NuxtRating :ratingValue="(movie.vote_average / 10) * 5" :read-only="true" :activeColor="'#800080'" />
                </div>
              </div>
            </li>
          </ul>
          <div class="text-center p-2 border-t cursor-pointer text-blue-500 hover:underline" @click="handleSearch">
            Ver todos los resultados
          </div>
        </div>
      </div>

      <div class="flex items-center gap-2">
        <UButton v-if="!user" :size="'md'" to="/login" color="purple" class="inline">Login</UButton>
        <UButton v-if="!user" :size="'md'" to="/register" color="gray" class="inline">Sign Up</UButton>
        <ProfileNav v-if="user" />
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useSupabaseAuthClient, useSupabaseUser } from '#imports';

const q = ref('');
const dropdownResults = ref([]);
const showDropdown = ref(false); // Estado para controlar la visibilidad del dropdown
const dropdownContainer = ref(null); // Referencia al contenedor del dropdown
const supabase = useSupabaseAuthClient();
const user = useSupabaseUser();
const router = useRouter();

// Función para manejar la búsqueda en tiempo real
const fetchDropdownResults = async () => {
  if (q.value.trim() === '') {
    dropdownResults.value = [];
    showDropdown.value = false;
    return;
  }
  const { data, error } = await supabase.rpc('advanced_search', { query: q.value });
  if (!error) {
    dropdownResults.value = data.slice(0, 5);
    showDropdown.value = true;
  }
};

// Función para manejar la búsqueda completa al presionar Enter
const handleSearch = () => {
  if (q.value.trim() !== '') {
    showDropdown.value = false;
    router.push({ path: '/search', query: { q: q.value } });
  }
};

// Función para redirigir al detalle de la película
const goToMovieDetail = (id) => {
  showDropdown.value = false;
  router.push(`/movies/${id}`);
};

// Función para cerrar el dropdown al hacer clic fuera
const handleClickOutside = (event) => {
  if (dropdownContainer.value && !dropdownContainer.value.contains(event.target)) {
    showDropdown.value = false;
  }
};

// Detectar clics fuera del dropdown
onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>
