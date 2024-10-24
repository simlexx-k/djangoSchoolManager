import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import RegistrationView from '@/views/RegistrationView.vue'
import { useAuthStore } from '@/stores/auth'
import CoursesView from '../views/CoursesView.vue'
import AssignmentsView from '../views/AssignmentsView.vue'
import GradesView from '../views/GradesView.vue'
import AttendanceView from '../views/AttendanceView.vue'
import ScheduleView from '../views/ScheduleView.vue'
import MessagesView from '../views/MessagesView.vue'
import ResourcesView from '../views/ResourcesView.vue'
import UserProfile from '../views/UserProfile.vue'
import AboutView from '../views/AboutView.vue'
import ContactView from '../views/ContactView.vue'
import ExamsView from '../views/ExamsView.vue'
import AssignmentSubmitView from '../views/AssignmentSubmitView.vue'
import SubmissionView from '../views/SubmissionView.vue'
import GradedAssignmentsView from '@/views/GradedAssignmentsView.vue'
import GradedAssignmentDetailView from '@/views/GradedAssignmentDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true }
    },
    {
      path: '/register',
      name: 'Register',
      component: RegistrationView
    },
    {
      path: '/courses',
      name: 'Courses',
      component: CoursesView
    },
    {
      path: '/assignments',
      name: 'Assignments',
      component: AssignmentsView
    },
    {
      path: '/grades',
      name: 'Grades',
      component: GradesView
    },
    {
      path: '/attendance',
      name: 'Attendance',
      component: AttendanceView
    },
    {
      path: '/schedule',
      name: 'Schedule',
      component: ScheduleView
    },
    {
      path: '/messages',
      name: 'Messages',
      component: MessagesView
    },
    {
      path: '/resources',
      name: 'Resources',
      component: ResourcesView
    },
    {
      path: '/profile',
      name: 'UserProfile',
      component: UserProfile,
      meta: { requiresAuth: true }
    },
    {
      path: '/about',
      name: 'About',
      component: AboutView
    },
    {
      path: '/contact',
      name: 'Contact',
      component: ContactView
    },
    {
      path: '/exams',
      name: 'Exams',
      component: ExamsView
    },
    {
      path: '/assignments/:id/submit',
      name: 'AssignmentSubmit',
      component: AssignmentSubmitView
    },
    {
      path: '/assignments/:id/submission',
      name: 'AssignmentSubmission',
      component: SubmissionView,
      meta: { requiresAuth: true }
    },
    {
      path: '/graded-assignments',
      name: 'GradedAssignments',
      component: GradedAssignmentsView
    },
    {
      path: '/graded-assignments/:id',
      name: 'GradedAssignmentDetail',
      component: GradedAssignmentDetailView,
      props: true
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router
