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
    @click="goToDetails"
    :class="`rounded-lg flex flex-col items-center bg-gray-200 shadow-lg cursor-pointer h-[350px] w-[150px] ${item.background}`"
  >
    <NuxtImg
      :src="item.poster_url"
      :alt="item.title"
      sizes="100px md:200px"
      class="object-cover flex-grow w-full rounded-t-lg"
      draggable="false"
    />
    <div class="flex flex-col items-center justify-between h-[30%] p-4">
      <h3 class="text-xs font-display text-slate-800 text-center line-clamp-3" style="max-width: 100%; overflow: hidden">
        {{ item.title }}
      </h3>
      <NuxtRating
        class="flex w-full justify-center"
        :read-only="true"
        :ratingValue="item.vote_average"
        :activeColor="'#800080'"
      />
    </div>
  </div>
</template>