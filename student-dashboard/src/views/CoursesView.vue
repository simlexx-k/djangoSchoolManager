<template>
  <div class="subjects p-6 bg-gray-100 min-h-screen">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-800 mb-6">My Subjects</h1>
      
      <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="i in 6" :key="i" class="bg-white rounded-lg shadow-md p-6 animate-pulse">
          <div class="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
          <div class="h-3 bg-gray-200 rounded w-1/2 mb-2"></div>
          <div class="h-3 bg-gray-200 rounded w-5/6 mb-4"></div>
          <div class="h-20 bg-gray-200 rounded mb-4"></div>
          <div class="flex justify-between items-center">
            <div class="h-8 bg-gray-200 rounded w-1/3"></div>
            <div class="h-8 bg-gray-200 rounded w-1/3"></div>
          </div>
        </div>
      </div>

      <div v-else-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded" role="alert">
        <p class="font-bold">Error</p>
        <p>{{ error }}</p>
      </div>

      <div v-else-if="subjects.length === 0" class="text-center py-10">
        <p class="text-xl text-gray-600">No subjects available at the moment.</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="subject in subjects" :key="subject.id" class="bg-white rounded-lg shadow-md overflow-hidden transition duration-300 ease-in-out transform hover:scale-105">
          <div class="p-6">
            <h2 class="text-xl font-semibold text-gray-800 mb-2">{{ subject.name }}</h2>
            <p class="text-sm text-gray-600 mb-2">Teacher: {{ subject.instructor }}</p>
            <p class="text-sm text-gray-500 mb-4">Code: {{ subject.code }}</p>
            <p class="text-gray-700 mb-4 h-20 overflow-y-auto">{{ subject.description }}</p>
            <div class="flex justify-between items-center">
              <span class="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                {{ subject.credits }} credits
              </span>
              <button @click="viewSubjectDetails(subject.id)" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">
                View Details
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/config'

const subjects = ref([])
const isLoading = ref(true)
const error = ref(null)

const fetchSubjects = async () => {
  isLoading.value = true
  error.value = null
  try {
    const response = await api.get('/student/courses/')
    subjects.value = response.data
  } catch (err) {
    console.error('Error fetching subjects:', err)
    error.value = 'Failed to load subjects. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const viewSubjectDetails = (subjectId) => {
  // Implement navigation to subject details page
  console.log(`Viewing details for subject ${subjectId}`)
}

onMounted(fetchSubjects)

defineExpose({ fetchSubjects })
</script>
