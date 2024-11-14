<template>
  <main class="px-10 overflow-y-auto page xl:px-12">
    <section
      class="container mx-auto flex flex-col gap-5 items-center justify-center mt-6 scroll-mt-[120px] min-h-screen"
    >
      <div v-if="movie" class="text-center">
        <h1 class="text-4xl font-bold mb-2">{{ movie.title }}</h1>
        <p class="text-gray-500">{{ movie.year }} | {{ movie.vote_average }} | {{ movie.genre }} min</p>
      </div>

      <div v-if="movie" class="flex flex-col md:flex-row gap-8 mt-8 w-full">
        <NuxtImg
          :src="movie.poster_url"
          :alt="movie.title"
          class="md:w-1/3 w-full aspect-[2/3] object-cover rounded-lg"
        />
        <div class="flex flex-col md:w-2/3">
          <NuxtRating
            class="flex w-full justify-center mb-4"
            :read-only="true"
            :ratingValue="(movie.vote_average / 10) * 5"
            :rating-size="30"
            :activeColor="'#800080'"
          />
          <p class="text-gray-500 text-lg md:text-xl">{{ movie.overview }}</p>
        </div>
      </div>

      <div v-if="movie" class="mt-8 bg-gray-200 p-4 rounded-lg w-full">
        <h2 class="text-3xl text-center font-bold mb-6">Info</h2>
        <div class="grid grid-cols-5 gap-4 text-gray-700">
          <div class="font-bold col-span-1">Director:</div>
          <div class="col-span-4">{{ movie.director }}</div>

          <div class="font-bold col-span-1">Actores:</div>
          <div class="col-span-4">{{ movie.actors }}</div>

          <div class="font-bold col-span-1">Idioma:</div>
          <div class="col-span-4">{{ movie.language }}</div>

          <div class="font-bold col-span-1">Género:</div>
          <div class="col-span-4">{{ movie.genre }}</div>

          <div class="font-bold col-span-1">Fecha de estreno:</div>
          <div class="col-span-4">{{ movie.release_date }}</div>
        </div>
      </div>
    </section>
  </main>
</template>

  
  <script setup lang="ts">
  
  const movie = ref({
    title: 'Dummy Movie Title',
    year: 2023,
    vote_average: 8.5,
    genre: 'Sci-Fi',
    poster_url: '/img/joker.jpg',
    overview: 'Forever alone in a crowd, failed comedian Arthur Fleck seeks connection as he walks the streets of Gotham City. Arthur wears two masks -- the one he paints for his day job as a clown, and the guise he projects in a futile attempt to feel like hes part of the world around him. Isolated, bullied and disregarded by society, Fleck begins a slow descent into madness as he transforms into the criminal mastermind known as the Joker.',
    director: 'This is a dummy movie overview. Replace with actual data from Supabase.',
    actors: 'This is a dummy movie overview. Replace with actual data from Supabase.',
    language: 'This is a dummy movie overview. Replace with actual data from Supabase.',
    release_date: 'This is a dummy movie overview. Replace with actual data from Supabase.'
    });
  
  </script>