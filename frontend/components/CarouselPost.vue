<template>
    <div
      :class="`rounded-lg flex flex-col items-center bg-gray-200 shadow-lg h-[150px] w-[225px] ${item.background}`"
    >
      <div class="flex flex-col items-center justify-between h-[100%] p-4">
        <h3 class="text-sm font-display text-slate-800 text-center line-clamp-3" style="max-width: 100%; overflow: hidden">
          {{ item.title }}
        </h3>
        <!-- Nombre de la película -->
        <p class="text-sm text-gray-700 text-center font-bold">{{ item.movie_title }}</p>
        <p class="text-sm text-gray-600 text-center">{{ item.content }}</p>
      </div>
    </div>
  </template>
  
  <script setup>
  const props = defineProps({
    item: Object,
    index: Number,
  });
  </script>
  