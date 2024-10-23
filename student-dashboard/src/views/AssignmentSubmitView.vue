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
      
      <div v-else>
        <h2 class="text-xl font-semibold text-gray-800 mb-2">{{ assignment.title }}</h2>
        
        <div v-for="(section, index) in parsedContent" :key="index" class="mb-6">
          <div v-if="section.type === 'content'" v-html="section.content" class="prose max-w-none mb-4"></div>
          
          <div v-else-if="section.type === 'question'" class="border-l-4 border-blue-500 pl-4 mb-6">
            <div v-html="section.content" class="prose max-w-none mb-2"></div>
            <div class="mt-2">
              <label :for="'answer_' + section.questionNumber" class="block text-sm font-medium text-gray-700">Your Answer:</label>
              <textarea
                :id="'answer_' + section.questionNumber"
                v-model="responses[section.questionNumber]"
                rows="4"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                :placeholder="'Enter your answer for Question ' + section.questionNumber"
              ></textarea>
            </div>
          </div>
        </div>
        
        <form @submit.prevent="submitAssignment" class="mt-8">
          <button
            type="submit"
            :disabled="isSubmitting"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            {{ isSubmitting ? 'Submitting...' : 'Submit Assignment' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import studentApi from '@/api/student'
import DOMPurify from 'dompurify'

const route = useRoute()
const router = useRouter()

const assignment = ref(null)
const responses = ref({})
const isLoading = ref(true)
const isSubmitting = ref(false)
const error = ref(null)

const parsedContent = computed(() => {
  if (!assignment.value || !assignment.value.description) return []
  
  const parser = new DOMParser()
  const doc = parser.parseFromString(assignment.value.description, 'text/html')
  const elements = Array.from(doc.body.children)
  
  const sections = []
  let currentContent = ''

  elements.forEach((element) => {
    if (element.tagName === 'H3' && element.textContent.trim().toLowerCase().startsWith('question')) {
      if (currentContent) {
        sections.push({ type: 'content', content: currentContent })
        currentContent = ''
      }
      sections.push({
        type: 'question',
        questionNumber: sections.filter(s => s.type === 'question').length + 1,
        content: DOMPurify.sanitize(element.outerHTML)
      })
    } else {
      currentContent += DOMPurify.sanitize(element.outerHTML)
    }
  })

  if (currentContent) {
    sections.push({ type: 'content', content: currentContent })
  }

  return sections
})

const fetchAssignment = async () => {
  const assignmentId = route.params.id
  try {
    const response = await studentApi.getAssignment(assignmentId)
    if (response.data.results && response.data.results.length > 0) {
      assignment.value = response.data.results.find(a => a.id == assignmentId)
    } else {
      assignment.value = response.data
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
  const unansweredQuestions = Object.keys(responses.value).filter(key => !responses.value[key].trim())
  if (unansweredQuestions.length > 0) {
    alert(`Please answer all questions before submitting. Unanswered questions: ${unansweredQuestions.join(', ')}`)
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

onMounted(fetchAssignment)
</script>

