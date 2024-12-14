<template>
    <main class="flex-1 overflow-y-auto pt-4">
      <!-- Contingut principal -->
      <section class="container mx-auto px-4">
        <!-- Encabezado dinámico del filtro -->
        <h2 class="text-2xl font-display mb-4">
          Resultados de filtrado
        </h2>
        <p class="text-sm text-gray-500 mb-6">
          Filtros activos:
          <span class="font-semibold">Género:</span> {{ currentGenre }} |
          <span class="font-semibold">Orden:</span> {{ currentSort }}
        </p>

        <!-- Resultados del filtrado -->
        <div v-if="filterResults.length > 0" class="grid grid-cols-3 gap-6">
          <FilterResultCard
            v-for="movie in filterResults.slice(0, 30)"
            :key="movie.id"
            :movie="movie"
          />
        </div>
        <div v-else class="text-gray-500 mt-10">No se encontraron resultados.</div>
      </section>
    </main>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import FilterResultCard from '~/components/FilterResultCard.vue';
import { useSupabaseAuthClient } from '#imports';

useHead({
  title: 'Search',
  meta: [
    { name: 'description', content: 'Search results.' }
  ]
})

definePageMeta({
  layout: "home"
})

const filterResults = ref([]); // Almacenar resultados
const route = useRoute(); // Capturar parámetros de la URL
const router = useRouter(); // Router para manejar navegaciones
const client = useSupabaseAuthClient();

const currentGenre = ref(''); // Género actual
const currentSort = ref(''); // Orden actual

// Función para obtener los resultados del filtrado
const fetchFilterResults = async () => {
  const genre = route.query.genre || ''; // Obtener género de la URL
  const type = route.query.type || ''; // Obtener tipo de orden de la URL
  const length = null; // Longitud predeterminada

  // Guardar valores actuales para mostrar el estado del filtro
  currentGenre.value = genre || 'Todos';
  currentSort.value = type || 'Relevancia';

  // Realizar la llamada al backend
  const { data, error } = await client.rpc('sort_movies', {
    genre_: genre,
    type: type,
    length: length,
  });

  if (error) {
    console.error('Error fetching filtered movies:', error);
    return;
  }

  filterResults.value = data; // Asignar resultados
};

// Reaccionar a cambios en los parámetros de la URL
watch(
  () => route.query, // Observar cambios en la query de la URL
  () => {
    fetchFilterResults(); // Refrescar los resultados si los filtros cambian
  }
);

// Cargar resultados al montar el componente
fetchFilterResults();
</script>
