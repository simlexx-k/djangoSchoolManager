<template>
  <div class="min-h-screen bg-gray-100">
    <div class="py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <h1 class="text-4xl font-extrabold text-gray-900 text-center mb-8">About Masaba Student Dashboard</h1>
        
        <div class="bg-white shadow overflow-hidden sm:rounded-lg">
          <div class="px-4 py-5 sm:px-6">
            <h2 class="text-3xl leading-6 font-medium text-gray-900">Our Mission</h2>
            <p class="mt-1 max-w-2xl text-sm text-gray-500">Empowering students with seamless access to their academic journey.</p>
          </div>
          <div class="border-t border-gray-200 px-4 py-5 sm:p-0">
            <dl class="sm:divide-y sm:divide-gray-200">
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Founded</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">2023</dd>
              </div>
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Headquarters</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">Nairobi, Kenya</dd>
              </div>
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Students Served</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">10,000+</dd>
              </div>
            </dl>
          </div>
        </div>

        <div class="mt-10 grid gap-10 md:grid-cols-2 lg:grid-cols-3">
          <div v-for="(feature, index) in features" :key="index" class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <component :is="feature.icon" class="h-6 w-6 text-indigo-600" aria-hidden="true" />
                <h3 class="ml-3 text-lg leading-6 font-medium text-gray-900">{{ feature.name }}</h3>
              </div>
              <p class="mt-2 text-base text-gray-500">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { AcademicCapIcon, ChartBarIcon, ClockIcon } from '@heroicons/vue/24/outline'

const features = ref([
  {
    name: 'Comprehensive Learning Tools',
    description: 'Access a wide range of resources to enhance your academic performance.',
    icon: AcademicCapIcon,
  },
  {
    name: 'Real-time Progress Tracking',
    description: 'Monitor your grades and attendance with up-to-date information.',
    icon: ChartBarIcon,
  },
  {
    name: 'Efficient Time Management',
    description: 'Organize your schedule and never miss important deadlines.',
    icon: ClockIcon,
  },
])
</script>
