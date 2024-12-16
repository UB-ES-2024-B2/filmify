<script setup>
const props = defineProps({
  item: Object,
  index: Number,
});

const goToDetails = () => {
  navigateTo({
    path: `/movies/${props.item.title.replace(/\s+/g, '-').toLowerCase()}`,
    query: { id: props.item.id },
  });
};
</script>

<template>
  <div
    class="group relative rounded-lg overflow-hidden shadow-lg transform transition-transform duration-300 cursor-pointer "
    @click="goToDetails"
  >
    <NuxtImg
      :src="item.poster_url"
      :alt="item.title"
      sizes="100px md:200px"
      class="object-cover h-full w-full"
      draggable="false"
    />
    <div
      class="absolute inset-0 bg-black bg-opacity-50 flex flex-col justify-end p-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
    >
      <h3 class="text-white text-lg font-semibold truncate">{{ item.title }}</h3>
      <p class="text-gray-300 text-sm">{{ item.vote_average.toFixed(1) }} / 10</p>
    </div>
  </div>
</template>