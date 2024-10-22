<template>
  <div class="messages p-6">
    <h1 class="text-2xl font-bold mb-4">Messages</h1>
    <div v-if="isLoading" class="text-center py-4">Loading messages...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>
    <div v-else class="space-y-4">
      <div v-for="message in messages" :key="message.id" class="bg-white p-4 rounded shadow">
        <h2 class="text-lg font-semibold">{{ message.subject }}</h2>
        <p class="text-gray-600">From: {{ message.sender }}</p>
        <p class="text-gray-600">{{ new Date(message.date).toLocaleString() }}</p>
        <p class="mt-2">{{ message.content }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/config'

const messages = ref([])
const isLoading = ref(true)
const error = ref(null)

const fetchMessages = async () => {
  isLoading.value = true
  error.value = null
  try {
    const response = await api.get('/student/messages/')
    messages.value = response.data
  } catch (err) {
    console.error('Error fetching messages:', err)
    error.value = 'Failed to load messages. Please try again.'
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchMessages)

defineExpose({ fetchMessages })
</script>
