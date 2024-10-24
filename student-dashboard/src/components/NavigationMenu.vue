<template>
  <div class="h-screen flex overflow-hidden bg-gray-100 dark:bg-gray-900">
    <!-- Sidebar for larger screens -->
    <div class="hidden md:flex md:flex-shrink-0">
      <div class="flex flex-col w-64">
        <div class="flex flex-col h-0 flex-1">
          <div class="flex-1 flex flex-col overflow-y-auto">
            <!-- Updated top part of sidebar -->
            <div class="flex items-center flex-shrink-0 px-4 h-16 bg-white dark:bg-gray-800 shadow">
              <img class="h-8 w-auto" src="../assets/masabaLogo.png" alt="Masaba Logo">
              <span class="text-gray-800 dark:text-white ml-2 text-xl font-semibold">Masaba</span>
            </div>
            <nav class="flex-1 px-2 py-4 bg-gray-800 dark:bg-gray-900 space-y-1">
              <router-link
                v-for="item in visibleNavigationItems"
                :key="item.name"
                :to="item.href"
                :class="[
                  item.current 
                    ? 'bg-gray-900 text-white dark:bg-gray-700 dark:text-white' 
                    : 'text-gray-300 hover:bg-gray-700 hover:text-white dark:text-gray-400 dark:hover:bg-gray-800 dark:hover:text-white',
                  'group flex items-center px-2 py-2 text-sm font-medium rounded-md'
                ]"
                @click="setCurrentItem(item)"
              >
                <component 
                  :is="item.icon" 
                  class="mr-3 flex-shrink-0 h-6 w-6" 
                  :class="[
                    item.current 
                      ? 'text-gray-300 dark:text-gray-300' 
                      : 'text-gray-400 group-hover:text-gray-300 dark:text-gray-500 dark:group-hover:text-gray-300'
                  ]" 
                  aria-hidden="true" 
                />
                {{ item.name }}
              </router-link>
            </nav>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile sidebar -->
    <transition enter-active-class="transition ease-out duration-150" enter-from-class="opacity-0" enter-to-class="opacity-100" leave-active-class="transition ease-in duration-150" leave-from-class="opacity-100" leave-to-class="opacity-0">
      <div v-if="isMobile && sidebarOpen" class="fixed inset-0 flex z-40 md:hidden" role="dialog" aria-modal="true">
        <div class="fixed inset-0 bg-gray-600 bg-opacity-75" aria-hidden="true" @click="sidebarOpen = false"></div>
        <div class="relative flex-1 flex flex-col max-w-xs w-full">
          <!-- Updated top part of mobile sidebar -->
          <div class="flex items-center flex-shrink-0 px-4 h-16 bg-white dark:bg-gray-800 shadow">
            <img class="h-8 w-auto" src="../assets/masabaLogo.png" alt="Masaba Logo">
            <span class="text-gray-800 dark:text-white ml-2 text-xl font-semibold">Masaba</span>
          </div>
          <div class="flex-1 h-0 overflow-y-auto bg-gray-800 dark:bg-gray-900">
            <nav class="px-2 py-4 space-y-1">
              <router-link
                v-for="item in visibleNavigationItems"
                :key="item.name"
                :to="item.href"
                class="menu-item group flex items-center px-2 py-2 text-base font-medium rounded-md"
                :class="{ 'bg-gray-900 text-white': item.current }"
                @click="setCurrentItem(item)"
              >
                <component :is="item.icon" class="menu-item-icon mr-4 flex-shrink-0 h-6 w-6" aria-hidden="true" />
                {{ item.name }}
              </router-link>
            </nav>
          </div>
        </div>
      </div>
    </transition>

    <!-- Main content area -->
    <div class="flex flex-col w-0 flex-1 overflow-hidden">
      <!-- Top bar -->
      <div class="relative z-10 flex-shrink-0 flex h-16 bg-white dark:bg-gray-800 shadow">
        <button @click="sidebarOpen = true" class="md:hidden px-4 border-r border-gray-200 text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500">
          <span class="sr-only">Open sidebar</span>
          <Bars3Icon class="h-6 w-6" aria-hidden="true" />
        </button>
        <div class="flex-1 px-4 flex justify-between">
          <div class="flex-1 flex">
            <h1 class="text-2xl font-semibold text-gray-800 self-center">{{ currentPageTitle }}</h1>
          </div>
          <div class="ml-4 flex items-center md:ml-6">
            <button @click="toggleSearch" class="bg-white dark:bg-gray-800 p-1 rounded-full text-gray-400 dark:text-gray-300 hover:text-gray-500 dark:hover:text-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
              <span class="sr-only">Search</span>
              <MagnifyingGlassIcon class="h-6 w-6" aria-hidden="true" />
            </button>
            <button class="bg-white dark:bg-gray-800 p-1 rounded-full text-gray-400 dark:text-gray-300 hover:text-gray-500 dark:hover:text-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
              <span class="sr-only">View notifications</span>
              <BellIcon class="h-6 w-6" aria-hidden="true" />
            </button>

            <!-- Theme toggle button -->
            <button @click="toggleTheme" 
                    :class="[
                      'p-1 rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500',
                      isDarkMode 
                        ? 'bg-gray-700 text-gray-300 hover:bg-gray-600' 
                        : 'bg-gray-200 text-gray-400 hover:text-gray-500'
                    ]">
              <span class="sr-only">Toggle theme</span>
              <SunIcon v-if="isDarkMode" class="h-6 w-6 text-yellow-400" aria-hidden="true" />
              <MoonIcon v-else class="h-6 w-6 text-gray-600" aria-hidden="true" />
            </button>

            <!-- Profile dropdown -->
            <div class="ml-3 relative">
              <div>
                <button @click="toggleProfileMenu" class="max-w-xs bg-white dark:bg-gray-800 flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500" id="user-menu" aria-expanded="false" aria-haspopup="true">
                  <span class="sr-only">Open user menu</span>
                  <img class="h-8 w-8 rounded-full" :src="userAvatar" :alt="userName">
                </button>
              </div>
              <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                <div v-if="profileMenuOpen" class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white dark:bg-gray-800 ring-1 ring-black ring-opacity-5 focus:outline-none" role="menu" aria-orientation="vertical" aria-labelledby="user-menu">
                  <router-link to="/profile" class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700" role="menuitem">Your Profile</router-link>
                  <router-link to="/settings" class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700" role="menuitem">Settings</router-link>
                  <a @click="logout" href="#" class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700" role="menuitem">Sign out</a>
                </div>
              </transition>
            </div>
          </div>
        </div>
      </div>

      <!-- Main content -->
      <main class="flex-1 relative overflow-y-auto focus:outline-none">
        <div class="py-6">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
            <slot></slot>
          </div>
        </div>
      </main>
    </div>
  </div>

  <!-- Search Modal -->
  <transition enter-active-class="ease-out duration-300" enter-from-class="opacity-0" enter-to-class="opacity-100" leave-active-class="ease-in duration-200" leave-from-class="opacity-100" leave-to-class="opacity-0">
    <div v-if="searchOpen" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white dark:bg-gray-800 rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white dark:bg-gray-800 px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-gray-100" id="modal-title">
                  Search
                </h3>
                <div class="mt-2">
                  <input type="text" placeholder="Search..." class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100">
                </div>
              </div>
            </div>
          </div>
          <div class="bg-gray-50 dark:bg-gray-700 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button @click="toggleSearch" type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 dark:border-gray-600 shadow-sm px-4 py-2 bg-white dark:bg-gray-800 text-base font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import api from '@/api/config'
import {
  Bars3Icon,
  XMarkIcon,
  MagnifyingGlassIcon,
  BellIcon,
  HomeIcon,
  UsersIcon,
  FolderIcon,
  CalendarIcon,
  InboxIcon,
  ChartBarIcon,
  AcademicCapIcon,
  BookOpenIcon,
  InformationCircleIcon,
  EnvelopeIcon,
  SunIcon,
  MoonIcon,
  ClipboardDocumentListIcon,
  PencilSquareIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()
const sidebarOpen = ref(false)
const profileMenuOpen = ref(false)
const searchOpen = ref(false)
const isMobile = ref(false)
const unreadNotifications = ref(2) // Example value, replace with actual logic

const userName = ref('')
const userEmail = ref('')
const userAvatar = ref('')

const themeStore = useThemeStore()

const toggleTheme = () => {
  themeStore.theme = themeStore.theme === 'light' ? 'dark' : 'light'
}

const isDarkMode = computed(() => themeStore.theme === 'dark')

const navigationItems = ref([
  { name: 'Home', href: '/', icon: HomeIcon, current: false, requiresAuth: false, hideWhenAuth: true },
  { name: 'Overview', href: '/dashboard', icon: ChartBarIcon, current: true, requiresAuth: true },
  { name: 'Subjects', href: '/courses', icon: BookOpenIcon, current: false, requiresAuth: true },
  { name: 'Exams', href: '/exams', icon: ClipboardDocumentListIcon, current: false, requiresAuth: true },
  { name: 'Assignments', href: '/assignments', icon: PencilSquareIcon, current: false, requiresAuth: true },
  { name: 'Graded Assignments', href: '/graded-assignments', icon: AcademicCapIcon, current: false, requiresAuth: true },
  { name: 'Grades', href: '/grades', icon: AcademicCapIcon, current: false, requiresAuth: true },
  { name: 'Attendance', href: '/attendance', icon: UsersIcon, current: false, requiresAuth: true },
  { name: 'Schedule', href: '/schedule', icon: CalendarIcon, current: false, requiresAuth: true },
  { name: 'Messages', href: '/messages', icon: InboxIcon, current: false, requiresAuth: true },
  { name: 'Resources', href: '/resources', icon: FolderIcon, current: false, requiresAuth: true },
  { name: 'About', href: '/about', icon: InformationCircleIcon, current: false, requiresAuth: false, hideWhenAuth: true },
  { name: 'Contact', href: '/contact', icon: EnvelopeIcon, current: false, requiresAuth: false, hideWhenAuth: true },
])

const visibleNavigationItems = computed(() => {
  return navigationItems.value.filter(item => 
    (!item.requiresAuth && !authStore.isAuthenticated) || 
    (item.requiresAuth && authStore.isAuthenticated) ||
    (!item.hideWhenAuth && authStore.isAuthenticated)
  )
})

const currentPageTitle = computed(() => {
  const currentItem = navigationItems.value.find(item => item.current)
  return currentItem ? currentItem.name : 'Dashboard'
})

const fetchUserDetails = async () => {
  if (!authStore.isAuthenticated) return

  try {
    const response = await api.get('/learner/profile/')
    userName.value = response.data.name
    userEmail.value = response.data.email || 'No email provided'
    userAvatar.value = response.data.avatar || 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80'
  } catch (error) {
    console.error('Error fetching user details:', error)
  }
}

const logout = async () => {
  try {
    await authStore.logout()
    router.push('/login')
  } catch (error) {
    console.error('Error during logout:', error)
  }
}

const toggleProfileMenu = () => {
  profileMenuOpen.value = !profileMenuOpen.value
}

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

const toggleSearch = () => {
  searchOpen.value = !searchOpen.value
}

const toggleNotifications = () => {
  // Implement notification toggle functionality
}

const setCurrentItem = (item) => {
  navigationItems.value.forEach(navItem => {
    navItem.current = navItem.name === item.name
  })
  if (isMobile.value) {
    sidebarOpen.value = false
  }
}

const checkMobile = () => {
  isMobile.value = window.innerWidth < 768
}

onMounted(() => {
  if (authStore.isAuthenticated) {
    fetchUserDetails()
  }
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

// Set the current navigation item based on the current route
router.afterEach((to) => {
  const currentItem = navigationItems.value.find(item => item.href === to.path)
  if (currentItem) {
    setCurrentItem(currentItem)
  }
})

watch(() => themeStore.theme, (newTheme) => {
  if (newTheme === 'dark') {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}, { immediate: true })
</script>

<style scoped>
/* ... existing styles ... */

.dark .router-link-active,
.dark .router-link-exact-active {
  background-color: #111827; /* bg-gray-900 */
  color: #ffffff; /* text-white */
}

.dark .router-link-active:hover,
.dark .router-link-exact-active:hover {
  background-color: #1f2937; /* bg-gray-800 */
}

.dark .theme-toggle {
  background-color: #374151; /* bg-gray-700 */
  color: #d1d5db; /* text-gray-300 */
}

.dark .theme-toggle:hover {
  background-color: #4b5563; /* bg-gray-600 */
}
</style>
