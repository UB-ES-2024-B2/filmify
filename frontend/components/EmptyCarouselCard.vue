<template>
  <div 
    class="rounded-lg flex flex-col items-center bg-gray-200 shadow-lg cursor-pointer h-[350px] w-[150px] hover:shadow-2xl transition-shadow duration-200"
    @click="goToHome"
  >
    <div class="flex flex-col items-center justify-center h-full">
      <h1 class="text-4xl font-bold text-gray-500 hover:text-gray-700 transition-colors duration-200">+</h1>
      <p class="text-center text-gray-500 hover:text-gray-700 transition-colors duration-200">Explora las películas!</p>
    </div>
  </div>
</template>

<script setup lang="ts">
const goToHome = () => {
  navigateTo({
    path: '/', // Redirect to the home page
  });
};
</script>