<template>
  <div class="min-h-screen bg-gray-100">
    <div class="py-10">
      <header>
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 class="text-3xl font-bold leading-tight text-gray-900">Student Dashboard</h1>
        </div>
      </header>
      <main>
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
          <div v-if="isLoading" class="text-center py-12">
            <div class="spinner"></div>
            <p class="mt-4 text-sm text-gray-600">Loading your dashboard...</p>
          </div>

          <div v-else-if="error" class="rounded-md bg-red-50 p-4 mt-8">
            <div class="flex">
              <ExclamationCircleIcon class="h-5 w-5 text-red-400" aria-hidden="true" />
              <div class="ml-3">
                <h3 class="text-sm font-medium text-red-800">Error</h3>
                <div class="mt-2 text-sm text-red-700">
                  <p>{{ error }}</p>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="mt-8">
            <div class="bg-white overflow-hidden shadow rounded-lg divide-y divide-gray-200">
              <div class="px-4 py-5 sm:px-6">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  Welcome, {{ dashboardData.student_name }}!
                </h3>
                <p class="mt-1 max-w-2xl text-sm text-gray-500">
                  Grade: {{ dashboardData.grade || 'N/A' }} | Learner ID: {{ dashboardData.learner_id || 'N/A' }}
                </p>
              </div>
              <div class="px-4 py-5 sm:p-6">
                <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
                  <DashboardCard 
                    title="Attendance" 
                    :value="(dashboardData.attendance ?? 0) + '%'" 
                    icon="UserGroupIcon" 
                  />
                  <DashboardCard title="GPA" :value="dashboardData.gpa ? dashboardData.gpa.toFixed(2) : 'N/A'" icon="AcademicCapIcon" />
                  <DashboardCard 
                    title="Completed Courses" 
                    :value="dashboardData.completed_courses ?? 0" 
                    icon="CheckCircleIcon" 
                  />
                </div>
              </div>
            </div>

            <div class="mt-8 grid grid-cols-1 gap-5 sm:grid-cols-2">
              <div class="bg-white overflow-hidden shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                  <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Recent Grades</h3>
                  <ul class="divide-y divide-gray-200">
                    <li v-for="grade in dashboardData.recent_grades" :key="grade.course" class="py-3 flex justify-between items-center">
                      <span class="text-sm font-medium text-gray-900">{{ grade.course }}</span>
                      <span :class="gradeColorClass(grade.grade)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                        {{ grade.grade }}
                      </span>
                    </li>
                  </ul>
                </div>
              </div>

              <div class="bg-white overflow-hidden shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                  <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Upcoming Events</h3>
                  <ul class="divide-y divide-gray-200">
                    <li v-for="event in dashboardData.upcoming_events" :key="event.id" class="py-3">
                      <div class="flex items-center">
                        <CalendarIcon class="h-5 w-5 text-gray-400 mr-2" />
                        <p class="text-sm font-medium text-gray-900">{{ event.title }}</p>
                      </div>
                      <p class="mt-1 text-sm text-gray-500">{{ formatDate(event.date) }}</p>
                    </li>
                  </ul>
                </div>
              </div>
            </div>

            <div class="mt-8 bg-white overflow-hidden shadow rounded-lg">
              <div class="px-4 py-5 sm:p-6">
                <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Course Progress</h3>
                <div class="space-y-4">
                  <div v-for="course in dashboardData.course_progress" :key="course.id" class="flex items-center">
                    <div class="flex-1">
                      <p class="text-sm font-medium text-gray-900">{{ course.name }}</p>
                      <div class="mt-1 relative pt-1">
                        <div class="overflow-hidden h-2 text-xs flex rounded bg-indigo-200">
                          <div :style="{ width: course.progress + '%' }" class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-indigo-500"></div>
                        </div>
                      </div>
                    </div>
                    <p class="ml-4 text-sm font-medium text-gray-900">{{ course.progress }}%</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ExclamationCircleIcon, CalendarIcon } from '@heroicons/vue/24/solid'
import api from '@/api/config'
import DashboardCard from '@/components/DashboardCard.vue'

const dashboardData = ref({
  student_name: '',
  grade: '',
  learner_id: '',
  attendance: 0,
  gpa: null,
  completed_courses: 0,
  recent_grades: [],
  upcoming_events: [],
  course_progress: []
})

const isLoading = ref(true)
const error = ref(null)

const fetchDashboardData = async () => {
  isLoading.value = true
  error.value = null
  try {
    const response = await api.get('/student/dashboard/')
    dashboardData.value = { ...dashboardData.value, ...response.data }
  } catch (err) {
    console.error('Error fetching dashboard data:', err)
    error.value = 'Failed to load dashboard data. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const refreshDashboard = () => {
  fetchDashboardData()
}

const gradeColorClass = (grade) => {
  const gradeMap = {
    'A': 'bg-green-100 text-green-800',
    'B': 'bg-blue-100 text-blue-800',
    'C': 'bg-yellow-100 text-yellow-800',
    'D': 'bg-orange-100 text-orange-800',
    'F': 'bg-red-100 text-red-800'
  }
  return gradeMap[grade.charAt(0)] || 'bg-gray-100 text-gray-800'
}

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString(undefined, options)
}

onMounted(fetchDashboardData)

defineExpose({ refreshDashboard })
</script>

<style scoped>
.spinner {
  border: 4px solid #e2e8f0;
  border-top: 4px solid #4f46e5;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
