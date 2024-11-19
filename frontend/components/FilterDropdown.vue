<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useSupabaseClient } from '#imports';

const isDropdownOpen = ref(false);
const genres = ref([]); // Géneros dinámicos
const selectedGenre = ref('');
const sortOrder = ref('alfabético');
const router = useRouter();
const route = useRoute(); // Ruta actual para comprobar ubicación
const client = useSupabaseClient();

// Alternar el estado del dropdown
const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
};

// Obtener géneros desde la base de datos
const fetchGenres = async () => {
  const { data, error } = await client.from('Genres').select('*');
  if (error) {
    console.error('Error fetching genres:', error);
  } else {
    genres.value = data.map((genre) => ({
      id: genre.id,
      name: genre.name,
    }));
  }
};

// Redirigir con los filtros aplicados
const applyFilters = () => {
  isDropdownOpen.value = false; // Cerrar dropdown
  router.push({
    path: '/filter',
    query: {
      genre: selectedGenre.value || route.query.genre, // Preservar si no cambia
      type: sortOrder.value || route.query.type, // Preservar si no cambia
    },
  });
};

// Cargar géneros al montar
onMounted(() => {
  fetchGenres();
});
</script>

<template>
  <div class="relative">
    <!-- Botón para abrir el dropdown -->
    <UButton
      color="purple"
      size="sm"
      icon="i-heroicons-adjustments-horizontal-20-solid"
      class="flex items-center gap-2 px-4 py-2 focus:outline-none hover:bg-purple-700"
      @click="toggleDropdown"
    >
      <span class="font-medium">Filtros</span>
    </UButton>

    <!-- Dropdown -->
    <div
      v-if="isDropdownOpen"
      class="absolute right-0 mt-2 bg-white shadow-lg rounded-md border w-64 z-50 p-4"
    >
      <h3 class="font-semibold mb-2 text-gray-700">Filtrar por:</h3>

      <!-- Filtro por género -->
      <div class="mb-4">
        <label for="genre" class="block text-sm font-medium text-gray-700 mb-1">Género</label>
        <select
          id="genre"
          v-model="selectedGenre"
          class="w-full border rounded p-2"
        >
          <option value="">Todos</option>
          <option
            v-for="genre in genres"
            :key="genre.id"
            :value="genre.name"
          >
            {{ genre.name }}
          </option>
        </select>
      </div>

      <!-- Filtro por orden -->
      <div class="mb-4">
        <label for="sort" class="block text-sm font-medium text-gray-700 mb-1">Ordenar por</label>
        <select
          id="sort"
          v-model="sortOrder"
          class="w-full border rounded p-2"
        >
          <option value="alfabético">Alfabético</option>
          <option value="fecha">Fecha de Estreno</option>
          <option value="popularidad">Popularidad</option>
        </select>
      </div>

      <!-- Botón para aplicar filtros -->
      <UButton
        color="purple"
        size="sm"
        class="w-full px-4 py-2 mt-2"
        @click="applyFilters"
      >
        Aplicar Filtros
      </UButton>
    </div>
  </div>
</template>
