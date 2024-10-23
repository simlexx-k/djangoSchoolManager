<template>
  <div class="animate-pulse">
    <div v-if="type === 'text'" class="h-4 bg-gray-200 rounded w-3/4"></div>
    <div v-else-if="type === 'card'" class="h-24 bg-gray-200 rounded"></div>
    <div v-else-if="type === 'chart'" class="h-64 bg-gray-200 rounded"></div>
  </div>
</template>

<script>
export default {
  props: {
    type: {
      type: String,
      default: 'text'
    }
  }
}
</script>
