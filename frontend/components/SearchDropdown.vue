<template>
  <div class="relative flex-grow max-w-[1200px] min-w-[300px] ">
    <UInput
      color="purple"
      v-model="query"
      name="search"
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
          v-show="query !== ''"
          color="gray"
          variant="link"
          icon="i-heroicons-x-mark-20-solid"
          :padded="false"
          @click="query = ''"
        />
      </template>
    </UInput>

    <!-- Dropdown de resultados -->
    <div
      v-if="showDropdown && dropdownResults.length > 0"
      class="absolute bg-white shadow-lg border rounded-lg w-full mt-1 z-40"
    >
      <ul>
        <li
          v-for="movie in dropdownResults"
          :key="movie.id"
          class="p-2 hover:bg-gray-100 cursor-pointer"
          @click="goToMovieDetail(movie)"
        >
          <div class="flex items-center">
            <img
              :src="movie.poster_url"
              alt="Poster"
              class="w-10 h-14 object-cover rounded mr-2"
            />
            <div>
              <h3 class="font-semibold">{{ movie.title }}</h3>
              <p class="text-sm text-gray-500">{{ movie.release_date }}</p>
              <NuxtRating
                :ratingValue="(movie.vote_average / 10) * 5"
                :read-only="true"
                :activeColor="'#800080'"
              />
            </div>
          </div>
        </li>
      </ul>
      <div
        class="text-center p-2 border-t cursor-pointer text-blue-500 hover:underline"
        @click="handleSearch"
      >
        Ver todos los resultados
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useSupabaseAuthClient } from '#imports';

const query = ref('');
const dropdownResults = ref([]);
const showDropdown = ref(false);
const router = useRouter();
const supabase = useSupabaseAuthClient();

// Función para manejar la búsqueda en tiempo real
const fetchDropdownResults = async () => {
  if (query.value.trim() === '') {
    dropdownResults.value = [];
    showDropdown.value = false;
    return;
  }
  const { data, error } = await supabase.rpc('advanced_search', { query: query.value });
  if (!error) {
    dropdownResults.value = data.slice(0, 5);
    showDropdown.value = true;
  }
};

// Función para manejar la búsqueda completa al presionar Enter
const handleSearch = () => {
  if (query.value.trim() !== '') {
    showDropdown.value = false;
    router.push({ path: '/search', query: { q: query.value } });
  }
};

// Función para redirigir al detalle de la película
const goToMovieDetail = (movie) => {
  showDropdown.value = false;
  navigateTo({
    path: `/movies/${movie.title.replace(/\s+/g, '-').toLowerCase()}`,
    query: { id: movie.id },
  });
};

// Función para cerrar el dropdown al hacer clic fuera
const handleClickOutside = (event) => {
  const dropdownContainer = document.querySelector('.relative.flex-grow');
  if (dropdownContainer && !dropdownContainer.contains(event.target)) {
    showDropdown.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>
