<template>
  <main class="px-10 overflow-y-auto dark:bg-slate-800 page xl:px-12">
    <section class="container mx-auto flex flex-col gap-5 items-center justify-center mt-6 scroll-mt-[120px] min-h-screen">
      <Profile :userData="userInfo" @modify-pfp="openModal" v-if="info"/>

<!-- Modal para crear el post-->
      <div v-if="isModalOpen" class="fixed inset-0 flex justify-center items-center bg-black bg-opacity-50" style="z-index: 10000;">
        <div class="bg-white p-6 rounded-md w-96">
          <h2 class="text-xl font-semibold mb-4">Modificar Foto de Perfil</h2>

          <img :src="newPFP" class="rounded img-fluid" alt="...">

          <!-- Input comentario-->
          <div style="margin-top: 2mm;">
            <input class="flex" type="file" accept="image/*" @change="onFileChange">
          </div>

          <!-- Botones -->
          <div class="flex justify-center gap-4" style="margin-top: 2mm;">
            <UButton @click="closeModal" class=" px-4" color="gray" size="md">Cancelar</UButton>
            <UButton @click="submitPFP" class=" px-4" color="purple" size="md">Modificar</UButton>
          </div>
        </div>
      </div>

      <h2 class="text-2xl font-display">Favoritas</h2>
      <template v-if="fav_list.length > 0">
        <UCarousel 
          class="px-10"
          v-slot="{ item, index }"
          :items="fav_list"
          :ui="{
            wrapper: 'w-full flex justify-center',
            container: 'flex justify-center gap-5',
            item: 'h-[350px] w-[150px]',
          }"
          arrows
        >
          <CarouselCard :item="item" :index="index" />
        </UCarousel>
      </template>
      <template v-else>
        <EmptyCarouselCard />
      </template>

      <h2 class="text-2xl font-display">Wishlist</h2>
      <template v-if="wish_list.length > 0">
        <UCarousel 
          class="px-10"
          v-slot="{ item, index }"
          :items="wish_list"
          :ui="{
            wrapper: 'w-full flex justify-center',
            container: 'flex justify-center gap-5',
            item: 'h-[350px] w-[150px]',
          }"
          arrows
        >
          <CarouselCard :item="item" :index="index" />
        </UCarousel>
      </template>
      <template v-else>
        <EmptyCarouselCard />
      </template>

    </section>
  </main>
</template>
  
<script setup lang="ts">

import { ref, onMounted } from 'vue';
import { ref as storage_Ref, uploadBytes, getDownloadURL } from 'firebase/storage';
const { $storage } = useNuxtApp();
const client = useSupabaseAuthClient();
const user = useSupabaseUser()

useHead({
  title: 'User profile',
  meta: [
    { name: 'description', content: 'Profile view.' }
  ]
});

definePageMeta({
  layout: "home"
});

// Reactive lists for favorites and wishlist
const fav_list = ref([]);
const wish_list = ref([]);

// Reactive user ID
const user_id = ref(null);

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
    user_id.value = user.user.id || null;
  }
};


const fetchFavList = async () => {
  if (!user_id.value) return;


  const { data, error } = await client.rpc('get_favorites', { user_id: user_id.value });
  if (error) {
    console.error('Error fetching favorites:', error);
  } else {
    fav_list.value = data;
  }
};


const fetchWishList = async () => {
  if (!user_id.value) return;

  const { data, error } = await client.rpc('get_wishlist', { user_id: user_id.value });
  if (error) {
    console.error('Error fetching wishlist:', error);
  } else {
    wish_list.value = data;
  }
};

onMounted(async () => {
  await fetchUserId();
  if (user_id.value) {
    await fetchFavList();
    await fetchWishList();
    await fetchUserInfo();
  }
});

const newPFP = ref([])
const userInfo = ref([])
const info = ref(false)
const fetchUserInfo = async () => {
  if (!user_id.value) return;

  const { data, error } = await client.rpc('getuserinfo', { user_id: user_id.value });
  if (error) {
    console.error('Error fetching user info:', error);
  } else {
    userInfo.value = data[0];
    if(userInfo.value.profile_image_url == ''){
      userInfo.value.profile_image_url = "https://firebasestorage.googleapis.com/v0/b/filmify-c99db.firebasestorage.app/o/userImages%2Fdefault-pfp.png?alt=media";    
    }
    info.value = true;
    newPFP.value = userInfo.value.profile_image_url;
  }
};

// Estado de modal
const isModalOpen = ref(false);

// Abre modal
const openModal = () => {
  isModalOpen.value = true;
};

const new_pfp_url = ref(null)
const submitPFP = () => {
  uploadImage();
  isModalOpen.value = false;
};

// Cierra modal
const closeModal = () => {
  newPFP.value = userInfo.value.profile_image_url;
  isModalOpen.value = false;
};
const file = ref(null)

const onFileChange = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files[0]) {
    file.value = input.files[0];
    const reader = new FileReader();

    reader.onload = (e) => {
      newPFP.value = e.target?.result as string;
    };

    reader.readAsDataURL(file.value);
  }
}


const maxSize = 5 * 1024 * 1024; // 5 MB
async function uploadImage() {
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

    const storageRef = storage_Ref($storage, 'userImages/' + user_id.value + "." + fileExtension);

    const snapshot = await uploadBytes(storageRef,upload_file);
    console.log('Imagen subida:', snapshot);


    const downloadURL = await getDownloadURL(storageRef);

    fetchAddPFP(downloadURL.split('&token')[0]);
  } catch (error) {
    console.error('Error al subir la imagen:', error);
    alert(error.message); // Mensaje de error para el usuario
  }
}

const fetchAddPFP = async (url) => {
  if (!user_id.value) return;

  const { data, error } = await client.rpc('add_profile_pic', { input_user_id: user_id.value, image: url });

  if (error) {
    console.error('Error fetching wishlist:', error);
  } else {
    if (data) {
      window.location.reload();
    }
  }
};
</script>
