<template>
  <div class="error-page">
    <h1>Oops! Something went wrong</h1>
    <p>{{ errorMessage }}</p>
    <button @click="reload" class="reload-button">Reload Page</button>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  errorMessage: {
    type: String,
    default: 'An unexpected error occurred.'
  }
})

const reload = () => {
  window.location.reload()
}
</script>

<style scoped>
.error-page {
  text-align: center;
  padding: 50px;
}
.reload-button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #008CBA;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>

