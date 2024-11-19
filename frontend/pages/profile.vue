<template>
  <main class="px-10 overflow-y-auto dark:bg-slate-800 page xl:px-12">
    <section class="container mx-auto flex flex-col gap-5 items-center justify-center mt-6 scroll-mt-[120px] min-h-screen">
      <Profile :userData="userData"/>

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
const client = useSupabaseAuthClient();
const user = useSupabaseUser()
const userData = user.value?.user_metadata

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
  }
});
</script>
