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
              size="xl"
              @click="openModal"
            >
              Post
            </UButton>
          </div>
        </div>

        <!-- Posts Container -->
        <div class="container mx-auto mt-6">
          <div class="space-y-6">
            <!-- Loop through posts -->
            <PostCard
              v-for="(post, index) in posts"
              :key="index"
              :post="post"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- Modal para crear el post-->
    <div 
      v-if="isModalOpen" 
      class="fixed inset-0 flex justify-center items-center bg-black bg-opacity-50"
    >
      <div class="bg-white p-6 rounded-md w-96">
        <h2 class="text-xl font-semibold mb-4">Crea un post</h2>

        <!-- Input Título -->
        <div class="mb-4">
          <label for="title" class="block text-sm font-medium text-gray-700">Título</label>
          <input 
            v-model="newPost.title" 
            type="text" 
            id="title" 
            class="mt-1 block w-full border border-gray-300 rounded-md p-2"
            placeholder="Escribe el título del post"
          />
        </div>

        <!-- Input comentario-->
        <div class="mb-4">
          <label for="content" class="block text-sm font-medium text-gray-700">Comentario</label>
          <textarea
            v-model="newPost.content"
            id="content"
            class="mt-1 block w-full border border-gray-300 rounded-md p-2"
            placeholder="Escribe tu comentario"
          ></textarea>
        </div>

        <!-- Botones -->
        <div class="flex justify-end gap-4">
          <UButton @click="closeModal" class=" px-4" color="gray" size="md">Cancelar</UButton>
          <UButton @click="submitPost" class=" px-4" color="purple" size="md">Post</UButton>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { useRoute } from 'vue-router';
import { useSupabaseUser } from '#imports';

// Dummy posts data (Now reactive)
const posts = ref([
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
]);

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

// Estado de modal
const isModalOpen = ref(false);
const newPost = ref({
  title: '',
  content: '',
});

// Abre modal
const openModal = () => {
  isModalOpen.value = true;
};

// Cierra modal
const closeModal = () => {
  isModalOpen.value = false;
  newPost.value = { title: '', content: '' }; // Resetea modal
};

// Handle post submission
const submitPost = () => {
  if (newPost.value.title && newPost.value.content) {
    posts.value.push({
      title: newPost.value.title,
      content: newPost.value.content,
      user: user?.user_metadata?.username, // Add user or anonymous
    });

    closeModal(); // Cierra tras publicar
  } else {
    alert('Escribe título y comentario.');
  }
};
</script>
  
  