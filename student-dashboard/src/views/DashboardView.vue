<template>
  <div class="dashboard bg-gray-100 min-h-screen p-6">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-800 mb-6">
        <template v-if="!isLoading">Welcome, {{ dashboardData.student_name }}</template>
        <SkeletonLoader v-else type="text" />
      </h1>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <DashboardCard v-if="!isLoading" title="Running Mean Score" :value="formatNumber(dashboardData.gpa)" icon="academic-cap" />
        <DashboardCard v-if="!isLoading" title="Attendance" :value="formatNumber(dashboardData.attendance) + '%'" icon="user-group" />
        <DashboardCard v-if="!isLoading" title="Subjects Taken" :value="dashboardData.completed_courses" icon="book-open" />
        <SkeletonLoader v-if="isLoading" type="card" v-for="i in 3" :key="i" />
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold mb-4">Recent Grades</h2>
          <ul v-if="!isLoading" class="space-y-2">
            <li v-for="grade in dashboardData.recent_grades" :key="grade.course" class="flex justify-between items-center">
              <span>{{ grade.course }}</span>
              <span class="font-semibold" :class="gradeColorClass(grade.grade)">{{ grade.grade }}</span>
            </li>
          </ul>
          <SkeletonLoader v-else type="text" v-for="i in 5" :key="i" class="mb-2" />
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold mb-4">Recent Subject Scores</h2>
          <div v-if="!isLoading && dashboardData.recent_scores.length > 0">
            <div v-for="score in dashboardData.recent_scores" :key="score.subject" class="mb-4">
              <div class="flex justify-between items-center mb-1">
                <span class="text-sm font-medium text-gray-600">{{ score.subject }}</span>
                <span class="text-sm font-semibold" :class="scoreColorClass(score.score)">
                  {{ formatNumber(score.score) }}%
                </span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="h-2 rounded-full" 
                     :class="scoreBackgroundClass(score.score)"
                     :style="{ width: `${score.score}%` }">
                </div>
              </div>
            </div>
          </div>
          <div v-else-if="!isLoading && dashboardData.recent_scores.length === 0" class="text-center text-gray-500 py-4">
            No recent scores available
          </div>
          <div v-else>
            <div v-for="i in 5" :key="i" class="mb-4 animate-pulse">
              <div class="flex justify-between items-center mb-1">
                <div class="h-4 bg-gray-200 rounded w-1/3"></div>
                <div class="h-4 bg-gray-200 rounded w-16"></div>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="h-2 bg-gray-300 rounded-full" style="width: 70%"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold mb-4">Upcoming Events</h2>
          <ul v-if="!isLoading" class="space-y-2">
            <li v-for="event in dashboardData.upcoming_events" :key="event.title" class="flex justify-between items-center">
              <span>{{ event.title }}</span>
              <span class="text-sm text-gray-500">{{ formatDate(event.date) }}</span>
            </li>
          </ul>
          <SkeletonLoader v-else type="text" v-for="i in 3" :key="i" class="mb-2" />
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold mb-4">Performance Trend</h2>
          <div v-if="!isLoading && performanceTrendChartData.datasets[0].data.length > 0" class="h-64">
            <PerformanceChart :chart-data="performanceTrendChartData" />
          </div>
          <p v-else-if="!isLoading" class="text-center text-gray-500">No performance data available</p>
          <SkeletonLoader v-else type="chart" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import DashboardCard from '@/components/DashboardCard.vue'
import PerformanceChart from '@/components/PerformanceChart.vue'
import SkeletonLoader from '@/components/SkeletonLoader.vue'
import studentApi from '@/api/student'

export default {
  components: {
    DashboardCard,
    PerformanceChart,
    SkeletonLoader,
  },
  setup() {
    const dashboardData = ref({})
    const isLoading = ref(true)
    const error = ref(null)

    const performanceTrendChartData = computed(() => {
      const data = dashboardData.value.performance_trend || []
      return {
        labels: data.map(item => formatDate(item.date)),
        datasets: [{
          label: 'Running Mean Score',
          data: data.map(item => item.avg_score),
          backgroundColor: 'rgba(59, 130, 246, 0.6)',
          borderColor: 'rgb(59, 130, 246)',
          borderWidth: 1
        }]
      }
    })

    const formatDate = (dateString) => {
      if (!dateString) return ''
      const options = { year: 'numeric', month: 'short' }
      return new Date(dateString).toLocaleDateString(undefined, options)
    }

    const formatNumber = (value) => {
      return value !== undefined ? value.toFixed(2) : 'N/A'
    }

    const gradeColorClass = (grade) => {
      const gradeMap = {
        'EE': 'text-green-600',  // Exceeds Expectations
        'ME': 'text-blue-600',   // Meets Expectations
        'AE': 'text-yellow-600', // Approaches Expectations
        'BE': 'text-red-600'     // Below Expectations
      }
      return gradeMap[grade] || 'text-gray-600'
    }

    const scoreColorClass = (score) => {
      if (score >= 90) return 'text-green-600'
      if (score >= 80) return 'text-blue-600'
      if (score >= 70) return 'text-yellow-600'
      if (score >= 60) return 'text-orange-600'
      return 'text-red-600'
    }

    const scoreBackgroundClass = (score) => {
      if (score >= 90) return 'bg-green-600'
      if (score >= 80) return 'bg-blue-600'
      if (score >= 70) return 'bg-yellow-600'
      if (score >= 60) return 'bg-orange-600'
      return 'bg-red-600'
    }

    onMounted(async () => {
      try {
        const response = await studentApi.getDashboard()
        dashboardData.value = response.data
        isLoading.value = false
      } catch (err) {
        console.error('Error fetching dashboard data:', err)
        error.value = 'Failed to load dashboard data. Please try again later.'
        isLoading.value = false
      }
    })

    return {
      dashboardData,
      performanceTrendChartData,
      formatDate,
      formatNumber,
      gradeColorClass,
      isLoading,
      error,
      scoreColorClass,
      scoreBackgroundClass
    }
  }
}
</script>
