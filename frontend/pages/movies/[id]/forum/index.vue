<template>
    <main>
      <section>
        <div v-if="!movieTitle || forum_exist === null" class="text-center">
          <p class="text-gray-500 text-lg">Loading forum...</p>
        </div>
  
        <div v-else>
          <div v-if="forum_exist">
            <!-- Forum Header -->
            <div class="flex justify-between items-center mb-6">
                <div>
                    <h1 class="text-4xl font-bold">{{ forum[0]?.name }}</h1>
                    <h3 class="">{{ forum[0]?.description }}</h3>
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
          <div v-else>
              <h1 class="text-4xl font-bold"> El Foro de la película {{ movieTitle }} aún no está disponible.</h1>
          </div>
        </div>
      </section>
    </main>
  </template>
  
  <script setup>
  import { useRoute } from 'vue-router';
  import { useSupabaseUser } from '#imports';
  import { ref, onMounted } from 'vue';
  
  useHead({
    title: 'Forum',
    meta: [{ name: 'description', content: 'Forum' }],
  });
  
  definePageMeta({
    layout: 'home',
  });
  
  const route = useRoute();
  const client = useSupabaseAuthClient()
  const user = useSupabaseUser();
  const movieId = route.query.id; // Access movie ID from query params
  const movieTitle = route.params.id; // Access movie title from route params


  const forum = ref([]);
  const forum_exist = ref(null)
  

  const fetchExistsForum = async () => {
    const { data, error } = await client.rpc('exists_forum',{input_movie_id: parseInt(movieId, 10)});

    if (error) {
      console.error('Error al comprobar si el foro existe:', error);
    } else {
      forum_exist.value = data;
      if (data){
        fetchForum();
      }
    }
  };


  const fetchForum = async () => {
    const { data, error } = await client.rpc('get_forum_info',{input_movie_id: parseInt(movieId, 10)});

    if (error) {
      console.error('Error al obtener la info de forum:', error);
    } else {
      forum.value = data;
    }
  };

  onMounted(fetchExistsForum);
  </script>
  
  