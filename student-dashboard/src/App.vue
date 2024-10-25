<script setup>
import { ref, onErrorCaptured, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import NotFoundError from './components/NotFoundError.vue'
import GeneralError from './components/GeneralError.vue'
import NavigationMenu from './components/NavigationMenu.vue'
import { useThemeStore } from '@/stores/theme'
import './assets/tailwind.css'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()
const error = ref(null)
const showNavigation = computed(() => {
  const routesWithoutNavigation = ['/login', '/register', '/forgot-password']
  return !routesWithoutNavigation.includes(router.currentRoute.value.path) && authStore.isAuthenticated
})

const isDarkMode = computed(() => {
  return themeStore.theme === 'dark' || 
    (themeStore.theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches)
})

const handleError = (e) => {
  console.error(e)
  error.value = e.message || 'An unexpected error occurred'
}

onErrorCaptured((e) => {
  handleError(e)
  return true // prevent the error from propagating further
})

router.onError((e) => {
  if (e.message.includes('Failed to fetch dynamically imported module')) {
    error.value = '404'
  } else {
    handleError(e)
  }
})
</script>

<template>
  <div id="app" :class="{ 'dark': isDarkMode }" class="bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100 min-h-screen">
    <NotFoundError v-if="error === '404'" />
    <GeneralError v-else-if="error" :errorMessage="error" />
    <NavigationMenu v-if="showNavigation">
      <RouterView />
    </NavigationMenu>
    <RouterView v-else @error="handleError" />
  </div>
</template>

<style>
@import './assets/base.css';

#app {
  font-family: Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  transition: background-color 0.3s, color 0.3s;
}

.dark {
  color-scheme: dark;
}
</style>
