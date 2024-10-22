<script setup>
defineProps({
  item: Object,
  index: Number,
});
</script>

<template>
  <div
    :class="`rounded-lg flex flex-col items-center bg-gray-200 shadow-lg cursor-pointer h-[300px] w-[150px] ${item.background}`"
  >
    <NuxtImg
      :src="item.poster.src"
      :alt="item.name"
      sizes="100px md:200px"
      class="object-cover h-4/5 w-full rounded-t-lg"
      draggable="false"
    />
    <div class="flex flex-col items-center justify-between h-2/5 p-4">
      <h3 class="text-md font-display text-slate-800 text-center">
        {{ item.name }}
      </h3>
      <NuxtRating
        class="flex w-full justify-center"
        :read-only="true"
        :ratingValue="item.rating"
        :activeColor="'#800080'"
      />
    </div>
  </div>
</template>