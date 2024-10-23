<!-- src/components/DashboardCard.vue -->
<template>
  <div class="bg-white rounded-lg shadow p-6">
    <div class="flex items-center">
      <div class="p-3 rounded-full bg-blue-100 text-blue-600 mr-4">
        <component :is="iconComponent" class="w-6 h-6" />
      </div>
      <div>
        <h3 class="text-sm font-medium text-gray-500">{{ title }}</h3>
        <p class="text-2xl font-semibold text-gray-900">{{ value }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { AcademicCapIcon, UserGroupIcon, BookOpenIcon } from '@heroicons/vue/24/outline'

export default {
  props: {
    title: String,
    value: [String, Number],
    icon: String,
  },
  setup(props) {
    const iconComponent = computed(() => {
      switch (props.icon) {
        case 'academic-cap':
          return AcademicCapIcon
        case 'user-group':
          return UserGroupIcon
        case 'book-open':
          return BookOpenIcon
        default:
          return null
      }
    })

    return { iconComponent }
  }
}
</script>
