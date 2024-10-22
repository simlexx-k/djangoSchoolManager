<!-- ContactView.vue -->
<template>
  <div class="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-4xl font-extrabold text-gray-900 text-center mb-8">Contact Us</h1>
      
      <div class="bg-white shadow overflow-hidden sm:rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900">Send us a message</h3>
          <div class="mt-5 md:mt-0 md:col-span-2">
            <form @submit.prevent="submitForm">
              <div class="grid grid-cols-6 gap-6">
                <div class="col-span-6 sm:col-span-3">
                  <label for="first-name" class="block text-sm font-medium text-gray-700">First name</label>
                  <input type="text" name="first-name" id="first-name" v-model="form.firstName" autocomplete="given-name" class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                </div>
                <div class="col-span-6 sm:col-span-3">
                  <label for="last-name" class="block text-sm font-medium text-gray-700">Last name</label>
                  <input type="text" name="last-name" id="last-name" v-model="form.lastName" autocomplete="family-name" class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                </div>
                <div class="col-span-6 sm:col-span-4">
                  <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
                  <input type="email" name="email" id="email" v-model="form.email" autocomplete="email" class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md">
                </div>
                <div class="col-span-6">
                  <label for="message" class="block text-sm font-medium text-gray-700">Message</label>
                  <textarea id="message" name="message" v-model="form.message" rows="3" class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"></textarea>
                </div>
              </div>
              <div class="mt-5">
                <button type="submit" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                  Send Message
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <div class="mt-10 bg-white shadow overflow-hidden sm:rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900">Other ways to reach us</h3>
          <div class="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-3">
            <div class="flex items-center">
              <PhoneIcon class="flex-shrink-0 h-6 w-6 text-gray-400" aria-hidden="true" />
              <span class="ml-3 text-base text-gray-500">+1 (555) 123-4567</span>
            </div>
            <div class="flex items-center">
              <EnvelopeIcon class="flex-shrink-0 h-6 w-6 text-gray-400" aria-hidden="true" />
              <span class="ml-3 text-base text-gray-500">support@masabadashboard.com</span>
            </div>
            <div class="flex items-center">
              <MapPinIcon class="flex-shrink-0 h-6 w-6 text-gray-400" aria-hidden="true" />
              <span class="ml-3 text-base text-gray-500">123 Education St, Nairobi, Kenya</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { PhoneIcon, EnvelopeIcon, MapPinIcon } from '@heroicons/vue/24/outline'

const form = ref({
  firstName: '',
  lastName: '',
  email: '',
  message: ''
})

const submitForm = () => {
  // Handle form submission here
  console.log('Form submitted:', form.value)
  // You would typically send this data to your backend API
}
</script>
