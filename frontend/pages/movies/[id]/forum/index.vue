<template>
    <main>
      <section>
        <div v-if="!movieTitle" class="text-center">
          <p class="text-gray-500 text-lg">Loading forum...</p>
        </div>
  
        <div v-else>

          <!-- Forum Header -->
            <div class="flex justify-between items-center mb-6">
                <div>
                    <h1 class="text-4xl font-bold">{{ movieTitle }}</h1>
                </div>
                <div>
                    <UButton 
                    v-if="user" 
                    class="mx-auto px-8"
                    color="purple"
                    size="xl">
                    Post
                    </UButton>
                </div>
            </div>
          <!-- Posts Container -->
          <div class="container mx-auto mt-6">
            <div class="space-y-6"> 
            </div>
          </div>
        </div>
      </section>
    </main>
  </template>
  
  <script setup>
  import { useRoute } from 'vue-router';
  import { useSupabaseUser } from '#imports';
  
  useHead({
    title: 'Forum',
    meta: [{ name: 'description', content: 'Forum' }],
  });
  
  definePageMeta({
    layout: 'home',
  });
  
  const route = useRoute();
  const user = useSupabaseUser();
  const movieId = route.query.id; // Access movie ID from query params
  const movieTitle = route.params.id; // Access movie title from route params
  </script>
  
  