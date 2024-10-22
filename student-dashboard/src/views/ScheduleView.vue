<template>
  <div class="schedule p-6">
    <h1 class="text-2xl font-bold mb-4">My Schedule</h1>
    <div v-if="isLoading" class="text-center py-4">Loading schedule...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>
    <div v-else class="grid grid-cols-7 gap-4">
      <div v-for="day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']" :key="day" class="font-bold text-center">
        {{ day }}
      </div>
      <template v-for="(classes, index) in schedule" :key="index">
        <div class="border p-2 min-h-[100px]">
          <div v-for="class_ in classes" :key="class_.id" class="mb-2 p-1 bg-blue-100 rounded">
            <p class="font-semibold">{{ class_.course_name }}</p>
            <p class="text-sm">{{ class_.time }}</p>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/config'

const schedule = ref([])
const isLoading = ref(true)
const error = ref(null)

const fetchSchedule = async () => {
  isLoading.value = true
  error.value = null
  try {
    const response = await api.get('/student/schedule/')
    schedule.value = response.data
  } catch (err) {
    console.error('Error fetching schedule:', err)
    error.value = 'Failed to load schedule. Please try again.'
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchSchedule)

defineExpose({ fetchSchedule })
</script>
