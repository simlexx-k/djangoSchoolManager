<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import NavigationMenu from './components/NavigationMenu.vue'
import { useThemeStore } from '@/stores/theme'
import './assets/tailwind.css'

const route = useRoute()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const showNavigation = computed(() => {
  const routesWithoutNavigation = ['/login', '/register', '/forgot-password']
  return !routesWithoutNavigation.includes(route.path) && authStore.isAuthenticated
})

const isDarkMode = computed(() => {
  return themeStore.theme === 'dark' || 
    (themeStore.theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches)
})

</script>

<template>
  <div id="app" :class="{ 'dark': isDarkMode }" class="bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100 min-h-screen">
    <NavigationMenu v-if="showNavigation">
      <RouterView />
    </NavigationMenu>
    <RouterView v-else />
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
