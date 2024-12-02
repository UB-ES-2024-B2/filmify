<template>
  <div v-if="userData" class="flex flex-col md:flex-row my-4 gap-6 md:gap-8 items-center">
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
      <h2 class="text-2xl font-bold">{{ userData.username }}</h2>
      <p>{{ userData.email }}</p>
      <p class="text-xs text-gray-500">{{ bio }}</p>
      <button 
        @click="toggleEditMode"
        class="bg-purple-600 text-white px-4 py-2 mt-4 rounded hover:bg-purple-800"
      >
        Modificar perfil
      </button>
    </div>

    <!-- Stats -->
    <div class="flex-shrink-0 flex flex-row md:flex-col justify-around text-center md:items-center gap-4 md:gap-2">
      <div>
        <p class="text-2xl font-bold text-purple-800">{{ averageRating }}</p>
        <p class="text-xs text-gray-500">Rating promedio</p>
      </div>
    </div>

    <!-- Edit Profile Modal -->
    <EditProfileModal
      v-if="editMode"
      :userData="userData"
      @close="toggleEditMode"
    />
  </div>
  <p v-else class="text-center text-gray-500">Cargando perfil...</p>
</template>


<script setup>
import { ref } from 'vue';
import EditProfileModal from '@/components/EditProfileModal.vue';

const props = defineProps({
  userData: Object
});

const profileImage = 'https://avatars.githubusercontent.com/u/113581734?v=4';
const bio = '"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."';
const averageRating = ref(null);

const fetchAverageRating = async () => {
  const { data, error } = await useSupabaseAuthClient().rpc('calculate_mean_rating', { user_id: props.userData.sub });
  if (error) {
    console.error(error);
  } else {
    averageRating.value = data;
  }
};

const editMode = ref(false);

const toggleEditMode = () => {
  editMode.value = !editMode.value;
};

onMounted(() => {
  fetchAverageRating();
});
</script>
