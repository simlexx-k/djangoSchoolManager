<template>
  <div class="assignment-submit p-6 bg-gray-100 min-h-screen">
    <div class="max-w-3xl mx-auto bg-white rounded-lg shadow-md p-6">
      <h1 class="text-2xl font-bold text-gray-800 mb-6">Submit Assignment</h1>
      
      <div v-if="isLoading" class="text-center py-4">
        <p class="text-gray-600">Loading assignment details...</p>
      </div>
      
      <div v-else-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4" role="alert">
        <p class="font-bold">Error</p>
        <p>{{ error }}</p>
      </div>
      
      <div v-else-if="assignment">
        <h2 class="text-xl font-semibold mb-2">{{ assignment.title }}</h2>
        <div class="text-gray-600 mb-4" v-html="assignment.description"></div>
        <p class="text-sm text-gray-500 mb-6">Due: {{ formatDate(assignment.due_date) }}</p>

        <form @submit.prevent="submitAssignment">
          <div v-for="question in assignment.objective_questions" :key="question.id" class="mb-6">
            <h3 class="text-lg font-medium mb-2">{{ question.question_text }}</h3>
            <div v-if="question.question_type === 'multiple_choice'" class="space-y-2">
              <label v-for="option in ['A', 'B', 'C', 'D']" :key="option" class="flex items-center">
                <input type="radio" :name="`question_${question.id}`" :value="option" v-model="responses[question.id]" class="mr-2">
                <span>{{ question[`option_${option.toLowerCase()}`] }}</span>
              </label>
            </div>
            <div v-else-if="question.question_type === 'true_false'" class="space-y-2">
              <label class="flex items-center">
                <input type="radio" :name="`question_${question.id}`" value="True" v-model="responses[question.id]" class="mr-2">
                <span>True</span>
              </label>
              <label class="flex items-center">
                <input type="radio" :name="`question_${question.id}`" value="False" v-model="responses[question.id]" class="mr-2">
                <span>False</span>
              </label>
            </div>
            <div v-else-if="question.question_type === 'short_answer'">
              <textarea v-model="responses[question.id]" rows="3" class="w-full p-2 border rounded"></textarea>
            </div>
          </div>

          <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600" :disabled="isSubmitting">
            {{ isSubmitting ? 'Submitting...' : 'Submit Assignment' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import studentApi from '@/api/student'

const route = useRoute()
const router = useRouter()

const assignment = ref(null)
const responses = ref({})
const isLoading = ref(true)
const isSubmitting = ref(false)
const error = ref(null)

const fetchAssignment = async () => {
  const assignmentId = route.params.id
  try {
    const response = await studentApi.getAssignment(assignmentId)
    if (response.data.results && response.data.results.length > 0) {
      assignment.value = response.data.results.find(a => a.id === parseInt(assignmentId)) || response.data.results[0]
    } else {
      error.value = 'Assignment not found.'
    }
    console.log('Fetched assignment:', assignment.value)
  } catch (err) {
    console.error('Error fetching assignment:', err)
    error.value = 'Failed to load assignment details. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const submitAssignment = async () => {
  const unansweredQuestions = assignment.value.objective_questions.filter(q => !responses.value[q.id])
  if (unansweredQuestions.length > 0) {
    alert(`Please answer all questions before submitting. Unanswered questions: ${unansweredQuestions.map(q => q.id).join(', ')}`)
    return
  }

  isSubmitting.value = true
  try {
    await studentApi.submitAssignment(assignment.value.id, { responses: responses.value })
    alert('Assignment submitted successfully!')
    router.push('/assignments')
  } catch (err) {
    console.error('Error submitting assignment:', err)
    error.value = 'Failed to submit assignment. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(fetchAssignment)
</script>
