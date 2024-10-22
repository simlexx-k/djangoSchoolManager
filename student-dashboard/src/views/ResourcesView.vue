<template>
  <div class="resources p-6">
    <h1 class="text-2xl font-bold mb-4">Learning Resources</h1>
    <div v-if="isLoading" class="text-center py-4">Loading resources...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="resource in resources" :key="resource.id" class="bg-white p-4 rounded shadow">
        <h2 class="text-lg font-semibold">{{ resource.title }}</h2>
        <p class="text-gray-600">{{ resource.type }}</p>
        <p class="mt-2">{{ resource.description }}</p>
        <a :href="resource.url" target="_blank" class="mt-2 inline-block bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
          Access Resource
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/config'

const resources = ref([])
const isLoading = ref(true)
const error = ref(null)

const fetchResources = async () => {
  isLoading.value = true
  error.value = null
  try {
    const response = await api.get('/student/resources/')
    resources.value = response.data
  } catch (err) {
    console.error('Error fetching resources:', err)
    error.value = 'Failed to load resources. Please try again.'
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchResources)

defineExpose({ fetchResources })
</script>
