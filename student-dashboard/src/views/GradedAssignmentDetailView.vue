<template>
  <div class="graded-assignment-detail p-6 bg-gray-50 min-h-screen">
    <div class="max-w-4xl mx-auto bg-white rounded-lg shadow-md overflow-hidden">
      <div v-if="isLoading">
        <SkeletonLoader type="card" class="h-32" />
        <div class="p-6 space-y-4">
          <SkeletonLoader type="text" v-for="i in 5" :key="i" />
        </div>
      </div>

      <div v-else-if="error" class="p-6 bg-red-100 border-l-4 border-red-500 text-red-700" role="alert">
        <p class="font-bold">Error</p>
        <p>{{ error }}</p>
      </div>

      <div v-else-if="assignment">
        <div class="px-6 py-4 bg-gradient-to-r from-blue-500 to-indigo-600 text-white">
          <h1 class="text-2xl font-bold mb-2">{{ assignment.assignment_title }}</h1>
          <p class="text-sm">Subject: {{ assignment.subject }}</p>
          <p class="text-sm">Submitted: {{ formatDate(assignment.submitted_at) }}</p>
        </div>

        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <span class="text-lg font-medium text-gray-700">Overall Score:</span>
            <span class="text-3xl font-bold" :class="scoreColor(assignment.score)">{{ assignment.score }}%</span>
          </div>

          <div v-if="assignment.feedback" class="mb-8">
            <h2 class="text-xl font-semibold mb-2">Feedback:</h2>
            <p class="text-gray-700 bg-gray-50 p-4 rounded-md">{{ assignment.feedback }}</p>
          </div>

          <div v-if="assignment.assignment_description" class="mb-8">
            <h2 class="text-xl font-semibold mb-2">Assignment Description:</h2>
            <p class="text-gray-700 bg-gray-50 p-4 rounded-md">{{ assignment.assignment_description }}</p>
          </div>

          <h2 class="text-xl font-semibold mb-4">Questions and Answers:</h2>
          <div v-for="(response, index) in assignment.question_responses" :key="index" class="mb-8 pb-6 border-b border-gray-200 last:border-b-0">
            <h3 class="text-lg font-medium mb-2">Question {{ index + 1 }}:</h3>
            <p class="text-gray-800 mb-4">{{ response.question_text }}</p>
            
            <div v-if="response.question_type === 'multiple_choice'" class="mb-4">
              <p class="font-medium text-gray-700 mb-2">Options:</p>
              <ul class="list-disc pl-5">
                <li v-for="(option, key) in response.options" :key="key" class="mb-1">
                  <span :class="{'font-bold': key === response.correct_answer}">
                    {{ key }}: {{ option }}
                  </span>
                  <span v-if="key === response.correct_answer" class="text-green-600 ml-2">(Correct)</span>
                  <span v-else-if="key === response.answer" class="text-red-600 ml-2">(Your Answer)</span>
                </li>
              </ul>
            </div>

            <div v-else-if="response.question_type === 'true_false'" class="mb-4">
              <p class="font-medium text-gray-700 mb-2">Options:</p>
              <ul class="list-disc pl-5">
                <li v-for="option in ['True', 'False']" :key="option" class="mb-1">
                  <span :class="{'font-bold': option === response.correct_answer}">
                    {{ option }}
                  </span>
                  <span v-if="option === response.correct_answer" class="text-green-600 ml-2">(Correct)</span>
                  <span v-else-if="option === response.answer" class="text-red-600 ml-2">(Your Answer)</span>
                </li>
              </ul>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <p class="font-medium text-gray-700">Your Answer:</p>
                <p class="text-gray-800 bg-gray-50 p-2 rounded">{{ response.answer }}</p>
              </div>
              <div>
                <p class="font-medium text-gray-700">Correct Answer:</p>
                <p class="text-gray-800 bg-gray-50 p-2 rounded">{{ response.correct_answer }}</p>
              </div>
            </div>

            <div class="flex items-center justify-between">
              <p :class="response.is_correct ? 'text-green-600' : 'text-red-600'" class="font-medium">
                {{ response.is_correct ? 'Correct' : 'Incorrect' }}
              </p>
              <p class="font-medium">Score: {{ response.score }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import studentApi from '@/api/student'
import SkeletonLoader from '@/components/SkeletonLoader.vue'

const route = useRoute()
const assignment = ref(null)
const isLoading = ref(true)
const error = ref(null)

const fetchAssignmentDetail = async () => {
  isLoading.value = true
  error.value = null
  try {
    const { data } = await studentApi.getGradedAssignmentDetail(route.params.id)
    assignment.value = data
    console.log('Fetched assignment:', data)
  } catch (err) {
    console.error('Error fetching assignment detail:', err)
    error.value = 'Failed to load assignment details. Please try again.'
  } finally {
    isLoading.value = false
  }
}

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

const questionTypeDisplay = (type) => {
  switch (type) {
    case 'multiple_choice':
      return 'Multiple Choice'
    case 'true_false':
      return 'True/False'
    case 'short_answer':
      return 'Short Answer'
    default:
      return type
  }
}

onMounted(fetchAssignmentDetail)
</script>
