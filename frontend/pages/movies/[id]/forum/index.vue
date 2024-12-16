<template>
  <main>
    <section>
      <div v-if="!movieTitle || forum_exist === null" class="text-center">


        <p id="loading-forum" class="text-gray-500 text-lg">Loading forum...</p>
      </div>

      <div v-else>
        <div v-if="forum_exist" id="forum-exists">
          <!-- Forum Title -->
          <div id="forum-header" class="flex justify-between items-center mb-6">
            <div>
                <h1 id="forum-name" class="text-4xl font-bold">{{ forum[0]?.name }}</h1>
                <h3 id="forum-description" class="">{{ forum[0]?.description }}</h3>
            </div>
            <div>
              <UButton 
                id="post-button"
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

          <div id="posts-container" class="container mx-auto mt-6">

            <div class="space-y-6">
              <!-- Loop through posts -->
              <PostCard @change-vote="changeVote" @delete-post="fetchDeletePost"
                v-for="(post, index) in posts"
                :key="index"
                :post="post"
              />
            </div>
          </div>
        </div>

        <div v-else id="forum-not-available">

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
        
        <div class="mb-4" v-if="boolImagePost">
          <img :src="postImage" class="rounded img-fluid" alt="...">
        </div>

        <div style="margin-top: 2mm;">
          <input class="flex" type="file" accept="image/*" @change="onFileChange" />
        </div>

        <!-- Botones -->
        <div class="flex justify-end gap-4">
          <UButton @click="closeModal" class=" px-4" color="gray" size="md">Cancelar</UButton>
          <br/>
          <UButton :disabled="BtnSubmitPost" @click="submitPost" class=" px-4" color="purple" size="md">Post</UButton>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';
import { useSupabaseUser } from '#imports';
import { ref, onMounted } from 'vue';
import { ref as storage_Ref, uploadBytes, getDownloadURL } from 'firebase/storage';

const { $storage } = useNuxtApp();

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

const BtnSubmitPost = ref(false)
// Abre modal
const openModal = () => {
  BtnSubmitPost.value = false;
  isModalOpen.value = true;
};

// Cierra modal
const closeModal = () => {
  isModalOpen.value = false;
  newPost.value = { title: '', content: '' }; // Resetea modal
  postImage.value = null;
  boolImagePost.value = false;
};

const boolImagePost = ref(false);

// Handle post submission
const submitPost = () => {
  BtnSubmitPost.value = true;
  if (newPost.value.title && newPost.value.content) {
    if (boolImagePost.value) {
      uploadImage()
    }
    else{
      fetchCreatePost()
      closeModal(); // Cierra tras publicar
    }
  } else {
    BtnSubmitPost.value = false;
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

const fetchDeletePost = async (post) => {
  const { error } = await client.rpc('delete_post_by_id',{ input_post_id: post.post_id, input_user_id: u_id.value});

  if (error) {
    console.error('Error al eliminar el post:', error);
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


const postImage = ref(null);
const file = ref(null);

const onFileChange = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files[0]) {
    file.value = input.files[0];
    const reader = new FileReader();

    reader.onload = (e) => {
      postImage.value = e.target?.result as string;
    };

    reader.readAsDataURL(file.value);
    boolImagePost.value = true;
  }
}


const maxSize = 5 * 1024 * 1024; // 5 MB
const uploadImage = async () => {
  try {
    const upload_file = file.value

    if (upload_file == null) {
      throw new Error('No has seleccionado la imagen.')
    }
    if (upload_file.size > maxSize){
      throw new Error('La imagen supera el límite de 5MB.')
    }
    if (!upload_file.type.startsWith('image/')) {
      throw new Error('Solo se permiten archivos de imagen.');
    }

    const fileName = upload_file.name;
    const fileExtension = fileName.substring(fileName.lastIndexOf('.') + 1);

    const storageRef = storage_Ref($storage, 'postsImages/' + movieId + u_id.value + Date.now() + "." + fileExtension);
 
    const snapshot = await uploadBytes(storageRef,upload_file);
    console.log('Imagen subida:', snapshot);


    const downloadURL = await getDownloadURL(storageRef);

    fetchCreatePostWithImage(downloadURL.split('&token')[0]);
    closeModal();

  } catch (error) {
    console.error('Error al subir la imagen:', error);
    alert(error.message); // Mensaje de error para el usuario
    closeModal();
  }
}

const fetchCreatePostWithImage = async (url) => {
  const { error } = await client.rpc('create_post',{title: newPost.value.title, content: newPost.value.content, input_movie_id: parseInt(movieId, 10), user_id: u_id.value, image: url});

  if (error) {
    console.error('Error al crear el post:', error);
  } 
  else {
    fetchPostsForum();
  }
};


</script>
  
  
  