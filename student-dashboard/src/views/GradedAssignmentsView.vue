<template>
  <div class="graded-assignments p-6 bg-gray-50 min-h-screen">
    <div class="max-w-6xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-800 mb-8">Graded Assignments</h1>
      
      <div v-if="isLoading">
        <div class="mb-8">
          <SkeletonLoader type="chart" />
        </div>
        <div v-for="i in 3" :key="i" class="mb-8">
          <SkeletonLoader type="card" />
          <div class="mt-4 space-y-2">
            <SkeletonLoader type="text" />
            <SkeletonLoader type="text" />
            <SkeletonLoader type="text" />
          </div>
        </div>
      </div>
      
      <div v-else-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6 rounded-md shadow" role="alert">
        <p class="font-bold">Error</p>
        <p>{{ error }}</p>
      </div>
      
      <div v-else-if="!filteredAndSortedAssignments.length" class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">No graded assignments</h3>
        <p class="mt-1 text-sm text-gray-500">You don't have any graded assignments yet.</p>
      </div>
      
      <div v-else>
        <div class="mb-6 flex flex-wrap justify-between items-center gap-4">
          <div class="flex space-x-4">
            <select v-model="filter" class="form-select rounded-md shadow-sm">
              <option value="all">All Assignments</option>
              <option value="recent">Recent (Last 30 days)</option>
              <option value="highScore">High Scores (90%+)</option>
            </select>
            <select v-model="sort" class="form-select rounded-md shadow-sm">
              <option value="dateDesc">Date (Newest First)</option>
              <option value="dateAsc">Date (Oldest First)</option>
              <option value="scoreDesc">Score (Highest First)</option>
              <option value="scoreAsc">Score (Lowest First)</option>
            </select>
          </div>
          <input v-model="search" type="text" placeholder="Search assignments..." class="form-input rounded-md shadow-sm">
        </div>

        <div class="mb-8">
          <h2 class="text-xl font-semibold mb-4">Performance Overview</h2>
          <canvas ref="chartRef" width="400" height="200"></canvas>
        </div>

        <div class="space-y-8">
          <div v-for="assignment in paginatedAssignments" :key="assignment.id" class="bg-white rounded-lg shadow-md overflow-hidden">
            <div class="px-6 py-4 bg-gradient-to-r from-blue-500 to-indigo-600">
              <h2 class="text-xl font-semibold text-white">{{ assignment.assignment_title }}</h2>
              <p class="text-sm text-blue-100">Submitted: {{ formatDate(assignment.submitted_at) }}</p>
            </div>
            
            <div class="px-6 py-4">
              <div class="flex items-center justify-between mb-4">
                <span class="text-lg font-medium text-gray-700">Score:</span>
                <span class="text-2xl font-bold" :class="scoreColor(assignment.score)">{{ assignment.score }}%</span>
              </div>
              
              <div v-if="assignment.feedback" class="mb-6">
                <h3 class="text-lg font-medium text-gray-700 mb-2">Feedback:</h3>
                <p class="text-gray-600 bg-gray-50 p-3 rounded-md">{{ assignment.feedback }}</p>
              </div>
              
              <div v-if="assignment.question_responses && assignment.question_responses.length > 0">
                <h3 @click="toggleQuestions(assignment.id)" class="text-lg font-medium text-gray-700 mb-4 cursor-pointer flex items-center">
                  <span>Questions and Answers</span>
                  <svg :class="{'rotate-180': expandedAssignments.includes(assignment.id)}" class="ml-2 h-5 w-5 transform transition-transform duration-200" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                </h3>
                <div v-show="expandedAssignments.includes(assignment.id)" class="space-y-4">
                  <div v-for="(response, index) in assignment.question_responses" :key="index" class="border-b border-gray-200 pb-4 last:border-b-0 last:pb-0">
                    <p class="font-medium text-gray-800 mb-2">Q{{ index + 1 }}: {{ response.question_text }}</p>
                    <div class="grid grid-cols-2 gap-4">
                      <div>
                        <p class="text-sm text-gray-500">Your answer:</p>
                        <p class="text-gray-700">{{ response.answer }}</p>
                      </div>
                      <div>
                        <p class="text-sm text-gray-500">Correct answer:</p>
                        <p class="text-gray-700">{{ response.correct_answer }}</p>
                      </div>
                    </div>
                    <p :class="response.is_correct ? 'text-green-600' : 'text-red-600'" class="mt-2 font-medium">
                      {{ response.is_correct ? 'Correct' : 'Incorrect' }} (Score: {{ response.score }})
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <router-link 
              :to="{ name: 'GradedAssignmentDetail', params: { id: assignment.id } }"
              class="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              View Details
            </router-link>
          </div>
        </div>

        <div class="mt-8 flex justify-center">
          <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
            <button @click="currentPage--" :disabled="currentPage === 1" class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
              Previous
            </button>
            <button v-for="page in totalPages" :key="page" @click="currentPage = page" :class="{'bg-blue-50 border-blue-500 text-blue-600': currentPage === page}" class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50">
              {{ page }}
            </button>
            <button @click="currentPage++" :disabled="currentPage === totalPages" class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
              Next
            </button>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import studentApi from '@/api/student'
import Chart from 'chart.js/auto'
import SkeletonLoader from '@/components/SkeletonLoader.vue'
import { useRouter } from 'vue-router'

const gradedAssignments = ref([])
const isLoading = ref(true)
const error = ref(null)
const filter = ref('all')
const sort = ref('dateDesc')
const search = ref('')
const expandedAssignments = ref([])
const currentPage = ref(1)
const itemsPerPage = 5
const chartRef = ref(null)
let chart = null
const router = useRouter()

const fetchGradedAssignments = async () => {
  isLoading.value = true
  error.value = null
  try {
    const data = await studentApi.getGradedAssignments()
    gradedAssignments.value = data
    console.log('Graded assignments:', gradedAssignments.value)
  } catch (err) {
    console.error('Error fetching graded assignments:', err)
    error.value = 'Failed to load graded assignments. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const filteredAndSortedAssignments = computed(() => {
  let result = [...gradedAssignments.value]
  
  if (filter.value === 'recent') {
    const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
    result = result.filter(a => new Date(a.submitted_at) >= thirtyDaysAgo)
  } else if (filter.value === 'highScore') {
    result = result.filter(a => a.score >= 90)
  }
  
  if (search.value) {
    const searchLower = search.value.toLowerCase()
    result = result.filter(a => a.assignment_title.toLowerCase().includes(searchLower))
  }
  
  result.sort((a, b) => {
    if (sort.value === 'dateDesc') return new Date(b.submitted_at) - new Date(a.submitted_at)
    if (sort.value === 'dateAsc') return new Date(a.submitted_at) - new Date(b.submitted_at)
    if (sort.value === 'scoreDesc') return b.score - a.score
    if (sort.value === 'scoreAsc') return a.score - b.score
  })
  
  return result
})

const paginatedAssignments = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredAndSortedAssignments.value.slice(start, end)
})

const totalPages = computed(() => Math.ceil(filteredAndSortedAssignments.value.length / itemsPerPage))

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const scoreColor = (score) => {
  if (score >= 90) return 'text-green-600'
  if (score >= 80) return 'text-blue-600'
  if (score >= 70) return 'text-yellow-600'
  return 'text-red-600'
}

const toggleQuestions = (assignmentId) => {
  const index = expandedAssignments.value.indexOf(assignmentId)
  if (index === -1) {
    expandedAssignments.value.push(assignmentId)
  } else {
    expandedAssignments.value.splice(index, 1)
  }
}

const createChart = () => {
  if (!chartRef.value) {
    console.warn('Chart canvas not found')
    return
  }

  if (chart) {
    chart.destroy()
  }

  const ctx = chartRef.value.getContext('2d')
  const labels = gradedAssignments.value.map(a => a.assignment_title)
  const scores = gradedAssignments.value.map(a => a.score)

  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Assignment Scores',
        data: scores,
        borderColor: 'rgb(59, 130, 246)',
        tension: 0.1
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          max: 100
        }
      }
    }
  })
}

watch([filter, sort, search], () => {
  currentPage.value = 1
})

onMounted(async () => {
  await fetchGradedAssignments()
  if (!error.value) {
    createChart()
  }
})
</script>
