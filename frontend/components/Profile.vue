<template>
    <div class="flex flex-col md:flex-row my-4 gap-6 md:gap-8 items-center"> <!-- Add items-center to center vertically -->
      <!-- Profile Image -->
      <div class="flex-shrink-0 flex flex-col items-center md:items-start">
        <NuxtImg
          class="rounded-full w-2/3 h-auto md:w-32 md:h-32"
          :src="profileImage"
          alt="Profile Image"
        />
      </div>
  
      <!-- Profile Info -->
      <div class="flex-grow text-center md:text-left">
        <h2 class="text-2xl font-bold">{{ username }}</h2>
        <p>{{ email }}</p>
        <p class="text-xs text-gray-500">{{ bio }}</p>
      </div>
  
      <!-- Stats -->
      <div class="flex-shrink-0 flex flex-row md:flex-col justify-around text-center md:items-center gap-4 md:gap-2">
        <div>
          <p class="text-2xl font-bold text-purple-800">{{ averageRating }}</p>
          <p class="text-xs text-gray-500">Rating promedio</p>
        </div>
      </div>
    </div>
  </template>
  
    
    <script setup>
    const profileImage = 'https://avatars.githubusercontent.com/u/113581734?v=4';
    const username = 'John Doe';
    const email = 'johndoe@example.com';
    const bio = '"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum." ';
    const averageRating = 4.5;
    </script>