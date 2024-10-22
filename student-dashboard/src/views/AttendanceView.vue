<template>
  <div class="attendance p-6">
    <h1 class="text-2xl font-bold mb-4">Attendance Record</h1>
    <div v-if="isLoading" class="text-center py-4">Loading attendance records...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>
    <div v-else class="overflow-x-auto">
      <table class="min-w-full bg-white">
        <thead>
          <tr>
            <th class="px-6 py-3 border-b-2 border-gray-300 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              Date
            </th>
            <th class="px-6 py-3 border-b-2 border-gray-300 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              Course
            </th>
            <th class="px-6 py-3 border-b-2 border-gray-300 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              Status
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in attendanceRecords" :key="record.id">
            <td class="px-6 py-4 whitespace-nowrap border-b border-gray-500">
              {{ new Date(record.date).toLocaleDateString() }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap border-b border-gray-500">
              {{ record.course_name }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap border-b border-gray-500">
              {{ record.status }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/config'

const attendanceRecords = ref([])
const isLoading = ref(true)
const error = ref(null)

const fetchAttendanceRecords = async () => {
  isLoading.value = true
  error.value = null
  try {
    const response = await api.get('/student/attendance/')
    attendanceRecords.value = response.data
  } catch (err) {
    console.error('Error fetching attendance records:', err)
    error.value = 'Failed to load attendance records. Please try again.'
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchAttendanceRecords)

defineExpose({ fetchAttendanceRecords })
</script>
