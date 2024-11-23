<template>
  <main>
    <section>
      <div v-if="!movieTitle" class="text-center">
        <p class="text-gray-500 text-lg">Loading forum...</p>
      </div>

      <div v-else>
        <!-- Forum Title -->
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
        <!-- Posts Container (single column) -->
        <div class="container mx-auto mt-6">
          <div class="space-y-6"> <!-- This ensures one column with vertical spacing -->
            <!-- Loop through dummy posts -->
            <PostCard
              v-for="(post, index) in dummyPosts"
              :key="index"
              :post="post"
            />
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { useRoute } from 'vue-router';
import { useSupabaseUser } from '#imports';

// Dummy posts data
const dummyPosts = [
  {
    title: 'Post Title 1',
    content: 'This is a short description of the post content. Lorem ipsum dolor sit amet.',
    user: 'User 1',
  },
  {
    title: 'Post Title 2',
    content: 'Another post description goes here. Quisque vitae mauris nec augue volutpat viverra.',
    user: 'User 2',
  },
  {
    title: 'Post Title 3',
    content: 'Yet another example of a post card. Proin tincidunt lacus in lacus aliquet pretium.',
    user: 'User 3',
  },
  {
    title: 'Post Title 4',
    content: 'Curabitur sed diam eget risus varius blandit sit amet non magna.',
    user: 'User 4',
  },
  {
    title: 'Post Title 5',
    content: 'Phasellus eget nisi sit amet erat pharetra pretium eget id felis.',
    user: 'User 5',
  },
];

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
  
  