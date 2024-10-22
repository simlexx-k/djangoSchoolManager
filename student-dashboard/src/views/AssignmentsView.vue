<template>
  <div class="assignments p-6">
    <h1 class="text-2xl font-bold mb-4">Assignments</h1>
    <div v-if="isLoading" class="text-center py-4">Loading assignments...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>
    <div v-else class="space-y-4">
      <div v-for="assignment in assignments" :key="assignment.id" class="bg-white p-4 rounded shadow">
        <h2 class="text-lg font-semibold">{{ assignment.title }}</h2>
        <p class="text-gray-600">Due: {{ new Date(assignment.due_date).toLocaleDateString() }}</p>
        <p class="mt-2">{{ assignment.description }}</p>
        <p class="mt-2 font-semibold">Status: {{ assignment.status }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/config'

const assignments = ref([])
const isLoading = ref(true)
const error = ref(null)

const fetchAssignments = async () => {
  isLoading.value = true
  error.value = null
  try {
    const response = await api.get('/student/assignments/')
    assignments.value = response.data
  } catch (err) {
    console.error('Error fetching assignments:', err)
    error.value = 'Failed to load assignments. Please try again.'
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchAssignments)

defineExpose({ fetchAssignments })
</script>
