<template>
  <main>
    <section>
      <div v-if="!movieTitle || forum_exist === null" class="text-center">
        <p class="text-gray-500 text-lg">Loading forum...</p>
      </div>

      <div v-else>
        <div v-if="forum_exist">
          <!-- Forum Title -->
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
              <PostCard @change-vote="changeVote"
                v-for="(post, index) in posts"
                :key="index"
                :post="post"
              />
            </div>
          </div>
        </div>
        <div v-else>
          <div class="flex justify-between items-center mb-6">
            <h1 class="text-4xl font-bold"> El Foro de la película {{ movieTitle }} aun no está disponible.</h1>
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
import { ref, onMounted } from 'vue';

useHead({
  title: 'Forum',
  meta: [{ name: 'description', content: 'Forum' }],
});

definePageMeta({
  layout: 'home',
});

const route = useRoute();
const client = useSupabaseAuthClient();
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
    fetchCreatePost();
    closeModal(); // Cierra tras publicar
  } else {
    alert('Escribe título y comentario.');
  }
};

const changeVote = (post, vote_type) => {
  if (post.vote === null){
    fetchVotePost(post, vote_type)
  }else{
    fetchUpdateVotePost(post, vote_type)
  }
};

const fetchVotePost = async (post, vote_type) => {
  const { error } = await client.rpc('vote_post',{input_user_id: u_id.value, input_post_id: post.post_id, vote: vote_type});

  if (error) {
    console.error('Error al crear el post:', error);
  } 
  else {
    fetchPostsForum();
  }
};

const fetchUpdateVotePost = async (post, vote_type) => {
  const { error } = await client.rpc('update_vote_post',{input_user_id: u_id.value, input_post_id: post.post_id, vote: vote_type});

  if (error) {
    console.error('Error al crear el post:', error);
  } 
  else {
    fetchPostsForum();
  }
};

const fetchCreatePost = async () => {
  const { error } = await client.rpc('create_post',{title: newPost.value.title, content: newPost.value.content, input_movie_id: parseInt(movieId, 10), user_id: u_id.value});

  if (error) {
    console.error('Error al crear el post:', error);
  } 
  else {
    fetchPostsForum();
  }
};


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
      fetchPostsForum();
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

// Dummy posts data (Now reactive)
const posts = ref([]);


// Reactive user ID
const u_id = ref(null);

const fetchPostsForum = async () => {
  
  const { data, error } = await client.rpc('get_posts',{input_movie_id: parseInt(movieId, 10), input_user_id: u_id.value});

  if (error) {
    console.error('Error al obtener posts:', error);
  } else {
    posts.value = data;
  }
};


const fetchUserId = async () => {
  const { data: sessionData, error: sessionError } = await client.auth.getSession();

  if (sessionError || !sessionData.session) {
    console.error('User is not authenticated:', sessionError);
    return;
  }

  const { data: user, error: userError } = await client.auth.getUser();


  if (userError) {
    console.error('Error fetching user:', userError);
  } else {
    u_id.value = user.user.id || null;
    fetchPostsForum();
  }
};

const set_UserId  = () => {
  if (user) {
    fetchUserId();
  }
};

onMounted(set_UserId);


</script>
  
  