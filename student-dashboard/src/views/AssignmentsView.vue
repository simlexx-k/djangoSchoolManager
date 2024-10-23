<template>
  <div class="assignments p-6 bg-gray-100 min-h-screen">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-800 mb-6">Assignments</h1>

      <div v-if="isLoading" class="space-y-4">
        <div v-for="i in 3" :key="i" class="bg-white rounded-lg shadow-md p-6 animate-pulse">
          <div class="h-6 bg-gray-200 rounded w-3/4 mb-4"></div>
          <div class="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
          <div class="h-4 bg-gray-200 rounded w-5/6 mb-4"></div>
          <div class="flex justify-between items-center">
            <div class="h-8 bg-gray-200 rounded w-1/4"></div>
            <div class="h-8 bg-gray-200 rounded w-1/4"></div>
          </div>
        </div>
      </div>

      <div v-else-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded" role="alert">
        <p class="font-bold">Error</p>
        <p>{{ error }}</p>
      </div>

      <div v-else-if="assignments.length === 0" class="text-center py-10">
        <p class="text-xl text-gray-600">No assignments available at the moment.</p>
      </div>

      <div v-else class="space-y-4">
        <div v-for="assignment in assignments" :key="assignment.id" 
             class="bg-white rounded-lg shadow-md overflow-hidden transition duration-300 ease-in-out hover:shadow-lg">
          <div class="p-6">
            <div class="flex justify-between items-start mb-4">
              <h2 class="text-xl font-semibold text-gray-800">{{ assignment.title }}</h2>
              <span :class="getStatusClass(assignment.status)">
                {{ assignment.status || 'Unknown' }}
              </span>
            </div>
            <div class="text-gray-600 mb-4 prose max-w-none" v-dompurify-html="assignment.description"></div>
            <div class="flex justify-between items-center text-sm">
              <span class="text-gray-500">
                Due: {{ formatDate(assignment.due_date) }}
              </span>
              <button @click="handleAssignmentAction(assignment)" 
                      class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded transition duration-300 ease-in-out">
                {{ getActionButtonText(assignment.status) }}
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
import { useRouter } from 'vue-router'
import studentApi from '@/api/student'
import VueDOMPurifyHTML from 'vue-dompurify-html'
import { createApp } from 'vue'

const app = createApp({})
app.use(VueDOMPurifyHTML)

const assignments = ref([])
const isLoading = ref(true)
const error = ref(null)
const router = useRouter()

const fetchAssignments = async () => {
  try {
    const response = await studentApi.getAssignments()
    assignments.value = response.data.results
    console.log('Fetched assignments:', assignments.value)
  } catch (error) {
    console.error('Error fetching assignments:', error)
    error.value = 'Failed to load assignments. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString(undefined, options)
}

const getStatusClass = (status) => {
  const baseClasses = 'px-2 py-1 rounded-full text-xs font-medium'
  if (!status) return `${baseClasses} bg-gray-100 text-gray-800`
  
  switch (status.toLowerCase()) {
    case 'completed':
      return `${baseClasses} bg-green-100 text-green-800`
    case 'in progress':
      return `${baseClasses} bg-yellow-100 text-yellow-800`
    case 'pending':
      return `${baseClasses} bg-red-100 text-red-800`
    default:
      return `${baseClasses} bg-gray-100 text-gray-800`
  }
}

const getActionButtonText = (status) => {
  if (!status) return 'View Details'
  
  switch (status.toLowerCase()) {
    case 'pending':
      return 'Start Assignment'
    case 'submitted':
      return 'View Submission'
    case 'graded':
      return 'View Grade'
    default:
      return 'View Details'
  }
}

const handleAssignmentAction = (assignment) => {
  const status = assignment.status ? assignment.status.toLowerCase() : 'unknown'
  switch (status) {
    case 'pending':
      router.push(`/assignments/${assignment.id}/submit`)
      break
    case 'submitted':
      router.push(`/assignments/${assignment.id}/submission`)
      break
    case 'graded':
      router.push(`/assignments/${assignment.id}/grade`)
      break
    default:
      router.push(`/assignments/${assignment.id}`)
  }
}

onMounted(fetchAssignments)

defineExpose({ fetchAssignments })
</script>
