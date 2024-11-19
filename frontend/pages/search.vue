<template>
  <div class="h-screen flex flex-col">
    <!-- Header Fijo -->
    <header class="fixed top-0 w-full z-10 bg-white shadow-md">
      <div class="container mx-auto px-4 py-4 flex justify-between items-center">
        <h1 class="text-purple-800 font-bold text-2xl">Filmify</h1>
        <UInput
          color="purple"
          v-model="route.query.q"
          placeholder="Buscar..."
          class="w-1/2"
          @keyup.enter="fetchSearchResults"
        />
      </div>
    </header>

    <!-- Contenedor principal desplazable -->
    <main class="flex-1 overflow-y-auto pt-20">
      <!-- Agregamos espacio para que no quede detrás del header -->
      <section class="container mx-auto px-4 py-8">
        <h2 class="text-2xl font-display mb-4">
          Resultados de búsqueda para "{{ route.query.q }}"
        </h2>

        <div v-if="searchResults.length > 0" class="space-y-6">
          <div
            v-for="(movie, index) in searchResults"
            :key="index"
            class="border-b border-gray-300 pb-4"
          >
            <SearchResultCard :movie="movie" />
          </div>
        </div>
        <div v-else class="text-gray-500 mt-10">No se encontraron resultados.</div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import SearchResultCard from '~/components/SearchResultCard.vue';
import { useSupabaseAuthClient } from '#imports';

const client = useSupabaseAuthClient();
const route = useRoute();
const searchResults = ref([]);

// Función para obtener los resultados de la búsqueda
const fetchSearchResults = async () => {
  const query = route.query.q || '';
  if (query) {
    const { data, error } = await client.rpc('advanced_search', { query });
    if (!error) {
      searchResults.value = data;
    }
  } else {
    searchResults.value = [];
  }
};

// Ejecutar la búsqueda al cargar la página o cuando cambia el query en la URL
onMounted(fetchSearchResults);
watch(() => route.query.q, fetchSearchResults);
</script>

<style scoped>
/* Sin CSS adicional */
</style>
