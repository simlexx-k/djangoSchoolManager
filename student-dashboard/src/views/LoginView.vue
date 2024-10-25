<template>
  <div class="min-h-screen flex flex-col justify-center items-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-10 bg-white p-10 rounded-xl shadow-lg">
      <div class="text-center">
        <img class="mx-auto h-16 w-auto" src="../assets/masabaLogo.png" alt="Masaba Logo">
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Sign in to your account
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Or
          <router-link to="/register" class="font-medium text-indigo-600 hover:text-indigo-500 transition-colors duration-300">
            create an account
          </router-link>
        </p>
      </div>
      <form @submit.prevent="handleSubmit" class="mt-8 space-y-6">
        <div class="space-y-6">
          <div class="relative">
            <input id="username" name="username" type="text" required
                   v-model="username"
                   class="input-field"
                   placeholder=" ">
            <label for="username" class="input-label">
              Username
            </label>
          </div>
          <div class="relative">
            <input id="password" name="password" type="password" required
                   v-model="password"
                   class="input-field"
                   placeholder=" ">
            <label for="password" class="input-label">
              Password
            </label>
          </div>
        </div>

        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input id="remember-me" name="remember-me" type="checkbox"
                   v-model="rememberMe"
                   class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded transition-colors duration-300">
            <label for="remember-me" class="ml-2 block text-sm text-gray-900">
              Remember me
            </label>
          </div>

          <div class="text-sm">
            <a href="#" class="font-medium text-indigo-600 hover:text-indigo-500 transition-colors duration-300">
              Forgot your password?
            </a>
          </div>
        </div>

        <div>
          <button type="submit"
                  :disabled="!isFormValid || isLoading"
                  :class="{'opacity-50 cursor-not-allowed': !isFormValid || isLoading, 'hover:bg-indigo-700': isFormValid && !isLoading}"
                  class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-300 shadow-md">
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg v-if="!isLoading" class="h-5 w-5 text-indigo-500 group-hover:text-indigo-400 transition-colors duration-300" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
              </svg>
              <svg v-else class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            {{ isLoading ? 'Signing in...' : 'Sign in' }}
          </button>
        </div>
      </form>
      <div v-if="error" class="mt-4 text-center text-sm text-red-600">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const rememberMe = ref(false);
const error = ref('');
const isLoading = ref(false);
const authStore = useAuthStore();
const router = useRouter();

const isFormValid = computed(() => {
  return username.value.trim() !== '' && password.value.trim() !== '';
});

const handleSubmit = async () => {
  if (isLoading.value || !isFormValid.value) return;
  
  isLoading.value = true;
  error.value = '';
  
  try {
    const result = await authStore.login({
      username: username.value,
      password: password.value,
      rememberMe: rememberMe.value
    });
    console.log('Login result:', result);
    router.push('/dashboard');
  } catch (err) {
    console.error('Login error details:', err);
    error.value = err.message || 'An error occurred during login';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.min-h-screen {
  background-image: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.max-w-md {
  animation: fadeIn 0.5s ease-out;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Modern input styles */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus {
  -webkit-text-fill-color: #4a5568;
  -webkit-box-shadow: 0 0 0px 1000px #ffffff inset;
  transition: background-color 5000s ease-in-out 0s;
}

.peer {
  @apply bg-white;
}

.peer:focus ~ label,
.peer:not(:placeholder-shown) ~ label {
  @apply -top-2.5 text-sm text-indigo-600 bg-white px-1;
  transform: translateY(-50%) scale(0.85);
}

input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus {
  -webkit-text-fill-color: #4a5568;
  -webkit-box-shadow: 0 0 0px 1000px #ffffff inset;
  transition: background-color 5000s ease-in-out 0s;
}

.input-field {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 2px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 1rem;
  line-height: 1.5;
  color: #1f2937;
  background-color: #ffffff;
  transition: all 0.3s ease;
}

.input-field:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.input-label {
  position: absolute;
  left: 0.75rem;
  top: 0.5rem;
  font-size: 1rem;
  color: #6b7280;
  pointer-events: none;
  transition: all 0.3s ease;
  background-color: #ffffff;
  padding: 0 0.25rem;
}

.input-field:focus ~ .input-label,
.input-field:not(:placeholder-shown) ~ .input-label {
  top: -0.5rem;
  left: 0.5rem;
  font-size: 0.875rem;
  color: #4f46e5;
}

/* Autofill styles */
.input-field:-webkit-autofill,
.input-field:-webkit-autofill:hover,
.input-field:-webkit-autofill:focus {
  -webkit-text-fill-color: #1f2937;
  -webkit-box-shadow: 0 0 0px 1000px #ffffff inset;
  transition: background-color 5000s ease-in-out 0s;
}
</style>
