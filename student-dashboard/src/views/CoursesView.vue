<template>
  <div class="courses p-6">
    <h1 class="text-2xl font-bold mb-4">My Courses</h1>
    <div v-if="isLoading" class="text-center py-4">Loading courses...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="course in courses" :key="course.id" class="bg-white p-4 rounded shadow">
        <h2 class="text-lg font-semibold">{{ course.name }}</h2>
        <p class="text-gray-600">{{ course.instructor }}</p>
        <p class="mt-2">{{ course.description }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/config'

const courses = ref([])
const isLoading = ref(true)
const error = ref(null)

const fetchCourses = async () => {
  isLoading.value = true
  error.value = null
  try {
    const response = await api.get('/student/courses/')
    courses.value = response.data
  } catch (err) {
    console.error('Error fetching courses:', err)
    error.value = 'Failed to load courses. Please try again.'
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchCourses)

defineExpose({ fetchCourses })
</script>
