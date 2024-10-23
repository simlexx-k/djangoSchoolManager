<!-- src/views/RegistrationView.vue -->
<template>
  <div class="registration-container bg-gray-100 dark:bg-gray-900 transition-colors duration-300">
    <div class="vector-background">
      <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
        <line class="vector-line" x1="0%" y1="50%" x2="100%" y2="50%" />
        <line class="vector-line" x1="0%" y1="25%" x2="100%" y2="75%" />
        <line class="vector-line" x1="0%" y1="75%" x2="100%" y2="25%" />
        <line class="vector-line" x1="25%" y1="0%" x2="75%" y2="100%" />
        <line class="vector-line" x1="75%" y1="0%" x2="25%" y2="100%" />
      </svg>
    </div>
    <div class="registration bg-white dark:bg-gray-800 shadow-lg">
      <div class="auth-options bg-gray-200 dark:bg-gray-700">
        <a href="#" class="auth-link text-blue-600 dark:text-blue-400">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
          </svg>
          Forgot Password?
        </a>
        <a href="#" class="auth-link text-blue-600 dark:text-blue-400">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
          </svg>
          Sign In
        </a>
      </div>
      <h2 class="text-gray-800 dark:text-gray-200">Student Registration</h2>
      <form @submit.prevent="register" class="registration-form">
        <div class="form-group">
          <label for="grade-select" class="text-gray-700 dark:text-gray-300">Select Grade:</label>
          <div class="input-with-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="input-icon">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.436 60.436 0 00-.491 6.347A48.627 48.627 0 0112 20.904a48.627 48.627 0 018.232-4.41 60.46 60.46 0 00-.491-6.347m-15.482 0a50.57 50.57 0 00-2.658-.813A59.905 59.905 0 0112 3.493a59.902 59.902 0 0110.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.697 50.697 0 0112 13.489a50.702 50.702 0 017.74-3.342M6.75 15a.75.75 0 100-1.5.75.75 0 000 1.5zm0 0v-3.675A55.378 55.378 0 0112 8.443m-7.007 11.55A5.981 5.981 0 006.75 15.75v-1.5" />
            </svg>
            <select id="grade-select" v-model="selectedGradeId" @change="fetchStudents"
                    class="bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-600">
              <option value="">Please select a grade</option>
              <option v-for="grade in grades" :key="grade.id" :value="grade.id">
                {{ grade.grade_name }}
              </option>
            </select>
          </div>
        </div>

        <div v-if="students.length > 0" class="form-group">
          <label for="student-select">Select Student:</label>
          <div class="input-with-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="input-icon">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
            </svg>
            <select id="student-select" v-model="selectedLearnerId">
              <option value="">Please select a student</option>
              <option v-for="student in students" :key="student.learner_id" :value="student.learner_id">
                {{ student.name }}
              </option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label for="username">Username:</label>
          <div class="input-with-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="input-icon">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
            </svg>
            <input id="username" v-model="username" placeholder="Enter username" required>
          </div>
        </div>

        <div class="form-group">
          <label for="password">Password:</label>
          <div class="input-with-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="input-icon">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
            </svg>
            <input id="password" v-model="password" type="password" placeholder="Enter password" required>
          </div>
        </div>

        <button type="submit" :disabled="!isFormValid" class="submit-button">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 mr-2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zM4 19.235v-.11a6.375 6.375 0 0112.75 0v.109A12.318 12.318 0 0110.374 21c-2.331 0-4.512-.645-6.374-1.766z" />
          </svg>
          Register
        </button>
      </form>
    </div>

    <!-- Add this floating theme toggle button -->
    <button @click="toggleTheme" class="theme-toggle">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
        <path v-if="themeStore.theme === 'dark'" stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
        <path v-else stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z" />
      </svg>
    </button>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import api from '@/api/config';
import { useThemeStore } from '@/stores/theme';

export default {
  setup() {
    const grades = ref([]);
    const students = ref([]);
    const selectedGradeId = ref('');
    const selectedLearnerId = ref('');
    const username = ref('');
    const password = ref('');

    const themeStore = useThemeStore();

    const themeButtonText = computed(() => {
      switch (themeStore.theme) {
        case 'light': return 'Switch to Dark Mode'
        case 'dark': return 'Switch to System Mode'
        default: return 'Switch to Light Mode'
      }
    })

    function toggleTheme() {
      switch (themeStore.theme) {
        case 'light':
          themeStore.theme = 'dark'
          break
        case 'dark':
          themeStore.theme = 'system'
          break
        default:
          themeStore.theme = 'light'
      }
    }

    const fetchGrades = async () => {
      try {
        const response = await api.get('/grades/');
        grades.value = response.data;
      } catch (error) {
        console.error('Error fetching grades:', error);
        alert('Failed to fetch grades. Please try again.');
      }
    };

    const fetchStudents = async () => {
      if (selectedGradeId.value) {
        try {
          const response = await api.get('/students/', { params: { grade_id: selectedGradeId.value } });
          students.value = response.data;
        } catch (error) {
          console.error('Error fetching students:', error);
          alert('Failed to fetch students. Please try again.');
        }
      } else {
        students.value = [];
      }
    };

    const register = async () => {
      if (!isFormValid.value) return;

      try {
        await api.post('/register/student/', {
          grade_id: selectedGradeId.value,
          learner_id: selectedLearnerId.value,
          username: username.value,
          password: password.value,
        });
        alert('Registration successful!');
        // Redirect to login or dashboard
      } catch (error) {
        console.error('Registration failed:', error);
        if (error.response?.data?.error === "Username already exists") {
          alert('This username is already taken. Please choose a different one.');
        } else if (error.response?.data?.error === "Student record not found") {
          alert('No matching student record found. Please check your details.');
        } else if (error.response?.data?.error === "This student already has an account") {
          alert('An account already exists for this student. Please log in instead.');
        } else {
          alert('Registration failed: ' + (error.response?.data?.error || 'Unknown error'));
        }
      }
    };

    const isFormValid = computed(() => {
      return selectedGradeId.value && 
             selectedLearnerId.value && 
             username.value.trim() !== '' && 
             password.value.trim() !== '';
    });

    onMounted(fetchGrades);

    return {
      grades,
      students,
      selectedGradeId,
      selectedLearnerId,
      username,
      password,
      fetchStudents,
      register,
      isFormValid,
      themeButtonText,
      toggleTheme,
      themeStore // Add this line to expose themeStore to the template
    };
  },
};
</script>

<style scoped>
.registration-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f3f4f6; /* light mode background */
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.dark .registration-container {
  background-color: #111827; /* dark mode background */
}

.vector-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.vector-line {
  stroke: rgba(0, 0, 0, 0.1);
  stroke-width: 1;
}

.dark .vector-line {
  stroke: rgba(255, 255, 255, 0.1);
}

@keyframes drawLine {
  0% {
    stroke-dashoffset: 100%;
  }
  100% {
    stroke-dashoffset: -100%;
  }
}

.vector-line:nth-child(1) {
  stroke-dasharray: 10, 5;
  animation: drawLine 20s linear infinite;
}

.vector-line:nth-child(2) {
  stroke-dasharray: 15, 10;
  animation: drawLine 25s linear infinite reverse;
}

.vector-line:nth-child(3) {
  stroke-dasharray: 5, 10;
  animation: drawLine 30s linear infinite;
}

.vector-line:nth-child(4) {
  stroke-dasharray: 20, 5;
  animation: drawLine 35s linear infinite reverse;
}

.vector-line:nth-child(5) {
  stroke-dasharray: 10, 15;
  animation: drawLine 40s linear infinite;
}

.registration {
  width: 100%;
  max-width: 400px;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  position: relative;
  z-index: 1;
  overflow: hidden;
}

.dark .registration {
  background-color: rgba(31, 41, 55, 0.9);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.auth-options {
  display: flex;
  justify-content: space-between;
  padding: 15px 30px;
  background-color: #e5e7eb; /* Darker gray for better contrast */
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.dark .auth-options {
  background-color: rgba(55, 65, 81, 0.9); /* Keep dark mode as is */
}

.auth-link {
  color: #3b82f6;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s;
  display: flex;
  align-items: center;
}

.dark .auth-link {
  color: #60a5fa;
}

.auth-link svg {
  width: 16px;
  height: 16px;
  margin-right: 5px;
}

.input-with-icon {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #64748b;
}

h2 {
  text-align: center;
  color: #1f2937; /* dark gray for light mode */
  margin: 30px 0;
  font-size: 24px;
  font-weight: 600;
}

.dark h2 {
  color: #f3f4f6; /* light gray for dark mode */
}

.registration-form {
  display: flex;
  flex-direction: column;
  padding: 0 30px 30px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #1f2937;
  font-size: 14px;
}

.dark label {
  color: #e5e7eb;
}

select,
input {
  width: 100%;
  padding: 12px 16px 12px 40px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  font-size: 16px;
  transition: border-color 0.3s, box-shadow 0.3s;
  background-color: #ffffff;
  color: #1f2937;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}

.dark select,
.dark input {
  background-color: #374151;
  color: #f3f4f6;
  border-color: #4b5563;
}

select {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2364748b'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 16px;
  padding-right: 40px;
}

select option {
  background-color: #ffffff;
  color: #1f2937;
}

.dark select option {
  background-color: #1e293b;
  color: #f3f4f6;
}

select::-ms-expand {
  display: none;
}

select:focus,
input:focus {
  outline: none;
  border-color: #60a5fa;
  box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.2);
}

.submit-button {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #3b82f6;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: background-color 0.3s, transform 0.1s;
}

.submit-button:hover:not(:disabled) {
  background-color: #2563eb;
}

.submit-button:active:not(:disabled) {
  transform: scale(0.98);
}

.submit-button:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.submit-button svg {
  margin-right: 8px;
}

@media (max-width: 480px) {
  .registration {
    max-width: 100%;
  }

  .auth-options,
  .registration-form {
    padding-left: 20px;
    padding-right: 20px;
  }

  h2 {
    font-size: 20px;
    margin: 20px 0;
  }

  select,
  input,
  .submit-button {
    font-size: 14px;
  }
}

.theme-toggle {
  position: fixed;
  top: 20px;
  right: 20px;
  background-color: rgba(209, 213, 219, 0.8);
  border: none;
  border-radius: 50%;
  padding: 10px;
  cursor: pointer;
  transition: background-color 0.3s;
  z-index: 1000;
}

.dark .theme-toggle {
  background-color: rgba(55, 65, 81, 0.8);
}

.theme-toggle:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.theme-toggle svg {
  width: 24px;
  height: 24px;
  color: #4b5563;
}

.dark .theme-toggle svg {
  color: #e5e7eb;
}
</style>

