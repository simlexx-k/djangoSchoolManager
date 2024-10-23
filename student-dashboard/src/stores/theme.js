import { ref, watch } from 'vue'
import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', () => {
  const theme = ref(localStorage.getItem('theme') || 'system')

  watch(theme, (newTheme) => {
    localStorage.setItem('theme', newTheme)
    updateTheme(newTheme)
  })

  function updateTheme(newTheme) {
    if (newTheme === 'dark' || (newTheme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  // Initialize theme
  updateTheme(theme.value)

  return { theme }
})

